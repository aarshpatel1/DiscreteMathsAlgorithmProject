"""Interactive Plotly visualization component for sorting algorithms."""

from typing import Any, Dict, List
import plotly.graph_objects as go


COLOR_DEFAULT = "#3B82F6"      # Vibrant Blue
COLOR_COMPARE = "#F59E0B"      # Vibrant Amber / Orange
COLOR_SWAP = "#EF4444"         # Vibrant Crimson / Red
COLOR_SORTED = "#10B981"       # Emerald Green
COLOR_KEY = "#8B5CF6"          # Purple for Key element


def create_sorting_bar_chart(step_data: Dict[str, Any]) -> go.Figure:
    """Creates a stylized Plotly bar chart visualizing an array at a specific sorting step.

    Args:
        step_data: State dictionary from sorting step generators.

    Returns:
        Plotly Figure object.
    """
    arr = step_data.get("array", [])
    n = len(arr)
    indices = list(range(n))

    # Determine color for each bar
    colors = [COLOR_DEFAULT] * n

    # Mark sorted elements
    sorted_set = set(step_data.get("sorted_indices", []))
    for idx in sorted_set:
        if 0 <= idx < n:
            colors[idx] = COLOR_SORTED

    # Mark actively compared elements
    comparing = step_data.get("comparing", [])
    for idx in comparing:
        if 0 <= idx < n:
            colors[idx] = COLOR_COMPARE

    if step_data.get("comparing_idx") is not None:
        c_idx = step_data["comparing_idx"]
        if 0 <= c_idx < n:
            colors[c_idx] = COLOR_COMPARE

    # Mark swapped elements
    swapped = step_data.get("swapped_pair", [])
    for idx in swapped:
        if 0 <= idx < n:
            colors[idx] = COLOR_SWAP

    # Mark key element (Insertion Sort / Binary Insertion Sort)
    key_idx = step_data.get("key_idx")
    if key_idx is not None and 0 <= key_idx < n:
        colors[key_idx] = COLOR_KEY

    # Mark minimum index (Selection Sort)
    min_idx = step_data.get("min_idx")
    if min_idx is not None and 0 <= min_idx < n:
        colors[min_idx] = COLOR_KEY

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=[f"[{i}]<br><b>{val}</b>" for i, val in enumerate(arr)],
            y=arr,
            marker_color=colors,
            marker_line_color="#1E293B",
            marker_line_width=1.5,
            text=arr,
            textposition="outside",
            textfont=dict(size=14, color="#0F172A"),
            hovertemplate="Index: %{x}<br>Value: %{y}<extra></extra>",
        )
    )

    max_val = max(arr) if arr else 100
    fig.update_layout(
        height=400,
        margin=dict(l=20, r=20, t=30, b=40),
        xaxis=dict(
            title="Array Index & Value",
            tickmode="linear",
            showgrid=False,
            title_font=dict(size=13),
        ),
        yaxis=dict(
            title="Element Value",
            range=[0, max_val * 1.25],
            showgrid=True,
            gridcolor="#E2E8F0",
            title_font=dict(size=13),
        ),
        plot_bgcolor="rgba(248, 250, 252, 0.8)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(size=12),
        showlegend=False,
    )

    return fig
