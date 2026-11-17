import subprocess

import ollama


def git_check(diff: str, report: str) -> str:
    response = ollama.generate(
        model="qwen3.5:4b",
        prompt=f"""
You are a security code reviewer. Check if the provided git diff introduces or repeats the vulnerability described in the security report.

Respond ONLY with valid JSON matching this schema:
{{"vulnerable": boolean, "reason": "one short sentence in English explaining why, or PASS if safe"}}

Security Report:
{report}

Git Diff:
{diff}

""",
        format="json",
        options={"temperature": 0.1},
        think=False,
    )
    return response["response"]


def get_push_diff() -> str:
    result = subprocess.run(
        ["git", "diff", "@{u}..HEAD"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
    )

    if result.returncode != 0:
        result = subprocess.run(
            ["git", "diff", "origin/main..HEAD"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=False,
        )

    return result.stdout
