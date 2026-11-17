import json
import sys
from pathlib import Path

from base_logic import *
from git_logic import *

report_names = []
reports = []
reports_vectors = []

folder = Path(__file__).resolve().parent.parent / "security_reports"
for file_path in folder.iterdir():
    if file_path.is_file() and file_path.suffix.lower() == ".pdf":
        report_names.append(file_path.name)
        reports.append(pdf_to_text(file_path))

for i in reports:
    reports_vectors.append(get_embedding(i))

diff = get_push_diff()
diff_vector = get_embedding(diff)
possible_scores = []

for i in reports_vectors:
    possible_scores.append(compare(diff_vector, i))

best_score = max(possible_scores)
best_score_id = possible_scores.index(best_score)

answer = json.loads(git_check(diff, reports[best_score_id]))

if answer["vulnerable"] == False:
    pass
else:
    print(answer["reason"])
    sys.exit(1)
