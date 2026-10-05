import json
from pathlib import Path


def save_report(results, filename="report.json"):
    output = Path(filename)

    if output.suffix.lower() == ".json":
        save_json(results, output)
    elif output.suffix.lower() in (".html", ".htm"):
        save_html(results, output)
    else:
        raise ValueError(
            f"Unsupported report format: {output.suffix}. "
            "Use .json or .html"
        )


def save_json(results, output):
    with output.open("w", encoding="utf-8") as f:
        json.dump(results, f, indent=4)

    print(f"[+] Report saved to {output}")


def save_html(results, output):
    rows = []

    for result in results:
        parameter = result.get("parameter", "")
        url = result.get("url", "")
        reflected = result.get("reflected", False)
        contexts = ", ".join(result.get("contexts", []))

        status = "REFLECTED" if reflected else "Not reflected"

        rows.append(
            f"""
            <tr>
                <td>{parameter}</td>
                <td>{status}</td>
                <td>{contexts or "-"}</td>
                <td><code>{url}</code></td>
            </tr>
            """
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Reflection Mapper Report</title>

    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background: #f5f5f5;
        }}

        h1 {{
            color: #222;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background: white;
        }}

        th, td {{
            padding: 12px;
            border: 1px solid #ddd;
            text-align: left;
        }}

        th {{
            background: #222;
            color: white;
        }}

        code {{
            word-break: break-all;
        }}
    </style>
</head>

<body>
    <h1>Reflection Mapper Report</h1>

    <p>
        Parameters tested: <strong>{len(results)}</strong>
    </p>

    <table>
        <thead>
            <tr>
                <th>Parameter</th>
                <th>Status</th>
                <th>Context</th>
                <th>Test URL</th>
            </tr>
        </thead>

        <tbody>
            {"".join(rows)}
        </tbody>
    </table>
</body>
</html>
"""

    output.write_text(html, encoding="utf-8")

    print(f"[+] Report saved to {output}")
