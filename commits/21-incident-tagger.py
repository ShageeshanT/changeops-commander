"""Auto-tag an incident description using keyword matching."""

KEYWORD_TAGS = {
    "timeout": "database",
    "latency": "performance",
    "500": "server-error",
    "auth": "authentication",
    "deploy": "deployment",
}


def auto_tag(description: str):
    text = description.lower()
    return sorted({tag for keyword, tag in KEYWORD_TAGS.items() if keyword in text})


if __name__ == "__main__":
    tags = auto_tag("Users seeing 500 errors after deploy, high latency on checkout")
    assert "server-error" in tags and "deployment" in tags
    print("incident_tagger: ok")
