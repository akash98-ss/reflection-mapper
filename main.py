@'
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse, parse_qs

from scanner import test_parameter, MARKER
from analyzer import detect_context
from reporter import save_report


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Reflection Mapper - Web parameter reflection scanner"
    )

    parser.add_argument(
        "-u",
        "--url",
        required=True,
        help="Target URL containing query parameters"
    )

    parser.add_argument(
        "--json",
        metavar="FILE",
        help="Save the report as JSON"
    )

    parser.add_argument(
        "--report",
        metavar="FILE",
        help="Save the report to the specified file"
    )

    parser.add_argument(
        "-t",
        "--threads",
        type=int,
        default=10,
        help="Number of concurrent workers (default: 10)"
    )

    return parser.parse_args()


def validate_url(url):
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise ValueError("URL must start with http:// or https://")

    if not parsed.netloc:
        raise ValueError("Invalid URL: missing hostname")

    return parsed


def main():
    args = parse_arguments()

    try:
        validate_url(args.url)
    except ValueError as e:
        print(f"[-] {e}")
        return 1

    target = args.url.strip()

    output_file = args.report or args.json or "report.json"

    params = parse_qs(urlparse(target).query)

    if not params:
        print("[-] No query parameters found in target URL.")
        print(f"    Target: {target}")
        return 1

    print(f"Target URL: {target}")
    print(f"Parameters: {', '.join(params.keys())}")
    print(f"Threads: {args.threads}")
    print()

    results = []

    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {
            executor.submit(test_parameter, target, param): param
            for param in params
        }

        for future in as_completed(futures):
            parameter = futures[future]

            try:
                result = future.result()
            except Exception as e:
                print(f"[-] {parameter}: {e}")
                continue

            if not result:
                continue

            if result.get("reflected"):
                result["contexts"] = detect_context(
                    result["response"],
                    MARKER
                )

            result.pop("response", None)

            results.append(result)

            status = "REFLECTED" if result.get("reflected") else "not reflected"
            print(f"[{status}] {parameter}")

    save_report(results, output_file)

    print()
    print(f"[+] Scan complete")
    print(f"[+] Results: {len(results)}")
    print(f"[+] Report: {output_file}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
'@ | Set-Content .\main.py