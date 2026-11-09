# Measurement code (Section 5)

How to set up and run the measurements is described in the top-level `README.md` (section "Reproducing": Tables 8–11, Table 9 Host column and Table S6, CDPruner diagnosis). This folder holds the scripts as used:

- `harness.py` — TTFT, end-to-end latency, peak memory and NVML energy; `methods/*.py` — one plug-in per method (including the changes of Section 5.1); `eval_acc.py`, `score.py`, `fill_pope.py` — accuracy (GQA, POPE, TextVQA, MME).
- Setup: `setup_env.sh`, `download.sh`, `check_env.py`, `pin_transformers.sh`, `clone_baselines.sh` (then check out the commits in `commits.csv`), `build_fastv_kv.sh`, `fastv_env.sh`.
- Runners: `run_harness.sh`, `run_acc.sh`, `run_py.sh`, `run_check.sh`, `run_acc_queue.sh`, `run_queue2.sh`; the replication machine used `pc2_run_all.sh` and `pc2_fastv.sh`.
- Tables: `make_table8.py`, `make_table_cross.py`; `accuracy_reported.csv` (Table 10); `BASELINES.md` (method notes, Korean).
- `jetson/` — Jetson Orin Nano harness, NF4 micro-benchmark, accuracy (Table 11); `profiling/` — TTFT GPU/host split and CDPruner memory diagnosis; `check_answer_length.py` — generation-cap check for Table 9.

The scripts expect to sit together in one directory (the project's `bench/`): copy the files of `profiling/` next to `harness.py` and `methods/`. Work files default to `~/vlmbench` (`WORK`); the conda installation is located with `CONDA_ROOT` (defaults to `~/colin` if present, otherwise `~/miniconda3`). Code comments are partly in Korean.
