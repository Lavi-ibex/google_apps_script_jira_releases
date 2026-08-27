/**
 * Google Apps Script backend for Ibex Jira Releases Google Sites embed.
 * Fetches release versions from Jira Cloud REST API v3, caches results for 1 hour,
 * and serves a responsive dashboard.
 */

// Configuration constants
var CACHE_KEY = 'IBEX_JIRA_RELEASES_CACHE';
var CACHE_EXPIRATION_SECONDS = 3600; // 1 hour
var AUTHORIZED_EMAIL_DOMAIN = 'ibex-ai.com';
var MAX_DESCRIPTION_LENGTH = 32767;

/**
 * HTTP GET entry point for Google Apps Script Web App.
 * Uses createHtmlOutputFromFile to completely prevent template compilation syntax errors.
 */
function doGet(e) {
  return HtmlService.createHtmlOutputFromFile('Index')
    .setTitle('Ibex Jira Releases')
    .addMetaTag('viewport', 'width=device-width, initial-scale=1')
    .setXFrameOptionsMode(HtmlService.XFrameOptionsMode.ALLOWALL);
}

/**
 * Public client-callable API to fetch releases.
 * @param {boolean} forceRefresh - If true, bypasses cache and queries Jira directly.
 */
function apiGetReleases(forceRefresh) {
  return getJiraReleases(!!forceRefresh);
}

/**
 * Updates the description of one Jira release version.
 * This function is callable from the dashboard only by signed-in Ibex users.
 * @param {string} versionId Jira version ID.
 * @param {string} description Replacement description, which may be empty.
 * @returns {Object} Safe confirmation payload.
 */
function apiUpdateReleaseDescription(versionId, description) {
  assertAuthorizedIbexUser();

  if (typeof versionId !== 'string' || !/^\d{1,20}$/.test(versionId)) {
    throw new Error('Invalid Jira release version ID.');
  }

  if (typeof description !== 'string' || description.length > MAX_DESCRIPTION_LENGTH) {
    throw new Error('Description must be text no longer than ' + MAX_DESCRIPTION_LENGTH + ' characters.');
  }

  var scriptProps = PropertiesService.getScriptProperties();
  var baseUrl = (scriptProps.getProperty('JIRA_BASE_URL') || 'https://ibex-ai.atlassian.net').replace(/\/+$/, '');
  var userEmail = scriptProps.getProperty('JIRA_USER_EMAIL');
  var apiToken = scriptProps.getProperty('JIRA_API_TOKEN');

  if (!userEmail || !apiToken) {
    throw new Error('Jira credentials are not configured.');
  }

  var response = UrlFetchApp.fetch(
    baseUrl + '/rest/api/2/version/' + encodeURIComponent(versionId),
    {
      method: 'put',
      contentType: 'application/json',
      headers: {
        'Authorization': 'Basic ' + Utilities.base64Encode(userEmail + ':' + apiToken),
        'Accept': 'application/json'
      },
      payload: JSON.stringify({ description: description }),
      muteHttpExceptions: true
    }
  );

  if (response.getResponseCode() !== 200) {
    throw new Error('Jira could not update the release description. HTTP ' + response.getResponseCode() + getSafeJiraValidationMessage(response) + '.');
  }

  CacheService.getScriptCache().remove(CACHE_KEY);
  return { id: versionId, description: description };
}

/**
 * Extracts a short Jira validation message without returning an unbounded response body.
 */
function getSafeJiraValidationMessage(response) {
  var rawBody = response.getContentText() || '';
  var message = '';

  try {
    var parsedBody = JSON.parse(rawBody);
    if (parsedBody.errorMessages && parsedBody.errorMessages.length) {
      message = parsedBody.errorMessages.join(' ');
    } else if (parsedBody.errors) {
      var fields = Object.keys(parsedBody.errors);
      message = fields.map(function(field) {
        return field + ': ' + parsedBody.errors[field];
      }).join(' ');
    }
  } catch (e) {
    message = '';
  }

  message = String(message).replace(/[\r\n\t]+/g, ' ').trim();
  return message ? ' - ' + message.slice(0, 240) : '';
}

/**
 * Ensures the active caller belongs to the permitted Workspace domain.
 */
function assertAuthorizedIbexUser() {
  var activeEmail = (Session.getActiveUser().getEmail() || '').toLowerCase();
  if (!activeEmail || activeEmail.slice(-(AUTHORIZED_EMAIL_DOMAIN.length + 1)) !== '@' + AUTHORIZED_EMAIL_DOMAIN) {
    throw new Error('You must be signed in with an authorized Ibex account to edit release descriptions.');
  }
}

/**
 * Fetches and processes Jira releases. Uses ScriptCache for 1-hour caching.
 * @param {boolean} forceRefresh - If true, bypasses the cache and queries Jira directly.
 * @returns {Array<Object>} List of release objects formatted for the UI.
 */
function getJiraReleases(forceRefresh) {
  var cache = CacheService.getScriptCache();
  
  if (!forceRefresh) {
    var cachedData = cache.get(CACHE_KEY);
    if (cachedData) {
      try {
        return JSON.parse(cachedData);
      } catch (e) {
        Logger.log('Cache parse failed, fetching fresh data from Jira: ' + e);
      }
    }
  }

  var scriptProps = PropertiesService.getScriptProperties();
  var baseUrl = (scriptProps.getProperty('JIRA_BASE_URL') || 'https://ibex-ai.atlassian.net').replace(/\/+$/, '');
  var projectKey = scriptProps.getProperty('JIRA_PROJECT_KEY') || 'IBX';
  var userEmail = scriptProps.getProperty('JIRA_USER_EMAIL');
  var apiToken = scriptProps.getProperty('JIRA_API_TOKEN');

  if (!userEmail || !apiToken) {
    throw new Error('Jira credentials not configured. Please set JIRA_USER_EMAIL and JIRA_API_TOKEN in Script Properties.');
  }

  var authHeader = 'Basic ' + Utilities.base64Encode(userEmail + ':' + apiToken);
  var url = baseUrl + '/rest/api/3/project/' + encodeURIComponent(projectKey) + '/versions';

  var options = {
    method: 'get',
    headers: {
      'Authorization': authHeader,
      'Accept': 'application/json'
    },
    muteHttpExceptions: true
  };

  var response = UrlFetchApp.fetch(url, options);
  var responseCode = response.getResponseCode();

  if (responseCode !== 200) {
    throw new Error('Failed to fetch Jira versions. HTTP ' + responseCode + ': ' + response.getContentText());
  }

  var rawVersions = JSON.parse(response.getContentText());
  var formattedVersions = processRawVersions(rawVersions, baseUrl, projectKey);

  // Store in cache (CacheService limit is 100KB per item)
  try {
    cache.put(CACHE_KEY, JSON.stringify(formattedVersions), CACHE_EXPIRATION_SECONDS);
  } catch (cacheErr) {
    Logger.log('Could not cache release data: ' + cacheErr);
  }

  return formattedVersions;
}

/**
 * Parses and sorts Jira version objects.
 * Priority: Unreleased (active/upcoming) -> Released (newest first) -> Archived.
 */
function processRawVersions(rawVersions, baseUrl, projectKey) {
  if (!Array.isArray(rawVersions)) {
    return [];
  }

  baseUrl = (baseUrl || 'https://ibex-ai.atlassian.net').replace(/\/+$/, '');
  projectKey = projectKey || 'IBX';

  // Show dated active versions and versions released during calendar year 2026.
  var visibleVersions = rawVersions.filter(function(v) {
    if (!v || v.archived || typeof v.releaseDate !== 'string' || v.releaseDate.trim() === '') {
      return false;
    }

    return !v.released || v.releaseDate.indexOf('2026-') === 0;
  });

  var formatted = visibleVersions.map(function(v) {
    var status = 'Unreleased';
    var statusCategory = 'unreleased';

    if (v.archived) {
      status = 'Archived';
      statusCategory = 'archived';
    } else if (v.released) {
      status = 'Released';
      statusCategory = 'released';
    } else if (v.overdue) {
      status = 'Overdue';
      statusCategory = 'overdue';
    }

    var releaseUrl = v.id 
      ? baseUrl + '/projects/' + encodeURIComponent(projectKey) + '/versions/' + encodeURIComponent(v.id)
      : baseUrl + '/projects/' + encodeURIComponent(projectKey) + '/versions';

    return {
      id: v.id,
      name: v.name || 'Unnamed Version',
      url: releaseUrl,
      status: status,
      statusCategory: statusCategory,
      released: !!v.released,
      archived: !!v.archived,
      overdue: !!v.overdue,
      releaseDate: v.releaseDate || '',
      userReleaseDate: v.userReleaseDate || v.releaseDate || 'No date set',
      startDate: v.startDate || '',
      description: v.description || 'No description provided.'
    };
  });

  // Sort logic:
  // 1. Unreleased / Overdue first (sorted by releaseDate ascending, versions without date at end)
  // 2. Released next (sorted by releaseDate descending, newest first)
  // 3. Archived last
  formatted.sort(function(a, b) {
    var catRank = { 'overdue': 1, 'unreleased': 2, 'released': 3, 'archived': 4 };
    var rankA = catRank[a.statusCategory] || 99;
    var rankB = catRank[b.statusCategory] || 99;

    if (rankA !== rankB) {
      return rankA - rankB;
    }

    if (a.statusCategory === 'released') {
      // Released: newest date first
      if (!a.releaseDate) return 1;
      if (!b.releaseDate) return -1;
      return b.releaseDate.localeCompare(a.releaseDate);
    } else {
      // Unreleased/Overdue: nearest date first
      if (!a.releaseDate) return 1;
      if (!b.releaseDate) return -1;
      return a.releaseDate.localeCompare(b.releaseDate);
    }
  });

  return formatted;
}
