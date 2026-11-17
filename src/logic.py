import subprocess
from pathlib import Path

import pymupdf as fitz
from fastembed import TextEmbedding

model = TextEmbedding(model_name="jinaai/jina-embeddings-v2-base-code")


def get_embedding(text: str) -> list[float]:
    return list(model.embed([text]))[0].tolist()  # noqa


def compare(vec1: list[float], vec2: list[float]) -> float:
    return sum(a * b for a, b in zip(vec1, vec2))


def pdf_to_text(path: Path | str) -> str:
    path = Path(path)
    with fitz.open(path) as pdf:
        return "\n".join(x.get_text() for x in pdf)


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
