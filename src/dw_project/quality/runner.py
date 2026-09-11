"""
Data Quality Pipeline
=====================

Purpose:
    Execute data quality checks and summarize their results

Description:
    Provides utilities for running a collection of quality
    checks, evaluating whether the quality gate passed,
    printing a human-readable quality report, and generating
    a summary of passed and failed checks.

Components:
    run_pipeline_checks():
        Executes all configured quality checks.
    quality_gate_passed():
        Determines whether all checks passed.
    print_quality_report():
        Print a formatted quality report.
    summary_quality():
        Summarizes the quality check results.
"""
from collections.abc import Callable
from .result import QualityResult
from dw_project.logger_config import quality_logger

def run_pipeline_checks(
        checks: list[Callable[[], QualityResult]],
) -> list[QualityResult]:
    """
    Execute all configured quality checks and return
    their results.
    """
    results = []

    for check in checks:
        result = check()
        results.append(result)

    return results

def quality_gate_passed(
        results: list[QualityResult],
) -> bool:
    """
    Return True when all quality checks have passed.
    """
    return all(
        result.passed
        for result in results
    )

def print_quality_report(
        results: list[QualityResult],
) -> None:
    """
    Print a formatted report containing the quality
    check results.
    """
    quality_logger.info("=" * 70)
    quality_logger.info("DATA QUALITY REPORT")
    quality_logger.info("=" * 70)

    for result in results:
        quality_logger.info(
            f"{result.status.value:<6} | "
            f"{result.rule_name:<35} | "
            f"affected={result.rows_affected}"
        )

        quality_logger.info(f"{result.message}")

    quality_logger.info("=" * 70)

def summary_quality(
        results: list[QualityResult],
) -> dict:
    """
    Return counts of total, passed, and failed quality
    checks.
    """
    return {
        "total_checks": len(results),
        "passed": sum(
            result.passed
            for result in results
        ),
        "failed": sum(
            not result.passed
            for result in results
        ),
    }