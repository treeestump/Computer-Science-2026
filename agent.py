#!/usr/bin/env python3
"""
Python File Analyzer
====================
Reads all .py files in a specified folder, sends each to Claude,
and generates an HTML report per file containing:
  - Pseudocode
  - Flowchart (SVG)
  - Trace table

Usage:
    python analyze_python_files.py <folder_path> [--output <output_dir>]

Requirements:
    pip install anthropic

Set your API key:
    export ANTHROPIC_API_KEY=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
"""

import os
import sys
import json
import argparse
import textwrap
from pathlib import Path
from datetime import datetime

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic package not found. Run: pip install anthropic")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Prompt
# ---------------------------------------------------------------------------

SYSTEM_PROMPT = """You are an expert Python code analyst. Given Python source code, return a single JSON object with exactly these keys:

"summary"     - 2-3 sentence plain-English description of what the code does.
"pseudocode"  - Clean, readable pseudocode as a plain string. Use indentation. No markdown fences.
"flowchart"   - A self-contained SVG string (no xml declaration, no DOCTYPE) illustrating the main control flow.
                Rules for the SVG:
                  * width="700" height="auto" (set an explicit height based on content, minimum 200)
                  * Rounded rectangles (rx=8) for Start/End nodes, fill=#dbeafe stroke=#3b82f6
                  * Regular rectangles (rx=4) for process steps, fill=#f1f5f9 stroke=#94a3b8
                  * Diamonds (polygon) for decisions, fill=#fef9c3 stroke=#ca8a04
                  * Arrows: marker-end with a simple arrowhead, stroke=#64748b
                  * Text: font-family=monospace font-size=13 fill=#1e293b
                  * Label Yes/No on decision branches
                  * Keep it readable - max ~15 nodes for large files, group steps logically
"trace_table" - Array of row objects simulating a representative execution trace.
                Each row MUST have: "step" (int), "line" (str), "operation" (str).
                Add extra keys for each important variable being tracked.
                Max 25 rows. Use realistic example inputs.

Return ONLY valid JSON. No markdown code fences. No commentary before or after."""


# ---------------------------------------------------------------------------
# API call
# ---------------------------------------------------------------------------

def analyze_file(client: anthropic.Anthropic, filename: str, code: str) -> dict:
    prompt = f'Analyze this Python file named "{filename}":\n\n```python\n{code}\n```'

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = "".join(block.text for block in message.content if hasattr(block, "text"))
    raw = raw.strip()

    # Strip markdown fences if the model added them despite instructions
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
    if raw.endswith("```"):
        raw = raw.rsplit("```", 1)[0]

    return json.loads(raw.strip())


# ---------------------------------------------------------------------------
# HTML report builder
# ---------------------------------------------------------------------------

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Analysis: {filename}</title>
<style>
  *, *::before, *::after {{ box-sizing: border-box; }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    font-size: 15px; line-height: 1.6;
    background: #f8fafc; color: #1e293b; margin: 0; padding: 0;
  }}
  .topbar {{
    background: #0f172a; color: #e2e8f0;
    padding: 14px 32px; display: flex; align-items: center; gap: 12px;
  }}
  .topbar .icon {{ font-size: 22px; }}
  .topbar h1 {{ font-size: 17px; font-weight: 600; margin: 0; }}
  .topbar .meta {{ margin-left: auto; font-size: 12px; color: #94a3b8; }}
  .container {{ max-width: 960px; margin: 0 auto; padding: 28px 24px 60px; }}
  .summary-box {{
    background: #fff; border: 1px solid #e2e8f0; border-radius: 10px;
    padding: 18px 22px; margin-bottom: 28px;
  }}
  .summary-box h2 {{ font-size: 13px; font-weight: 600; color: #64748b; margin: 0 0 6px; text-transform: uppercase; letter-spacing: .06em; }}
  .summary-box p {{ margin: 0; color: #334155; }}
  .section {{
    background: #fff; border: 1px solid #e2e8f0; border-radius: 10px;
    overflow: hidden; margin-bottom: 24px;
  }}
  .section-header {{
    padding: 13px 20px; background: #f1f5f9;
    border-bottom: 1px solid #e2e8f0;
    display: flex; align-items: center; gap: 9px;
  }}
  .section-header .badge {{
    font-size: 11px; font-weight: 600; padding: 3px 9px; border-radius: 20px;
    background: #dbeafe; color: #1d4ed8;
  }}
  .section-header h3 {{ margin: 0; font-size: 15px; font-weight: 600; }}
  .section-body {{ padding: 20px 22px; }}
  pre {{
    background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px;
    padding: 16px 18px; font-family: "JetBrains Mono", "Fira Code", monospace;
    font-size: 13px; line-height: 1.7; overflow-x: auto; margin: 0;
    white-space: pre-wrap; word-break: break-word;
  }}
  .flowchart-wrap {{ overflow-x: auto; text-align: center; padding: 10px 0; }}
  .flowchart-wrap svg {{ max-width: 100%; height: auto; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
  th {{
    background: #f1f5f9; text-align: left;
    padding: 9px 13px; border: 1px solid #e2e8f0;
    font-weight: 600; font-size: 12px; color: #475569;
  }}
  td {{ padding: 8px 13px; border: 1px solid #e2e8f0; vertical-align: top; font-family: monospace; }}
  tr:nth-child(even) td {{ background: #f8fafc; }}
  .footer {{ text-align: center; font-size: 12px; color: #94a3b8; margin-top: 40px; }}
</style>
</head>
<body>
<div class="topbar">
  <span class="icon">🐍</span>
  <h1>{filename}</h1>
  <span class="meta">Generated {timestamp}</span>
</div>
<div class="container">

  <div class="summary-box">
    <h2>Summary</h2>
    <p>{summary}</p>
  </div>

  <div class="section">
    <div class="section-header">
      <span class="badge">Flowchart</span>
      <h3>Control flow diagram</h3>
    </div>
    <div class="section-body">
      <div class="flowchart-wrap">
        {flowchart}
      </div>
    </div>
  </div>

  <div class="section">
    <div class="section-header">
      <span class="badge">Trace</span>
      <h3>Execution trace table</h3>
    </div>
    <div class="section-body">
      {trace_table_html}
    </div>
  </div>

  <div class="section">
    <div class="section-header">
      <span class="badge">Pseudocode</span>
      <h3>Algorithm pseudocode</h3>
    </div>
    <div class="section-body">
      <pre>{pseudocode}</pre>
    </div>
  </div>

  <div class="footer">
    Python File Analyzer &mdash; powered by Claude &mdash; {timestamp}
  </div>
</div>
</body>
</html>
"""


def build_trace_table(rows: list) -> str:
    if not rows:
        return "<p style='color:#64748b'>No trace data returned.</p>"
    cols = list(rows[0].keys())
    header = "".join(f"<th>{c}</th>" for c in cols)
    body_rows = []
    for row in rows:
        cells = "".join(f"<td>{str(row.get(c, ''))}</td>" for c in cols)
        body_rows.append(f"<tr>{cells}</tr>")
    return f"<table><thead><tr>{header}</tr></thead><tbody>{''.join(body_rows)}</tbody></table>"


def escape_html(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build_html(filename: str, data: dict) -> str:
    return HTML_TEMPLATE.format(
        filename=filename,
        timestamp=datetime.now().strftime("%Y-%m-%d %H:%M"),
        summary=escape_html(data.get("summary", "No summary provided.")),
        flowchart=data.get("flowchart", "<p>No flowchart generated.</p>"),
        trace_table_html=build_trace_table(data.get("trace_table", [])),
        pseudocode=escape_html(data.get("pseudocode", "No pseudocode generated.")),
    )


# ---------------------------------------------------------------------------
# Index page
# ---------------------------------------------------------------------------

INDEX_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Python Analysis Report</title>
<style>
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; background: #f8fafc; color: #1e293b; margin: 0; padding: 40px 24px; }}
  h1 {{ font-size: 24px; margin-bottom: 6px; }}
  .sub {{ color: #64748b; margin-bottom: 32px; font-size: 14px; }}
  .grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 16px; max-width: 900px; }}
  .card {{
    background: #fff; border: 1px solid #e2e8f0; border-radius: 10px;
    padding: 18px 20px; text-decoration: none; color: inherit;
    transition: box-shadow .15s;
  }}
  .card:hover {{ box-shadow: 0 4px 16px #0001; }}
  .card .icon {{ font-size: 28px; margin-bottom: 8px; }}
  .card h3 {{ margin: 0 0 6px; font-size: 15px; word-break: break-all; }}
  .card p {{ margin: 0; font-size: 13px; color: #64748b; }}
  .card .status {{ margin-top: 10px; font-size: 12px; font-weight: 600; color: #16a34a; }}
  .card .status.error {{ color: #dc2626; }}
</style>
</head>
<body>
<h1>🐍 Python file analysis</h1>
<p class="sub">Generated {timestamp} &mdash; {count} file(s) analyzed</p>
<div class="grid">
{cards}
</div>
</body>
</html>
"""


def build_index(results: list, timestamp: str) -> str:
    cards = []
    for r in results:
        status_cls = "error" if r["error"] else "status"
        status_text = f"Error: {r['error']}" if r["error"] else "Analysis complete"
        link = f'href="{r["report_file"]}"' if not r["error"] else ""
        tag = "a" if not r["error"] else "div"
        cards.append(f"""
  <{tag} class="card" {link}>
    <div class="icon">🐍</div>
    <h3>{r['filename']}</h3>
    <p>{r['summary']}</p>
    <div class="status {'' if not r['error'] else 'error'}">{status_text}</div>
  </{tag}>""")
    return INDEX_TEMPLATE.format(
        timestamp=timestamp,
        count=len(results),
        cards="\n".join(cards),
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Analyze Python files with Claude AI")
    parser.add_argument("folder", help="Folder containing .py files to analyze")
    parser.add_argument("--output", default="analysis_output", help="Output directory (default: analysis_output)")
    parser.add_argument("--recursive", action="store_true", help="Recurse into subdirectories")
    args = parser.parse_args()

    folder = Path(args.folder).resolve()
    if not folder.is_dir():
        print(f"ERROR: '{folder}' is not a valid directory.")
        sys.exit(1)

    api_key = "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"
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.")
        print("  export ANTHROPIC_API_KEY=sk-ant-...")
        sys.exit(1)

    glob_pattern = "**/*.py" if args.recursive else "*.py"
    py_files = sorted(folder.glob(glob_pattern))

    # Exclude __pycache__ and hidden dirs
    py_files = [f for f in py_files if "__pycache__" not in f.parts and not any(p.startswith(".") for p in f.parts)]

    if not py_files:
        print(f"No .py files found in '{folder}'.")
        sys.exit(0)

    output_dir = Path(args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {output_dir}")
    print(f"Found {len(py_files)} Python file(s) to analyze.\n")

    client = anthropic.Anthropic(api_key=api_key)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    results = []

    for i, py_path in enumerate(py_files, 1):
        rel = py_path.relative_to(folder)
        print(f"[{i}/{len(py_files)}] Analyzing: {rel} ...", end=" ", flush=True)

        code = py_path.read_text(encoding="utf-8", errors="replace")

        report_name = str(rel).replace(os.sep, "_").replace("/", "_") + ".html"
        result_entry = {
            "filename": str(rel),
            "report_file": report_name,
            "summary": "",
            "error": None,
        }

        try:
            data = analyze_file(client, str(rel), code)
            result_entry["summary"] = data.get("summary", "")

            html = build_html(str(rel), data)
            report_path = output_dir / report_name
            report_path.write_text(html, encoding="utf-8")
            print(f"✓  →  {report_name}")

        except json.JSONDecodeError as e:
            result_entry["error"] = f"JSON parse error: {e}"
            print(f"✗  JSON parse error")
        except Exception as e:
            result_entry["error"] = str(e)
            print(f"✗  {e}")

        results.append(result_entry)

    # Write index
    index_html = build_index(results, timestamp)
    index_path = output_dir / "index.html"
    index_path.write_text(index_html, encoding="utf-8")

    print(f"\n{'='*55}")
    print(f"Done! {sum(1 for r in results if not r['error'])}/{len(results)} file(s) analyzed successfully.")
    print(f"Open: {index_path}")


if __name__ == "__main__":
    main()