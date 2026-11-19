"""Greedy algorithms implementation with execution metrics and step tracing.

Includes:
- Cashier's Change-Making Algorithm
- Activity Selection / Interval Scheduling Algorithm
"""

from typing import Any, Dict, List, Tuple


# ==========================================
# 1. CASHIER'S CHANGE ALGORITHM
# ==========================================

def cashiers_algorithm(
    amount: int, denominations: List[int] = None
) -> Tuple[Dict[int, int], int]:
    """Pure Cashier's Algorithm for change making.

    Standard canonical denominations: [25, 10, 5, 1] (US quarters, dimes, nickels, pennies)
    or [500, 200, 100, 50, 20, 10, 5, 2, 1] (INR / European style).

    Returns:
        Tuple of (coin_counts_dict, total_coins).
    """
    if denominations is None:
        denominations = [25, 10, 5, 1]

    # Sort descending
    coins = sorted(denominations, reverse=True)
    counts = {}
    remaining = amount
    total_coins = 0

    for coin in coins:
        if remaining <= 0:
            counts[coin] = 0
            continue
        num_coins = remaining // coin
        counts[coin] = num_coins
        total_coins += num_coins
        remaining %= coin

    return counts, total_coins


def cashiers_algorithm_steps(
    amount: int,
    denominations: List[int] = None,
    currency_symbol: str = "$",
    denom_labels: Dict[int, str] = None,
    is_cents: bool = False,
) -> List[Dict[str, Any]]:
    """Cashier's algorithm yielding step-by-step state for visualization.

    Args:
        amount: Integer amount to make change for.
        denominations: List of positive integer denominations (descending).
        currency_symbol: Currency symbol (e.g. '$' for US currency, '₹' for INR).
        denom_labels: Optional mapping of denomination integer to human label.
        is_cents: If True, integer amounts represent cents and are formatted as $X.XX.
    """
    if denominations is None:
        denominations = [25, 10, 5, 1]

    coins = sorted(denominations, reverse=True)
    steps: List[Dict[str, Any]] = []
    counts: Dict[int, int] = {c: 0 for c in coins}
    remaining = amount

    def fmt_val(val: int) -> str:
        if currency_symbol == "$" and is_cents:
            return f"${val / 100:.2f} ({val}¢)" if val < 100 else f"${val / 100:.2f}"
        return f"{currency_symbol}{val}"

    def get_coin_label(c: int) -> str:
        if denom_labels and c in denom_labels:
            return denom_labels[c]
        if currency_symbol == "$" and is_cents:
            coin_names = {25: "Quarter ($0.25)", 10: "Dime ($0.10)", 5: "Nickel ($0.05)", 1: "Penny ($0.01)"}
            return coin_names.get(c, f"${c / 100:.2f}")
        return f"{currency_symbol}{c}"

    steps.append({
        "step": 0,
        "remaining": remaining,
        "current_coin": None,
        "coins_used": dict(counts),
        "total_coins": 0,
        "status": "start",
        "description": f"Target amount: {fmt_val(amount)}. Available denominations (greedy descending order): {[get_coin_label(c) for c in coins]}.",
    })

    total_coins = 0
    for coin in coins:
        coin_lbl = get_coin_label(coin)
        if remaining == 0:
            steps.append({
                "step": len(steps),
                "remaining": 0,
                "current_coin": coin,
                "coins_used": dict(counts),
                "total_coins": total_coins,
                "status": "skipped",
                "description": f"Remaining amount is {fmt_val(0)}. Denomination {coin_lbl} skipped.",
            })
            continue

        num = remaining // coin
        if num > 0:
            counts[coin] = num
            total_coins += num
            remaining -= num * coin
            subtotal = num * coin
            steps.append({
                "step": len(steps),
                "remaining": remaining,
                "current_coin": coin,
                "coins_used": dict(counts),
                "total_coins": total_coins,
                "status": "taken",
                "description": f"Greedy choice: Selected {num} coin(s) of value {coin_lbl} (Subtotal: {fmt_val(subtotal)}). Remaining balance: {fmt_val(remaining)}.",
            })
        else:
            steps.append({
                "step": len(steps),
                "remaining": remaining,
                "current_coin": coin,
                "coins_used": dict(counts),
                "total_coins": total_coins,
                "status": "cannot_fit",
                "description": f"Denomination {coin_lbl} exceeds remaining amount {fmt_val(remaining)}. 0 coins taken.",
            })

    steps.append({
        "step": len(steps),
        "remaining": remaining,
        "current_coin": None,
        "coins_used": dict(counts),
        "total_coins": total_coins,
        "status": "complete",
        "description": f"Cashier's algorithm completed! Total coins used: {total_coins}. Remaining unresolved: {fmt_val(remaining)}.",
    })

    return steps


# ==========================================
# 2. ACTIVITY SELECTION ALGORITHM
# ==========================================

def activity_selection(
    activities: List[Dict[str, Any]]
) -> Tuple[List[Dict[str, Any]], int]:
    """Pure Activity Selection algorithm (Earliest Finish Time First).

    Args:
        activities: List of dicts, each having {'id': Any, 'start': int, 'finish': int}.

    Returns:
        Tuple of (selected_activities, count).
    """
    if not activities:
        return [], 0

    # Sort activities by finish time
    sorted_acts = sorted(activities, key=lambda a: (a["finish"], a["start"]))
    selected = [sorted_acts[0]]
    last_finish = sorted_acts[0]["finish"]

    for act in sorted_acts[1:]:
        if act["start"] >= last_finish:
            selected.append(act)
            last_finish = act["finish"]

    return selected, len(selected)


def activity_selection_steps(
    activities: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Activity selection yielding step-by-step state for visualization."""
    steps: List[Dict[str, Any]] = []

    if not activities:
        return steps

    # Sort activities by finish time
    sorted_acts = sorted(activities, key=lambda a: (a["finish"], a["start"]))

    steps.append({
        "step": 0,
        "activities": sorted_acts,
        "current_idx": None,
        "last_finish": -1,
        "selected_ids": [],
        "status": "start",
        "description": f"Sorted {len(sorted_acts)} activities by finish time (Greedy Earliest Finish Time First strategy).",
    })

    # Greedily pick first activity
    first = sorted_acts[0]
    selected_ids = [first["id"]]
    last_finish = first["finish"]

    steps.append({
        "step": 1,
        "activities": sorted_acts,
        "current_idx": 0,
        "last_finish": last_finish,
        "selected_ids": list(selected_ids),
        "status": "selected",
        "description": f"Greedy choice: Selected Activity '{first['id']}' [Start: {first['start']}, Finish: {first['finish']}] with earliest finish time.",
    })

    for i in range(1, len(sorted_acts)):
        act = sorted_acts[i]
        compatible = (act["start"] >= last_finish)

        if compatible:
            selected_ids.append(act["id"])
            old_finish = last_finish
            last_finish = act["finish"]
            steps.append({
                "step": len(steps),
                "activities": sorted_acts,
                "current_idx": i,
                "last_finish": last_finish,
                "selected_ids": list(selected_ids),
                "status": "selected",
                "description": f"Activity '{act['id']}' [Start: {act['start']}, Finish: {act['finish']}] starts >= last finish time ({old_finish}). Compatible and SELECTED!",
            })
        else:
            steps.append({
                "step": len(steps),
                "activities": sorted_acts,
                "current_idx": i,
                "last_finish": last_finish,
                "selected_ids": list(selected_ids),
                "status": "rejected",
                "description": f"Activity '{act['id']}' [Start: {act['start']}, Finish: {act['finish']}] conflicts with current finish time ({last_finish}). REJECTED.",
            })

    steps.append({
        "step": len(steps),
        "activities": sorted_acts,
        "current_idx": None,
        "last_finish": last_finish,
        "selected_ids": list(selected_ids),
        "status": "complete",
        "description": f"Optimal schedule found! Selected {len(selected_ids)} mutually compatible activities: {selected_ids}.",
    })

    return steps
