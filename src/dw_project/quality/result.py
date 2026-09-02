"""
Data Quality Result Models
==========================

Purpose:
    Define reusable models for representing data
    quality rule results.
    
Description:
    Provides a status enumeration and a dataclass for 
    capturing the outcome of a data quality check 
    including the rule name, rows evaluated, affected 
    rows, and a descriptive message.

Component:
    QualityStatus:
        Defines PASS and FAIL quality statues.
    QualityResult: 
        Stores the result of a data quality rule evaluation.
"""
from dataclasses import dataclass
from enum import Enum

class QualityStatus(str, Enum):
    """
    Represent the possible outcomes of a
    data qualty rule.
    """
    PASS = "PASS"
    FAIL = "FAIL"

@dataclass
class QualityResult:
    """
    Store the result and summary of a data
    quality rule evaluation.
    """
    rule_name: str
    status: str
    row_checked: int
    rows_affected: int
    message: str

    @property
    def passed(self) -> bool:
        """
        Return True when the quality rule passed.
        """
        return self.status == QualityStatus.PASS