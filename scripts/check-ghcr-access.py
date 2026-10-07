#!/usr/bin/env python3
"""Check the organization secret before starting expensive image builds."""
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

DISTRIBUTIONS = ('Ubuntu', 'Debian', 'Centos', 'Alpine', 'Fedora', 'AlmaLinux', 'ArchLinux', 'RockyLinux')
CLASSIC_TOKEN_URL = 'https://github.com/settings/tokens/new?scopes=write:packages'


def request(url, authorization, method='GET'):
    headers = {'Authorization': authorization, 'User-Agent': 'Low-Price-Hosting/Container'}
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers, method=method), timeout=30) as response:
        return response.status, response.headers, response.read()


def check_upload(token, username, repository):
    basic = base64.b64encode((username + ':' + token).encode()).decode()
    query = urllib.parse.urlencode({'service': 'ghcr.io', 'scope': 'repository:' + repository + ':pull,push'})
    _, _, body = request('https://ghcr.io/token?' + query, 'Basic ' + basic)
    result = json.loads(body)
    registry_token = result.get('token') or result.get('access_token')
    if not registry_token:
        raise RuntimeError('GHCR did not issue a registry access token.')
    authorization = 'Bearer ' + registry_token
    # Start and cancel an empty blob upload; no image or tag is published.
    status, headers, _ = request('https://ghcr.io/v2/' + repository + '/blobs/uploads/', authorization, 'POST')
    if status != 202:
        raise RuntimeError('GHCR did not allow a package upload.')
    location = urllib.parse.urljoin('https://ghcr.io', headers.get('Location', ''))
    parsed = urllib.parse.urlparse(location)
    if parsed.scheme != 'https' or parsed.netloc != 'ghcr.io' or not parsed.path.startswith('/v2/' + repository + '/blobs/uploads/'):
        raise RuntimeError('GHCR returned an unexpected upload location.')
    request(location, authorization, 'DELETE')


def check(selected):
    if selected not in ('all', *DISTRIBUTIONS):
        raise RuntimeError('Unknown distribution in registry access check.')
    token = os.environ.get('GH_TOKEN', '').strip()
    if not token:
        raise RuntimeError('GH_TOKEN is unavailable. Grant Container access to the organization Actions secret.')
    fine_grained = token.startswith('github_pat_')
    token_type = 'fine-grained PAT' if fine_grained else 'classic PAT' if token.startswith('ghp_') else 'other GitHub token'
    print('GH_TOKEN type: ' + token_type, flush=True)
    try:
        _, headers, body = request('https://api.github.com/user', 'Bearer ' + token)
    except urllib.error.HTTPError as error:
        if error.code == 401:
            raise RuntimeError('GH_TOKEN is invalid, expired, or revoked.') from None
        raise
    username = json.loads(body).get('login', '')
    if not re.fullmatch(r'[A-Za-z0-9-]+', username):
        raise RuntimeError('GitHub did not return a valid token owner.')
    print('GH_TOKEN owner: ' + username, flush=True)
    if fine_grained:
        raise RuntimeError('GitHub Packages does not support fine-grained PATs, even with all repository permissions. '
                           'Replace the organization GH_TOKEN secret with a classic PAT granting write:packages: ' + CLASSIC_TOKEN_URL)
    scopes_header = headers.get('X-OAuth-Scopes')
    if scopes_header is not None:
        scopes = {scope.strip() for scope in scopes_header.split(',')}
        allowed = 'write:packages' in scopes
        print('GH_TOKEN write:packages scope: ' + ('present' if allowed else 'absent'), flush=True)
        if not allowed:
            raise RuntimeError('GH_TOKEN lacks write:packages. Repository or organization permissions do not grant package upload access. '
                               'Update the classic PAT stored in the organization GH_TOKEN secret: ' + CLASSIC_TOKEN_URL)
    for distribution in DISTRIBUTIONS if selected == 'all' else (selected,):
        repository = 'low-price-hosting/' + distribution.lower()
        try:
            check_upload(token, username, repository)
        except urllib.error.HTTPError as error:
            raise RuntimeError(f'GH_TOKEN cannot upload to ghcr.io/{repository} (HTTP {error.code}). '
                               'Check package Write access, organization PAT policy, and SSO authorization if required.') from None
        print('GHCR upload access verified: ' + repository, flush=True)


if __name__ == '__main__':
    try:
        check(sys.argv[1] if len(sys.argv) == 2 else 'all')
    except urllib.error.HTTPError as error:
        print(f'::error::GitHub rejected the GH_TOKEN check (HTTP {error.code}).', flush=True)
        sys.exit(1)
    except (urllib.error.URLError, TimeoutError, ValueError) as error:
        # Never print credentials, response bodies, URLs containing tokens, or request objects.
        print('::error::GH_TOKEN access check failed (' + type(error).__name__ + ').', flush=True)
        sys.exit(1)
    except RuntimeError as error:
        print('::error::' + str(error), flush=True)
        sys.exit(1)
