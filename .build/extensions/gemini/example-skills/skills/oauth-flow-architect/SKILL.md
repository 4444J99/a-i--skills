---
name: oauth-flow-architect
description: Implements OAuth 2.0 and OpenID Connect authentication flows with proper security, token management, and common provider integrations.
license: MIT
---

# OAuth Flow Architect

This skill provides guidance for implementing OAuth 2.0 and OpenID Connect (OIDC) authentication flows securely and correctly.

## Core Competencies

- **OAuth 2.0 Flows**: Authorization Code, PKCE, Client Credentials
- **OpenID Connect**: ID tokens, UserInfo, discovery
- **Token Management**: Refresh, revocation, storage
- **Security**: CSRF, token theft, redirect URI validation

## OAuth 2.0 Fundamentals

### The Problem OAuth Solves

```
Without OAuth:                   With OAuth:
┌──────┐  credentials  ┌──────┐  ┌──────┐            ┌──────┐
│ User │──────────────▶│ App  │  │ User │            │ App  │
└──────┘               └──┬───┘  └──┬───┘            └──┬───┘
                          │         │ Login at          │
                          │         │ provider          │
                          ▼         ▼                   │
                       ┌──────┐  ┌──────┐  token     ┌──────┐
                       │Google│  │Google│───────────▶│Google│
                       └──────┘  └──────┘            └──────┘

App has your password        App never sees password
```

### OAuth Roles

| Role | Description | Example |
|------|-------------|---------|
| Resource Owner | User who owns data | End user |
| Client | Application requesting access | Your app |
| Authorization Server | Issues tokens | Google, Auth0 |
| Resource Server | Hosts protected resources | Google API |

### Grant Types Overview

| Grant Type | Use Case | Security Level |
|------------|----------|----------------|
| Authorization Code + PKCE | Web apps, mobile, SPAs | Highest |
| Authorization Code | Traditional server apps | High |
| Client Credentials | Machine-to-machine | High |
| Refresh Token | Token renewal | High |
| Implicit (deprecated) | Legacy SPAs | Low |
| Password (deprecated) | Legacy migrations | Low |

## Authorization Code Flow with PKCE

The recommended flow for all user-facing applications.

### Flow Diagram

```
┌──────┐                              ┌─────────────┐                    ┌──────────┐
│ User │                              │   Client    │                    │  Auth    │
│      │                              │   (App)     │                    │  Server  │
└──┬───┘                              └──────┬──────┘                    └────┬─────┘
   │  1. Click "Login"                       │                               │
   │────────────────────────────────────────▶│                               │
   │                                         │  2. Generate code_verifier    │
   │                                         │     code_challenge = SHA256() │
   │                                         │                               │
   │  3. Redirect to authorization endpoint  │                               │
   │◀────────────────────────────────────────│                               │
   │                                         │                               │
   │  4. Redirect (login at auth server)     │                               │
   │────────────────────────────────────────────────────────────────────────▶│
   │                                         │                               │
   │  5. User authenticates & consents       │                               │
   │◀────────────────────────────────────────────────────────────────────────│
   │                                         │                               │
   │  6. Redirect with authorization code    │                               │
   │────────────────────────────────────────▶│                               │
   │                                         │                               │
   │                                         │  7. Exchange code + verifier  │
   │                                         │     for tokens                │
   │                                         │──────────────────────────────▶│
   │                                         │                               │
   │                                         │  8. Access token + ID token   │
   │                                         │◀──────────────────────────────│
   │                                         │                               │
   │  9. User is logged in                   │                               │
   │◀────────────────────────────────────────│                               │
```

### Implementation

```python
import secrets
import hashlib
import base64
from urllib.parse import urlencode

class OAuthClient:
    """OAuth 2.0 client with PKCE"""

    def __init__(self, config):
        self.client_id = config['client_id']
        self.client_secret = config.get('client_secret')  # Optional with PKCE
        self.redirect_uri = config['redirect_uri']
        self.authorization_endpoint = config['authorization_endpoint']
        self.token_endpoint = config['token_endpoint']
        self.scopes = config.get('scopes', ['openid', 'profile', 'email'])

    def generate_pkce(self):
        """Generate PKCE code verifier and challenge"""
        # Code verifier: 43-128 chars, URL-safe
        code_verifier = secrets.token_urlsafe(32)

        # Code challenge: SHA256 hash of verifier
        digest = hashlib.sha256(code_verifier.encode()).digest()
        code_challenge = base64.urlsafe_b64encode(digest).rstrip(b'=').decode()

        return code_verifier, code_challenge

    def get_authorization_url(self, state=None):
        """Build authorization URL for redirect"""
        code_verifier, code_challenge = self.generate_pkce()

        # State for CSRF protection
        state = state or secrets.token_urlsafe(16)

        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': ' '.join(self.scopes),
            'state': state,
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256'
        }

        url = f"{self.authorization_endpoint}?{urlencode(params)}"

        return {
            'url': url,
            'state': state,
            'code_verifier': code_verifier  # Store server-side
        }

    async def exchange_code(self, code, code_verifier):
        """Exchange authorization code for tokens"""
        data = {
            'grant_type': 'authorization_code',
            'client_id': self.client_id,
            'code': code,
            'redirect_uri': self.redirect_uri,
            'code_verifier': code_verifier
        }

        # Include client_secret if confidential client
        if self.client_secret:
            data['client_secret'] = self.client_secret

        response = await self.http.post(
            self.token_endpoint,
            data=data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )

        if response.status_code != 200:
            raise OAuthError(response.json())

        return response.json()  # {access_token, refresh_token, id_token, ...}
```

### Callback Handler

```python
from flask import request, session, redirect

@app.route('/callback')
async def oauth_callback():
    # Verify state to prevent CSRF
    state = request.args.get('state')
    stored_state = session.get('oauth_state')

    if not state or state != stored_state:
        return 'Invalid state parameter', 400

    # Check for errors
    error = request.args.get('error')
    if error:
        error_desc = request.args.get('error_description', 'Unknown error')
        return f'OAuth error: {error_desc}', 400

    # Exchange code for tokens
    code = request.args.get('code')
    code_verifier = session.get('oauth_code_verifier')

    try:
        tokens = await oauth_client.exchange_code(code, code_verifier)
    except OAuthError as e:
        return f'Token exchange failed: {e}', 400

    # Validate ID token if using OIDC
    if 'id_token' in tokens:
        user_info = validate_id_token(tokens['id_token'])
    else:
        user_info = await fetch_userinfo(tokens['access_token'])

    # Create session
    session['user'] = user_info
    session['tokens'] = tokens

    # Clean up OAuth state
    session.pop('oauth_state', None)
    session.pop('oauth_code_verifier', None)

    return redirect('/dashboard')
```

## OpenID Connect

OIDC adds identity layer on top of OAuth 2.0.

### ID Token Structure

```python
# ID token is a JWT with claims
{
    # Standard claims
    "iss": "https://accounts.google.com",  # Issuer
    "sub": "110169484474386276334",         # Subject (user ID)
    "aud": "your-client-id",                # Audience
    "exp": 1706616000,                      # Expiration
    "iat": 1706612400,                      # Issued at
    "nonce": "abc123",                      # Replay protection

    # Profile claims
    "name": "Alice Smith",
    "email": "alice@example.com",
    "email_verified": true,
    "picture": "https://..."
}
```

### ID Token Validation

```python
import jwt
from jwt import PyJWKClient

class IDTokenValidator:
    """Validate OIDC ID tokens"""

    def __init__(self, issuer, client_id, jwks_uri):
        self.issuer = issuer
        self.client_id = client_id
        self.jwks_client = PyJWKClient(jwks_uri)

    def validate(self, id_token, nonce=None):
        """Validate and decode ID token"""
        try:
            # Get signing key
            signing_key = self.jwks_client.get_signing_key_from_jwt(id_token)

            # Decode and validate
            claims = jwt.decode(
                id_token,
                signing_key.key,
                algorithms=['RS256'],
                audience=self.client_id,
                issuer=self.issuer
            )

            # Verify nonce if provided
            if nonce and claims.get('nonce') != nonce:
                raise ValueError('Invalid nonce')

            return claims

        except jwt.ExpiredSignatureError:
            raise AuthenticationError('ID token expired')
        except jwt.InvalidAudienceError:
            raise AuthenticationError('Invalid audience')
        except jwt.InvalidIssuerError:
            raise AuthenticationError('Invalid issuer')
        except Exception as e:
            raise AuthenticationError(f'Token validation failed: {e}')
```

### OIDC Discovery

```python
async def discover_oidc_config(issuer):
    """Fetch OIDC provider configuration"""
    discovery_url = f"{issuer.rstrip('/')}/.well-known/openid-configuration"

    response = await http.get(discovery_url)
    config = response.json()

    return {
        'authorization_endpoint': config['authorization_endpoint'],
        'token_endpoint': config['token_endpoint'],
        'userinfo_endpoint': config['userinfo_endpoint'],
        'jwks_uri': config['jwks_uri'],
        'scopes_supported': config['scopes_supported'],
        'response_types_supported': config['response_types_supported']
    }

# Example: Google
# https://accounts.google.com/.well-known/openid-configuration
```

## Client Credentials Flow

For machine-to-machine authentication (no user involved).

```python
class ClientCredentialsAuth:
    """OAuth client credentials flow"""

    def __init__(self, client_id, client_secret, token_endpoint):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_endpoint = token_endpoint
        self._token = None
        self._token_expiry = None

    async def get_token(self, scopes=None):
        """Get access token, refreshing if needed"""
        if self._token and self._token_expiry > time.time():
            return self._token

        data = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }

        if scopes:
            data['scope'] = ' '.join(scopes)

        response = await http.post(
            self.token_endpoint,
            data=data,
            headers={'Content-Type': 'application/x-www-form-urlencoded'}
        )

        tokens = response.json()
        self._token = tokens['access_token']
        self._token_expiry = time.time() + tokens.get('expires_in', 3600) - 60

        return self._token
```

## Token Management

### Refresh Token Flow

```python
class TokenManager:
    """Manage access and refresh tokens"""

    def __init__(self, oauth_client, token_storage):
        self.oauth = oauth_client
        self.storage = token_storage

    async def get_valid_access_token(self, user_id):
        """Get valid access token, refreshing if needed"""
        tokens = await self.storage.get_tokens(user_id)

        if not tokens:
            raise AuthenticationError('No tokens found')

        # Check if access token is still valid (with buffer)
        if tokens.get('expires_at', 0) > time.time() + 60:
            return tokens['access_token']

        # Refresh the token
        if 'refresh_token' not in tokens:
            raise AuthenticationError('No refresh token, re-auth required')

        new_tokens = await self._refresh(tokens['refresh_token'])
        await self.storage.save_tokens(user_id, new_tokens)

        return new_tokens['access_token']

    async def _refresh(self, refresh_token):
        """Exchange refresh token for new access token"""
        data = {
            'grant_type': 'refresh_token',
            'client_id': self.oauth.client_id,
            'refresh_token': refresh_token
        }

        if self.oauth.client_secret:
            data['client_secret'] = self.oauth.client_secret

        response = await http.post(
            self.oauth.token_endpoint,
            data=data
        )

        if response.status_code != 200:
            raise TokenRefreshError(response.json())

        tokens = response.json()
        tokens['expires_at'] = time.time() + tokens.get('expires_in', 3600)

        return tokens
```

### Token Storage Security

```python
class SecureTokenStorage:
    """Store tokens securely"""

    def __init__(self, encryption_key, backend):
        self.cipher = Fernet(encryption_key)
        self.backend = backend  # Redis, database, etc.

    async def save_tokens(self, user_id, tokens):
        """Encrypt and store tokens"""
        # Encrypt sensitive fields
        encrypted = {
            'access_token': self._encrypt(tokens['access_token']),
            'expires_at': tokens['expires_at']
        }

        if 'refresh_token' in tokens:
            encrypted['refresh_token'] = self._encrypt(tokens['refresh_token'])

        if 'id_token' in tokens:
            # ID token doesn't need encryption (it's signed, not secret)
            encrypted['id_token'] = tokens['id_token']

        await self.backend.set(f"tokens:{user_id}", json.dumps(encrypted))

    async def get_tokens(self, user_id):
        """Retrieve and decrypt tokens"""
        data = await self.backend.get(f"tokens:{user_id}")
        if not data:
            return None

        encrypted = json.loads(data)

        return {
            'access_token': self._decrypt(encrypted['access_token']),
            'refresh_token': self._decrypt(encrypted.get('refresh_token', '')),
            'expires_at': encrypted['expires_at'],
            'id_token': encrypted.get('id_token')
        }

    def _encrypt(self, value):
        if not value:
            return ''
        return self.cipher.encrypt(value.encode()).decode()

    def _decrypt(self, value):
        if not value:
            return ''
        return self.cipher.decrypt(value.encode()).decode()
```

## Security Considerations

### Redirect URI Validation

```python
def validate_redirect_uri(redirect_uri, registered_uris):
    """Strict redirect URI validation"""
    # Exact match required (no wildcards in production)
    if redirect_uri not in registered_uris:
        raise SecurityError('Invalid redirect_uri')

    # Additional checks
    parsed = urlparse(redirect_uri)

    # Must be HTTPS (except localhost for development)
    if parsed.scheme != 'https':
        if parsed.hostname not in ('localhost', '127.0.0.1'):
            raise SecurityError('Redirect URI must use HTTPS')

    # No fragments
    if parsed.fragment:
        raise SecurityError('Redirect URI cannot have fragment')

    return True
```

### CSRF Protection

```python
# State parameter prevents CSRF attacks

# 1. Generate state before redirect
state = secrets.token_urlsafe(32)
session['oauth_state'] = state

# 2. Include in authorization URL
auth_url = f"{authorization_endpoint}?state={state}&..."

# 3. Verify on callback
if request.args.get('state') != session.get('oauth_state'):
    abort(400, 'CSRF detected')
```

### Common Vulnerabilities

| Vulnerability | Prevention |
|--------------|------------|
| CSRF | State parameter, SameSite cookies |
| Token theft | HTTPS only, secure storage |
| Open redirect | Strict redirect URI validation |
| Code injection | PKCE, short-lived codes |
| Replay | Nonce in ID tokens |

## Provider-Specific Setup

### Google

```python
GOOGLE_CONFIG = {
    'client_id': 'xxx.apps.googleusercontent.com',
    'client_secret': 'xxx',
    'authorization_endpoint': 'https://accounts.google.com/o/oauth2/v2/auth',
    'token_endpoint': 'https://oauth2.googleapis.com/token',
    'userinfo_endpoint': 'https://openidconnect.googleapis.com/v1/userinfo',
    'scopes': ['openid', 'email', 'profile']
}
```

### GitHub (OAuth 2.0, not OIDC)

```python
GITHUB_CONFIG = {
    'client_id': 'xxx',
    'client_secret': 'xxx',
    'authorization_endpoint': 'https://github.com/login/oauth/authorize',
    'token_endpoint': 'https://github.com/login/oauth/access_token',
    'userinfo_endpoint': 'https://api.github.com/user',
    'scopes': ['read:user', 'user:email']
}
```

## References

- `references/oauth-security.md` - Security best practices and threats
- `references/provider-configs.md` - Configuration for common providers
- `references/token-patterns.md` - Token storage and refresh patterns
