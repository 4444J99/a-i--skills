# OAuth Provider Configurations

## Google

```python
GOOGLE_CONFIG = {
    'client_id': 'xxx.apps.googleusercontent.com',
    'client_secret': 'xxx',
    'authorization_endpoint': 'https://accounts.google.com/o/oauth2/v2/auth',
    'token_endpoint': 'https://oauth2.googleapis.com/token',
    'userinfo_endpoint': 'https://openidconnect.googleapis.com/v1/userinfo',
    'jwks_uri': 'https://www.googleapis.com/oauth2/v3/certs',
    'issuer': 'https://accounts.google.com',
    'scopes': ['openid', 'email', 'profile']
}
```

### Additional Scopes

| Scope | Access |
|-------|--------|
| `https://www.googleapis.com/auth/gmail.readonly` | Read Gmail |
| `https://www.googleapis.com/auth/calendar` | Calendar access |
| `https://www.googleapis.com/auth/drive` | Google Drive |

### Consent Screen Params

```python
# Force consent screen
params['prompt'] = 'consent'

# Select specific account
params['prompt'] = 'select_account'

# Both
params['prompt'] = 'consent select_account'

# Login hint (pre-fill email)
params['login_hint'] = 'user@example.com'
```

## GitHub (OAuth 2.0, not OIDC)

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

### Common Scopes

| Scope | Access |
|-------|--------|
| `read:user` | Public profile |
| `user:email` | Email addresses |
| `repo` | Full repo access |
| `repo:status` | Commit status |
| `admin:org` | Org management |

### Note: GitHub Token Format

GitHub requires Accept header for token endpoint:

```python
response = requests.post(
    'https://github.com/login/oauth/access_token',
    data={'client_id': ..., 'code': ...},
    headers={'Accept': 'application/json'}  # Required!
)
```

## Microsoft (Azure AD)

```python
# Single tenant
MICROSOFT_CONFIG = {
    'client_id': 'xxx',
    'client_secret': 'xxx',
    'tenant': 'your-tenant-id',
    'authorization_endpoint': f'https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize',
    'token_endpoint': f'https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token',
    'jwks_uri': f'https://login.microsoftonline.com/{tenant}/discovery/v2.0/keys',
    'issuer': f'https://login.microsoftonline.com/{tenant}/v2.0',
    'scopes': ['openid', 'email', 'profile']
}

# Multi-tenant
tenant = 'common'  # or 'organizations' or 'consumers'
```

### Common Scopes

| Scope | Access |
|-------|--------|
| `User.Read` | Basic profile |
| `Mail.Read` | Read Outlook mail |
| `Calendars.ReadWrite` | Calendar |
| `Files.ReadWrite` | OneDrive |

## Apple (Sign in with Apple)

```python
import jwt

APPLE_CONFIG = {
    'client_id': 'com.your.app.id',  # Service ID
    'team_id': 'ABCD1234',
    'key_id': 'KEYID12345',
    'private_key_path': 'AuthKey_KEYID12345.p8',
    'authorization_endpoint': 'https://appleid.apple.com/auth/authorize',
    'token_endpoint': 'https://appleid.apple.com/auth/token',
    'scopes': ['name', 'email']
}

def generate_apple_client_secret():
    """Apple requires JWT as client secret"""
    now = int(time.time())
    with open(APPLE_CONFIG['private_key_path']) as f:
        private_key = f.read()

    return jwt.encode(
        {
            'iss': APPLE_CONFIG['team_id'],
            'iat': now,
            'exp': now + 86400 * 180,  # Max 6 months
            'aud': 'https://appleid.apple.com',
            'sub': APPLE_CONFIG['client_id']
        },
        private_key,
        algorithm='ES256',
        headers={'kid': APPLE_CONFIG['key_id']}
    )
```

## Facebook

```python
FACEBOOK_CONFIG = {
    'client_id': 'xxx',  # App ID
    'client_secret': 'xxx',
    'authorization_endpoint': 'https://www.facebook.com/v18.0/dialog/oauth',
    'token_endpoint': 'https://graph.facebook.com/v18.0/oauth/access_token',
    'userinfo_endpoint': 'https://graph.facebook.com/me?fields=id,name,email',
    'scopes': ['email', 'public_profile']
}
```

### Permissions

| Permission | Access |
|------------|--------|
| `email` | User email |
| `public_profile` | Basic info |
| `user_friends` | Friends list |
| `user_photos` | Photos |

## Auth0

```python
AUTH0_CONFIG = {
    'domain': 'your-domain.auth0.com',
    'client_id': 'xxx',
    'client_secret': 'xxx',
    'authorization_endpoint': 'https://your-domain.auth0.com/authorize',
    'token_endpoint': 'https://your-domain.auth0.com/oauth/token',
    'userinfo_endpoint': 'https://your-domain.auth0.com/userinfo',
    'jwks_uri': 'https://your-domain.auth0.com/.well-known/jwks.json',
    'issuer': 'https://your-domain.auth0.com/',
    'scopes': ['openid', 'profile', 'email']
}
```

## Okta

```python
OKTA_CONFIG = {
    'domain': 'your-domain.okta.com',
    'client_id': 'xxx',
    'client_secret': 'xxx',
    'authorization_endpoint': 'https://your-domain.okta.com/oauth2/v1/authorize',
    'token_endpoint': 'https://your-domain.okta.com/oauth2/v1/token',
    'userinfo_endpoint': 'https://your-domain.okta.com/oauth2/v1/userinfo',
    'jwks_uri': 'https://your-domain.okta.com/oauth2/v1/keys',
    'issuer': 'https://your-domain.okta.com',
    'scopes': ['openid', 'profile', 'email']
}
```

## Generic OIDC Discovery

```python
import requests

def discover_oidc(issuer):
    """Auto-discover OIDC configuration"""
    discovery_url = f"{issuer.rstrip('/')}/.well-known/openid-configuration"
    response = requests.get(discovery_url)
    response.raise_for_status()

    config = response.json()
    return {
        'issuer': config['issuer'],
        'authorization_endpoint': config['authorization_endpoint'],
        'token_endpoint': config['token_endpoint'],
        'userinfo_endpoint': config.get('userinfo_endpoint'),
        'jwks_uri': config['jwks_uri'],
        'scopes_supported': config.get('scopes_supported', []),
        'response_types_supported': config.get('response_types_supported', [])
    }
```
