"""Searching algorithms implementation with execution metrics and step tracing.

Includes:
- Linear Search
- Binary Search
"""

from typing import Any, Dict, List, Tuple


def linear_search(arr: List[Any], target: Any) -> Tuple[int, int]:
    """Pure linear search for benchmarking.

    Args:
        arr: List of elements.
        target: Element to find.

    Returns:
        Tuple of (found_index, comparisons_count). Returns (-1, comparisons) if not found.
    """
    comparisons = 0
    for i, val in enumerate(arr):
        comparisons += 1
        if val == target:
            return i, comparisons
    return -1, comparisons


def linear_search_steps(arr: List[Any], target: Any) -> List[Dict[str, Any]]:
    """Linear search yielding step-by-step state for visualization.

    Returns list of state snapshots.
    """
    steps: List[Dict[str, Any]] = []
    comparisons = 0

    steps.append({
        "step": 0,
        "array": list(arr),
        "current_idx": None,
        "target": target,
        "comparisons": 0,
        "status": "start",
        "description": f"Starting Linear Search for target {target}. Array length: {len(arr)}.",
    })

    found = False
    found_idx = -1

    for i, val in enumerate(arr):
        comparisons += 1
        if val == target:
            found = True
            found_idx = i
            steps.append({
                "step": len(steps),
                "array": list(arr),
                "current_idx": i,
                "target": target,
                "comparisons": comparisons,
                "status": "found",
                "description": f"Target {target} FOUND at index {i} after {comparisons} comparison(s)!",
            })
            break
        else:
            steps.append({
                "step": len(steps),
                "array": list(arr),
                "current_idx": i,
                "target": target,
                "comparisons": comparisons,
                "status": "comparing",
                "description": f"Checking index {i}: arr[{i}] = {val} != {target}. Moving to next element.",
            })

    if not found:
        steps.append({
            "step": len(steps),
            "array": list(arr),
            "current_idx": None,
            "target": target,
            "comparisons": comparisons,
            "status": "not_found",
            "description": f"Target {target} NOT FOUND in array after scanning all {len(arr)} elements.",
        })

    return steps


def binary_search(arr: List[Any], target: Any) -> Tuple[int, int]:
    """Pure binary search for benchmarking (assumes arr is sorted).

    Args:
        arr: Sorted list of elements.
        target: Element to find.

    Returns:
        Tuple of (found_index, comparisons_count).
    """
    comparisons = 0
    low = 0
    high = len(arr) - 1

    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        if arr[mid] == target:
            return mid, comparisons
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1, comparisons


def binary_search_steps(arr: List[Any], target: Any) -> List[Dict[str, Any]]:
    """Binary search yielding step-by-step state for visualization.

    Assumes array is sorted (or caller sorts it).
    """
    steps: List[Dict[str, Any]] = []
    comparisons = 0
    low = 0
    high = len(arr) - 1

    steps.append({
        "step": 0,
        "array": list(arr),
        "low": low,
        "high": high,
        "mid": None,
        "target": target,
        "comparisons": 0,
        "status": "start",
        "description": f"Starting Binary Search for target {target} in sorted array of size {len(arr)}.",
    })

    found = False

    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        mid_val = arr[mid]

        if mid_val == target:
            found = True
            steps.append({
                "step": len(steps),
                "array": list(arr),
                "low": low,
                "high": high,
                "mid": mid,
                "target": target,
                "comparisons": comparisons,
                "status": "found",
                "description": f"arr[mid={mid}] = {mid_val} matches target {target}! Search completed in {comparisons} comparison(s).",
            })
            break
        elif mid_val < target:
            steps.append({
                "step": len(steps),
                "array": list(arr),
                "low": low,
                "high": high,
                "mid": mid,
                "target": target,
                "comparisons": comparisons,
                "status": "adjust_right",
                "description": f"arr[mid={mid}] = {mid_val} < {target}. Target lies to the right. Adjusting low from {low} to {mid + 1}.",
            })
            low = mid + 1
        else:
            steps.append({
                "step": len(steps),
                "array": list(arr),
                "low": low,
                "high": high,
                "mid": mid,
                "target": target,
                "comparisons": comparisons,
                "status": "adjust_left",
                "description": f"arr[mid={mid}] = {mid_val} > {target}. Target lies to the left. Adjusting high from {high} to {mid - 1}.",
            })
            high = mid - 1

    if not found:
        steps.append({
            "step": len(steps),
            "array": list(arr),
            "low": low,
            "high": high,
            "mid": None,
            "target": target,
            "comparisons": comparisons,
            "status": "not_found",
            "description": f"Search interval exhausted (low={low} > high={high}). Target {target} is NOT present in the array.",
        })

    return steps
