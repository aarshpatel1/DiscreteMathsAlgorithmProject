"""Pytest test suite for complexity analysis and benchmarking engines."""

import pandas as pd
import pytest
from analysis.complexity import (
    ALGORITHM_METADATA,
    ASYMPTOTIC_NOTATIONS,
    COMPLEXITY_CLASSES,
    calculate_growth_data,
)
from analysis.benchmarking import (
    benchmark_sorting_single,
    benchmark_sorting_suite,
    benchmark_searching_suite,
)


def test_complexity_metadata():
    assert len(ALGORITHM_METADATA) >= 10
    for algo, data in ALGORITHM_METADATA.items():
        assert "category" in data
        assert "best_time" in data
        assert "avg_time" in data
        assert "worst_time" in data
        assert "space" in data


def test_asymptotic_notations():
    assert "Big-O (O) - Asymptotic Upper Bound" in ASYMPTOTIC_NOTATIONS
    assert "Big-Omega (Ω) - Asymptotic Lower Bound" in ASYMPTOTIC_NOTATIONS
    assert "Big-Theta (Θ) - Asymptotically Tight Bound" in ASYMPTOTIC_NOTATIONS


def test_growth_data_calculation():
    data = calculate_growth_data(max_n=30, num_points=50)
    assert "n" in data
    assert len(data["n"]) == 50
    assert "Linear: O(n)" in data
    assert "Quadratic: O(n²)" in data


def test_sorting_benchmark():
    df = benchmark_sorting_suite(
        algorithms=["Bubble Sort", "Insertion Sort"],
        sizes=[20, 40],
        distribution="Random",
        trials=1,
    )
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 4
    assert "Execution Time (ms)" in df.columns
    assert "Comparisons" in df.columns


def test_searching_benchmark():
    df = benchmark_searching_suite(sizes=[50, 100], trials=1)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 4
    assert "Algorithm" in df.columns
