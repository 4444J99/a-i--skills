# Webhook Provider Examples

## Stripe

### Event Structure

```json
{
  "id": "evt_1234567890",
  "object": "event",
  "api_version": "2023-10-16",
  "created": 1706616000,
  "type": "payment_intent.succeeded",
  "data": {
    "object": {
      "id": "pi_1234567890",
      "amount": 2000,
      "currency": "usd",
      "status": "succeeded"
    }
  },
  "livemode": true,
  "pending_webhooks": 1,
  "request": {
    "id": "req_1234567890",
    "idempotency_key": null
  }
}
```

### Handler Example

```python
import stripe
from flask import Flask, request

@app.route('/webhooks/stripe', methods=['POST'])
def stripe_webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, STRIPE_ENDPOINT_SECRET
        )
    except stripe.error.SignatureVerificationError:
        return 'Invalid signature', 400

    # Handle event types
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        handle_successful_payment(payment_intent)

    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        handle_failed_payment(payment_intent)

    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        handle_subscription_cancelled(subscription)

    return '', 200
```

### Common Event Types

| Event | When |
|-------|------|
| `payment_intent.succeeded` | Payment completed |
| `payment_intent.payment_failed` | Payment failed |
| `customer.subscription.created` | New subscription |
| `customer.subscription.updated` | Subscription changed |
| `customer.subscription.deleted` | Subscription cancelled |
| `invoice.paid` | Invoice paid |
| `invoice.payment_failed` | Invoice payment failed |

## GitHub

### Event Structure

```json
{
  "action": "opened",
  "number": 123,
  "pull_request": {
    "id": 1234567890,
    "title": "Fix bug",
    "user": {
      "login": "username"
    },
    "head": {
      "ref": "feature-branch"
    },
    "base": {
      "ref": "main"
    }
  },
  "repository": {
    "full_name": "owner/repo"
  },
  "sender": {
    "login": "username"
  }
}
```

### Handler Example

```python
import hmac
import hashlib

@app.route('/webhooks/github', methods=['POST'])
def github_webhook():
    signature = request.headers.get('X-Hub-Signature-256')
    event_type = request.headers.get('X-GitHub-Event')

    if not verify_github_signature(request.data, signature):
        return 'Invalid signature', 401

    payload = request.json

    if event_type == 'push':
        handle_push(payload)
    elif event_type == 'pull_request':
        action = payload.get('action')
        if action == 'opened':
            handle_pr_opened(payload)
        elif action == 'closed' and payload['pull_request']['merged']:
            handle_pr_merged(payload)
    elif event_type == 'issues':
        handle_issue(payload)

    return '', 200
```

### Common Event Types

| Event | Actions |
|-------|---------|
| `push` | Commits pushed |
| `pull_request` | opened, closed, merged, synchronize |
| `issues` | opened, closed, assigned |
| `issue_comment` | created, edited, deleted |
| `release` | published, released |

## Twilio

### Event Structure

```
POST /webhooks/twilio
Content-Type: application/x-www-form-urlencoded

AccountSid=AC1234567890
ApiVersion=2010-04-01
From=%2B15551234567
To=%2B15559876543
Body=Hello+World
MessageSid=SM1234567890
```

### Handler Example

```python
from twilio.request_validator import RequestValidator

@app.route('/webhooks/twilio', methods=['POST'])
def twilio_webhook():
    validator = RequestValidator(TWILIO_AUTH_TOKEN)

    # Build full URL for validation
    url = request.url
    params = request.form.to_dict()
    signature = request.headers.get('X-Twilio-Signature')

    if not validator.validate(url, params, signature):
        return 'Invalid signature', 403

    # Handle incoming SMS
    from_number = request.form.get('From')
    body = request.form.get('Body')

    process_sms(from_number, body)

    # Return TwiML response
    return '''<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Message>Thanks for your message!</Message>
    </Response>''', 200, {'Content-Type': 'text/xml'}
```

## Slack

### Event Structure

```json
{
  "token": "verification_token",
  "team_id": "T1234567890",
  "api_app_id": "A1234567890",
  "event": {
    "type": "message",
    "channel": "C1234567890",
    "user": "U1234567890",
    "text": "Hello",
    "ts": "1234567890.123456"
  },
  "type": "event_callback",
  "event_id": "Ev1234567890",
  "event_time": 1234567890
}
```

### Handler Example

```python
@app.route('/webhooks/slack', methods=['POST'])
def slack_webhook():
    # URL verification challenge
    if request.json.get('type') == 'url_verification':
        return request.json['challenge']

    # Verify signature
    timestamp = request.headers.get('X-Slack-Request-Timestamp')
    signature = request.headers.get('X-Slack-Signature')

    if not verify_slack_signature(request.data, timestamp, signature):
        return 'Invalid signature', 403

    event = request.json.get('event', {})
    event_type = event.get('type')

    if event_type == 'message':
        # Ignore bot messages
        if event.get('bot_id'):
            return '', 200
        handle_message(event)

    elif event_type == 'app_mention':
        handle_mention(event)

    return '', 200
```

## SendGrid

### Event Structure

```json
[
  {
    "email": "user@example.com",
    "timestamp": 1706616000,
    "event": "delivered",
    "sg_event_id": "sg_event_id",
    "sg_message_id": "sg_message_id"
  }
]
```

### Handler Example

```python
@app.route('/webhooks/sendgrid', methods=['POST'])
def sendgrid_webhook():
    # SendGrid uses signed webhooks (optional)
    signature = request.headers.get('X-Twilio-Email-Event-Webhook-Signature')
    timestamp = request.headers.get('X-Twilio-Email-Event-Webhook-Timestamp')

    if signature:
        if not verify_sendgrid_signature(request.data, signature, timestamp):
            return 'Invalid signature', 403

    events = request.json

    for event in events:
        event_type = event.get('event')

        if event_type == 'delivered':
            mark_email_delivered(event['email'], event['sg_message_id'])
        elif event_type == 'bounce':
            handle_bounce(event['email'], event.get('reason'))
        elif event_type == 'open':
            track_email_open(event['email'], event['sg_message_id'])
        elif event_type == 'click':
            track_email_click(event['email'], event.get('url'))
        elif event_type == 'spam_report':
            handle_spam_report(event['email'])

    return '', 200
```

### Common Event Types

| Event | Description |
|-------|-------------|
| `processed` | Email accepted |
| `delivered` | Email delivered |
| `bounce` | Email bounced |
| `open` | Email opened |
| `click` | Link clicked |
| `spam_report` | Marked as spam |
| `unsubscribe` | Unsubscribed |
