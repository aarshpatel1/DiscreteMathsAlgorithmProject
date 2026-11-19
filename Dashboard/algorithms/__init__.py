"""Algorithms package for searching, sorting, string matching, greedy, and supplementary algorithms."""

from .searching import (
    linear_search,
    linear_search_steps,
    binary_search,
    binary_search_steps,
)
from .sorting import (
    bubble_sort,
    bubble_sort_steps,
    insertion_sort,
    insertion_sort_steps,
    selection_sort,
    selection_sort_steps,
    binary_insertion_sort,
    binary_insertion_sort_steps,
)
from .string_matching import (
    naive_string_match,
    naive_string_match_steps,
)
from .greedy import (
    cashiers_algorithm,
    cashiers_algorithm_steps,
    activity_selection,
    activity_selection_steps,
)
from .majority_vote import (
    boyer_moore_majority,
    boyer_moore_majority_steps,
)
from .stable_matching import (
    gale_shapley,
    gale_shapley_steps,
)

__all__ = [
    "linear_search",
    "linear_search_steps",
    "binary_search",
    "binary_search_steps",
    "bubble_sort",
    "bubble_sort_steps",
    "insertion_sort",
    "insertion_sort_steps",
    "selection_sort",
    "selection_sort_steps",
    "binary_insertion_sort",
    "binary_insertion_sort_steps",
    "naive_string_match",
    "naive_string_match_steps",
    "cashiers_algorithm",
    "cashiers_algorithm_steps",
    "activity_selection",
    "activity_selection_steps",
    "boyer_moore_majority",
    "boyer_moore_majority_steps",
    "gale_shapley",
    "gale_shapley_steps",
]
