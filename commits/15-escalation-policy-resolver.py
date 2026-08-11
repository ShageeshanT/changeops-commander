"""Resolve the next responder in an escalation policy chain."""


def next_responder(policy_chain, unavailable=None):
    """policy_chain: ordered list of names. Returns first available responder."""
    unavailable = unavailable or set()
    for name in policy_chain:
        if name not in unavailable:
            return name
    return None


if __name__ == "__main__":
    chain = ["Asha", "Bimal", "Chamath"]
    assert next_responder(chain, unavailable={"Asha"}) == "Bimal"
    print("escalation_policy_resolver: ok")
