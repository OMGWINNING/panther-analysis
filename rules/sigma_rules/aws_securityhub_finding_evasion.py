def rule(event):
    if all(
        [
            event.deep_get("eventSource", default="") == "securityhub.amazonaws.com",
            event.deep_get("eventName", default="")
            in ["BatchUpdateFindings", "DeleteInsight", "UpdateFindings", "UpdateInsight"],
        ]
    ):
        return True
    return False
