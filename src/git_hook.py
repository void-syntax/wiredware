import json
import sys
from pathlib import Path

from rich.console import Console

from base_logic import *
from git_logic import *

report_names = []
reports = []
reports_vectors = []

console = Console(stderr=True)
console.rule("[bold cyan]WIREDWARE AI SECURITY GATE[/]")

folder = Path(__file__).resolve().parent.parent / "security_reports"
if folder.exists():
    for file_path in folder.iterdir():
        if file_path.is_file() and file_path.suffix.lower() == ".pdf":
            report_names.append(file_path.name)
            reports.append(pdf_to_text(file_path))

console.print(
    f"report scan: [bold green]OK[/], loaded reports: [bold yellow]{len(reports)}[/]"
)

if not reports:
    console.print("[yellow]no security reports found, skipping check...[/]")
    sys.exit(0)

diff = get_push_diff()
if not diff or not diff.strip():
    console.print("[bold green]PASSED![/] [dim](empty diff)[/]")
    sys.exit(0)

for i in reports:
    reports_vectors.append(get_embedding(i))

console.print("report to vector conversion: [bold green]OK[/]")

diff_vector = get_embedding(diff)
possible_scores = []

console.print("git diff to vector conversion: [bold green]OK[/]")

for i in reports_vectors:
    possible_scores.append(compare(diff_vector, i))

console.print("finding best possible match: [bold green]OK[/]")

best_score = max(possible_scores)
best_score_id = possible_scores.index(best_score)

answer = json.loads(git_check(diff, reports[best_score_id]))

console.print("AI vulnerability checking: [bold green]OK[/]")

if answer["vulnerable"]:
    snippet = answer.get("snippet", "").strip()
    console.print(f"[bold red]BLOCKED![/] [white]reason:[/] {answer['reason']}")
    if snippet:
        console.print(f"[dim]vulnerable code:[/] [bold yellow]{snippet}[/]")
    sys.exit(1)
else:
    console.print("[bold green]PASSED! pushing...[/]")
