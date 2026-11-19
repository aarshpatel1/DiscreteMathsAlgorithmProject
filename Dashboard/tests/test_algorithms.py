"""Pytest test suite for searching, sorting, string matching, greedy, and supplementary algorithms."""

import pytest
from algorithms.searching import (
    linear_search,
    linear_search_steps,
    binary_search,
    binary_search_steps,
)
from algorithms.sorting import (
    bubble_sort,
    bubble_sort_steps,
    insertion_sort,
    insertion_sort_steps,
    selection_sort,
    selection_sort_steps,
    binary_insertion_sort,
    binary_insertion_sort_steps,
)
from algorithms.string_matching import (
    naive_string_match,
    naive_string_match_steps,
)
from algorithms.greedy import (
    cashiers_algorithm,
    cashiers_algorithm_steps,
    activity_selection,
    activity_selection_steps,
)
from algorithms.majority_vote import (
    boyer_moore_majority,
    boyer_moore_majority_steps,
)
from algorithms.stable_matching import (
    gale_shapley,
    gale_shapley_steps,
)
from utils.data_generator import generate_array, parse_custom_array


# ==========================================
# 1. SEARCHING TESTS
# ==========================================

def test_linear_search():
    arr = [10, 50, 30, 70, 80, 20]
    idx, comps = linear_search(arr, 30)
    assert idx == 2
    assert comps == 3

    idx_not_found, comps_nf = linear_search(arr, 999)
    assert idx_not_found == -1
    assert comps_nf == len(arr)

    # Empty array
    assert linear_search([], 5) == (-1, 0)

    # Steps test
    steps = linear_search_steps(arr, 30)
    assert len(steps) > 0
    assert steps[-1]["status"] == "found"
    assert steps[-1]["current_idx"] == 2


def test_binary_search():
    arr = [10, 20, 30, 40, 50, 60, 70, 80]
    idx, comps = binary_search(arr, 60)
    assert idx == 5
    assert comps > 0

    idx_nf, _ = binary_search(arr, 25)
    assert idx_nf == -1

    # Steps test
    steps = binary_search_steps(arr, 60)
    assert len(steps) > 0
    assert steps[-1]["status"] == "found"
    assert steps[-1]["mid"] == 5


# ==========================================
# 2. SORTING TESTS
# ==========================================

@pytest.mark.parametrize("sort_func", [
    bubble_sort,
    insertion_sort,
    selection_sort,
    binary_insertion_sort,
])
def test_sorting_algorithms(sort_func):
    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [],
        [42],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [4, 2, 4, 3, 2, 1, 4],
        [-5, 10, -20, 0, 15],
    ]

    for arr in test_cases:
        expected = sorted(arr)
        result, comps, ops = sort_func(arr)
        assert result == expected
        assert comps >= 0
        assert ops >= 0


def test_sorting_steps():
    arr = [5, 2, 4, 1, 3]
    expected = [1, 2, 3, 4, 5]

    for step_func in [
        bubble_sort_steps,
        insertion_sort_steps,
        selection_sort_steps,
        binary_insertion_sort_steps,
    ]:
        steps = step_func(arr)
        assert len(steps) > 1
        final_arr = steps[-1]["array"]
        assert final_arr == expected


# ==========================================
# 3. STRING MATCHING TESTS
# ==========================================

def test_naive_string_match():
    text = "AABAACAADAABAABA"
    pattern = "AABA"
    matches, comps = naive_string_match(text, pattern)
    assert matches == [0, 9, 12]
    assert comps > 0

    # No match
    matches_none, _ = naive_string_match(text, "XYZ")
    assert matches_none == []

    # Pattern longer than text
    assert naive_string_match("AB", "ABCDE") == ([], 0)

    # Step test
    steps = naive_string_match_steps(text, pattern)
    assert len(steps) > 0
    assert steps[-1]["matches_found"] == [0, 9, 12]


# ==========================================
# 4. GREEDY ALGORITHMS TESTS
# ==========================================

def test_cashiers_algorithm():
    # US standard denominations: 25, 10, 5, 1
    counts, total = cashiers_algorithm(67, [25, 10, 5, 1])
    assert counts[25] == 2  # 50
    assert counts[10] == 1  # 60
    assert counts[5] == 1   # 65
    assert counts[1] == 2   # 67
    assert total == 6

    # 0 amount
    counts_zero, total_zero = cashiers_algorithm(0)
    assert total_zero == 0

    steps = cashiers_algorithm_steps(67, [25, 10, 5, 1])
    assert len(steps) > 0
    assert steps[-1]["total_coins"] == 6

    # Test US currency formatting with $ and cents
    denom_labels = {25: "$0.25 (Quarter)", 10: "$0.10 (Dime)", 5: "$0.05 (Nickel)", 1: "$0.01 (Penny)"}
    us_steps = cashiers_algorithm_steps(
        67,
        denominations=[25, 10, 5, 1],
        currency_symbol="$",
        denom_labels=denom_labels,
        is_cents=True,
    )
    assert len(us_steps) > 0
    assert us_steps[-1]["total_coins"] == 6
    assert "$" in us_steps[0]["description"]
    assert "$0.67" in us_steps[0]["description"]
    assert "$0.25" in us_steps[1]["description"]


def test_activity_selection():
    activities = [
        {"id": "A1", "start": 1, "finish": 4},
        {"id": "A2", "start": 3, "finish": 5},
        {"id": "A3", "start": 0, "finish": 6},
        {"id": "A4", "start": 5, "finish": 7},
        {"id": "A5", "start": 3, "finish": 9},
        {"id": "A6", "start": 5, "finish": 9},
        {"id": "A7", "start": 6, "finish": 10},
        {"id": "A8", "start": 8, "finish": 11},
        {"id": "A9", "start": 8, "finish": 12},
        {"id": "A10", "start": 2, "finish": 14},
        {"id": "A11", "start": 12, "finish": 16},
    ]

    selected, count = activity_selection(activities)
    # Compatible set should be size 4 (e.g. A1, A4, A8, A11)
    assert count == 4
    selected_ids = [a["id"] for a in selected]
    assert "A1" in selected_ids
    assert "A4" in selected_ids
    assert "A8" in selected_ids
    assert "A11" in selected_ids

    steps = activity_selection_steps(activities)
    assert len(steps) > 0
    assert len(steps[-1]["selected_ids"]) == 4


# ==========================================
# 5. MAJORITY VOTE TESTS
# ==========================================

def test_boyer_moore_majority():
    # Clear majority
    arr1 = [2, 2, 1, 1, 1, 2, 2]  # 2 appears 4 times out of 7 (> 3.5)
    cand, is_maj, count = boyer_moore_majority(arr1)
    assert cand == 2
    assert is_maj is True
    assert count == 4

    # No majority
    arr2 = [1, 2, 3, 4, 5]
    cand2, is_maj2, count2 = boyer_moore_majority(arr2)
    assert is_maj2 is False

    # Steps test
    steps = boyer_moore_majority_steps(arr1)
    assert len(steps) > 0
    assert steps[-1]["is_majority"] is True


# ==========================================
# 6. STABLE MATCHING TESTS
# ==========================================

def test_gale_shapley():
    # Men preference lists
    men_prefs = {
        "m1": ["w1", "w2", "w3"],
        "m2": ["w2", "w1", "w3"],
        "m3": ["w1", "w2", "w3"],
    }
    # Women preference lists
    women_prefs = {
        "w1": ["m2", "m1", "m3"],
        "w2": ["m1", "m2", "m3"],
        "w3": ["m1", "m2", "m3"],
    }

    matches, proposals = gale_shapley(men_prefs, women_prefs)
    assert len(matches) == 3
    # Check that every woman has a unique partner
    assert len(set(matches.values())) == 3
    assert proposals > 0

    steps = gale_shapley_steps(men_prefs, women_prefs)
    assert len(steps) > 0
    assert steps[-1]["action"] == "complete"


# ==========================================
# 7. UTILITY & DATA GENERATOR TESTS
# ==========================================

def test_data_generator():
    for dist in ["Random", "Sorted", "Reverse Sorted", "Nearly Sorted", "Duplicates"]:
        arr = generate_array(20, distribution=dist, seed=123)
        assert len(arr) == 20
        if dist == "Sorted":
            assert arr == sorted(arr)
        elif dist == "Reverse Sorted":
            assert arr == sorted(arr, reverse=True)

    parsed = parse_custom_array("10, 25, 4, 88, 1")
    assert parsed == [10, 25, 4, 88, 1]
