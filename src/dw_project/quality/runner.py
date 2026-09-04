from collections.abc import Callable
from .result import QualityResult

def run_pipeline_checks(
        checks: list[Callable[[], QualityResult]],
) -> list[QualityResult]:

    results = []

    for check in checks:
        result = check()
        results.append(result)

    return results

def quality_gate_passed(
        results: list[QualityResult],
) -> bool:

    return all(
        result.passed
        for result in results
    )

def print_quality_report(
        results: list[QualityResult],
) -> None:

    print("\nDATA QUALITY REPORT")
    print("=" * 70)

    for result in results:
        print(
            f"{result.status.value:<6} | "
            f"{result.rule_name:<35} | "
            f"affected={result.rows_affected}"
        )

        print(f"{result.message}")

    print("=" * 70)

def summary_quality(
        results: list[QualityResult],
) -> dict:

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