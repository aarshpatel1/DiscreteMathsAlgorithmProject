"""Complexity metadata, mathematical definitions, and asymptotic growth functions."""

import math
from typing import Any, Callable, Dict, List
import numpy as np


# Metadata matrix for all algorithms in the platform
ALGORITHM_METADATA: Dict[str, Dict[str, Any]] = {
    # Searching
    "Linear Search": {
        "category": "Searching",
        "best_time": "O(1)",
        "avg_time": "O(n)",
        "worst_time": "O(n)",
        "space": "O(1)",
        "in_place": True,
        "stable": "N/A",
        "rosen_ref": "Rosen Section 3.1",
        "description": "Sequentially checks each element of the list until a match is found or the whole list has been searched.",
    },
    "Binary Search": {
        "category": "Searching",
        "best_time": "O(1)",
        "avg_time": "O(log n)",
        "worst_time": "O(log n)",
        "space": "O(1)",
        "in_place": True,
        "stable": "N/A",
        "rosen_ref": "Rosen Section 3.1",
        "description": "Repeatedly halves the sorted search interval by comparing target with the middle element.",
    },
    # Sorting
    "Bubble Sort": {
        "category": "Sorting",
        "best_time": "O(n)",
        "avg_time": "O(n^2)",
        "worst_time": "O(n^2)",
        "space": "O(1)",
        "in_place": True,
        "stable": "Yes",
        "rosen_ref": "Rosen Section 3.1",
        "description": "Repeatedly swaps adjacent out-of-order elements until no swaps are needed (with early termination).",
    },
    "Insertion Sort": {
        "category": "Sorting",
        "best_time": "O(n)",
        "avg_time": "O(n^2)",
        "worst_time": "O(n^2)",
        "space": "O(1)",
        "in_place": True,
        "stable": "Yes",
        "rosen_ref": "Rosen Section 3.1",
        "description": "Builds the final sorted array one item at a time by shifting larger elements rightward.",
    },
    "Selection Sort": {
        "category": "Sorting",
        "best_time": "O(n^2)",
        "avg_time": "O(n^2)",
        "worst_time": "O(n^2)",
        "space": "O(1)",
        "in_place": True,
        "stable": "No (in standard swap form)",
        "rosen_ref": "Rosen Section 3.1",
        "description": "Repeatedly identifies minimum element from unsorted sublist and moves it to the sorted prefix.",
    },
    "Binary Insertion Sort": {
        "category": "Sorting",
        "best_time": "O(n log n)",
        "avg_time": "O(n^2)",
        "worst_time": "O(n^2)",
        "space": "O(1)",
        "in_place": True,
        "stable": "Yes",
        "rosen_ref": "Rosen Section 3.1",
        "description": "Optimizes standard insertion sort by using binary search to find insertion position in O(log n) comparisons (shifts remain O(n^2)).",
    },
    # String Matching
    "Naive String Matching": {
        "category": "String Matching",
        "best_time": "O(n)",
        "avg_time": "O(n + m)",
        "worst_time": "O(n * m)",
        "space": "O(1)",
        "in_place": True,
        "stable": "N/A",
        "rosen_ref": "Rosen Section 3.1",
        "description": "Checks all possible shift positions s in [0..n-m] and matches pattern characters sequentially.",
    },
    # Greedy
    "Cashier's Algorithm": {
        "category": "Greedy Algorithms",
        "best_time": "O(k)",
        "avg_time": "O(k)",
        "worst_time": "O(k)",
        "space": "O(1)",
        "in_place": True,
        "stable": "N/A",
        "rosen_ref": "Rosen Section 3.1",
        "description": "Greedily picks highest value coin denomination <= remaining change. Optimal for standard coin systems.",
    },
    "Activity Selection": {
        "category": "Greedy Algorithms",
        "best_time": "O(n log n)",
        "avg_time": "O(n log n)",
        "worst_time": "O(n log n)",
        "space": "O(n)",
        "in_place": False,
        "stable": "N/A",
        "rosen_ref": "Rosen Section 3.1",
        "description": "Schedules maximum number of mutually compatible activities by greedily selecting earliest finish time.",
    },
    # Supplementary
    "Boyer-Moore Majority Vote": {
        "category": "Supplementary Algorithms",
        "best_time": "O(n)",
        "avg_time": "O(n)",
        "worst_time": "O(n)",
        "space": "O(1)",
        "in_place": True,
        "stable": "N/A",
        "rosen_ref": "Streaming / Discrete Algorithms",
        "description": "Finds candidate with net positive votes in Phase 1 and verifies candidate in Phase 2 in strictly linear time.",
    },
    "Gale-Shapley Stable Matching": {
        "category": "Supplementary Algorithms",
        "best_time": "O(n)",
        "avg_time": "O(n log n)",
        "worst_time": "O(n^2)",
        "space": "O(n^2)",
        "in_place": False,
        "stable": "Always Stable",
        "rosen_ref": "Rosen Section 3.1 / Gale-Shapley",
        "description": "Proposer-optimal algorithm guaranteeing a stable matching in at most n^2 iterations.",
    },
}

ASYMPTOTIC_NOTATIONS = {
    "Big-O (O) - Asymptotic Upper Bound": {
        "symbol": "O(g(n))",
        "formal_definition": r"f(n) \text{ is } O(g(n)) \iff \exists c > 0, k \ge 0 \text{ such that } |f(n)| \le c \cdot |g(n)| \quad \forall n > k",
        "meaning": "Provides a worst-case upper bound on execution growth rate. The algorithm will never grow faster than c * g(n).",
        "example": "Binary search comparisons are O(log n); Bubble sort is O(n^2).",
    },
    "Big-Omega (Ω) - Asymptotic Lower Bound": {
        "symbol": "Ω(g(n))",
        "formal_definition": r"f(n) \text{ is } \Omega(g(n)) \iff \exists c > 0, k \ge 0 \text{ such that } |f(n)| \ge c \cdot |g(n)| \quad \forall n > k",
        "meaning": "Provides a best-case lower bound. The algorithm takes at least c * g(n) operations for sufficiently large n.",
        "example": "Comparison-based sorting requires Ω(n log n) comparisons in the worst case.",
    },
    "Big-Theta (Θ) - Asymptotically Tight Bound": {
        "symbol": "Θ(g(n))",
        "formal_definition": r"f(n) \text{ is } \Theta(g(n)) \iff f(n) \text{ is } O(g(n)) \text{ and } f(n) \text{ is } \Omega(g(n))",
        "meaning": "Tight sandwich bound. f(n) grows at precisely the same rate as g(n) up to constant factors.",
        "example": "Selection sort comparisons are Θ(n^2) on ALL input permutations.",
    },
    "Little-o (o) - Strict Upper Bound": {
        "symbol": "o(g(n))",
        "formal_definition": r"\lim_{n \to \infty} \frac{f(n)}{g(n)} = 0",
        "meaning": "f(n) becomes insignificant relative to g(n) as n increases.",
        "example": "n is o(n^2); log n is o(n).",
    },
}

# Standard Complexity Classes
COMPLEXITY_CLASSES: Dict[str, Dict[str, Any]] = {
    "Constant: O(1)": {
        "func": lambda n: np.ones_like(n, dtype=float),
        "latex": r"O(1)",
        "color": "#10B981",  # Emerald
        "note": "Array index lookup, basic arithmetic operations.",
    },
    "Logarithmic: O(log n)": {
        "func": lambda n: np.log2(np.maximum(n, 1)),
        "latex": r"O(\log n)",
        "color": "#06B6D4",  # Cyan
        "note": "Binary Search, balanced search tree operations.",
    },
    "Linear: O(n)": {
        "func": lambda n: n.astype(float),
        "latex": r"O(n)",
        "color": "#3B82F6",  # Blue
        "note": "Linear Search, counting loop, Boyer-Moore majority vote.",
    },
    "Linearithmic: O(n log n)": {
        "func": lambda n: n * np.log2(np.maximum(n, 1)),
        "latex": r"O(n \log n)",
        "color": "#8B5CF6",  # Purple
        "note": "Merge sort, Quick sort (avg), Activity selection sorting.",
    },
    "Quadratic: O(n²)": {
        "func": lambda n: n.astype(float) ** 2,
        "latex": r"O(n^2)",
        "color": "#F59E0B",  # Amber
        "note": "Bubble sort, Selection sort, Insertion sort (worst).",
    },
    "Cubic: O(n³)": {
        "func": lambda n: n.astype(float) ** 3,
        "latex": r"O(n^3)",
        "color": "#EF4444",  # Red
        "note": "Naive matrix multiplication, Floyd-Warshall all-pairs shortest paths.",
    },
    "Exponential: O(2ⁿ)": {
        "func": lambda n: 2.0 ** np.minimum(n, 30),  # clip to avoid overflow
        "latex": r"O(2^n)",
        "color": "#EC4899",  # Pink
        "note": "Recursive Fibonacci, subset generation, exhaustive brute force.",
    },
}


def calculate_growth_data(max_n: int = 50, num_points: int = 100) -> Dict[str, np.ndarray]:
    """Generates numerical values for all complexity classes across range [1, max_n]."""
    n_vals = np.linspace(1, max_n, num_points)
    result = {"n": n_vals}
    for name, data in COMPLEXITY_CLASSES.items():
        result[name] = data["func"](n_vals)
    return result
