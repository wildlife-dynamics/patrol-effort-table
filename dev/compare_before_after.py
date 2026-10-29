"""Compare the existing summary-table metrics between two sets of harness runs.

Usage (from the inner workflow env):
    pixi run --frozen python ../dev/compare_before_after.py <before_results_root> <after_results_root> <case> [<case> ...]

Each root holds one directory per case as `dev/run-test-cases.sh` leaves them
(`<root>/<case>/<hash>_summary_table.html` + `result.json`). For every case, every
dashboard view's table is parsed, rows are matched on the group-key columns, and
every column present on BOTH sides is compared (so leg-metric columns that only the
new workflow emits are ignored). Exit code 1 on any difference.
"""

import json
import re
import sys
from pathlib import Path

TOL = 1e-9


def table_rows(html: str) -> list[dict]:
    """The ag-grid rowData array: the JSON array whose objects carry the grid's column fields."""
    arrays = []
    for m in re.findall(r'(\[\{"[^"]+":.*?\}\])', html, re.S):
        try:
            arrays.append(json.loads(m))
        except json.JSONDecodeError:
            continue
    fields = {d["field"] for a in arrays for d in a if isinstance(d, dict) and "field" in d}
    for a in arrays:
        if a and isinstance(a[0], dict) and fields and fields <= set(a[0]):
            return a
    return []


def views(root: Path, case: str) -> dict[str, list[dict]]:
    result = json.loads((root / case / "result.json").read_text())
    out = {}
    for key, widgets in result["result"]["views"].items():
        for w in widgets:
            if w["widget_type"] != "table":
                continue
            html = (root / case / Path(w["data"]).name).read_text()
            out[key] = table_rows(html)
    return out


def row_key(row: dict, numeric_cols: set[str]) -> tuple:
    return tuple((k, v) for k, v in row.items() if k not in numeric_cols)


def compare(before: dict[str, list[dict]], after: dict[str, list[dict]]) -> list[str]:
    diffs = []
    # A view only the new workflow produces (e.g. a "None" spatial group holding legs
    # that have no track) is reported, not failed: it cannot change an existing row.
    if set(before) - set(after):
        diffs.append(f"views lost: {sorted(set(before) - set(after))}")
    extra = sorted(set(after) - set(before))
    if extra:
        print(f"      info: view(s) only in after: {extra}")
    for key in sorted(set(before) & set(after)):
        b_rows, a_rows = before[key], after[key]
        shared = set(b_rows[0]) & set(a_rows[0]) if b_rows and a_rows else set()
        numeric = {c for c in shared if any(isinstance(r.get(c), (int, float)) for r in b_rows + a_rows)}
        b_idx = {row_key({c: r[c] for c in shared}, numeric): r for r in b_rows}
        a_idx = {row_key({c: r[c] for c in shared}, numeric): r for r in a_rows}
        if set(b_idx) != set(a_idx):
            diffs.append(f"{key}: row keys differ: only-before={sorted(set(b_idx) - set(a_idx))} only-after={sorted(set(a_idx) - set(b_idx))}")
        for k in sorted(set(b_idx) & set(a_idx)):
            for c in sorted(numeric):
                b, a = b_idx[k].get(c), a_idx[k].get(c)
                if (b is None) != (a is None) or (b is not None and abs(float(b) - float(a)) > TOL):
                    diffs.append(f"{key} {dict(k)} {c}: before={b} after={a}")
    return diffs


def main() -> None:
    before_root, after_root, *cases = sys.argv[1:]
    failed = False
    for case in cases:
        b, a = views(Path(before_root), case), views(Path(after_root), case)
        n_rows = sum(len(r) for r in a.values())
        shared_views = sorted(set(b) & set(a))
        n_cols = len(set(b[shared_views[0]][0]) & set(a[shared_views[0]][0])) if shared_views else 0
        diffs = compare(b, a)
        status = "DIFF" if diffs else "same"
        print(f"{status:4} {case}: {len(a)} view(s), {n_rows} row(s), {n_cols} shared column(s)")
        for d in diffs:
            print("     ", d)
        failed |= bool(diffs)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
