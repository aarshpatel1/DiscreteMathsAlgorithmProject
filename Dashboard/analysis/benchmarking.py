"""Empirical benchmarking engine for measuring execution time and operation counts."""

import time
from typing import Any, Callable, Dict, List, Tuple
import pandas as pd

from algorithms.searching import linear_search, binary_search
from algorithms.sorting import (
    bubble_sort,
    insertion_sort,
    selection_sort,
    binary_insertion_sort,
)
from algorithms.majority_vote import boyer_moore_majority
from analysis.complexity import ALGORITHM_METADATA
from utils.data_generator import generate_array


SORTING_ALGORITHMS: Dict[str, Callable[[List[int]], Tuple[List[int], int, int]]] = {
    "Bubble Sort": bubble_sort,
    "Insertion Sort": insertion_sort,
    "Selection Sort": selection_sort,
    "Binary Insertion Sort": binary_insertion_sort,
}


def benchmark_sorting_single(
    algo_name: str,
    arr: List[int],
    trials: int = 3,
) -> Dict[str, Any]:
    """Runs a sorting algorithm on a copy of arr over multiple trials.

    Measures mean execution time and records operation counts.
    """
    func = SORTING_ALGORITHMS[algo_name]
    times: List[float] = []
    comparisons = 0
    swaps_or_shifts = 0

    for _ in range(trials):
        arr_copy = list(arr)
        t_start = time.perf_counter()
        _, comps, ops = func(arr_copy)
        t_end = time.perf_counter()
        times.append((t_end - t_start) * 1000.0)  # milliseconds
        comparisons = comps
        swaps_or_shifts = ops

    avg_time = sum(times) / len(times)

    return {
        "Algorithm": algo_name,
        "Input Size (n)": len(arr),
        "Execution Time (ms)": round(avg_time, 4),
        "Comparisons": comparisons,
        "Swaps / Shifts": swaps_or_shifts,
        "Total Operations": comparisons + swaps_or_shifts,
        "Theoretical Avg": ALGORITHM_METADATA.get(algo_name, {}).get("avg_time", "N/A"),
        "Theoretical Worst": ALGORITHM_METADATA.get(algo_name, {}).get("worst_time", "N/A"),
    }


def benchmark_sorting_suite(
    algorithms: List[str],
    sizes: List[int],
    distribution: str = "Random",
    trials: int = 3,
    seed: int = 42,
) -> pd.DataFrame:
    """Runs sorting suite across multiple sizes and algorithms on identical datasets.

    Returns:
        pd.DataFrame containing consolidated benchmarking results.
    """
    results: List[Dict[str, Any]] = []

    for size in sizes:
        # Generate base test array so all algorithms compete on EXACT SAME input
        base_arr = generate_array(size, distribution=distribution, seed=seed)

        for algo in algorithms:
            if algo in SORTING_ALGORITHMS:
                res = benchmark_sorting_single(algo, base_arr, trials=trials)
                res["Distribution"] = distribution
                results.append(res)

    return pd.DataFrame(results)


def benchmark_searching_suite(
    sizes: List[int],
    trials: int = 5,
    seed: int = 42,
) -> pd.DataFrame:
    """Benchmarks Linear Search vs Binary Search across array sizes."""
    import random
    results: List[Dict[str, Any]] = []

    for size in sizes:
        # Sorted array for fair binary search
        arr = generate_array(size, distribution="Sorted", min_val=1, max_val=size * 5, seed=seed)
        # Select target that is present (~middle or random) and one absent
        target = random.choice(arr)

        # 1. Linear Search
        lin_times: List[float] = []
        lin_comps = 0
        for _ in range(trials):
            t0 = time.perf_counter()
            _, lin_comps = linear_search(arr, target)
            t1 = time.perf_counter()
            lin_times.append((t1 - t0) * 1000.0)

        results.append({
            "Algorithm": "Linear Search",
            "Input Size (n)": size,
            "Execution Time (ms)": round(sum(lin_times) / len(lin_times), 5),
            "Comparisons": lin_comps,
            "Target Found": True,
            "Theoretical Avg": "O(n)",
        })

        # 2. Binary Search
        bin_times: List[float] = []
        bin_comps = 0
        for _ in range(trials):
            t0 = time.perf_counter()
            _, bin_comps = binary_search(arr, target)
            t1 = time.perf_counter()
            bin_times.append((t1 - t0) * 1000.0)

        results.append({
            "Algorithm": "Binary Search",
            "Input Size (n)": size,
            "Execution Time (ms)": round(sum(bin_times) / len(bin_times), 5),
            "Comparisons": bin_comps,
            "Target Found": True,
            "Theoretical Avg": "O(log n)",
        })

    return pd.DataFrame(results)
