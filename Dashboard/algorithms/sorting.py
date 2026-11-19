"""Sorting algorithms implementation with execution metrics and step tracing.

Includes:
- Bubble Sort
- Insertion Sort
- Selection Sort
- Binary Insertion Sort
"""

from typing import Any, Dict, List, Tuple


# ==========================================
# 1. BUBBLE SORT
# ==========================================

def bubble_sort(arr: List[Any]) -> Tuple[List[Any], int, int]:
    """Pure Bubble Sort for benchmarking.

    Returns:
        (sorted_array, comparisons, swaps)
    """
    a = list(arr)
    n = len(a)
    comparisons = 0
    swaps = 0

    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            comparisons += 1
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                swapped = True
        if not swapped:
            break

    return a, comparisons, swaps


def bubble_sort_steps(arr: List[Any]) -> List[Dict[str, Any]]:
    """Bubble sort yielding step-by-step state for visualization."""
    steps: List[Dict[str, Any]] = []
    a = list(arr)
    n = len(a)
    comparisons = 0
    swaps = 0
    sorted_indices = set()

    steps.append({
        "step": 0,
        "array": list(a),
        "comparing": [],
        "swapped_pair": [],
        "sorted_indices": list(sorted_indices),
        "comparisons": 0,
        "swaps": 0,
        "description": f"Initial array of size {n}. Beginning Bubble Sort passes.",
    })

    if n <= 1:
        steps.append({
            "step": 1,
            "array": list(a),
            "comparing": [],
            "swapped_pair": [],
            "sorted_indices": list(range(n)),
            "comparisons": 0,
            "swaps": 0,
            "description": "Array is already sorted (0 or 1 element).",
        })
        return steps

    for i in range(n - 1):
        any_swapped = False
        for j in range(n - 1 - i):
            comparisons += 1
            is_greater = a[j] > a[j + 1]

            steps.append({
                "step": len(steps),
                "array": list(a),
                "comparing": [j, j + 1],
                "swapped_pair": [],
                "sorted_indices": list(sorted_indices),
                "comparisons": comparisons,
                "swaps": swaps,
                "description": f"Pass {i+1}: Comparing arr[{j}]={a[j]} and arr[{j+1}]={a[j+1]}.",
            })

            if is_greater:
                a[j], a[j + 1] = a[j + 1], a[j]
                swaps += 1
                any_swapped = True
                steps.append({
                    "step": len(steps),
                    "array": list(a),
                    "comparing": [],
                    "swapped_pair": [j, j + 1],
                    "sorted_indices": list(sorted_indices),
                    "comparisons": comparisons,
                    "swaps": swaps,
                    "description": f"arr[{j}] > arr[{j+1}]: Swapped {a[j+1]} and {a[j]}.",
                })

        sorted_indices.add(n - 1 - i)
        steps.append({
            "step": len(steps),
            "array": list(a),
            "comparing": [],
            "swapped_pair": [],
            "sorted_indices": list(sorted_indices),
            "comparisons": comparisons,
            "swaps": swaps,
            "description": f"Pass {i+1} complete. Element at index {n - 1 - i} ({a[n - 1 - i]}) is now locked in its sorted position.",
        })

        if not any_swapped:
            # All remaining elements are sorted
            for k in range(n):
                sorted_indices.add(k)
            steps.append({
                "step": len(steps),
                "array": list(a),
                "comparing": [],
                "swapped_pair": [],
                "sorted_indices": list(sorted_indices),
                "comparisons": comparisons,
                "swaps": swaps,
                "description": "Early termination: No swaps occurred in this pass, meaning the array is completely sorted!",
            })
            break

    # Ensure all indices marked sorted at end
    sorted_indices = set(range(n))
    steps.append({
        "step": len(steps),
        "array": list(a),
        "comparing": [],
        "swapped_pair": [],
        "sorted_indices": list(sorted_indices),
        "comparisons": comparisons,
        "swaps": swaps,
        "description": f"Sorting complete! Total comparisons: {comparisons}, Total swaps: {swaps}.",
    })

    return steps


# ==========================================
# 2. INSERTION SORT
# ==========================================

def insertion_sort(arr: List[Any]) -> Tuple[List[Any], int, int]:
    """Pure Insertion Sort for benchmarking.

    Returns:
        (sorted_array, comparisons, shifts)
    """
    a = list(arr)
    n = len(a)
    comparisons = 0
    shifts = 0

    for i in range(1, n):
        key = a[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if a[j] > key:
                a[j + 1] = a[j]
                shifts += 1
                j -= 1
            else:
                break
        a[j + 1] = key

    return a, comparisons, shifts


def insertion_sort_steps(arr: List[Any]) -> List[Dict[str, Any]]:
    """Insertion sort yielding step-by-step state for visualization."""
    steps: List[Dict[str, Any]] = []
    a = list(arr)
    n = len(a)
    comparisons = 0
    shifts = 0

    steps.append({
        "step": 0,
        "array": list(a),
        "key_idx": None,
        "comparing_idx": None,
        "sorted_indices": [0] if n > 0 else [],
        "comparisons": 0,
        "shifts": 0,
        "description": f"Initial array. The single element arr[0]={a[0] if n > 0 else None} is trivially sorted.",
    })

    if n <= 1:
        return steps

    for i in range(1, n):
        key = a[i]
        j = i - 1

        steps.append({
            "step": len(steps),
            "array": list(a),
            "key_idx": i,
            "comparing_idx": None,
            "sorted_indices": list(range(i)),
            "comparisons": comparisons,
            "shifts": shifts,
            "description": f"Selected key arr[{i}] = {key} to insert into the sorted subarray [0..{i-1}].",
        })

        while j >= 0:
            comparisons += 1
            steps.append({
                "step": len(steps),
                "array": list(a),
                "key_idx": i,
                "comparing_idx": j,
                "sorted_indices": list(range(i)),
                "comparisons": comparisons,
                "shifts": shifts,
                "description": f"Comparing key {key} with arr[{j}] = {a[j]}.",
            })

            if a[j] > key:
                a[j + 1] = a[j]
                shifts += 1
                steps.append({
                    "step": len(steps),
                    "array": list(a),
                    "key_idx": j,  # slot where key will move
                    "comparing_idx": j + 1,
                    "sorted_indices": list(range(i)),
                    "comparisons": comparisons,
                    "shifts": shifts,
                    "description": f"arr[{j}]={a[j]} > {key}: Shifted element {a[j]} right to index {j+1}.",
                })
                j -= 1
            else:
                steps.append({
                    "step": len(steps),
                    "array": list(a),
                    "key_idx": i,
                    "comparing_idx": j,
                    "sorted_indices": list(range(i)),
                    "comparisons": comparisons,
                    "shifts": shifts,
                    "description": f"arr[{j}]={a[j]} <= {key}: Found correct insertion point at index {j+1}.",
                })
                break

        a[j + 1] = key
        steps.append({
            "step": len(steps),
            "array": list(a),
            "key_idx": j + 1,
            "comparing_idx": None,
            "sorted_indices": list(range(i + 1)),
            "comparisons": comparisons,
            "shifts": shifts,
            "description": f"Inserted key {key} at index {j+1}. Subarray [0..{i}] is now sorted.",
        })

    steps.append({
        "step": len(steps),
        "array": list(a),
        "key_idx": None,
        "comparing_idx": None,
        "sorted_indices": list(range(n)),
        "comparisons": comparisons,
        "shifts": shifts,
        "description": f"Insertion Sort complete! Total comparisons: {comparisons}, Total shifts: {shifts}.",
    })

    return steps


# ==========================================
# 3. SELECTION SORT
# ==========================================

def selection_sort(arr: List[Any]) -> Tuple[List[Any], int, int]:
    """Pure Selection Sort for benchmarking.

    Returns:
        (sorted_array, comparisons, swaps)
    """
    a = list(arr)
    n = len(a)
    comparisons = 0
    swaps = 0

    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            comparisons += 1
            if a[j] < a[min_idx]:
                min_idx = j
        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            swaps += 1

    return a, comparisons, swaps


def selection_sort_steps(arr: List[Any]) -> List[Dict[str, Any]]:
    """Selection sort yielding step-by-step state for visualization."""
    steps: List[Dict[str, Any]] = []
    a = list(arr)
    n = len(a)
    comparisons = 0
    swaps = 0
    sorted_indices = set()

    steps.append({
        "step": 0,
        "array": list(a),
        "current_i": 0,
        "current_j": None,
        "min_idx": None,
        "sorted_indices": [],
        "comparisons": 0,
        "swaps": 0,
        "description": f"Initial array of size {n}. Beginning Selection Sort.",
    })

    if n <= 1:
        steps.append({
            "step": 1,
            "array": list(a),
            "current_i": 0,
            "current_j": None,
            "min_idx": 0,
            "sorted_indices": list(range(n)),
            "comparisons": 0,
            "swaps": 0,
            "description": "Array is already sorted (0 or 1 element).",
        })
        return steps

    for i in range(n - 1):
        min_idx = i
        steps.append({
            "step": len(steps),
            "array": list(a),
            "current_i": i,
            "current_j": None,
            "min_idx": min_idx,
            "sorted_indices": list(sorted_indices),
            "comparisons": comparisons,
            "swaps": swaps,
            "description": f"Pass {i+1}: Searching for the minimum element in [arr[{i}..{n-1}]]. Initial min at index {min_idx} (val: {a[min_idx]}).",
        })

        for j in range(i + 1, n):
            comparisons += 1
            is_smaller = a[j] < a[min_idx]

            steps.append({
                "step": len(steps),
                "array": list(a),
                "current_i": i,
                "current_j": j,
                "min_idx": min_idx,
                "sorted_indices": list(sorted_indices),
                "comparisons": comparisons,
                "swaps": swaps,
                "description": f"Comparing arr[{j}]={a[j]} with current min arr[{min_idx}]={a[min_idx]}.",
            })

            if is_smaller:
                min_idx = j
                steps.append({
                    "step": len(steps),
                    "array": list(a),
                    "current_i": i,
                    "current_j": j,
                    "min_idx": min_idx,
                    "sorted_indices": list(sorted_indices),
                    "comparisons": comparisons,
                    "swaps": swaps,
                    "description": f"New minimum found: arr[{min_idx}] = {a[min_idx]}.",
                })

        if min_idx != i:
            a[i], a[min_idx] = a[min_idx], a[i]
            swaps += 1
            sorted_indices.add(i)
            steps.append({
                "step": len(steps),
                "array": list(a),
                "current_i": i,
                "current_j": None,
                "min_idx": min_idx,
                "sorted_indices": list(sorted_indices),
                "comparisons": comparisons,
                "swaps": swaps,
                "description": f"Swapped minimum element {a[i]} into index {i} with {a[min_idx]}.",
            })
        else:
            sorted_indices.add(i)
            steps.append({
                "step": len(steps),
                "array": list(a),
                "current_i": i,
                "current_j": None,
                "min_idx": min_idx,
                "sorted_indices": list(sorted_indices),
                "comparisons": comparisons,
                "swaps": swaps,
                "description": f"Element at index {i} ({a[i]}) is already the minimum. No swap needed.",
            })

    sorted_indices = set(range(n))
    steps.append({
        "step": len(steps),
        "array": list(a),
        "current_i": None,
        "current_j": None,
        "min_idx": None,
        "sorted_indices": list(sorted_indices),
        "comparisons": comparisons,
        "swaps": swaps,
        "description": f"Selection Sort complete! Total comparisons: {comparisons}, Total swaps: {swaps}.",
    })

    return steps


# ==========================================
# 4. BINARY INSERTION SORT
# ==========================================

def binary_search_insertion_pos(a: List[Any], key: Any, start: int, end: int) -> Tuple[int, int]:
    """Binary search to find insertion position of key in sorted sub-array a[start..end].

    Returns:
        (insertion_index, comparisons)
    """
    low = start
    high = end
    comparisons = 0

    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        if a[mid] == key:
            return mid + 1, comparisons
        elif a[mid] < key:
            low = mid + 1
        else:
            high = mid - 1

    return low, comparisons


def binary_insertion_sort(arr: List[Any]) -> Tuple[List[Any], int, int]:
    """Pure Binary Insertion Sort for benchmarking.

    Reduces comparisons from O(n^2) to O(n log n), though shifts remain O(n^2).

    Returns:
        (sorted_array, comparisons, shifts)
    """
    a = list(arr)
    n = len(a)
    total_comparisons = 0
    total_shifts = 0

    for i in range(1, n):
        key = a[i]
        pos, comps = binary_search_insertion_pos(a, key, 0, i - 1)
        total_comparisons += comps

        # Shift elements
        j = i - 1
        while j >= pos:
            a[j + 1] = a[j]
            total_shifts += 1
            j -= 1
        a[pos] = key

    return a, total_comparisons, total_shifts


def binary_insertion_sort_steps(arr: List[Any]) -> List[Dict[str, Any]]:
    """Binary insertion sort yielding step-by-step state for visualization."""
    steps: List[Dict[str, Any]] = []
    a = list(arr)
    n = len(a)
    comparisons = 0
    shifts = 0

    steps.append({
        "step": 0,
        "array": list(a),
        "key_idx": None,
        "insert_pos": None,
        "sorted_indices": [0] if n > 0 else [],
        "comparisons": 0,
        "shifts": 0,
        "description": f"Initial array. Binary Insertion Sort will use binary search to locate insertion slots in O(log k).",
    })

    if n <= 1:
        return steps

    for i in range(1, n):
        key = a[i]
        low = 0
        high = i - 1

        steps.append({
            "step": len(steps),
            "array": list(a),
            "key_idx": i,
            "insert_pos": None,
            "sorted_indices": list(range(i)),
            "comparisons": comparisons,
            "shifts": shifts,
            "description": f"Extracting key arr[{i}] = {key}. Using Binary Search to find its exact position in sorted slice [0..{i-1}].",
        })

        # Step-by-step binary search for position
        while low <= high:
            mid = (low + high) // 2
            comparisons += 1
            steps.append({
                "step": len(steps),
                "array": list(a),
                "key_idx": i,
                "binary_low": low,
                "binary_high": high,
                "binary_mid": mid,
                "insert_pos": None,
                "sorted_indices": list(range(i)),
                "comparisons": comparisons,
                "shifts": shifts,
                "description": f"Binary Search: mid={mid} (val: {a[mid]}) vs key={key}.",
            })

            if a[mid] == key:
                low = mid + 1
                break
            elif a[mid] < key:
                low = mid + 1
            else:
                high = mid - 1

        pos = low
        steps.append({
            "step": len(steps),
            "array": list(a),
            "key_idx": i,
            "insert_pos": pos,
            "sorted_indices": list(range(i)),
            "comparisons": comparisons,
            "shifts": shifts,
            "description": f"Binary Search determined insertion slot is index {pos}. Now shifting elements [{pos}..{i-1}] to the right.",
        })

        # Shift elements
        j = i - 1
        while j >= pos:
            a[j + 1] = a[j]
            shifts += 1
            j -= 1

        a[pos] = key
        steps.append({
            "step": len(steps),
            "array": list(a),
            "key_idx": pos,
            "insert_pos": pos,
            "sorted_indices": list(range(i + 1)),
            "comparisons": comparisons,
            "shifts": shifts,
            "description": f"Inserted key {key} at index {pos}. Subarray [0..{i}] is now sorted.",
        })

    steps.append({
        "step": len(steps),
        "array": list(a),
        "key_idx": None,
        "insert_pos": None,
        "sorted_indices": list(range(n)),
        "comparisons": comparisons,
        "shifts": shifts,
        "description": f"Binary Insertion Sort complete! Total comparisons: {comparisons}, Total shifts: {shifts}.",
    })

    return steps
