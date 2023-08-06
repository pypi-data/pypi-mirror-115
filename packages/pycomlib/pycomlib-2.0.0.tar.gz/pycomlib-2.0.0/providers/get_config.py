def configuration():
    x = {
        "email": {
            "endpoint": "",
            "header": {
                "Authorization": "Basic c3NzOmZmZg==",
                "accept": "application/json",
                "content-type": "application/json",
                "x-myntra-client-id": "pretrpims",
                "x-myntra-idea-tenant" : "5"
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