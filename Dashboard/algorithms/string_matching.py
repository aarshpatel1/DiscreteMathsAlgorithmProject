"""Naive String Matching algorithm implementation with execution metrics and step tracing."""

from typing import Any, Dict, List, Tuple


def naive_string_match(text: str, pattern: str) -> Tuple[List[int], int]:
    """Pure Naive String Matching algorithm for benchmarking.

    Args:
        text: Main text string of length n.
        pattern: Pattern string of length m to find.

    Returns:
        Tuple of (list_of_match_indices, comparisons_count).
    """
    n = len(text)
    m = len(pattern)
    matches = []
    comparisons = 0

    if m == 0 or n == 0 or m > n:
        return matches, comparisons

    for s in range(n - m + 1):
        match = True
        for j in range(m):
            comparisons += 1
            if text[s + j] != pattern[j]:
                match = False
                break
        if match:
            matches.append(s)

    return matches, comparisons


def naive_string_match_steps(text: str, pattern: str) -> List[Dict[str, Any]]:
    """Naive string matching yielding step-by-step state for visualization."""
    steps: List[Dict[str, Any]] = []
    n = len(text)
    m = len(pattern)
    comparisons = 0
    matches_found: List[int] = []

    steps.append({
        "step": 0,
        "text": text,
        "pattern": pattern,
        "shift": 0,
        "pattern_idx": 0,
        "text_idx": 0,
        "status": "start",
        "matches_found": [],
        "comparisons": 0,
        "description": f"Searching for pattern '{pattern}' (len={m}) in text '{text}' (len={n}). Possible shifts: 0 to {max(0, n - m)}.",
    })

    if m == 0 or n == 0 or m > n:
        steps.append({
            "step": 1,
            "text": text,
            "pattern": pattern,
            "shift": 0,
            "pattern_idx": 0,
            "text_idx": 0,
            "status": "end",
            "matches_found": [],
            "comparisons": 0,
            "description": "Pattern is empty or longer than text. No search necessary.",
        })
        return steps

    for s in range(n - m + 1):
        steps.append({
            "step": len(steps),
            "text": text,
            "pattern": pattern,
            "shift": s,
            "pattern_idx": 0,
            "text_idx": s,
            "status": "shift_start",
            "matches_found": list(matches_found),
            "comparisons": comparisons,
            "description": f"Shift s = {s}: Aligning pattern '{pattern}' starting at text[{s}] ('{text[s:s+m]}').",
        })

        is_match = True
        for j in range(m):
            comparisons += 1
            t_char = text[s + j]
            p_char = pattern[j]
            char_equal = (t_char == p_char)

            if char_equal:
                steps.append({
                    "step": len(steps),
                    "text": text,
                    "pattern": pattern,
                    "shift": s,
                    "pattern_idx": j,
                    "text_idx": s + j,
                    "status": "match_char",
                    "matches_found": list(matches_found),
                    "comparisons": comparisons,
                    "description": f"Match at shift {s}, char {j}: pattern[{j}]='{p_char}' == text[{s+j}]='{t_char}'.",
                })
            else:
                is_match = False
                steps.append({
                    "step": len(steps),
                    "text": text,
                    "pattern": pattern,
                    "shift": s,
                    "pattern_idx": j,
                    "text_idx": s + j,
                    "status": "mismatch",
                    "matches_found": list(matches_found),
                    "comparisons": comparisons,
                    "description": f"Mismatch at shift {s}, char {j}: pattern[{j}]='{p_char}' != text[{s+j}]='{t_char}'. Advancing shift.",
                })
                break

        if is_match:
            matches_found.append(s)
            steps.append({
                "step": len(steps),
                "text": text,
                "pattern": pattern,
                "shift": s,
                "pattern_idx": m - 1,
                "text_idx": s + m - 1,
                "status": "full_match",
                "matches_found": list(matches_found),
                "comparisons": comparisons,
                "description": f"🎉 Full pattern match found at shift s = {s} (indices {s} to {s + m - 1})!",
            })

    steps.append({
        "step": len(steps),
        "text": text,
        "pattern": pattern,
        "shift": n - m,
        "pattern_idx": 0,
        "text_idx": 0,
        "status": "completed",
        "matches_found": list(matches_found),
        "comparisons": comparisons,
        "description": f"Search complete! Total matches: {len(matches_found)} at positions {matches_found}. Total comparisons: {comparisons}.",
    })

    return steps
