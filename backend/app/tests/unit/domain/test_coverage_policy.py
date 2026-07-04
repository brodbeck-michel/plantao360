import pytest
from app.domain.policies.coverage_policy import CoveragePolicy, CoverageCheckResult


def test_coverage_policy_covered():
    policy = CoveragePolicy(min_doctors=2)
    result = policy.has_minimum_coverage(3)
    assert result.is_covered is True
    assert result.current_doctors == 3
    assert result.min_required == 2


def test_coverage_policy_not_covered():
    policy = CoveragePolicy(min_doctors=2)
    result = policy.has_minimum_coverage(1)
    assert result.is_covered is False
    assert result.current_doctors == 1


def test_coverage_policy_exact():
    policy = CoveragePolicy(min_doctors=2)
    result = policy.has_minimum_coverage(2)
    assert result.is_covered is True


def test_coverage_policy_has_sufficient_adding():
    policy = CoveragePolicy(min_doctors=2)
    result = policy.has_sufficient_doctors(current_count=1, adding=1)
    assert result.is_covered is True


def test_coverage_policy_has_sufficient_removing():
    policy = CoveragePolicy(min_doctors=2)
    result = policy.has_sufficient_doctors(current_count=2, removing=1)
    assert result.is_covered is False


def test_coverage_policy_would_removal_leave_uncovered():
    policy = CoveragePolicy(min_doctors=2)
    result = policy.would_removal_leave_uncovered(current_count=2)
    assert result.is_covered is False


def test_coverage_policy_would_removal_still_covered():
    policy = CoveragePolicy(min_doctors=2)
    result = policy.would_removal_leave_uncovered(current_count=3)
    assert result.is_covered is True
