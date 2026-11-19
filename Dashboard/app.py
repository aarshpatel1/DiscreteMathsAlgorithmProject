"""Algorithm Analysis & Visualization Platform

Interactive learning, algorithm execution, complexity analysis, and performance benchmarking.
Built with Streamlit and Plotly.
"""

import os
import sys
import time
from typing import Any, Dict, List

# Ensure current directory is in Python path for smooth imports
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# Platform packages
from algorithms.searching import (
    linear_search,
    linear_search_steps,
    binary_search,
    binary_search_steps,
)
from algorithms.sorting import (
    bubble_sort,
    bubble_sort_steps,
    insertion_sort,
    insertion_sort_steps,
    selection_sort,
    selection_sort_steps,
    binary_insertion_sort,
    binary_insertion_sort_steps,
)
from algorithms.string_matching import (
    naive_string_match,
    naive_string_match_steps,
)
from algorithms.greedy import (
    cashiers_algorithm,
    cashiers_algorithm_steps,
    activity_selection,
    activity_selection_steps,
)
from algorithms.majority_vote import (
    boyer_moore_majority,
    boyer_moore_majority_steps,
)
from algorithms.stable_matching import (
    gale_shapley,
    gale_shapley_steps,
)
from analysis.complexity import (
    ALGORITHM_METADATA,
    ASYMPTOTIC_NOTATIONS,
    COMPLEXITY_CLASSES,
    calculate_growth_data,
)
from analysis.benchmarking import (
    benchmark_sorting_suite,
    benchmark_searching_suite,
    SORTING_ALGORITHMS,
)
from utils.data_generator import generate_array, parse_custom_array
from visualizations.sorting_visualizer import create_sorting_bar_chart
from visualizations.searching_visualizer import create_searching_bar_chart
from visualizations.complexity_charts import (
    create_growth_chart,
    create_benchmark_time_chart,
    create_benchmark_ops_chart,
    create_activity_timeline_chart,
    create_cashier_bar_chart,
)

# ==========================================
# PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="Algorithm Analysis & Visualization Platform",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for polished academic UI & crisp Light Theme using Streamlit's default typography
st.markdown(
    """
    <style>
    /* Main container refinements */
    .main .block-container {
        padding-top: 1.8rem;
        padding-bottom: 2.5rem;
    }
    
    /* Card design */
    .metric-card {
        background: linear-gradient(135deg, #F8FAFC 0%, #EFF6FF 100%);
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    .metric-title {
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #64748B;
        font-weight: 700;
        margin-bottom: 0.25rem;
    }
    .metric-val {
        font-size: 1.8rem;
        font-weight: 800;
        color: #1E293B;
    }
    .metric-desc {
        font-size: 0.8rem;
        color: #94A3B8;
        margin-top: 0.2rem;
    }
    
    /* Badge tags */
    .badge-tag {
        display: inline-block;
        padding: 0.2rem 0.55rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.35rem;
    }
    .badge-time { background-color: #DBEAFE; color: #1E40AF; }
    .badge-space { background-color: #DCFCE7; color: #166534; }
    .badge-cat { background-color: #F3E8FF; color: #6B21A8; }
    
    /* Step description banner */
    .step-banner {
        background: #F1F5F9;
        border-left: 5px solid #3B82F6;
        padding: 0.9rem 1.2rem;
        border-radius: 6px;
        font-size: 0.95rem;
        color: #0F172A;
        margin-top: 0.6rem;
        margin-bottom: 0.8rem;
    }
    
    /* Control toolbar buttons */
    .stButton > button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
st.sidebar.image(
    "https://img.icons8.com/fluency/96/data-configuration.png",
    width=64,
)
st.sidebar.title("Algorithm Platform")
st.sidebar.caption("DA-IICT Discrete Mathematics Project")

PAGES = [
    "📊 Dashboard Overview",
    "📖 Algorithm Fundamentals",
    "🔍 Searching Algorithms",
    "🔃 Sorting Algorithms",
    "🔤 String Matching",
    "⚡ Greedy Algorithms",
    "📈 Complexity & Growth",
    "🔬 Benchmarking Engine",
    "🧩 Supplementary Algorithms",
]

# Navigation state handling and callback
def navigate_to(page_name: str) -> None:
    """Callback to switch active module via the sidebar radio widget state."""
    st.session_state["nav_selection"] = page_name
    st.session_state["current_page"] = page_name

if "nav_selection" not in st.session_state:
    st.session_state["nav_selection"] = PAGES[0]

selected_page = st.sidebar.radio(
    "Select Module",
    PAGES,
    key="nav_selection",
)
st.session_state["current_page"] = selected_page

st.sidebar.markdown("---")
st.sidebar.info(
    "💡 **Academic Reference**:\n"
    "Based on *Kenneth H. Rosen*, Discrete Mathematics and Its Applications (Chapter 3: Algorithms & Complexity)."
)


# ==========================================
# MODULE 1: DASHBOARD OVERVIEW
# ==========================================
if selected_page == "📊 Dashboard Overview":
    st.title("⚡ Algorithm Analysis & Visualization Platform")
    st.markdown(
        "An interactive environment for discrete algorithms exploration, step-by-step visual execution, "
        "asymptotic complexity modeling, and empirical benchmarking."
    )

    # Top KPI Metrics Cards
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-title">Implemented Algorithms</div>
                <div class="metric-val">10</div>
                <div class="metric-desc">Searching, Sorting, Greedy, Strings</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c2:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-title">Core Categories</div>
                <div class="metric-val">5</div>
                <div class="metric-desc">Fundamental & Applied Discrete Maths</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c3:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-title">Visual Execution Engine</div>
                <div class="metric-val">Interactive</div>
                <div class="metric-desc">Step-by-step with Play, Pause, Speed</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c4:
        st.markdown(
            """
            <div class="metric-card">
                <div class="metric-title">Empirical Benchmarks</div>
                <div class="metric-val">Sub-Millisecond</div>
                <div class="metric-desc">High-precision performance profiling</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### 🚀 Quick Navigation Links")
    qa_cols1 = st.columns(4)
    qa_cols1[0].button("🔍 Searching Visualizer", on_click=navigate_to, args=("🔍 Searching Algorithms",), use_container_width=True, key="qa_nav_search")
    qa_cols1[1].button("🔃 Sorting Visualizer", on_click=navigate_to, args=("🔃 Sorting Algorithms",), use_container_width=True, key="qa_nav_sort")
    qa_cols1[2].button("🔤 String Matching", on_click=navigate_to, args=("🔤 String Matching",), use_container_width=True, key="qa_nav_string")
    qa_cols1[3].button("⚡ Greedy Algorithms", on_click=navigate_to, args=("⚡ Greedy Algorithms",), use_container_width=True, key="qa_nav_greedy")

    qa_cols2 = st.columns(4)
    qa_cols2[0].button("📈 Complexity & Growth", on_click=navigate_to, args=("📈 Complexity & Growth",), use_container_width=True, key="qa_nav_growth")
    qa_cols2[1].button("🔬 Empirical Benchmarks", on_click=navigate_to, args=("🔬 Benchmarking Engine",), use_container_width=True, key="qa_nav_bench")
    qa_cols2[2].button("🧩 Supplementary Algos", on_click=navigate_to, args=("🧩 Supplementary Algorithms",), use_container_width=True, key="qa_nav_supp")
    qa_cols2[3].button("📖 Algorithm Fundamentals", on_click=navigate_to, args=("📖 Algorithm Fundamentals",), use_container_width=True, key="qa_nav_fund")

    st.markdown("---")

    col_left, col_right = st.columns([1.2, 1])

    with col_left:
        st.subheader("📋 Master Algorithm Complexity Matrix")
        df_meta = pd.DataFrame.from_dict(ALGORITHM_METADATA, orient="index").reset_index()
        df_meta.rename(columns={"index": "Algorithm"}, inplace=True)
        display_df = df_meta[
            ["Algorithm", "category", "best_time", "avg_time", "worst_time", "space", "in_place"]
        ].rename(
            columns={
                "category": "Category",
                "best_time": "Best Time",
                "avg_time": "Average Time",
                "worst_time": "Worst Time",
                "space": "Aux Space",
                "in_place": "In-Place",
            }
        )
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    with col_right:
        st.subheader("📊 Category Distribution")
        cat_counts = df_meta["category"].value_counts().reset_index()
        cat_counts.columns = ["Category", "Count"]
        fig_cat = px.pie(
            cat_counts,
            names="Category",
            values="Count",
            color_discrete_sequence=px.colors.qualitative.Pastel,
            hole=0.45,
        )
        fig_cat.update_layout(
            margin=dict(l=10, r=10, t=10, b=10),
            height=320,
            paper_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(fig_cat, use_container_width=True)

    # Sample Quick Benchmark Spotlight
    st.subheader("⚡ Quick Benchmark Spotlight (Sorting on n = 250 elements)")
    with st.spinner("Profiling sample benchmark..."):
        spotlight_df = benchmark_sorting_suite(
            algorithms=["Bubble Sort", "Insertion Sort", "Selection Sort", "Binary Insertion Sort"],
            sizes=[250],
            trials=2,
            seed=42,
        )
        c_spot1, c_spot2 = st.columns([1, 1])
        with c_spot1:
            fig_spot_time = px.bar(
                spotlight_df,
                x="Algorithm",
                y="Execution Time (ms)",
                color="Algorithm",
                title="Execution Time (ms) - Lower is Faster",
                text_auto=".2f",
            )
            fig_spot_time.update_layout(height=300, showlegend=False, margin=dict(t=30, b=20, l=10, r=10))
            st.plotly_chart(fig_spot_time, use_container_width=True)

        with c_spot2:
            fig_spot_ops = px.bar(
                spotlight_df,
                x="Algorithm",
                y="Comparisons",
                color="Algorithm",
                title="Number of Element Comparisons - Lower is More Efficient",
                text_auto=True,
            )
            fig_spot_ops.update_layout(height=300, showlegend=False, margin=dict(t=30, b=20, l=10, r=10))
            st.plotly_chart(fig_spot_ops, use_container_width=True)


# ==========================================
# MODULE 2: ALGORITHM FUNDAMENTALS
# ==========================================
elif selected_page == "📖 Algorithm Fundamentals":
    st.title("📖 Algorithm Fundamentals")
    st.markdown(
        "An algorithm is a finite sequence of unambiguous, well-defined instructions for solving a class of problems "
        "or performing a computation. In Discrete Mathematics (Rosen §3.1), every proper algorithm must satisfy essential formal properties."
    )

    t1, t2, t3 = st.tabs(["🏛️ Fundamental Properties", "🛡️ Correctness & Loop Invariants", "⚙️ Pseudocode Mechanics"])

    with t1:
        st.subheader("Seven Key Properties of Algorithms")
        props = [
            ("1. Input", "An algorithm has specified input values from a specified set of objects."),
            ("2. Output", "From each set of input values, an algorithm produces output values from a specified set of objects (the solution)."),
            ("3. Definiteness", "Each step of an algorithm must be precisely defined without ambiguity."),
            ("4. Correctness", "An algorithm should produce the correct output values for each set of valid input values."),
            ("5. Finiteness", "An algorithm must produce the desired output after a finite (though perhaps large) number of steps for any input in the set."),
            ("6. Effectiveness", "It must be possible to perform each step of an algorithm exactly and in a finite amount of time."),
            ("7. Generality", "The procedure must be applicable for all problems of the desired form, not just for a specific set of input values."),
        ]
        for name, desc in props:
            with st.expander(f"**{name}**", expanded=True):
                st.write(desc)

    with t2:
        st.subheader("Algorithm Correctness & Loop Invariants")
        st.markdown(
            """
            Proving that an algorithm is correct requires demonstrating that it yields the specified output for all valid inputs.
            For iterative algorithms containing loops, the standard technique is **Mathematical Induction via Loop Invariants**.
            
            A **Loop Invariant** is a predicate (condition) about program variables that is true before and after each iteration of a loop.
            """
        )
        st.info(
            """
            **The Three Invariant Obligations:**
            1. **Initialization:** The invariant is true prior to the first iteration of the loop (Base Case).
            2. **Maintenance:** If the invariant is true before an iteration of the loop, it remains true before the next iteration (Inductive Step).
            3. **Termination:** When the loop terminates, the invariant provides a useful property that helps prove the algorithm is correct.
            """
        )

        st.markdown("#### Example: Insertion Sort Loop Invariant")
        st.latex(
            r"\text{Invariant: At the start of each iteration } i, \text{ the subarray } A[0 \dots i-1] \text{ contains the original elements but in sorted order.}"
        )
        st.write(
            "- **Initialization**: At $i=1$, subarray $A[0..0]$ contains just 1 element, which is trivially sorted.\n"
            "- **Maintenance**: During iteration $i$, $A[i]$ is inserted into its proper place in $A[0..i-1]$, yielding sorted $A[0..i]$.\n"
            "- **Termination**: The loop ends when $i=n$. Hence, $A[0..n-1]$ contains all original elements in sorted order."
        )

    with t3:
        st.subheader("Standard Discrete Maths Pseudocode Conventions")
        st.code(
            """
procedure LinearSearch(x: integer, a1, a2, ..., an: distinct integers)
    i := 1
    while (i <= n and x != ai)
        i := i + 1
    if i <= n then location := i
    else location := 0
    return location
            """,
            language="pascal",
        )
        st.caption("Standard Rosen-style linear search specification.")


# ==========================================
# MODULE 3: SEARCHING ALGORITHMS
# ==========================================
elif selected_page == "🔍 Searching Algorithms":
    st.title("🔍 Searching Algorithms Visualizer")
    st.markdown(
        "Interactive step-by-step visual execution of **Linear Search** and **Binary Search**."
    )

    col_setup, col_controls = st.columns([1, 1.2])

    with col_setup:
        st.subheader("⚙️ Configuration")
        algo_choice = st.radio(
            "Select Algorithm",
            ["Linear Search", "Binary Search"],
            horizontal=True,
            key="search_algo_radio",
        )
        input_type = st.radio(
            "Input Method",
            ["Generate Random", "Manual Comma-separated"],
            horizontal=True,
            key="search_input_type_radio",
        )

        # Track algorithm switch to reset state cleanly
        if st.session_state.get("search_prev_algo") != algo_choice:
            st.session_state["search_prev_algo"] = algo_choice
            st.session_state["search_step_idx"] = 0
            if "search_array" in st.session_state and algo_choice == "Binary Search":
                st.session_state["search_array"] = sorted(st.session_state["search_array"])

        if "search_seed" not in st.session_state:
            st.session_state["search_seed"] = 42

        if input_type == "Generate Random":
            arr_size = st.slider("Array Size (n)", min_value=5, max_value=25, value=12, key="search_arr_size")
            if st.session_state.get("search_prev_size") != arr_size:
                st.session_state["search_prev_size"] = arr_size
                st.session_state["search_seed"] = int(time.time() * 1000) % 100000
                st.session_state["search_step_idx"] = 0

            # Re-seed button
            if st.button("🎲 Generate New Random Array", key="search_reseed_btn", use_container_width=True):
                st.session_state["search_seed"] = int(time.time() * 1000) % 100000
                st.session_state["search_step_idx"] = 0

            # Generate stable array
            if algo_choice == "Binary Search":
                st.caption("Note: Binary Search requires a sorted array; elements are generated in ascending order.")
                base_arr = sorted(generate_array(arr_size, distribution="Random", min_val=5, max_val=95, seed=st.session_state["search_seed"]))
            else:
                base_arr = generate_array(arr_size, distribution="Random", min_val=5, max_val=95, seed=st.session_state["search_seed"])

            st.session_state["search_array"] = base_arr
        else:
            custom_str = st.text_input("Enter comma-separated integers", value="12, 28, 35, 47, 59, 68, 74, 85, 92", key="search_custom_str")
            try:
                base_arr = parse_custom_array(custom_str)
                if algo_choice == "Binary Search":
                    base_arr.sort()
            except Exception:
                st.error("Invalid custom array format. Using default array.")
                base_arr = [10, 20, 30, 40, 50, 60]
            st.session_state["search_array"] = base_arr

        # Target selection with stable default
        if base_arr:
            default_target = base_arr[len(base_arr) // 2]
        else:
            default_target = 42

        if "search_target_val" not in st.session_state:
            st.session_state["search_target_val"] = int(default_target)

        target_val = st.number_input("Target Value to Find", value=int(default_target), step=1, key="search_target_num")
        if st.session_state.get("search_prev_target") != target_val:
            st.session_state["search_prev_target"] = target_val
            st.session_state["search_step_idx"] = 0

    # Precompute steps
    if algo_choice == "Linear Search":
        steps = linear_search_steps(base_arr, target_val)
    else:
        steps = binary_search_steps(base_arr, target_val)

    max_search_step = max(0, len(steps) - 1)
    if "search_step_idx" not in st.session_state:
        st.session_state["search_step_idx"] = 0
    st.session_state["search_step_idx"] = max(0, min(st.session_state["search_step_idx"], max_search_step))

    def set_search_step(val: int):
        st.session_state["search_step_idx"] = max(0, min(val, max_search_step))

    def step_search(delta: int):
        curr = st.session_state.get("search_step_idx", 0)
        st.session_state["search_step_idx"] = max(0, min(curr + delta, max_search_step))

    with col_controls:
        st.subheader("🕹️ Playback Controls")
        c_btn1, c_btn2, c_btn3, c_btn4 = st.columns(4)

        c_btn1.button("⏮️ Reset", on_click=set_search_step, args=(0,), use_container_width=True, key="btn_s_reset")
        c_btn2.button("◀️ Prev Step", on_click=step_search, args=(-1,), use_container_width=True, key="btn_s_prev")
        c_btn3.button("▶️ Next Step", on_click=step_search, args=(1,), use_container_width=True, key="btn_s_next")
        c_btn4.button("⏭️ Final Step", on_click=set_search_step, args=(max_search_step,), use_container_width=True, key="btn_s_final")

        st.slider(
            "Jump to Step",
            min_value=0,
            max_value=max_search_step,
            key="search_step_idx",
        )

        curr_step_idx = st.session_state["search_step_idx"]
        curr_step = steps[curr_step_idx]

        # Live Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("Current Step", f"{curr_step_idx} / {max_search_step}")
        m2.metric("Comparisons", curr_step.get("comparisons", 0))
        m3.metric("Status", curr_step.get("status", "in_progress").upper())

    # Step Description Banner
    st.markdown(
        f"""
        <div class="step-banner">
            <b>Step {curr_step_idx}:</b> {curr_step.get('description', '')}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Plotly Visualization
    fig_search = create_searching_bar_chart(
        curr_step, algo_type="Linear" if algo_choice == "Linear Search" else "Binary"
    )
    st.plotly_chart(fig_search, use_container_width=True)

    # Legend & Complexity explanation
    with st.expander("ℹ️ Visualization Legend & Complexity Analysis", expanded=True):
        col_l1, col_l2 = st.columns(2)
        with col_l1:
            st.markdown(
                r"""
                **Visual Color Codes:**
                - 🟦 **Blue / Light Blue**: Unsearched / Active interval $[low, high]$.
                - 🟨 **Amber**: Currently compared element.
                - 🟪 **Purple**: Binary Search Midpoint index $mid = \lfloor (low + high) / 2 \rfloor$.
                - 🟩 **Green**: Target element FOUND!
                - ⬜ **Grey**: Eliminated search interval.
                """
            )
        with col_l2:
            st.markdown(
                f"""
                **Theoretical Complexity ({algo_choice}):**
                - Best Case: $O(1)$ (Element at first checked index)
                - Average Case: ${ALGORITHM_METADATA[algo_choice]['avg_time']}$
                - Worst Case: ${ALGORITHM_METADATA[algo_choice]['worst_time']}$
                - Auxiliary Space: $O(1)$
                """
            )


# ==========================================
# MODULE 4: SORTING ALGORITHMS
# ==========================================
elif selected_page == "🔃 Sorting Algorithms":
    st.title("🔃 Sorting Algorithms Visualizer")
    st.markdown(
        "Interactive step-by-step visual execution of **Bubble Sort**, **Insertion Sort**, **Selection Sort**, "
        "and **Binary Insertion Sort**."
    )

    col_sort_setup, col_sort_ctrls = st.columns([1, 1.2])

    with col_sort_setup:
        st.subheader("⚙️ Configuration")
        algo_name = st.selectbox(
            "Select Sorting Algorithm",
            ["Bubble Sort", "Insertion Sort", "Selection Sort", "Binary Insertion Sort"],
            key="sort_algo_select",
        )

        input_mode = st.radio("Array Source", ["Generate Random", "Manual Input"], horizontal=True, key="sort_input_mode")

        # Track algorithm switch to reset state cleanly
        if st.session_state.get("sort_prev_algo") != algo_name:
            st.session_state["sort_prev_algo"] = algo_name
            st.session_state["sort_step_idx"] = 0

        if "sort_seed" not in st.session_state:
            st.session_state["sort_seed"] = 42

        if input_mode == "Generate Random":
            arr_len = st.slider("Array Size (n)", min_value=5, max_value=25, value=10, key="sort_arr_len")
            distrib = st.selectbox(
                "Distribution",
                ["Random", "Nearly Sorted", "Reverse Sorted", "Duplicates"],
                key="sort_distrib_select",
            )

            # Check if size or distribution changed
            if st.session_state.get("sort_prev_len") != arr_len or st.session_state.get("sort_prev_distrib") != distrib:
                st.session_state["sort_prev_len"] = arr_len
                st.session_state["sort_prev_distrib"] = distrib
                st.session_state["sort_seed"] = int(time.time() * 1000) % 100000
                st.session_state["sort_step_idx"] = 0

            # Re-seed button
            if st.button("🎲 Generate New Random Array", key="sort_reseed_btn", use_container_width=True):
                st.session_state["sort_seed"] = int(time.time() * 1000) % 100000
                st.session_state["sort_step_idx"] = 0

            seed = st.session_state.get("sort_seed", 42)
            arr_input = generate_array(arr_len, distribution=distrib, seed=seed)
            st.session_state["sort_array"] = arr_input
        else:
            custom_arr_text = st.text_input("Enter comma-separated numbers", value="29, 10, 14, 37, 13, 25, 8", key="sort_custom_input")
            try:
                arr_input = parse_custom_array(custom_arr_text)
            except Exception:
                st.error("Invalid array format.")
                arr_input = [5, 3, 8, 4, 2]
            st.session_state["sort_array"] = arr_input

    # Precompute step states
    if algo_name == "Bubble Sort":
        steps = bubble_sort_steps(arr_input)
    elif algo_name == "Insertion Sort":
        steps = insertion_sort_steps(arr_input)
    elif algo_name == "Selection Sort":
        steps = selection_sort_steps(arr_input)
    else:
        steps = binary_insertion_sort_steps(arr_input)

    max_sort_step = max(0, len(steps) - 1)
    if "sort_step_idx" not in st.session_state:
        st.session_state["sort_step_idx"] = 0
    st.session_state["sort_step_idx"] = max(0, min(st.session_state["sort_step_idx"], max_sort_step))

    def set_sort_step(val: int):
        st.session_state["sort_step_idx"] = max(0, min(val, max_sort_step))

    def step_sort(delta: int):
        curr = st.session_state.get("sort_step_idx", 0)
        st.session_state["sort_step_idx"] = max(0, min(curr + delta, max_sort_step))

    with col_sort_ctrls:
        st.subheader("🕹️ Playback Controls")
        sb1, sb2, sb3, sb4 = st.columns(4)

        sb1.button("⏮️ Reset", on_click=set_sort_step, args=(0,), key="sort_reset_btn", use_container_width=True)
        sb2.button("◀️ Prev Step", on_click=step_sort, args=(-1,), key="sort_prev_btn", use_container_width=True)
        sb3.button("▶️ Next Step", on_click=step_sort, args=(1,), key="sort_next_btn", use_container_width=True)
        sb4.button("⏭️ Final Step", on_click=set_sort_step, args=(max_sort_step,), key="sort_end_btn", use_container_width=True)

        st.slider(
            "Jump to Step",
            min_value=0,
            max_value=max_sort_step,
            key="sort_step_idx",
        )

        current_idx = st.session_state["sort_step_idx"]
        current_step = steps[current_idx]

        # Live Metrics
        sm1, sm2, sm3, sm4 = st.columns(4)
        sm1.metric("Step", f"{current_idx} / {max_sort_step}")
        sm2.metric("Comparisons", current_step.get("comparisons", 0))
        sm3.metric("Swaps / Shifts", current_step.get("swaps", current_step.get("shifts", 0)))
        sm4.metric("Sorted Items", f"{len(current_step.get('sorted_indices', []))} / {len(arr_input)}")

    # Step Description Banner
    st.markdown(
        f"""
        <div class="step-banner">
            <b>Step {current_idx}:</b> {current_step.get('description', '')}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Plotly Bar Chart
    fig_sort = create_sorting_bar_chart(current_step)
    st.plotly_chart(fig_sort, use_container_width=True)

    # Explanation and discrete math properties
    with st.expander(f"📚 {algo_name} Algorithm Properties & Complexity", expanded=True):
        meta = ALGORITHM_METADATA.get(algo_name, {})
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown(
                f"""
                - **Algorithm Family:** Comparison-based Exchange / Insertion / Selection
                - **Best-case Time:** ${meta.get('best_time', 'N/A')}$
                - **Average-case Time:** ${meta.get('avg_time', 'N/A')}$
                - **Worst-case Time:** ${meta.get('worst_time', 'N/A')}$
                - **Auxiliary Space:** ${meta.get('space', 'O(1)')}$ (In-place: {meta.get('in_place', True)})
                - **Stable Sort:** {meta.get('stable', 'Yes')}
                """
            )
        with col_m2:
            st.markdown(
                f"""
                **Discrete Mathematics Insight:**
                {meta.get('description', '')}
                
                **Color Legend:**
                - 🟦 **Blue**: Unsorted elements
                - 🟨 **Amber**: Actively compared elements
                - 🟥 **Red**: Swapped elements
                - 🟪 **Purple**: Active insertion key or minimum element
                - 🟩 **Green**: Elements locked in final sorted position
                """
            )


# ==========================================
# MODULE 5: STRING MATCHING
# ==========================================
elif selected_page == "🔤 String Matching":
    st.title("🔤 Naive String Matching Visualizer")
    st.markdown(
        r"The **Naive String-Matching Algorithm** finds all occurrences of a pattern $P[0 \dots m-1]$ within a text $T[0 \dots n-1]$ "
        r"by checking every possible shift $s \in [0, n - m]$."
    )

    col_sm_setup, col_sm_ctrls = st.columns([1, 1.2])

    with col_sm_setup:
        st.subheader("⚙️ Strings Setup")
        preset = st.selectbox(
            "Select Preset Example or Custom",
            [
                "Custom Strings",
                "Rosen Textbook Example (AABAACAADAABAABA)",
                "Discrete Mathematics (DISCRETE_MATH)",
                "Repeated Characters (AAAAAAAB)",
            ],
        )

        if preset == "Rosen Textbook Example (AABAACAADAABAABA)":
            default_text = "AABAACAADAABAABA"
            default_pattern = "AABA"
        elif preset == "Discrete Mathematics (DISCRETE_MATH)":
            default_text = "DISCRETE_MATHEMATICS_AND_ALGORITHMS"
            default_pattern = "MATH"
        elif preset == "Repeated Characters (AAAAAAAB)":
            default_text = "AAAAAAAAB"
            default_pattern = "AAAB"
        else:
            default_text = "ABCABCDABABCDABCDABDE"
            default_pattern = "ABCDABD"

        text_val = st.text_input("Text String (T)", value=default_text)
        pattern_val = st.text_input("Pattern String (P)", value=default_pattern)

    steps_sm = naive_string_match_steps(text_val, pattern_val)

    max_sm_step = max(0, len(steps_sm) - 1)
    if "sm_step_idx" not in st.session_state:
        st.session_state["sm_step_idx"] = 0
    st.session_state["sm_step_idx"] = max(0, min(st.session_state["sm_step_idx"], max_sm_step))

    def set_sm_step(val: int):
        st.session_state["sm_step_idx"] = max(0, min(val, max_sm_step))

    def step_sm(delta: int):
        curr = st.session_state.get("sm_step_idx", 0)
        st.session_state["sm_step_idx"] = max(0, min(curr + delta, max_sm_step))

    with col_sm_ctrls:
        st.subheader("🕹️ Playback Controls")
        sm_b1, sm_b2, sm_b3, sm_b4 = st.columns(4)

        sm_b1.button("⏮️ Reset", on_click=set_sm_step, args=(0,), key="sm_reset_btn", use_container_width=True)
        sm_b2.button("◀️ Prev Step", on_click=step_sm, args=(-1,), key="sm_prev_btn", use_container_width=True)
        sm_b3.button("▶️ Next Step", on_click=step_sm, args=(1,), key="sm_next_btn", use_container_width=True)
        sm_b4.button("⏭️ Final Step", on_click=set_sm_step, args=(max_sm_step,), key="sm_end_btn", use_container_width=True)

        st.slider(
            "Jump to Shift Step",
            min_value=0,
            max_value=max_sm_step,
            key="sm_step_idx",
        )

        curr_sm_idx = st.session_state["sm_step_idx"]
        curr_sm = steps_sm[curr_sm_idx]

        # Metrics
        smm1, smm2, smm3 = st.columns(3)
        smm1.metric("Current Shift (s)", curr_sm.get("shift", 0))
        smm2.metric("Comparisons", curr_sm.get("comparisons", 0))
        smm3.metric("Matches Found", len(curr_sm.get("matches_found", [])))

    st.markdown(
        f"""
        <div class="step-banner">
            <b>Step {curr_sm_idx}:</b> {curr_sm.get('description', '')}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Visual alignment grid of characters
    s = curr_sm.get("shift", 0)
    p_idx = curr_sm.get("pattern_idx", 0)
    t_idx = curr_sm.get("text_idx", 0)
    status = curr_sm.get("status", "")

    # Build interactive HTML alignment display
    html_grid = "<div style='overflow-x: auto; font-family: monospace; font-size: 1.15rem; line-height: 2.2rem; background: #F8FAFC; padding: 1.2rem; border-radius: 8px; border: 1px solid #CBD5E1;'>"
    html_grid += "<div style='font-weight: 700; color: #475569; margin-bottom: 0.2rem;'>INDEX &nbsp;: "
    for i in range(len(text_val)):
        html_grid += f"<span style='display:inline-block; width:30px; text-align:center; color:#94A3B8; font-size:0.8rem;'>{i}</span>"
    html_grid += "</div>"

    html_grid += "<div style='font-weight: 700; color: #1E293B;'>TEXT &nbsp; : "
    for i, ch in enumerate(text_val):
        bg = "#FFFFFF"
        color = "#0F172A"
        border = "1px solid #CBD5E1"

        if i in curr_sm.get("matches_found", []):
            bg = "#DCFCE7"  # Match start
        if i == t_idx and status in ["match_char", "mismatch"]:
            if status == "match_char":
                bg = "#10B981"
                color = "#FFFFFF"
            else:
                bg = "#EF4444"
                color = "#FFFFFF"

        html_grid += f"<span style='display:inline-block; width:30px; text-align:center; background:{bg}; color:{color}; border:{border}; border-radius:4px; margin-right:2px; font-weight:700;'>{ch}</span>"
    html_grid += "</div>"

    # Pattern row with leading spaces equal to shift s
    html_grid += f"<div style='font-weight: 700; color: #3B82F6; margin-top: 0.5rem;'>PATTERN: "
    for _ in range(s):
        html_grid += "<span style='display:inline-block; width:30px; margin-right:2px;'>&nbsp;</span>"

    for j, ch in enumerate(pattern_val):
        bg = "#EFF6FF"
        color = "#1D4ED8"
        border = "1px solid #93C5FD"

        if j == p_idx and status in ["match_char", "mismatch"]:
            if status == "match_char":
                bg = "#10B981"
                color = "#FFFFFF"
            else:
                bg = "#EF4444"
                color = "#FFFFFF"

        html_grid += f"<span style='display:inline-block; width:30px; text-align:center; background:{bg}; color:{color}; border:{border}; border-radius:4px; margin-right:2px; font-weight:700;'>{ch}</span>"

    html_grid += "</div></div>"
    st.markdown(html_grid, unsafe_allow_html=True)

    with st.expander("📚 Mathematical Complexity of Naive String Matching", expanded=True):
        st.markdown(
            r"""
            - **Text Length**: $n = |T|$, **Pattern Length**: $m = |P|$
            - **Number of possible shifts**: $n - m + 1$
            - **Character comparisons per shift**: Between $1$ (immediate mismatch) and $m$ (full match)
            - **Best-case Time**: $O(n)$ (When first character always mismatches)
            - **Worst-case Time**: $O((n - m + 1) \cdot m) = O(n \cdot m)$ (e.g. Text: `AAAAAAAAAA`, Pattern: `AAAB`)
            - **Auxiliary Space**: $O(1)$
            """
        )


# ==========================================
# MODULE 6: GREEDY ALGORITHMS
# ==========================================
elif selected_page == "⚡ Greedy Algorithms":
    st.title("⚡ Greedy Algorithms Visualizer")
    st.markdown(
        "A **greedy algorithm** makes the locally optimal choice at each stage with the hope of finding a global optimum. "
        "Here we explore **Cashier's Change Algorithm** and **Activity Selection / Interval Scheduling**."
    )

    t_greedy1, t_greedy2 = st.tabs(["💰 Cashier's Change-Making Algorithm", "📅 Activity Selection Scheduling"])

    # --- TAB 1: CASHIER'S ALGORITHM ---
    with t_greedy1:
        st.subheader("Cashier's Change-Making Algorithm (Rosen §3.1)")
        gc1, gc2 = st.columns([1, 1.2])

        with gc1:
            currency_preset = st.selectbox(
                "Currency System",
                [
                    "US Currency ($) — Standard Coins [Quarters ($0.25), Dimes ($0.10), Nickels ($0.05), Pennies ($0.01)]",
                    "US Currency ($) — Bills & Coins [$100, $50, $20, $10, $5, $1, $0.25, $0.10, $0.05, $0.01]",
                    "Indian Rupee (₹) — ₹500, ₹200, ₹100, ₹50, ₹20, ₹10, ₹5, ₹2, ₹1",
                    "Custom Denominations",
                ],
                key="greedy_currency_preset",
            )

            if currency_preset.startswith("US Currency ($) — Standard Coins"):
                currency_symbol = "$"
                is_cents = True
                denoms = [25, 10, 5, 1]
                denom_labels = {25: "$0.25 (Quarter)", 10: "$0.10 (Dime)", 5: "$0.05 (Nickel)", 1: "$0.01 (Penny)"}
                target_amount = st.number_input(
                    "Target Amount in Cents (¢)",
                    min_value=1,
                    max_value=5000,
                    value=67,
                    step=1,
                    key="greedy_amt_us_coins",
                    help="67 cents = $0.67 (classic Rosen Chapter 3 example)",
                )
                st.caption(f"💵 Dollar Equivalent: **${target_amount / 100:.2f}** ({target_amount} cents)")
            elif currency_preset.startswith("US Currency ($) — Bills"):
                currency_symbol = "$"
                is_cents = True
                denoms = [10000, 5000, 2000, 1000, 500, 100, 25, 10, 5, 1]
                denom_labels = {
                    10000: "$100 Bill",
                    5000: "$50 Bill",
                    2000: "$20 Bill",
                    1000: "$10 Bill",
                    500: "$5 Bill",
                    100: "$1 Bill",
                    25: "$0.25 (Quarter)",
                    10: "$0.10 (Dime)",
                    5: "$0.05 (Nickel)",
                    1: "$0.01 (Penny)",
                }
                target_amount = st.number_input(
                    "Target Amount in Cents (¢)",
                    min_value=1,
                    max_value=1000000,
                    value=287,
                    step=1,
                    key="greedy_amt_us_bills",
                    help="287 cents = $2.87 ($2 Bill/2x$1 + 3 Quarters + 1 Dime + 2 Pennies)",
                )
                st.caption(f"💵 Dollar Equivalent: **${target_amount / 100:.2f}**")
            elif currency_preset.startswith("Indian"):
                currency_symbol = "₹"
                is_cents = False
                denoms = [500, 200, 100, 50, 20, 10, 5, 2, 1]
                denom_labels = {c: f"₹{c}" for c in denoms}
                target_amount = st.number_input("Target Amount (₹)", min_value=1, max_value=50000, value=388, step=1, key="greedy_amt_inr")
            else:
                currency_symbol = st.text_input("Currency Symbol", value="$", key="greedy_custom_sym")
                is_cents = False
                cust_denoms = st.text_input("Enter comma-separated denominations (descending)", value="50, 20, 10, 5, 1", key="greedy_custom_denoms")
                try:
                    denoms = parse_custom_array(cust_denoms)
                except Exception:
                    denoms = [25, 10, 5, 1]
                denom_labels = {c: f"{currency_symbol}{c}" for c in denoms}
                target_amount = st.number_input("Target Amount", min_value=1, max_value=10000, value=73, step=1, key="greedy_amt_custom")

        # Steps calculation
        steps_cashier = cashiers_algorithm_steps(
            target_amount,
            denominations=denoms,
            currency_symbol=currency_symbol,
            denom_labels=denom_labels,
            is_cents=is_cents,
        )

        max_cashier_step = max(0, len(steps_cashier) - 1)
        if "cashier_step_idx" not in st.session_state:
            st.session_state["cashier_step_idx"] = 0
        st.session_state["cashier_step_idx"] = max(0, min(st.session_state["cashier_step_idx"], max_cashier_step))

        def set_cashier_step(val: int):
            st.session_state["cashier_step_idx"] = max(0, min(val, max_cashier_step))

        def step_cashier(delta: int):
            curr = st.session_state.get("cashier_step_idx", 0)
            st.session_state["cashier_step_idx"] = max(0, min(curr + delta, max_cashier_step))

        with gc2:
            st.subheader("🕹️ Step-by-Step Playback Controls")
            cb1, cb2, cb3, cb4 = st.columns(4)
            cb1.button("⏮️ Reset", on_click=set_cashier_step, args=(0,), key="cashier_btn_reset", use_container_width=True)
            cb2.button("◀️ Prev Step", on_click=step_cashier, args=(-1,), key="cashier_btn_prev", use_container_width=True)
            cb3.button("▶️ Next Step", on_click=step_cashier, args=(1,), key="cashier_btn_next", use_container_width=True)
            cb4.button("⏭️ Final Step", on_click=set_cashier_step, args=(max_cashier_step,), key="cashier_btn_final", use_container_width=True)

            st.slider(
                "Jump to Step",
                min_value=0,
                max_value=max_cashier_step,
                key="cashier_step_idx",
            )

            curr_c_idx = st.session_state["cashier_step_idx"]
            curr_c_step = steps_cashier[curr_c_idx]

            # Live Metrics
            cm1, cm2, cm3 = st.columns(3)
            cm1.metric("Current Step", f"{curr_c_idx} / {max_cashier_step}")
            cm2.metric("Coins Used So Far", curr_c_step.get("total_coins", 0))
            if currency_symbol == "$" and is_cents:
                cm3.metric("Remaining Balance", f"${curr_c_step.get('remaining', 0) / 100:.2f}")
            else:
                cm3.metric("Remaining Balance", f"{currency_symbol}{curr_c_step.get('remaining', 0)}")

        # Step Description Banner
        st.markdown(
            f"""
            <div class="step-banner">
                <b>Step {curr_c_idx}:</b> {curr_c_step.get('description', '')}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Plotly Bar Chart
        fig_cashier = create_cashier_bar_chart(
            curr_c_step,
            denominations=denoms,
            currency_symbol=currency_symbol,
            denom_labels=denom_labels,
            is_cents=is_cents,
        )
        st.plotly_chart(fig_cashier, use_container_width=True)

        # Summary Table
        final_step = steps_cashier[-1]
        coins_used_dict = final_step.get("coins_used", {})
        table_rows = []
        for k in denoms:
            v = coins_used_dict.get(k, 0)
            if v > 0:
                lbl = denom_labels.get(k, f"{currency_symbol}{k}")
                if currency_symbol == "$" and is_cents:
                    subtotal_str = f"${(k * v) / 100:.2f}"
                    denom_str = f"${k / 100:.2f}"
                else:
                    subtotal_str = f"{currency_symbol}{k * v}"
                    denom_str = f"{currency_symbol}{k}"
                table_rows.append({
                    "Denomination": denom_str,
                    "Unit Name": lbl,
                    "Coins Used": v,
                    "Subtotal": subtotal_str,
                })

        st.subheader("📋 Final Greedy Coin Allocation Table")
        if table_rows:
            st.dataframe(pd.DataFrame(table_rows), use_container_width=True, hide_index=True)
        else:
            st.info("Amount is 0; no coins needed.")

        with st.expander("ℹ️ Optimality & Canonical Systems Note", expanded=False):
            st.markdown(
                """
                **When does the Greedy Cashier's algorithm work?**
                The cashier's algorithm is provably optimal (minimizes total coins) for **canonical coin systems** 
                (such as US currency `[25, 10, 5, 1]` and European/Indian currency systems).
                
                However, for arbitrary denominations like `[25, 20, 10, 5, 1]`, to make change for `40`:
                - Greedy takes: `25 + 10 + 5` = 3 coins.
                - Dynamic Programming / Optimal is: `20 + 20` = 2 coins!
                """
            )

    # --- TAB 2: ACTIVITY SELECTION ---
    with t_greedy2:
        st.subheader("Activity Selection / Interval Scheduling (Earliest Finish Time First)")
        st.markdown(
            "Given a set of $n$ activities with start and finish times $[s_i, f_i)$, schedule the maximum number of mutually compatible activities."
        )

        preset_acts = st.selectbox(
            "Select Scenario",
            [
                "Classic Rosen Textbook Example (11 Activities)",
                "Classroom Lecture Hall Scheduling",
                "Custom Interval Set",
            ],
        )

        if preset_acts.startswith("Classic"):
            acts_input = [
                {"id": 1, "start": 1, "finish": 4},
                {"id": 2, "start": 3, "finish": 5},
                {"id": 3, "start": 0, "finish": 6},
                {"id": 4, "start": 5, "finish": 7},
                {"id": 5, "start": 3, "finish": 9},
                {"id": 6, "start": 5, "finish": 9},
                {"id": 7, "start": 6, "finish": 10},
                {"id": 8, "start": 8, "finish": 11},
                {"id": 9, "start": 8, "finish": 12},
                {"id": 10, "start": 2, "finish": 14},
                {"id": 11, "start": 12, "finish": 16},
            ]
        elif preset_acts.startswith("Classroom"):
            acts_input = [
                {"id": "CS101", "start": 9, "finish": 11},
                {"id": "MA201", "start": 10, "finish": 12},
                {"id": "EC102", "start": 11, "finish": 13},
                {"id": "HS101", "start": 12, "finish": 14},
                {"id": "CS204", "start": 13, "finish": 15},
                {"id": "PH101", "start": 14, "finish": 16},
            ]
        else:
            acts_input = [
                {"id": "A", "start": 1, "finish": 3},
                {"id": "B", "start": 2, "finish": 5},
                {"id": "C", "start": 4, "finish": 7},
                {"id": "D", "start": 6, "finish": 9},
            ]

        steps_act = activity_selection_steps(acts_input)
        max_act_step = max(0, len(steps_act) - 1)
        if "act_step_idx" not in st.session_state:
            st.session_state["act_step_idx"] = 0
        st.session_state["act_step_idx"] = max(0, min(st.session_state["act_step_idx"], max_act_step))

        def set_act_step(val: int):
            st.session_state["act_step_idx"] = max(0, min(val, max_act_step))

        def step_act(delta: int):
            curr = st.session_state.get("act_step_idx", 0)
            st.session_state["act_step_idx"] = max(0, min(curr + delta, max_act_step))

        act_b1, act_b2, act_b3, act_b4 = st.columns(4)
        act_b1.button("⏮️ Reset", on_click=set_act_step, args=(0,), key="act_reset_btn", use_container_width=True)
        act_b2.button("◀️ Prev Step", on_click=step_act, args=(-1,), key="act_prev_btn", use_container_width=True)
        act_b3.button("▶️ Next Step", on_click=step_act, args=(1,), key="act_next_btn", use_container_width=True)
        act_b4.button("⏭️ Final Step", on_click=set_act_step, args=(max_act_step,), key="act_end_btn", use_container_width=True)

        st.slider(
            "Jump to Scheduling Step",
            min_value=0,
            max_value=max_act_step,
            key="act_step_idx",
        )

        curr_act_idx = st.session_state["act_step_idx"]
        curr_act_step = steps_act[curr_act_idx]

        st.markdown(
            f"""
            <div class="step-banner">
                <b>Step {curr_act_idx}:</b> {curr_act_step.get('description', '')}
            </div>
            """,
            unsafe_allow_html=True,
        )

        fig_act = create_activity_timeline_chart(
            activities=curr_act_step.get("activities", acts_input),
            selected_ids=curr_act_step.get("selected_ids", []),
            current_idx=curr_act_step.get("current_idx"),
        )
        st.plotly_chart(fig_act, use_container_width=True)

        st.markdown(
            f"**Selected Compatible Activities ({len(curr_act_step.get('selected_ids', []))}):** "
            f"`{curr_act_step.get('selected_ids', [])}`"
        )


# ==========================================
# MODULE 7: COMPLEXITY & GROWTH
# ==========================================
elif selected_page == "📈 Complexity & Growth":
    st.title("📈 Asymptotic Complexity & Growth Analyzer")
    st.markdown(
        r"Explore asymptotic notations ($O$, $\Omega$, $\Theta$, $o$) and compare theoretical growth rates interactively."
    )

    t_c1, t_c2 = st.tabs(["📐 Asymptotic Growth Curves", "📖 Formal Definitions & Notations"])

    with t_c1:
        st.subheader("Interactive Growth Comparison")
        c_opts1, c_opts2 = st.columns([1, 1])

        with c_opts1:
            chosen_classes = st.multiselect(
                "Select Complexity Functions to Compare",
                options=list(COMPLEXITY_CLASSES.keys()),
                default=[
                    "Constant: O(1)",
                    "Logarithmic: O(log n)",
                    "Linear: O(n)",
                    "Linearithmic: O(n log n)",
                    "Quadratic: O(n²)",
                ],
            )
        with c_opts2:
            max_input_n = st.slider("Max Input Size (n)", min_value=10, max_value=100, value=40)
            use_log_scale = st.checkbox("Use Logarithmic Y-axis (useful for exponential / cubic growth)", value=False)

        fig_growth = create_growth_chart(
            selected_classes=chosen_classes,
            max_n=max_input_n,
            log_scale=use_log_scale,
        )
        st.plotly_chart(fig_growth, use_container_width=True)

        st.markdown("### Complexity Class Summary Cheat-Sheet")
        classes_summary = []
        for name, d in COMPLEXITY_CLASSES.items():
            classes_summary.append({"Complexity Class": name, "LaTeX Formula": d["latex"], "Typical Algorithms / Operations": d["note"]})
        st.dataframe(pd.DataFrame(classes_summary), use_container_width=True, hide_index=True)

    with t_c2:
        st.subheader("Formal Definitions of Asymptotic Notations")
        for title, info in ASYMPTOTIC_NOTATIONS.items():
            with st.expander(f"**{title}** — {info['symbol']}", expanded=True):
                st.latex(info["formal_definition"])
                st.markdown(f"**Significance:** {info['meaning']}")
                st.markdown(f"**Examples:** *{info['example']}*")


# ==========================================
# MODULE 8: BENCHMARKING ENGINE
# ==========================================
elif selected_page == "🔬 Benchmarking Engine":
    st.title("🔬 Empirical Benchmarking Engine")
    st.markdown(
        "Run real-time performance benchmarks across algorithms on identical datasets. "
        "Distinguish **empirical measurements** (clock time, cache misses, Python runtime) from **theoretical asymptotic complexity**."
    )

    st.warning(
        "⚠️ **Measurement Disclaimer**: Measured execution times depend on hardware CPU architecture, background OS tasks, "
        "and Python interpreter overhead. Operation counts (comparisons & swaps) provide invariant empirical metrics."
    )

    bench_tab1, bench_tab2 = st.tabs(["🔃 Sorting Suite Benchmarks", "🔍 Searching Suite Benchmarks"])

    with bench_tab1:
        st.subheader("Sorting Algorithms Comparative Profiler")
        b_c1, b_c2, b_c3 = st.columns(3)

        with b_c1:
            selected_algos = st.multiselect(
                "Algorithms to Profile",
                options=list(SORTING_ALGORITHMS.keys()),
                default=["Bubble Sort", "Insertion Sort", "Selection Sort", "Binary Insertion Sort"],
            )

        with b_c2:
            test_sizes = st.multiselect(
                "Input Sizes (n)",
                options=[25, 50, 100, 200, 400, 600, 800, 1000],
                default=[50, 100, 200, 400],
            )

        with b_c3:
            dist_choice = st.selectbox(
                "Input Dataset Distribution",
                ["Random", "Sorted", "Reverse Sorted", "Nearly Sorted", "Duplicates"],
            )
            trials_count = st.slider("Averaging Trials", min_value=1, max_value=5, value=3)

        if st.button("🚀 Run Sorting Benchmark", use_container_width=True):
            if not selected_algos or not test_sizes:
                st.error("Please select at least one algorithm and one input size.")
            else:
                with st.spinner("Benchmarking in progress..."):
                    bench_df = benchmark_sorting_suite(
                        algorithms=selected_algos,
                        sizes=sorted(test_sizes),
                        distribution=dist_choice,
                        trials=trials_count,
                    )
                    st.session_state["last_sorting_bench"] = bench_df

        if "last_sorting_bench" in st.session_state:
            bench_df = st.session_state["last_sorting_bench"]
            st.markdown("### 📊 Benchmark Visualizations")
            col_bchart1, col_bchart2 = st.columns(2)

            with col_bchart1:
                fig_time = create_benchmark_time_chart(bench_df)
                st.plotly_chart(fig_time, use_container_width=True)

            with col_bchart2:
                fig_ops = create_benchmark_ops_chart(bench_df, metric="Comparisons")
                st.plotly_chart(fig_ops, use_container_width=True)

            st.markdown("### 📋 Detailed Benchmark Results Table")
            st.dataframe(bench_df, use_container_width=True, hide_index=True)

            # CSV Download
            csv_data = bench_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Download Results as CSV",
                data=csv_data,
                file_name="sorting_benchmark_results.csv",
                mime="text/csv",
            )

    with bench_tab2:
        st.subheader("Searching Algorithms Profiler (Linear vs Binary)")
        search_sizes = st.multiselect(
            "Array Sizes (n) for Search Profiling",
            options=[100, 500, 1000, 2000, 5000, 10000, 25000, 50000],
            default=[500, 2000, 10000, 25000],
        )

        if st.button("🚀 Run Searching Benchmark", use_container_width=True):
            if not search_sizes:
                st.error("Please select at least one array size.")
            else:
                with st.spinner("Profiling search algorithms..."):
                    search_df = benchmark_searching_suite(sizes=sorted(search_sizes))
                    st.session_state["last_searching_bench"] = search_df

        if "last_searching_bench" in st.session_state:
            search_df = st.session_state["last_searching_bench"]
            s_c1, s_c2 = st.columns(2)
            with s_c1:
                fig_s_time = px.line(
                    search_df,
                    x="Input Size (n)",
                    y="Execution Time (ms)",
                    color="Algorithm",
                    markers=True,
                    title="Search Execution Time vs Input Size (ms)",
                )
                fig_s_time.update_layout(height=400)
                st.plotly_chart(fig_s_time, use_container_width=True)

            with s_c2:
                fig_s_comps = px.bar(
                    search_df,
                    x="Input Size (n)",
                    y="Comparisons",
                    color="Algorithm",
                    barmode="group",
                    title="Number of Element Comparisons",
                )
                fig_s_comps.update_layout(height=400)
                st.plotly_chart(fig_s_comps, use_container_width=True)

            st.dataframe(search_df, use_container_width=True, hide_index=True)


# ==========================================
# MODULE 9: SUPPLEMENTARY ALGORITHMS
# ==========================================
elif selected_page == "🧩 Supplementary Algorithms":
    st.title("🧩 Supplementary Discrete Algorithms")
    st.markdown(
        "Exploration of specialized discrete algorithms: **Boyer-Moore Majority Vote** and **Gale-Shapley Stable Matching**."
    )

    t_sup1, t_sup2 = st.tabs(["🗳️ Boyer-Moore Majority Vote", "🤝 Gale-Shapley Stable Matching"])

    # --- TAB 1: BOYER-MOORE MAJORITY VOTE ---
    with t_sup1:
        st.subheader("Boyer-Moore Majority Vote Algorithm")
        st.markdown(
            r"Finds the majority element in an array (an element that occurs strictly more than $\lfloor n/2 \rfloor$ times) "
            r"in strictly **$O(n)$ time** and **$O(1)$ auxiliary space** using a streaming counter."
        )

        vote_preset = st.selectbox(
            "Vote Stream Preset",
            [
                "Clear Majority: [2, 2, 1, 1, 1, 2, 2] (Candidate '2')",
                "Letter Votes: ['A', 'A', 'B', 'C', 'A', 'A'] (Candidate 'A')",
                "No Majority: [1, 2, 3, 4, 5, 2]",
                "Custom Array",
            ],
        )
        if vote_preset.startswith("Clear"):
            stream_arr = [2, 2, 1, 1, 1, 2, 2]
        elif vote_preset.startswith("Letter"):
            stream_arr = ["A", "A", "B", "C", "A", "A"]
        elif vote_preset.startswith("No"):
            stream_arr = [1, 2, 3, 4, 5, 2]
        else:
            cust_stream = st.text_input("Enter comma-separated items", value="7, 7, 3, 7, 2, 7, 5, 7")
            stream_arr = [x.strip() for x in cust_stream.split(",") if x.strip()]

        steps_vote = boyer_moore_majority_steps(stream_arr)
        max_vote_step = max(0, len(steps_vote) - 1)
        if "vote_step_idx" not in st.session_state:
            st.session_state["vote_step_idx"] = 0
        st.session_state["vote_step_idx"] = max(0, min(st.session_state["vote_step_idx"], max_vote_step))

        def set_vote_step(val: int):
            st.session_state["vote_step_idx"] = max(0, min(val, max_vote_step))

        def step_vote(delta: int):
            curr = st.session_state.get("vote_step_idx", 0)
            st.session_state["vote_step_idx"] = max(0, min(curr + delta, max_vote_step))

        vb1, vb2, vb3, vb4 = st.columns(4)
        vb1.button("⏮️ Reset", on_click=set_vote_step, args=(0,), key="v_reset_btn", use_container_width=True)
        vb2.button("◀️ Prev Step", on_click=step_vote, args=(-1,), key="v_prev_btn", use_container_width=True)
        vb3.button("▶️ Next Step", on_click=step_vote, args=(1,), key="v_next_btn", use_container_width=True)
        vb4.button("⏭️ Final Step", on_click=set_vote_step, args=(max_vote_step,), key="v_end_btn", use_container_width=True)

        st.slider(
            "Jump to Streaming Step",
            min_value=0,
            max_value=max_vote_step,
            key="vote_step_idx",
        )

        curr_vote_idx = st.session_state["vote_step_idx"]
        curr_v = steps_vote[curr_vote_idx]

        st.markdown(
            f"""
            <div class="step-banner">
                <b>Step {curr_vote_idx} (Phase {curr_v.get('phase', 1)}):</b> {curr_v.get('description', '')}
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Metrics
        vm1, vm2, vm3, vm4 = st.columns(4)
        vm1.metric("Phase", f"Phase {curr_v.get('phase', 1)}")
        vm2.metric("Active Candidate", str(curr_v.get("candidate", "None")))
        vm3.metric("Counter", curr_v.get("count", 0))
        vm4.metric("Verification Count", curr_v.get("actual_count", "Pending"))

    # --- TAB 2: GALE-SHAPLEY STABLE MATCHING ---
    with t_sup2:
        st.subheader("Gale-Shapley Stable Marriage / Matching Algorithm")
        st.markdown(
            "Solves the stable marriage problem: given $n$ men and $n$ women, each with a ranked preference list of the opposite sex, "
            "pair them up such that there is **no blocking pair** (two individuals of opposite sex who both prefer each other over their current partners)."
        )

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown("**Men Preference Lists (Proposers)**")
            men_prefs = {
                "Arthur": ["Beth", "Alice", "Carol"],
                "Ben": ["Alice", "Beth", "Carol"],
                "Charlie": ["Beth", "Carol", "Alice"],
            }
            st.json(men_prefs)

        with col_g2:
            st.markdown("**Women Preference Lists (Receivers)**")
            women_prefs = {
                "Alice": ["Arthur", "Ben", "Charlie"],
                "Beth": ["Ben", "Arthur", "Charlie"],
                "Carol": ["Arthur", "Charlie", "Ben"],
            }
            st.json(women_prefs)

        steps_gs = gale_shapley_steps(men_prefs, women_prefs)
        max_gs_step = max(0, len(steps_gs) - 1)
        if "gs_step_idx" not in st.session_state:
            st.session_state["gs_step_idx"] = 0
        st.session_state["gs_step_idx"] = max(0, min(st.session_state["gs_step_idx"], max_gs_step))

        def set_gs_step(val: int):
            st.session_state["gs_step_idx"] = max(0, min(val, max_gs_step))

        def step_gs(delta: int):
            curr = st.session_state.get("gs_step_idx", 0)
            st.session_state["gs_step_idx"] = max(0, min(curr + delta, max_gs_step))

        gs_b1, gs_b2, gs_b3, gs_b4 = st.columns(4)
        gs_b1.button("⏮️ Reset", on_click=set_gs_step, args=(0,), key="gs_reset_btn", use_container_width=True)
        gs_b2.button("◀️ Prev Step", on_click=step_gs, args=(-1,), key="gs_prev_btn", use_container_width=True)
        gs_b3.button("▶️ Next Step", on_click=step_gs, args=(1,), key="gs_next_btn", use_container_width=True)
        gs_b4.button("⏭️ Final Step", on_click=set_gs_step, args=(max_gs_step,), key="gs_end_btn", use_container_width=True)

        st.slider(
            "Jump to Engagement Step",
            min_value=0,
            max_value=max_gs_step,
            key="gs_step_idx",
        )

        curr_gs_idx = st.session_state["gs_step_idx"]
        curr_gs = steps_gs[curr_gs_idx]

        st.markdown(
            f"""
            <div class="step-banner">
                <b>Step {curr_gs_idx}:</b> {curr_gs.get('description', '')}
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("### Current Engagements State")
        eng_data = curr_gs.get("engagements", {})
        if eng_data:
            eng_df = pd.DataFrame([{"Receiver (Woman)": w, "Partner (Man)": m} for w, m in eng_data.items()])
            st.dataframe(eng_df, use_container_width=True, hide_index=True)
        else:
            st.info("No engagements formed yet. Proposers are currently free.")
