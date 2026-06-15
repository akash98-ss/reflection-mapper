from urllib.parse import urlparse, parse_qs
from concurrent.futures import ThreadPoolExecutor

from scanner import test_parameter, MARKER
from analyzer import detect_context
from reporter import save_report

target = input("Target URL: ").strip()

params = parse_qs(urlparse(target).query)

results = []

with ThreadPoolExecutor(max_workers=10) as executor:
    futures = []

    for param in params:
        futures.append(executor.submit(test_parameter, target, param))

    for future in futures:
        result = future.result()

        if not result:
            continue

        if result.get("reflected"):
            result["contexts"] = detect_context(
                result["response"],
                MARKER
            )

        results.append(result)

save_report(results)

print("Report saved to report.json")