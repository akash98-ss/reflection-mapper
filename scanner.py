import requests
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

MARKER = "XSS_REFLECTION_TEST_123456"

def test_parameter(url, parameter):
    parsed = urlparse(url)
    params = parse_qs(parsed.query)

    if parameter not in params:
        return None

    params[parameter] = [MARKER]

    new_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        urlencode(params, doseq=True),
        parsed.fragment
    ))

    try:
        response = requests.get(new_url, timeout=10)

        return {
            "parameter": parameter,
            "url": new_url,
            "reflected": MARKER in response.text,
            "response": response.text
        }

    except Exception as e:
        return {
            "parameter": parameter,
            "error": str(e)
        }