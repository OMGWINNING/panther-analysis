def rule(event):
    if all(
        [
            event.deep_get("eventSource", default="") == "ec2.amazonaws.com",
            event.deep_get("requestParameters", "attribute", default="") == "userData",
            event.deep_get("eventName", default="") == "ModifyInstanceAttribute",
        ]
    ):
        return True
    return False
