# Token Management Patterns

## Token Storage Options

### Web Applications

| Storage | Security | Persistence | Use Case |
|---------|----------|-------------|----------|
| HttpOnly Cookie | High | Session/Persistent | Server-rendered apps |
| Server Session | High | Session | Traditional web apps |
| Memory (SPA) | Medium | None | Short sessions |

### Mobile Applications

| Storage | Security | Use Case |
|---------|----------|----------|
| Keychain (iOS) | High | Production |
| Keystore (Android) | High | Production |
| Encrypted Storage | Medium | Cross-platform |

### Backend Services

| Storage | Security | Use Case |
|---------|----------|----------|
| Environment Variables | Medium | Tokens only |
| Secrets Manager | High | Production |
| Encrypted Database | High | Multi-tenant |

## Cookie-Based Token Storage

```python
from flask import make_response

def set_token_cookies(response, tokens, secure=True):
    """Store tokens in HttpOnly cookies"""

    # Access token - short expiry
    response.set_cookie(
        'access_token',
        tokens['access_token'],
        httponly=True,
        secure=secure,
        samesite='Strict',
        max_age=tokens.get('expires_in', 3600)
    )

    # Refresh token - longer expiry
    if 'refresh_token' in tokens:
        response.set_cookie(
            'refresh_token',
            tokens['refresh_token'],
            httponly=True,
            secure=secure,
            samesite='Strict',
            max_age=86400 * 30,  # 30 days
            path='/auth/refresh'  # Only sent to refresh endpoint
        )

    return response

def get_access_token(request):
    """Get access token from cookie"""
    return request.cookies.get('access_token')
```

## Token Refresh Pattern

### Proactive Refresh

```python
class TokenManager:
    """Proactive token refresh before expiry"""

    REFRESH_BUFFER = 60  # Refresh 60s before expiry

    def __init__(self, oauth_client, storage):
        self.oauth = oauth_client
        self.storage = storage

    async def get_token(self, user_id):
        tokens = await self.storage.get(user_id)
        if not tokens:
            raise NotAuthenticatedError()

        # Check if needs refresh
        if self._should_refresh(tokens):
            tokens = await self._refresh(user_id, tokens)

        return tokens['access_token']

    def _should_refresh(self, tokens):
        expires_at = tokens.get('expires_at', 0)
        return time.time() > (expires_at - self.REFRESH_BUFFER)

    async def _refresh(self, user_id, tokens):
        try:
            new_tokens = await self.oauth.refresh_token(
                tokens['refresh_token']
            )
            new_tokens['expires_at'] = time.time() + new_tokens['expires_in']
            await self.storage.set(user_id, new_tokens)
            return new_tokens
        except RefreshError:
            await self.storage.delete(user_id)
            raise NotAuthenticatedError("Refresh failed, please login again")
```

### Reactive Refresh (On 401)

```python
class APIClient:
    """Client that refreshes on 401"""

    def __init__(self, token_manager):
        self.tokens = token_manager

    async def request(self, method, url, **kwargs):
        token = await self.tokens.get_token()  # allow-secret

        response = await self._make_request(
            method, url, token=token, **kwargs  # allow-secret
        )

        if response.status_code == 401:
            # Try refresh and retry once
            try:
                token = await self.tokens.force_refresh()  # allow-secret
                response = await self._make_request(
                    method, url, token=token, **kwargs  # allow-secret
                )
            except RefreshError:
                raise NotAuthenticatedError()

        return response
```

## Token Rotation

### Refresh Token Rotation

```python
class RotatingRefreshTokenStore:
    """Issue new refresh token on each use"""

    def __init__(self, db):
        self.db = db

    async def exchange_refresh_token(self, old_token):
        # Get token record
        record = await self.db.get_refresh_token(old_token)
        if not record:
            raise InvalidTokenError()

        # Check if already used
        if record['used']:
            # Possible token theft - revoke entire family
            await self.revoke_family(record['family_id'])
            raise SecurityError("Refresh token reuse detected")

        # Mark as used
        await self.db.mark_token_used(old_token)

        # Generate new refresh token (same family)
        new_token = self.generate_token()
        await self.db.create_refresh_token({
            'token': new_token,
            'family_id': record['family_id'],
            'user_id': record['user_id'],
            'used': False
        })

        return new_token

    async def revoke_family(self, family_id):
        """Revoke all tokens in family"""
        await self.db.delete_tokens_by_family(family_id)
```

## Token Revocation

```python
class TokenRevocation:
    """Handle token revocation"""

    def __init__(self, token_store, blocklist):
        self.store = token_store
        self.blocklist = blocklist

    async def revoke_user_tokens(self, user_id):
        """Revoke all tokens for a user (logout everywhere)"""
        await self.store.delete_user_tokens(user_id)

    async def revoke_access_token(self, token):
        """Add access token to blocklist"""
        # Decode to get expiry
        claims = decode_token(token)
        ttl = claims['exp'] - time.time()

        if ttl > 0:
            # Add to blocklist until it would expire anyway
            await self.blocklist.add(token, ttl=int(ttl))

    async def is_revoked(self, token):
        """Check if token is revoked"""
        return await self.blocklist.contains(token)
```

## Multi-Device Token Management

```python
class DeviceTokenManager:
    """Manage tokens per device"""

    async def create_session(self, user_id, device_info):
        """Create new session for device"""
        session = {
            'id': generate_session_id(),
            'user_id': user_id,
            'device': device_info,
            'created_at': time.time(),
            'last_used': time.time()
        }
        await self.db.create_session(session)
        return session

    async def get_user_sessions(self, user_id):
        """List all active sessions for user"""
        sessions = await self.db.get_sessions_by_user(user_id)
        return [{
            'id': s['id'],
            'device': s['device'],
            'created_at': s['created_at'],
            'last_used': s['last_used'],
            'is_current': s['id'] == current_session_id
        } for s in sessions]

    async def revoke_session(self, session_id, user_id):
        """Revoke specific session"""
        session = await self.db.get_session(session_id)
        if session['user_id'] != user_id:
            raise ForbiddenError()
        await self.db.delete_session(session_id)

    async def revoke_all_other_sessions(self, user_id, current_session_id):
        """Revoke all sessions except current"""
        await self.db.delete_sessions_except(user_id, current_session_id)
```

## Offline Token Access

```python
class OfflineTokenManager:
    """Handle offline access (long-lived tokens)"""

    async def request_offline_access(self, user_id, purpose):
        """Request offline access for specific purpose"""
        # Requires user consent
        consent = await self.get_user_consent(user_id, purpose)
        if not consent:
            raise ConsentRequiredError()

        # Issue long-lived refresh token
        token = await self.oauth.get_token_with_scope('offline_access')  # allow-secret

        # Store with metadata
        await self.db.store_offline_token({
            'user_id': user_id,
            'purpose': purpose,
            'token': encrypt(token),
            'granted_at': time.time(),
            'scopes': token['scope']
        })

        return token

    async def use_offline_token(self, user_id, purpose):
        """Use stored offline token"""
        record = await self.db.get_offline_token(user_id, purpose)
        if not record:
            raise NoOfflineAccessError()

        token = decrypt(record['token'])  # allow-secret

        # Refresh if needed
        if self._is_expired(token):
            token = await self.oauth.refresh_token(token['refresh_token'])  # allow-secret
            await self._update_stored_token(record['id'], token)

        return token['access_token']
```
