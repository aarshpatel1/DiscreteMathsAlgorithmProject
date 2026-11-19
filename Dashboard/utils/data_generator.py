"""Data generator for algorithms and benchmarking.

Supports various distributions:
- Random
- Sorted (ascending)
- Reverse sorted (descending)
- Nearly sorted (small number of perturbations)
- Many duplicates (few unique elements)
"""

import random
from typing import List, Optional


def generate_array(
    size: int,
    distribution: str = "Random",
    min_val: int = 5,
    max_val: int = 100,
    seed: Optional[int] = None,
) -> List[int]:
    """Generate an array of integers based on specified distribution.

    Args:
        size: Number of elements in the array.
        distribution: One of 'Random', 'Sorted', 'Reverse Sorted', 'Nearly Sorted', 'Duplicates'.
        min_val: Minimum integer value.
        max_val: Maximum integer value.
        seed: Optional random seed for reproducibility.

    Returns:
        List of integers.
    """
    if seed is not None:
        random.seed(seed)

    if size <= 0:
        return []

    if distribution == "Sorted":
        arr = [random.randint(min_val, max_val) for _ in range(size)]
        arr.sort()
        return arr

    elif distribution == "Reverse Sorted":
        arr = [random.randint(min_val, max_val) for _ in range(size)]
        arr.sort(reverse=True)
        return arr

    elif distribution == "Nearly Sorted":
        arr = [random.randint(min_val, max_val) for _ in range(size)]
        arr.sort()
        # Perform ~5-10% swaps
        num_swaps = max(1, int(size * 0.08))
        for _ in range(num_swaps):
            i = random.randint(0, size - 1)
            j = random.randint(0, size - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr

    elif distribution == "Duplicates":
        # Only 3-5 unique values
        unique_vals = [random.randint(min_val, max_val) for _ in range(min(4, max(2, size // 2)))]
        return [random.choice(unique_vals) for _ in range(size)]

    else:  # "Random" default
        return [random.randint(min_val, max_val) for _ in range(size)]


def parse_custom_array(text: str) -> List[int]:
    """Parse comma or space separated string into list of integers.

    Args:
        text: Input string like "12, 45, 2, 8, 19" or "12 45 2 8 19".

    Returns:
        List of parsed integers.
    """
    clean_text = text.replace(",", " ").strip()
    if not clean_text:
        return []
    tokens = clean_text.split()
    return [int(t) for t in tokens]
