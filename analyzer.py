import re

def detect_context(response, marker):
    contexts = []

    if f">{marker}<" in response:
        contexts.append("HTML")

    attr_pattern = rf'=["\']{marker}["\']'
    if re.search(attr_pattern, response):
        contexts.append("ATTRIBUTE")

    js_pattern = rf'["\']{marker}["\']'
    if re.search(js_pattern, response):
        contexts.append("JAVASCRIPT_POSSIBLE")

    return contexts