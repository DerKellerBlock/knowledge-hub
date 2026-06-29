"""Knowledge Hub Quality Evaluation Platform — CLI scripts.

Submodules
----------
scorer : pure functions (load_golden_dataset, validate_question, score_*,
        evaluate_question, aggregate_domain_scores, generate_*_report).
run_evaluation : CLI wrapper around hybrid_search.search + scorer.

These scripts are not part of the runtime Knowledge Hub; they are part
of the dev-time Quality Evaluation Platform (see spec
``docs/superpowers/specs/2026-06-29-knowledge-hub-quality-evaluation-platform-design.md``).
"""
