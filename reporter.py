return {
    "parameter": parameter,
    "url": new_url,
    "status_code": response.status_code,
    "response_length": len(response.text),
    "reflected": MARKER in response.text
}
