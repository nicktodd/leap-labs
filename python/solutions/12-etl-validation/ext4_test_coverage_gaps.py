"""Extension 4: coverage. Run from this folder:

    python -m pytest --cov=payments_etl --cov-branch --cov-report=term-missing test_payments_etl.py
    python -m pytest --cov=payments_etl --cov-branch --cov-report=term-missing test_payments_etl.py ext4_test_coverage_gaps.py

The first run reports payments_etl.py at 84%, with lines 149-152 (run_pipeline) and 156-165
(the __main__ block) missing. The unit and output tests call extract, transform and load one
at a time, so nothing checks that run_pipeline wires them together (for example, that it
passes out_dir to load). The tests below close that gap.
"""
import pandas as pd
import pytest

from payments_etl import extract, read_fx, run_pipeline, transform


def test_run_pipeline_end_to_end(tmp_path):
    raw, clean, rejects, (clean_path, rejects_path) = run_pipeline(out_dir=tmp_path)
    # The files land in the folder that was passed in, not the default output/ folder.
    assert clean_path.parent == tmp_path
    assert rejects_path.parent == tmp_path
    assert len(pd.read_csv(clean_path)) == len(clean) == 138
    assert len(pd.read_csv(rejects_path)) == len(rejects) == 5
    assert len(raw) == 143


# Coverage measures which LINES ran, not which DATA cases were tried. transform() is
# vectorised pandas code with no if statements, so it shows as fully covered, yet no test
# feeds it a channel that normalise_channel cannot map. That row keeps channel = NaN and is
# neither cleaned nor rejected. The test below documents the gap: it is marked xfail
# (expected to fail) until transform() gains an "unknown channel" reject rule, and strict=True
# makes the suite fail if the rule is added without removing the marker.
@pytest.mark.xfail(strict=True, reason="transform() has no reject rule for an unknown channel")
def test_unknown_channel_is_rejected():
    raw = extract()
    raw.loc[raw["txn_id"] == "P0001", "channel"] = "Telephone"
    clean, rejects = transform(raw, read_fx())
    assert "P0001" in set(rejects["txn_id"])
    assert clean["channel"].notna().all()
