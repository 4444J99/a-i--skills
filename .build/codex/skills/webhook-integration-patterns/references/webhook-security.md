# Webhook Security Guide

## Signature Verification

### HMAC-SHA256 Implementation

```python
import hmac
import hashlib

def verify_webhook_signature(payload, signature, secret, timestamp=None):
    """
    Verify HMAC-SHA256 signature

    Common formats:
    - sha256=<hex>
    - v1=<hex>
    - Just <hex>
    """
    # Extract hash from signature header
    if signature.startswith('sha256='):
        provided_hash = signature[7:]
    elif signature.startswith('v1='):
        provided_hash = signature[3:]
    else:
        provided_hash = signature

    # Build signed payload
    if timestamp:
        signed_payload = f"{timestamp}.{payload}"
    else:
        signed_payload = payload

    # Compute expected signature
    expected = hmac.new(
        secret.encode(),
        signed_payload.encode(),
        hashlib.sha256
    ).hexdigest()

    # Constant-time comparison (prevents timing attacks)
    return hmac.compare_digest(expected, provided_hash)
```

### Timestamp Validation

```python
import time

MAX_AGE_SECONDS = 300  # 5 minutes

def validate_timestamp(timestamp_header):
    """Prevent replay attacks with timestamp validation"""
    try:
        timestamp = int(timestamp_header)
    except (ValueError, TypeError):
        raise SecurityError("Invalid timestamp format")

    current_time = int(time.time())
    age = abs(current_time - timestamp)

    if age > MAX_AGE_SECONDS:
        raise SecurityError(f"Timestamp too old: {age}s")

    return True
```

## Provider-Specific Verification

### Stripe

```python
import stripe

def verify_stripe_webhook(payload, sig_header, endpoint_secret):
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
        return event
    except stripe.error.SignatureVerificationError:
        raise SecurityError("Invalid Stripe signature")
```

### GitHub

```python
def verify_github_webhook(payload, signature, secret):
    """GitHub uses sha256=<hex> format"""
    if not signature.startswith('sha256='):
        return False

    expected = 'sha256=' + hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected, signature)
```

### Slack

```python
def verify_slack_request(body, timestamp, signature, signing_secret):
    """Slack's request verification"""
    # Check timestamp
    if abs(time.time() - float(timestamp)) > 300:
        return False

    # Compute signature
    sig_basestring = f"v0:{timestamp}:{body}"
    expected = 'v0=' + hmac.new(
        signing_secret.encode(),
        sig_basestring.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected, signature)
```

## IP Allowlisting

### Provider IP Ranges

```python
# Keep updated from provider documentation
ALLOWED_IPS = {
    'stripe': [
        '3.18.12.63',
        '3.130.192.231',
        # ... see Stripe docs
    ],
    'github': [
        '192.30.252.0/22',
        '185.199.108.0/22',
        '140.82.112.0/20',
        '143.55.64.0/20',
    ],
    'twilio': [
        '54.172.60.0/23',
        '54.244.51.0/24',
        '54.171.127.192/26',
        # ... see Twilio docs
    ]
}

import ipaddress

def verify_source_ip(client_ip, provider):
    """Verify IP is from expected provider"""
    allowed = ALLOWED_IPS.get(provider, [])

    for allowed_range in allowed:
        if '/' in allowed_range:
            # CIDR notation
            network = ipaddress.ip_network(allowed_range)
            if ipaddress.ip_address(client_ip) in network:
                return True
        else:
            # Single IP
            if client_ip == allowed_range:
                return True

    return False
```

## TLS/HTTPS

### Enforce HTTPS

```python
# Flask
@app.before_request
def force_https():
    if not request.is_secure:
        return "HTTPS required", 403

# Or via reverse proxy (nginx)
# location /webhooks {
#     if ($scheme != "https") {
#         return 403;
#     }
# }
```

### Certificate Pinning (Advanced)

```python
import ssl
import certifi

def create_ssl_context_with_pinning(expected_fingerprint):
    """Pin to specific certificate"""
    context = ssl.create_default_context(cafile=certifi.where())

    def verify_callback(conn, cert, errno, depth, ok):
        if depth == 0:  # Leaf certificate
            # Get fingerprint
            fingerprint = cert.digest("sha256").decode()
            return fingerprint == expected_fingerprint
        return ok

    context.verify_mode = ssl.CERT_REQUIRED
    return context
```

## Secret Management

### Rotation Strategy

```python
class WebhookSecretManager:
    """Manage webhook secret rotation"""

    def __init__(self, storage):
        self.storage = storage

    def rotate_secret(self, endpoint_id):
        """Rotate to new secret while supporting old"""
        old_secret = self.storage.get_current_secret(endpoint_id)
        new_secret = self.generate_secret()

        self.storage.set_secrets(endpoint_id, {
            'current': new_secret,
            'previous': old_secret,
            'rotated_at': time.time()
        })

        return new_secret

    def get_verification_secrets(self, endpoint_id):
        """Get secrets for verification (current + grace period)"""
        secrets = self.storage.get_secrets(endpoint_id)
        result = [secrets['current']]

        # Accept previous for 24 hours after rotation
        if secrets.get('previous'):
            if time.time() - secrets['rotated_at'] < 86400:
                result.append(secrets['previous'])

        return result

    def verify(self, endpoint_id, payload, signature):
        """Try all valid secrets"""
        for secret in self.get_verification_secrets(endpoint_id):
            if verify_signature(payload, signature, secret):
                return True
        return False

    @staticmethod
    def generate_secret(length=32):
        import secrets
        return secrets.token_urlsafe(length)
```

## Rate Limiting

```python
from collections import defaultdict
import time

class WebhookRateLimiter:
    """Prevent abuse via rate limiting"""

    def __init__(self, max_per_minute=60, max_per_hour=1000):
        self.max_minute = max_per_minute
        self.max_hour = max_per_hour
        self.requests = defaultdict(list)

    def is_allowed(self, endpoint_id):
        now = time.time()
        requests = self.requests[endpoint_id]

        # Clean old entries
        requests[:] = [t for t in requests if now - t < 3600]

        # Check limits
        minute_count = sum(1 for t in requests if now - t < 60)
        hour_count = len(requests)

        if minute_count >= self.max_minute:
            return False, "Rate limit: too many per minute"
        if hour_count >= self.max_hour:
            return False, "Rate limit: too many per hour"

        requests.append(now)
        return True, None
```

## Security Checklist

- [ ] Signature verification implemented
- [ ] Timestamp validation to prevent replay
- [ ] HTTPS enforced
- [ ] IP allowlisting (if provider supports)
- [ ] Rate limiting in place
- [ ] Secrets stored securely (not in code)
- [ ] Secret rotation process defined
- [ ] Logging of failed verifications
- [ ] Monitoring for anomalies
