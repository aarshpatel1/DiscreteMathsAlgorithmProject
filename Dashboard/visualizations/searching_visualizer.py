"""Interactive Plotly visualization component for searching algorithms."""

from typing import Any, Dict, List
import plotly.graph_objects as go


COLOR_DEFAULT = "#3B82F6"      # Blue (unexplored)
COLOR_CURRENT = "#F59E0B"      # Amber (active search target / pointer)
COLOR_MID = "#8B5CF6"          # Purple (binary search midpoint)
COLOR_FOUND = "#10B981"        # Emerald Green (found)
COLOR_ELIMINATED = "#CBD5E1"   # Greyed out (eliminated from search window)
COLOR_WINDOW = "#93C5FD"       # Light blue (active search range)


def create_searching_bar_chart(step_data: Dict[str, Any], algo_type: str = "Linear") -> go.Figure:
    """Creates a stylized Plotly chart visualizing an array at a searching step.

    Args:
        step_data: State dictionary from searching step generators.
        algo_type: 'Linear' or 'Binary'.

    Returns:
        Plotly Figure object.
    """
    arr = step_data.get("array", [])
    n = len(arr)
    target = step_data.get("target")

    colors = [COLOR_DEFAULT] * n

    if algo_type == "Linear":
        curr = step_data.get("current_idx")
        status = step_data.get("status")

        if curr is not None:
            # Elements before current that didn't match are eliminated
            for i in range(curr):
                colors[i] = COLOR_ELIMINATED

            if status == "found":
                colors[curr] = COLOR_FOUND
            else:
                colors[curr] = COLOR_CURRENT
        elif status == "not_found":
            colors = [COLOR_ELIMINATED] * n

    elif algo_type == "Binary":
        low = step_data.get("low", 0)
        high = step_data.get("high", n - 1)
        mid = step_data.get("mid")
        status = step_data.get("status")

        # Grey out out-of-range elements
        for i in range(n):
            if i < low or i > high:
                colors[i] = COLOR_ELIMINATED
            else:
                colors[i] = COLOR_WINDOW

        if mid is not None and 0 <= mid < n:
            if status == "found":
                colors[mid] = COLOR_FOUND
            else:
                colors[mid] = COLOR_MID

    fig = go.Figure()

    # Annotation text above bars
    annotations = []
    labels = []
    for i, val in enumerate(arr):
        lbl = f"[{i}]<br><b>{val}</b>"
        labels.append(lbl)

    fig.add_trace(
        go.Bar(
            x=labels,
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

    # In binary search, add pointer markers for Low, Mid, High
    if algo_type == "Binary":
        low = step_data.get("low")
        high = step_data.get("high")
        mid = step_data.get("mid")

        pointer_labels = []
        if low is not None and 0 <= low < n:
            annotations.append(
                dict(
                    x=labels[low],
                    y=0,
                    text="<b>LOW ▲</b>",
                    showarrow=False,
                    yshift=-25,
                    font=dict(color="#2563EB", size=12),
                )
            )
        if high is not None and 0 <= high < n:
            annotations.append(
                dict(
                    x=labels[high],
                    y=0,
                    text="<b>HIGH ▲</b>",
                    showarrow=False,
                    yshift=-40 if high == low else -25,
                    font=dict(color="#DC2626", size=12),
                )
            )
        if mid is not None and 0 <= mid < n:
            annotations.append(
                dict(
                    x=labels[mid],
                    y=0,
                    text="<b>MID ▲</b>",
                    showarrow=False,
                    yshift=-55 if (mid == low or mid == high) else -25,
                    font=dict(color="#7C3AED", size=12),
                )
            )

    max_val = max(arr) if arr else 100
    fig.update_layout(
        height=430,
        margin=dict(l=20, r=20, t=30, b=70),
        font=dict(size=12),
        xaxis=dict(
            title="Array Index & Value",
            tickmode="linear",
            showgrid=False,
            title_font=dict(size=13),
        ),
        yaxis=dict(
            title="Element Value",
            range=[0, max_val * 1.3],
            showgrid=True,
            gridcolor="#E2E8F0",
            title_font=dict(size=13),
        ),
        plot_bgcolor="rgba(248, 250, 252, 0.8)",
        paper_bgcolor="rgba(0,0,0,0)",
        annotations=annotations,
        showlegend=False,
    )

    return fig
