ADD_DEL_IAM_IDP_SAML_EVENT_NAMES = [
    "CreateSAMLProvider",
    "DeleteSAMLProvider",
    "UpdateSAMLProvider",
    "CreateOpenIDConnectProvider",
    "DeleteOpenIDConnectProvider"
]

EVENT_SOURCE = "iam.amazonaws.com"


def rule(event):
    if (
        event.get("eventSource") == EVENT_SOURCE and
        event.get("eventName") in ADD_DEL_IAM_IDP_SAML_EVENT_NAMES and
        event.deep_get("userIdentity", "sessionContext", "sessionIssuer", "userName") not in ["pulumi", "AtlantisRole", None]
    ):
        return True
    return False


def title(event):
    return (
        f"User [{event.deep_get('userIdentity', 'arn')}]"
        f"performed a [{event.get('eventName')}] "
        f"action in AWS account [{event.get('recipientAccountId')}]."
    )
