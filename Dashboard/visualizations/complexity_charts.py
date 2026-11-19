"""Plotly charts for asymptotic growth, empirical benchmarks, and activity scheduling."""

from typing import Any, Dict, List
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from analysis.complexity import COMPLEXITY_CLASSES, calculate_growth_data


def create_growth_chart(
    selected_classes: List[str] = None,
    max_n: int = 50,
    log_scale: bool = False,
) -> go.Figure:
    """Creates interactive Plotly line chart comparing mathematical growth rates.

    Args:
        selected_classes: List of complexity class names to plot.
        max_n: Maximum value on x-axis (n).
        log_scale: Whether y-axis should use logarithmic scale.

    Returns:
        Plotly Figure object.
    """
    if selected_classes is None:
        selected_classes = list(COMPLEXITY_CLASSES.keys())

    data = calculate_growth_data(max_n=max_n)
    n_vals = data["n"]

    fig = go.Figure()

    for name in selected_classes:
        if name in COMPLEXITY_CLASSES:
            y_vals = data[name]
            meta = COMPLEXITY_CLASSES[name]
            fig.add_trace(
                go.Scatter(
                    x=n_vals,
                    y=y_vals,
                    mode="lines",
                    name=name,
                    line=dict(color=meta["color"], width=3),
                    hovertemplate=f"<b>{name}</b><br>n = %{{x:.1f}}<br>f(n) = %{{y:.2f}}<extra></extra>",
                )
            )

    fig.update_layout(
        title=f"Asymptotic Growth Rate Comparison (n = 1 to {max_n})",
        font=dict(family="Inter, sans-serif"),
        xaxis=dict(
            title="Input Size (n)",
            showgrid=True,
            gridcolor="#E2E8F0",
            title_font=dict(family="Inter, sans-serif"),
            tickfont=dict(family="Inter, sans-serif"),
        ),
        yaxis=dict(
            title="Operations f(n)",
            type="log" if log_scale else "linear",
            showgrid=True,
            gridcolor="#E2E8F0",
            title_font=dict(family="Inter, sans-serif"),
            tickfont=dict(family="Inter, sans-serif"),
        ),
        hovermode="x unified",
        plot_bgcolor="rgba(248, 250, 252, 0.9)",
        paper_bgcolor="rgba(0,0,0,0)",
        legend=dict(
            yanchor="top",
            y=0.98,
            xanchor="left",
            x=0.02,
            bgcolor="rgba(255, 255, 255, 0.8)",
            bordercolor="#CBD5E1",
            borderwidth=1,
            font=dict(family="Inter, sans-serif"),
        ),
        height=500,
        margin=dict(l=20, r=20, t=50, b=30),
    )

    return fig


def create_benchmark_time_chart(df: pd.DataFrame) -> go.Figure:
    """Creates line chart comparing empirical execution times across input sizes."""
    if df.empty:
        return go.Figure()

    fig = px.line(
        df,
        x="Input Size (n)",
        y="Execution Time (ms)",
        color="Algorithm",
        markers=True,
        title="Execution Time vs Input Size (Empirical Benchmark)",
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=8),
    )

    fig.update_layout(
        font=dict(family="Inter, sans-serif"),
        plot_bgcolor="rgba(248, 250, 252, 0.9)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(
            title="Execution Time (ms)",
            showgrid=True,
            gridcolor="#E2E8F0",
            title_font=dict(family="Inter, sans-serif"),
            tickfont=dict(family="Inter, sans-serif"),
        ),
        xaxis=dict(
            title="Input Size (n)",
            showgrid=True,
            gridcolor="#E2E8F0",
            title_font=dict(family="Inter, sans-serif"),
            tickfont=dict(family="Inter, sans-serif"),
        ),
        height=450,
        margin=dict(l=20, r=20, t=50, b=30),
    )

    return fig


def create_benchmark_ops_chart(df: pd.DataFrame, metric: str = "Comparisons") -> go.Figure:
    """Creates grouped bar chart for Comparisons or Swaps across algorithms."""
    if df.empty or metric not in df.columns:
        return go.Figure()

    fig = px.bar(
        df,
        x="Input Size (n)",
        y=metric,
        color="Algorithm",
        barmode="group",
        title=f"{metric} Count by Algorithm and Input Size",
    )

    fig.update_layout(
        font=dict(family="Inter, sans-serif"),
        plot_bgcolor="rgba(248, 250, 252, 0.9)",
        paper_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(
            title=f"{metric} Count",
            showgrid=True,
            gridcolor="#E2E8F0",
            title_font=dict(family="Inter, sans-serif"),
            tickfont=dict(family="Inter, sans-serif"),
        ),
        xaxis=dict(
            title_font=dict(family="Inter, sans-serif"),
            tickfont=dict(family="Inter, sans-serif"),
        ),
        height=420,
        margin=dict(l=20, r=20, t=50, b=30),
    )

    return fig


def create_activity_timeline_chart(
    activities: List[Dict[str, Any]],
    selected_ids: List[Any],
    current_idx: int = None,
) -> go.Figure:
    """Gantt / Timeline chart for Activity Selection visualization."""
    fig = go.Figure()
    selected_set = set(selected_ids)

    for i, act in enumerate(activities):
        is_selected = act["id"] in selected_set
        is_current = (current_idx == i)

        if is_selected:
            color = "#10B981"  # Emerald
            status = "Selected"
        elif is_current:
            color = "#F59E0B"  # Amber
            status = "Evaluating"
        else:
            color = "#94A3B8"  # Slate grey
            status = "Rejected / Pending"

        # Horizontal bar
        fig.add_trace(
            go.Bar(
                name=f"Activity {act['id']}",
                y=[f"Act {act['id']}"],
                x=[act["finish"] - act["start"]],
                base=[act["start"]],
                orientation="h",
                marker=dict(color=color, line=dict(color="#1E293B", width=1.5)),
                text=f"[{act['start']} -> {act['finish']}] ({status})",
                textposition="inside",
                insidetextanchor="middle",
                textfont=dict(color="#FFFFFF", size=11, family="Inter, sans-serif"),
                hovertemplate=f"Activity {act['id']}<br>Start: {act['start']}<br>Finish: {act['finish']}<br>Status: {status}<extra></extra>",
                showlegend=False,
            )
        )

    fig.update_layout(
        title="Activity Selection Schedule Timeline",
        font=dict(family="Inter, sans-serif"),
        xaxis=dict(
            title="Time Units",
            showgrid=True,
            gridcolor="#E2E8F0",
            dtick=1,
            title_font=dict(family="Inter, sans-serif"),
            tickfont=dict(family="Inter, sans-serif"),
        ),
        yaxis=dict(
            title="Activities",
            autorange="reversed",
            title_font=dict(family="Inter, sans-serif"),
            tickfont=dict(family="Inter, sans-serif"),
        ),
        height=380,
        plot_bgcolor="rgba(248, 250, 252, 0.9)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=50, b=30),
    )

    return fig


def create_cashier_bar_chart(
    step_data: Dict[str, Any],
    denominations: List[int],
    currency_symbol: str = "$",
    denom_labels: Dict[int, str] = None,
    is_cents: bool = False,
) -> go.Figure:
    """Creates a Plotly bar chart visualizing coin selections for Cashier's Algorithm."""
    fig = go.Figure()
    coins_used = step_data.get("coins_used", {})
    curr_coin = step_data.get("current_coin")
    status = step_data.get("status", "")

    labels = []
    counts = []
    colors = []
    subtotals = []

    for c in denominations:
        if denom_labels and c in denom_labels:
            lbl = denom_labels[c]
        elif currency_symbol == "$" and is_cents:
            names = {25: "Quarter ($0.25)", 10: "Dime ($0.10)", 5: "Nickel ($0.05)", 1: "Penny ($0.01)"}
            lbl = names.get(c, f"${c/100:.2f}")
        else:
            lbl = f"{currency_symbol}{c}"
        labels.append(lbl)

        cnt = coins_used.get(c, 0)
        counts.append(cnt)

        if currency_symbol == "$" and is_cents:
            subtotals.append(f"${(cnt * c) / 100:.2f}")
        else:
            subtotals.append(f"{currency_symbol}{cnt * c}")

        if c == curr_coin:
            if status == "taken":
                colors.append("#10B981")  # Emerald green (taken)
            elif status == "cannot_fit":
                colors.append("#EF4444")  # Red (cannot fit)
            elif status == "skipped":
                colors.append("#94A3B8")  # Slate (skipped)
            else:
                colors.append("#F59E0B")  # Amber (evaluating)
        elif cnt > 0:
            colors.append("#3B82F6")  # Blue (already taken)
        else:
            colors.append("#E2E8F0")  # Light slate (unprocessed / 0)

    fig.add_trace(
        go.Bar(
            x=labels,
            y=counts,
            marker=dict(color=colors, line=dict(color="#1E293B", width=1.5)),
            text=[f"{c} coins<br>({s})" if c > 0 else "0" for c, s in zip(counts, subtotals)],
            textposition="outside",
            textfont=dict(family="Inter, sans-serif", size=13, color="#0F172A"),
            hovertemplate="Denomination: %{x}<br>Count: %{y}<extra></extra>",
        )
    )

    max_c = max(counts) if counts and max(counts) > 0 else 1
    fig.update_layout(
        title="Coins / Units Selected per Denomination",
        font=dict(family="Inter, sans-serif"),
        xaxis=dict(
            title="Denomination",
            showgrid=False,
            title_font=dict(family="Inter, sans-serif"),
            tickfont=dict(family="Inter, sans-serif"),
        ),
        yaxis=dict(
            title="Number of Coins",
            range=[0, max_c * 1.35 + 1],
            showgrid=True,
            gridcolor="#E2E8F0",
            dtick=1,
            title_font=dict(family="Inter, sans-serif"),
            tickfont=dict(family="Inter, sans-serif"),
        ),
        plot_bgcolor="rgba(248, 250, 252, 0.9)",
        paper_bgcolor="rgba(0,0,0,0)",
        height=360,
        margin=dict(l=20, r=20, t=50, b=30),
        showlegend=False,
    )

    return fig
