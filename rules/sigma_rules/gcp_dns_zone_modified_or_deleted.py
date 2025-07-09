def rule(event):
    if event.deep_get("protoPayload", "methodName", default="") in [
        "Dns.ManagedZones.Delete",
        "Dns.ManagedZones.Update",
        "Dns.ManagedZones.Patch",
    ]:
        return True
    return False
