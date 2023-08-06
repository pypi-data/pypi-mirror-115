def configuration():
    x = {
        "email": {
            "endpoint": "http://mainpersis-hermes.dockins.myntra.com/myntra-notification-service/platform/notification/v2/email/event/publishWithUidx",
            "header": {
                "Authorization": "Basic c3NzOmZmZg==",
                "accept": "application/json",
                "content-type": "application/json",
                "x-myntra-client-id": "pretrpims"
            }
        },
        "slack": {
            "slack_url": "https://hooks.slack.com/services/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",
            "header": {
                "content-type": "application/json"
            }
        }
    }
    return x