# Testing Webhooks

## Local Development

### ngrok

Expose local server to internet:

```bash
# Start your local server
python app.py  # Running on localhost:5000

# In another terminal, start ngrok
ngrok http 5000

# Output:
# Forwarding https://abc123.ngrok.io -> http://localhost:5000
```

Use the ngrok URL as your webhook endpoint during development.

### localtunnel

```bash
npm install -g localtunnel
lt --port 5000
# https://wild-tiger-42.loca.lt
```

### Cloudflare Tunnel

```bash
cloudflared tunnel --url http://localhost:5000
```

## Testing Tools

### Webhook.site

- Visit https://webhook.site
- Get unique URL
- Point webhooks there
- See all incoming requests

### RequestBin

```bash
# Self-hosted option
docker run -p 8080:8080 requestbin/requestbin
```

## Manual Testing

### cURL

```bash
# Basic webhook test
curl -X POST https://your-app.com/webhooks/provider \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Signature: sha256=abc123..." \
  -H "X-Webhook-Timestamp: 1706616000" \
  -d '{"type": "test", "data": {}}'
```

### Generate Signatures

```python
import hmac
import hashlib
import time
import json

def generate_test_webhook(payload, secret):
    """Generate signed test webhook"""
    timestamp = int(time.time())
    payload_json = json.dumps(payload)

    signed_payload = f"{timestamp}.{payload_json}"
    signature = hmac.new(
        secret.encode(),
        signed_payload.encode(),
        hashlib.sha256
    ).hexdigest()

    return {
        'payload': payload_json,
        'headers': {
            'X-Webhook-Signature': f'sha256={signature}',
            'X-Webhook-Timestamp': str(timestamp),
            'Content-Type': 'application/json'
        }
    }

# Usage
test = generate_test_webhook(
    {'type': 'payment.completed', 'amount': 100},
    'your-secret'
)
print(f"curl -X POST http://localhost:5000/webhook \\")
for k, v in test['headers'].items():
    print(f"  -H '{k}: {v}' \\")
print(f"  -d '{test['payload']}'")
```

## Provider CLI Tools

### Stripe CLI

```bash
# Install
brew install stripe/stripe-cli/stripe

# Login
stripe login

# Forward events to local
stripe listen --forward-to localhost:5000/webhooks/stripe

# Trigger test events
stripe trigger payment_intent.succeeded
stripe trigger customer.subscription.created
```

### GitHub CLI

```bash
# Create webhook
gh api repos/{owner}/{repo}/hooks -f url=https://your-url.com/webhook \
  -f content_type=json -f events[]="push" -f events[]="pull_request"

# Redeliver webhook
gh api repos/{owner}/{repo}/hooks/{hook_id}/deliveries/{delivery_id}/attempts \
  -X POST
```

## Automated Testing

### Unit Tests

```python
import pytest
from unittest.mock import patch
import hmac
import hashlib

def generate_signature(payload, secret, timestamp):
    signed = f"{timestamp}.{payload}"
    return 'sha256=' + hmac.new(
        secret.encode(), signed.encode(), hashlib.sha256
    ).hexdigest()

class TestWebhookHandler:

    def test_valid_signature(self, client):
        payload = '{"type": "test"}'
        timestamp = "1706616000"
        signature = generate_signature(payload, 'test-secret', timestamp)

        response = client.post('/webhook',
            data=payload,
            headers={
                'X-Webhook-Signature': signature,
                'X-Webhook-Timestamp': timestamp,
                'Content-Type': 'application/json'
            }
        )

        assert response.status_code == 200

    def test_invalid_signature(self, client):
        response = client.post('/webhook',
            data='{"type": "test"}',
            headers={
                'X-Webhook-Signature': 'sha256=invalid',
                'X-Webhook-Timestamp': '1706616000',
                'Content-Type': 'application/json'
            }
        )

        assert response.status_code == 401

    def test_expired_timestamp(self, client):
        payload = '{"type": "test"}'
        old_timestamp = "1000000000"  # Very old
        signature = generate_signature(payload, 'test-secret', old_timestamp)

        response = client.post('/webhook',
            data=payload,
            headers={
                'X-Webhook-Signature': signature,
                'X-Webhook-Timestamp': old_timestamp,
                'Content-Type': 'application/json'
            }
        )

        assert response.status_code == 401

    def test_idempotency(self, client):
        """Same webhook processed only once"""
        payload = '{"id": "evt_123", "type": "test"}'
        timestamp = str(int(time.time()))
        signature = generate_signature(payload, 'test-secret', timestamp)

        headers = {
            'X-Webhook-Signature': signature,
            'X-Webhook-Timestamp': timestamp,
            'Content-Type': 'application/json'
        }

        # First request
        response1 = client.post('/webhook', data=payload, headers=headers)
        assert response1.status_code == 200

        # Second request (same event ID)
        response2 = client.post('/webhook', data=payload, headers=headers)
        assert response2.status_code == 200  # Still 200, but not reprocessed

        # Verify processed only once
        assert get_process_count('evt_123') == 1
```

### Integration Tests

```python
@pytest.mark.integration
class TestWebhookIntegration:

    def test_end_to_end_flow(self):
        """Test full webhook flow"""
        # Create test data
        order = create_test_order()

        # Simulate webhook
        webhook_payload = {
            'type': 'payment.completed',
            'data': {'order_id': order.id}
        }

        send_test_webhook(webhook_payload)

        # Wait for processing
        time.sleep(1)

        # Verify state changed
        order.refresh()
        assert order.status == 'paid'
        assert order.paid_at is not None
```

## Monitoring & Debugging

### Logging

```python
import logging

logger = logging.getLogger('webhooks')

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    # Log incoming request
    logger.info(f"Webhook received: {request.headers.get('X-Webhook-ID')}")
    logger.debug(f"Headers: {dict(request.headers)}")
    logger.debug(f"Payload: {request.data[:500]}")  # Truncate

    try:
        # Process
        result = process_webhook(request)
        logger.info(f"Webhook processed: {result}")
        return '', 200

    except Exception as e:
        logger.error(f"Webhook failed: {e}", exc_info=True)
        return '', 500
```

### Replay Failed Webhooks

```python
class WebhookReplaySystem:
    """Store and replay failed webhooks"""

    def store_failed(self, webhook_id, payload, headers, error):
        self.db.store({
            'id': webhook_id,
            'payload': payload,
            'headers': headers,
            'error': str(error),
            'failed_at': time.time(),
            'retry_count': 0
        })

    def replay(self, webhook_id):
        """Replay a failed webhook"""
        failed = self.db.get(webhook_id)
        return self.send_to_handler(failed['payload'], failed['headers'])

    def replay_all_recent(self, hours=24):
        """Replay all recent failures"""
        cutoff = time.time() - (hours * 3600)
        failed = self.db.query(failed_at__gt=cutoff)
        for webhook in failed:
            self.replay(webhook['id'])
```
