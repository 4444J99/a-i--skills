# OAuth Security Best Practices

## Common Vulnerabilities

### 1. Authorization Code Injection

**Attack**: Attacker substitutes their auth code for victim's

**Prevention**:
- Use PKCE (Proof Key for Code Exchange)
- Bind state to session
- Single-use authorization codes

```python
# PKCE implementation
import secrets
import hashlib
import base64

def generate_pkce():
    code_verifier = secrets.token_urlsafe(32)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).rstrip(b'=').decode()

    return code_verifier, code_challenge
```

### 2. CSRF Attacks

**Attack**: Trick user into authorizing attacker's account

**Prevention**:
- Use state parameter
- Bind state to session
- Use cryptographically random state

```python
import secrets

def generate_state():
    return secrets.token_urlsafe(32)

def validate_state(received_state, session_state):
    if not received_state or received_state != session_state:
        raise SecurityError("Invalid state parameter")
```

### 3. Open Redirectors

**Attack**: Use your callback as open redirect

**Prevention**:
- Strict redirect URI matching
- No wildcards in redirect URIs
- Validate redirect URI server-side

```python
def validate_redirect_uri(redirect_uri, registered_uris):
    """Exact match only - no wildcards"""
    if redirect_uri not in registered_uris:
        raise SecurityError("Invalid redirect_uri")

    parsed = urlparse(redirect_uri)

    # Must be HTTPS (except localhost)
    if parsed.scheme != 'https':
        if parsed.hostname not in ('localhost', '127.0.0.1'):
            raise SecurityError("Redirect URI must use HTTPS")

    # No fragments
    if parsed.fragment:
        raise SecurityError("Redirect URI cannot have fragment")

    return True
```

### 4. Token Theft

**Attack**: Steal tokens from storage, logs, or URLs

**Prevention**:
- Never store tokens in local storage (XSS vulnerable)
- Use httpOnly cookies for web apps
- Encrypt tokens at rest
- Never log tokens
- Use short token lifetimes

```python
# Secure token storage
from cryptography.fernet import Fernet

class SecureTokenStore:
    def __init__(self, key):
        self.cipher = Fernet(key)

    def store(self, user_id, tokens):
        encrypted = self.cipher.encrypt(
            json.dumps(tokens).encode()
        )
        self.db.set(f"tokens:{user_id}", encrypted)

    def retrieve(self, user_id):
        encrypted = self.db.get(f"tokens:{user_id}")
        if not encrypted:
            return None
        return json.loads(
            self.cipher.decrypt(encrypted).decode()
        )
```

### 5. Insufficient Scope Validation

**Attack**: Obtain more permissions than granted

**Prevention**:
- Validate scopes in access token
- Principle of least privilege
- Check scopes before each operation

```python
def require_scope(required_scope):
    def decorator(f):
        def wrapped(*args, **kwargs):
            token = get_current_token()  # allow-secret
            if required_scope not in token.scopes:
                raise ForbiddenError(f"Requires scope: {required_scope}")
            return f(*args, **kwargs)
        return wrapped
    return decorator

@require_scope('write:users')
def update_user(user_id, data):
    # Only executes if token has write:users scope
    pass
```

## Token Security

### Access Token Best Practices

1. **Short lifetime**: 15-60 minutes
2. **Single audience**: One service per token
3. **Minimal scopes**: Only what's needed
4. **Opaque or JWT**: JWT for stateless, opaque for revocability

### Refresh Token Best Practices

1. **Longer lifetime**: Days to months
2. **Rotate on use**: Issue new refresh token with each use
3. **Detect reuse**: If old token used, revoke family
4. **Bind to client**: Client ID must match

```python
class RefreshTokenManager:
    def refresh(self, refresh_token, client_id):
        stored = self.get_token(refresh_token)

        # Validate
        if not stored:
            raise InvalidTokenError("Unknown refresh token")
        if stored['client_id'] != client_id:
            raise InvalidTokenError("Client mismatch")
        if stored['used']:
            # Token reuse detected - possible theft
            self.revoke_token_family(stored['family_id'])
            raise SecurityError("Token reuse detected")

        # Mark as used
        stored['used'] = True
        self.save_token(refresh_token, stored)

        # Issue new tokens
        new_access_token = self.generate_access_token(stored)
        new_refresh_token = self.generate_refresh_token(
            client_id=client_id,
            family_id=stored['family_id']  # Same family
        )

        return new_access_token, new_refresh_token
```

## ID Token Validation

```python
import jwt
from jwt import PyJWKClient

def validate_id_token(token, config):
    """Full ID token validation"""

    # 1. Get signing key from JWKS
    jwks_client = PyJWKClient(config['jwks_uri'])
    signing_key = jwks_client.get_signing_key_from_jwt(token)

    # 2. Decode and validate
    try:
        claims = jwt.decode(
            token,
            signing_key.key,
            algorithms=['RS256'],
            audience=config['client_id'],
            issuer=config['issuer']
        )
    except jwt.ExpiredSignatureError:
        raise SecurityError("Token expired")
    except jwt.InvalidAudienceError:
        raise SecurityError("Invalid audience")
    except jwt.InvalidIssuerError:
        raise SecurityError("Invalid issuer")

    # 3. Additional validations
    # Check nonce (if used)
    if config.get('nonce') and claims.get('nonce') != config['nonce']:
        raise SecurityError("Invalid nonce")

    # Check authorized party (if present)
    if 'azp' in claims and claims['azp'] != config['client_id']:
        raise SecurityError("Invalid authorized party")

    return claims
```

## Security Checklist

### Authorization Flow
- [ ] Using PKCE for all clients
- [ ] State parameter for CSRF protection
- [ ] Strict redirect URI validation
- [ ] Single-use authorization codes
- [ ] Codes expire quickly (< 10 min)

### Token Management
- [ ] Tokens encrypted at rest
- [ ] No tokens in URLs or logs
- [ ] Short access token lifetime
- [ ] Refresh token rotation
- [ ] Token revocation implemented

### Client Security
- [ ] Confidential clients use client secrets
- [ ] Public clients use PKCE only
- [ ] Client secrets never exposed
- [ ] Per-environment credentials

### Transport Security
- [ ] HTTPS everywhere
- [ ] HSTS enabled
- [ ] Secure cookies (HttpOnly, Secure, SameSite)
