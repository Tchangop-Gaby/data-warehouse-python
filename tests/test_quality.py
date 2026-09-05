import pandas as pd

from dw_project.quality.checks import (
    check_not_null,
    check_unique,
)
from dw_project.quality.result import QualityStatus


def test_not_null_passes():
    df = pd.DataFrame({
        "customer_id": [1, 2, 3]
    })

    result = check_not_null(
        df,
        "customer_id",
        "customer_id_not_null",
    )

    assert result.status == QualityStatus.PASS
    assert result.rows_affected == 0

def test_not_null_fails():
    df = pd.DataFrame({
        "customer_id": [1, None, 3]
    })

    result = check_not_null(
        df,
        "customer_id",
        "customer_id_not_null",
    )

    assert result.status == QualityStatus.FAIL
    assert result.rows_affected == 1

def test_unique_fails():
    df = pd.DataFrame({
        "customer_id": [1, 2, 2, 3]
    })

    result = check_unique(
        df,
        "customer_id",
        "customer_id_unique",
    )

    assert result.status == QualityStatus.FAIL
    assert result.rows_affected == 2