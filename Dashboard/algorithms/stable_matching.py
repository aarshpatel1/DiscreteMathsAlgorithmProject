"""Gale-Shapley Stable Matching (Stable Marriage) Algorithm implementation.

Guarantees a stable matching in O(n^2) proposals where no two individuals prefer each other over their assigned partners.
"""

from typing import Any, Dict, List, Tuple


def gale_shapley(
    proposer_prefs: Dict[str, List[str]],
    receiver_prefs: Dict[str, List[str]]
) -> Tuple[Dict[str, str], int]:
    """Pure Gale-Shapley Algorithm for stable matching.

    Args:
        proposer_prefs: Mapping proposer -> list of receivers in order of preference.
        receiver_prefs: Mapping receiver -> list of proposers in order of preference.

    Returns:
        Tuple of (receiver_to_proposer_matching, total_proposals).
    """
    proposers = list(proposer_prefs.keys())
    free_proposers = list(proposers)
    proposals_made: Dict[str, int] = {p: 0 for p in proposers}
    # Current partner of each receiver: receiver -> proposer
    engagements: Dict[str, str] = {}
    total_proposals = 0

    # Build rank lookup for receivers: receiver -> {proposer: rank} (lower rank is preferred)
    receiver_rank: Dict[str, Dict[str, int]] = {}
    for r, p_list in receiver_prefs.items():
        receiver_rank[r] = {p: idx for idx, p in enumerate(p_list)}

    while free_proposers:
        m = free_proposers.pop(0)
        # Next woman on m's preference list
        w_idx = proposals_made[m]
        if w_idx >= len(proposer_prefs[m]):
            continue  # Exhausted list
        w = proposer_prefs[m][w_idx]
        proposals_made[m] += 1
        total_proposals += 1

        if w not in engagements:
            # Receiver is free
            engagements[w] = m
        else:
            current_partner = engagements[w]
            # Check if receiver prefers new proposer m over current_partner
            if receiver_rank[w].get(m, float('inf')) < receiver_rank[w].get(current_partner, float('inf')):
                # Receiver ditches current partner for m
                engagements[w] = m
                free_proposers.append(current_partner)
            else:
                # Receiver rejects m
                free_proposers.append(m)

    return engagements, total_proposals


def gale_shapley_steps(
    proposer_prefs: Dict[str, List[str]],
    receiver_prefs: Dict[str, List[str]]
) -> List[Dict[str, Any]]:
    """Gale-Shapley algorithm yielding step-by-step state for visualization."""
    steps: List[Dict[str, Any]] = []
    proposers = list(proposer_prefs.keys())
    free_proposers = list(proposers)
    proposals_made: Dict[str, int] = {p: 0 for p in proposers}
    engagements: Dict[str, str] = {}
    total_proposals = 0

    receiver_rank: Dict[str, Dict[str, int]] = {}
    for r, p_list in receiver_prefs.items():
        receiver_rank[r] = {p: idx for idx, p in enumerate(p_list)}

    steps.append({
        "step": 0,
        "free_proposers": list(free_proposers),
        "engagements": dict(engagements),
        "current_proposer": None,
        "current_receiver": None,
        "action": "start",
        "total_proposals": 0,
        "description": f"Initialized Gale-Shapley with {len(proposers)} proposers and {len(receiver_prefs)} receivers.",
    })

    while free_proposers:
        m = free_proposers.pop(0)
        w_idx = proposals_made[m]
        if w_idx >= len(proposer_prefs[m]):
            continue

        w = proposer_prefs[m][w_idx]
        proposals_made[m] += 1
        total_proposals += 1

        if w not in engagements:
            engagements[w] = m
            steps.append({
                "step": len(steps),
                "free_proposers": list(free_proposers),
                "engagements": dict(engagements),
                "current_proposer": m,
                "current_receiver": w,
                "action": "accepted_free",
                "total_proposals": total_proposals,
                "description": f"'{m}' proposed to '{w}'. '{w}' was free and ACCEPTED the engagement.",
            })
        else:
            current_partner = engagements[w]
            m_rank = receiver_rank[w].get(m, 999)
            curr_rank = receiver_rank[w].get(current_partner, 999)

            if m_rank < curr_rank:
                engagements[w] = m
                free_proposers.append(current_partner)
                steps.append({
                    "step": len(steps),
                    "free_proposers": list(free_proposers),
                    "engagements": dict(engagements),
                    "current_proposer": m,
                    "current_receiver": w,
                    "action": "switched",
                    "total_proposals": total_proposals,
                    "description": (
                        f"'{m}' proposed to '{w}'. '{w}' prefers '{m}' (rank #{m_rank + 1}) "
                        f"over '{current_partner}' (rank #{curr_rank + 1})! "
                        f"'{w}' breaks engagement with '{current_partner}' and pairs with '{m}'."
                    ),
                })
            else:
                free_proposers.append(m)
                steps.append({
                    "step": len(steps),
                    "free_proposers": list(free_proposers),
                    "engagements": dict(engagements),
                    "current_proposer": m,
                    "current_receiver": w,
                    "action": "rejected",
                    "total_proposals": total_proposals,
                    "description": (
                        f"'{m}' proposed to '{w}', but '{w}' prefers current partner '{current_partner}' "
                        f"(rank #{curr_rank + 1}) over '{m}' (rank #{m_rank + 1}). Proposal REJECTED."
                    ),
                })

    steps.append({
        "step": len(steps),
        "free_proposers": [],
        "engagements": dict(engagements),
        "current_proposer": None,
        "current_receiver": None,
        "action": "complete",
        "total_proposals": total_proposals,
        "description": f"Stable matching achieved in {total_proposals} proposals! No blocking pairs exist.",
    })

    return steps
