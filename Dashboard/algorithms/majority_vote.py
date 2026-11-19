"""Boyer-Moore Majority Vote Algorithm implementation with execution metrics and step tracing.

Finds the element that occurs more than n/2 times in O(n) time and O(1) space.
"""

from typing import Any, Dict, List, Tuple


def boyer_moore_majority(arr: List[Any]) -> Tuple[Any, bool, int]:
    """Pure Boyer-Moore Majority Vote algorithm for benchmarking.

    Returns:
        Tuple of (candidate, is_majority, count).
    """
    if not arr:
        return None, False, 0

    # Phase 1: Candidate Selection
    candidate = None
    count = 0
    for val in arr:
        if count == 0:
            candidate = val
            count = 1
        elif val == candidate:
            count += 1
        else:
            count -= 1

    # Phase 2: Verification
    actual_count = sum(1 for val in arr if val == candidate)
    is_majority = actual_count > (len(arr) // 2)

    return candidate, is_majority, actual_count


def boyer_moore_majority_steps(arr: List[Any]) -> List[Dict[str, Any]]:
    """Boyer-Moore Majority Vote yielding step-by-step state for visualization."""
    steps: List[Dict[str, Any]] = []
    n = len(arr)

    steps.append({
        "step": 0,
        "phase": 1,
        "array": list(arr),
        "current_idx": None,
        "candidate": None,
        "count": 0,
        "status": "start",
        "description": f"Starting Boyer-Moore Majority Vote algorithm on array of size {n}. Majority threshold is > {n // 2}.",
    })

    if not arr:
        return steps

    # Phase 1: Candidate Selection
    candidate = None
    count = 0

    for i, val in enumerate(arr):
        if count == 0:
            candidate = val
            count = 1
            steps.append({
                "step": len(steps),
                "phase": 1,
                "array": list(arr),
                "current_idx": i,
                "candidate": candidate,
                "count": count,
                "status": "new_candidate",
                "description": f"Step {i+1} (Phase 1): Counter was 0. New candidate selected: '{val}'. Counter set to 1.",
            })
        elif val == candidate:
            count += 1
            steps.append({
                "step": len(steps),
                "phase": 1,
                "array": list(arr),
                "current_idx": i,
                "candidate": candidate,
                "count": count,
                "status": "increment",
                "description": f"Step {i+1} (Phase 1): arr[{i}]='{val}' matches candidate '{candidate}'. Counter incremented to {count}.",
            })
        else:
            count -= 1
            steps.append({
                "step": len(steps),
                "phase": 1,
                "array": list(arr),
                "current_idx": i,
                "candidate": candidate,
                "count": count,
                "status": "decrement",
                "description": f"Step {i+1} (Phase 1): arr[{i}]='{val}' != candidate '{candidate}'. Counter decremented to {count}.",
            })

    # End of Phase 1
    steps.append({
        "step": len(steps),
        "phase": 1,
        "array": list(arr),
        "current_idx": None,
        "candidate": candidate,
        "count": count,
        "status": "phase1_complete",
        "description": f"Phase 1 complete! Identified candidate is '{candidate}'. Moving to Phase 2 (Verification).",
    })

    # Phase 2: Verification
    actual_count = 0
    for i, val in enumerate(arr):
        matches = (val == candidate)
        if matches:
            actual_count += 1
        steps.append({
            "step": len(steps),
            "phase": 2,
            "array": list(arr),
            "current_idx": i,
            "candidate": candidate,
            "count": count,
            "actual_count": actual_count,
            "status": "verifying",
            "description": f"Phase 2 Verification at index {i}: arr[{i}] = '{val}' {'==' if matches else '!='} candidate '{candidate}'. Total occurrences so far: {actual_count}.",
        })

    is_majority = actual_count > (n // 2)
    steps.append({
        "step": len(steps),
        "phase": 2,
        "array": list(arr),
        "current_idx": None,
        "candidate": candidate,
        "count": count,
        "actual_count": actual_count,
        "is_majority": is_majority,
        "status": "finished",
        "description": (
            f"Result: Candidate '{candidate}' appears {actual_count} times out of {n} (> {n // 2}). "
            f"{'VALID MAJORITY ELEMENT!' if is_majority else 'NO MAJORITY ELEMENT EXISTS.'}"
        ),
    })

    return steps
