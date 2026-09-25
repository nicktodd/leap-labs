"""Extension 2: idempotency. Run:  python -m pytest -v ext2_test_idempotency.py

A pipeline is idempotent when running it again on the same input produces the same output.
Scheduled pipelines are re-run after failures, and a re-run must not change the result, add
rows or reorder them: downstream jobs, audits and "has anything changed?" checks compare files.
"""
import hashlib

import pytest

from payments_etl import run_pipeline

OUTPUT_FILES = ["clean_transactions.csv", "rejected_transactions.csv"]


def sha256_of(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.fixture(scope="module")
def two_runs(tmp_path_factory):
    # tmp_path is function-scoped, so a module-scoped fixture uses tmp_path_factory instead.
    first = tmp_path_factory.mktemp("run1")
    second = tmp_path_factory.mktemp("run2")
    run_pipeline(out_dir=first)
    run_pipeline(out_dir=second)
    return first, second


@pytest.mark.parametrize("name", OUTPUT_FILES)
def test_two_runs_are_byte_identical(two_runs, name):
    first, second = two_runs
    # Comparing hashes compares every byte: values, column order, row order, float formatting
    # and line endings. A DataFrame comparison would miss formatting differences.
    assert sha256_of(first / name) == sha256_of(second / name)


def test_rerun_into_same_folder_overwrites(tmp_path):
    # Running twice into the same folder must replace the files, not append to them.
    run_pipeline(out_dir=tmp_path)
    before = {name: sha256_of(tmp_path / name) for name in OUTPUT_FILES}
    run_pipeline(out_dir=tmp_path)
    after = {name: sha256_of(tmp_path / name) for name in OUTPUT_FILES}
    assert before == after
    assert sorted(p.name for p in tmp_path.iterdir()) == sorted(OUTPUT_FILES)
