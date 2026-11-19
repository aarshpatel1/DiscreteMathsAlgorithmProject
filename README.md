# ⚡ Algorithm Analysis & Visualization Platform

> **Interactive learning, algorithm execution, complexity analysis, and performance benchmarking.**  
> *Developed for Discrete Mathematics & Algorithmics (DA-IICT / Kenneth H. Rosen Discrete Mathematics Curriculum).*

---

## 🎯 Project Overview

The **Algorithm Analysis & Visualization Platform** is an interactive, browser-based educational and benchmarking platform designed to bridge the gap between theoretical algorithm analysis (asymptotic bounds, invariants, correctness proofs) and empirical execution behavior (comparisons, memory shifts, clock time, dataset distribution sensitivity).

Built in **Python** using **Streamlit** and **Plotly**, the platform provides granular, step-by-step visual execution with state navigation, interactive mathematical growth models, and a high-precision benchmarking suite.

---

## 🏗️ Project Architecture & Directory Structure

```
Algorithm_Analysis_Project/
│
├── Dashboard/
│   ├── app.py                      # Main Streamlit dashboard application
│   ├── requirements.txt            # Python dependencies (Streamlit, Plotly, Pandas, NumPy, Pytest)
│   │
│   ├── algorithms/                 # Reusable pure algorithm engines & step generators
│   │   ├── __init__.py
│   │   ├── searching.py            # Linear Search & Binary Search
│   │   ├── sorting.py              # Bubble, Insertion, Selection, Binary Insertion Sort
│   │   ├── string_matching.py      # Naive String Matching
│   │   ├── greedy.py               # Cashier's Change & Activity Scheduling
│   │   ├── majority_vote.py        # Boyer-Moore Majority Vote
│   │   └── stable_matching.py      # Gale-Shapley Stable Matching
│   │
│   ├── visualizations/             # Plotly rendering and interactive charts
│   │   ├── __init__.py
│   │   ├── sorting_visualizer.py   # State-driven sorting bar charts
│   │   ├── searching_visualizer.py # Searching visualizer with pointers & interval elimination
│   │   └── complexity_charts.py    # Asymptotic growth curves & Gantt scheduling timelines
│   │
│   ├── analysis/                   # Complexity modeling & profiling engine
│   │   ├── __init__.py
│   │   ├── complexity.py           # Theoretical complexity metadata & asymptotic definitions
│   │   └── benchmarking.py         # Multi-trial timer & operation counter
│   │
│   ├── utils/                      # Dataset generation utilities
│   │   ├── __init__.py
│   │   └── data_generator.py       # Random, sorted, reverse, nearly sorted, duplicates distributions
│   │
│   └── tests/                      # Automated Pytest validation suite
│       ├── test_algorithms.py      # Correctness & step verification
│       └── test_analysis.py        # Complexity & benchmarking tests
│
└── README.md                       # Comprehensive platform documentation
```

---

## 🧩 Implemented Modules & Features

### 1. 📊 Dashboard Overview
- **Metrics Bar**: Implemented algorithms count (10), categories count (5), visualizer engine status, and microsecond precision badge.
- **Master Complexity Matrix**: Consolidated interactive table detailing Best, Average, Worst Time Complexity, Auxiliary Space, Stability, and In-Place attributes for all algorithms.
- **Category Breakdown**: Interactive donut chart.
- **Quick Benchmark Spotlight**: Real-time sample profiling on $n = 250$ comparing sorting times and comparison counts.
- **Quick Jump Links**: Instant navigation to any visualizer.

### 2. 📖 Algorithm Fundamentals
- **Seven Formal Algorithm Properties** (Rosen §3.1): Input, Output, Definiteness, Correctness, Finiteness, Effectiveness, Generality.
- **Loop Invariants & Mathematical Induction**: Three core obligations (Initialization, Maintenance, Termination) with formal proofs (e.g. Insertion Sort invariant).
- **Discrete Maths Pseudocode Mechanics**: Standard notation for algorithmic specifications.

### 3. 🔍 Searching Algorithms Visualizer
- **Algorithms**: Linear Search ($O(n)$) and Binary Search ($O(\log n)$).
- **Controls**: Array size slider, Random generation, Manual comma-separated input, Target element selector.
- **Step-by-Step Playback**: Reset, Previous Step, Next Step, Final Step, Direct Step Slider.
- **Visuals**: Dynamic Plotly bar chart with pointer arrows (`LOW ▲`, `MID ▲`, `HIGH ▲`), active search interval highlight, eliminated elements greyed out, and green target match indicator.

### 4. 🔃 Sorting Algorithms Visualizer
- **Algorithms**:
  - **Bubble Sort**: Adjacent element comparison and bubble-up with early termination flag.
  - **Insertion Sort**: Subarray insertion with right-shifts.
  - **Selection Sort**: Unsorted minimum search and boundary swap.
  - **Binary Insertion Sort**: $O(\log n)$ binary search position locator with $O(n^2)$ shifts.
- **Data Distributions**: Random, Nearly Sorted (8% perturbations), Reverse Sorted, Many Duplicates.
- **Color Coding**:
  - 🟦 Blue: Unsorted elements
  - 🟨 Amber: Elements currently compared
  - 🟥 Red: Elements swapped / shifted
  - 🟪 Purple: Active insertion key / minimum index
  - 🟩 Green: Locked in sorted position

### 5. 🔤 String Matching Visualizer
- **Algorithm**: Naive String Matching algorithm ($O(n \cdot m)$ worst case).
- **Presets**: Rosen textbook example (`AABAACAADAABAABA`), Discrete Mathematics, Repeated character strings, Custom inputs.
- **Interactive Matrix Grid**: Two-tier monospace visualizer displaying Text index, Text character cells, and Pattern character cells sliding by shift $s$, highlighting matching vs mismatching characters in real time.

### 6. ⚡ Greedy Algorithms
- **Cashier's Change-Making Algorithm (Rosen §3.1)**:
  - Systems supported:
    - **US Currency ($)**: Standard coins (Quarters `$0.25`, Dimes `$0.10`, Nickels `$0.05`, Pennies `$0.01`) and Bills & Coins (`$100`, `$50`, `$20`, `$10`, `$5`, `$1`, `$0.25`, `$0.10`, `$0.05`, `$0.01`).
    - **Indian Rupee (₹)**: `₹500`, `₹200`, `₹100`, `₹50`, `₹20`, `₹10`, `₹5`, `₹2`, `₹1`.
    - **Custom Denominations**: User-defined descending currency systems.
  - Interactive step-by-step playback with synced slider, decision step banner, and Plotly coin allocation bar chart.
  - Final breakdown table with `$`/`₹` formatted denominations, coin counts, and subtotals.
  - Direct alignment with Kenneth H. Rosen Chapter 3 & `Algorithm_Analysis.ipynb` (e.g. 67 cents = `$0.67` resulting in 2 Quarters, 1 Dime, 1 Nickel, 2 Pennies = 6 coins).
  - Theoretical note on **canonical coin systems** vs arbitrary non-canonical systems.
- **Activity Selection (Interval Scheduling)**:
  - Strategy: Earliest Finish Time First ($O(n \log n)$).
  - Presets: Rosen textbook 11-activity instance, classroom scheduling, custom intervals.
  - Interactive step-by-step slider navigation and Plotly Gantt / Horizontal Timeline chart showing accepted vs rejected tasks.

### 7. 📈 Complexity & Growth Analyzer
- **Interactive Asymptotic Growth Curves**: Toggle and overlay $O(1)$, $O(\log n)$, $O(n)$, $O(n \log n)$, $O(n^2)$, $O(n^3)$, and $O(2^n)$.
- **Customizable Scales**: Linear and Logarithmic Y-axis toggles with $n \in [10, 100]$.
- **Mathematical Formulations**: LaTeX definitions of Big-$O$, Big-$\Omega$, Big-$\Theta$, and Little-$o$.

### 8. 🔬 Empirical Benchmarking Engine
- **Fair Testing Architecture**: All selected algorithms execute against the exact same seed-generated array.
- **Metrics Collected**:
  - Execution Time in milliseconds (`time.perf_counter()` over $k$ averaging trials).
  - Number of Element Comparisons.
  - Number of Swaps / Shifts.
- **Dual Profilers**:
  - Sorting Suite: Bubble vs Insertion vs Selection vs Binary Insertion.
  - Searching Suite: Linear Search vs Binary Search up to $n = 50,000$.
- **Exporting**: One-click **Download Results as CSV**.
- **Scientific Clarification**: Clear distinction between empirical hardware/interpreter clock time and invariant asymptotic operation counts.

### 9. 🧩 Supplementary Discrete Algorithms
- **Boyer-Moore Majority Vote Algorithm**:
  - Streaming $O(n)$ time and $O(1)$ space algorithm.
  - Interactive Phase 1 (Candidate counter cancellation) and Phase 2 (Frequency threshold $> n/2$ validation).
- **Gale-Shapley Stable Matching (Stable Marriage)**:
  - Solves the bipartite stable matching problem with no blocking pairs in $O(n^2)$ proposals.
  - Preference ranking tables and live engagement tracking.

---

## 🚀 Setup & Execution Guide

### Prerequisites
- Python 3.9+ (Tested on Python 3.13)
- pip

### 1. Clone or Open Workspace
```bash
cd "f:\DAIICT (DAU)\Discrete Maths\Algorithm Project"
```

### 2. Install Dependencies
```bash
pip install -r Dashboard/requirements.txt
```
*(Dependencies: `streamlit`, `plotly`, `pandas`, `numpy`, `pytest`)*

### 3. Launch the Streamlit Platform
```bash
streamlit run Dashboard/app.py
```
The platform will launch in your browser at `http://localhost:8501`.

---

## 🧪 Automated Testing Suite

The project includes an automated **Pytest** validation suite covering algorithm correctness, boundary conditions (empty lists, duplicates, reverse ordered lists), step generation, complexity metadata, and benchmarking runners.

To run the test suite:
```bash
# Windows PowerShell
$env:PYTHONPATH="Dashboard"
python -m pytest Dashboard/tests -v
```

**Test Results:**
```
============================= test session starts =============================
collected 18 items

Dashboard/tests/test_algorithms.py::test_linear_search PASSED            [  5%]
Dashboard/tests/test_algorithms.py::test_binary_search PASSED            [ 11%]
Dashboard/tests/test_algorithms.py::test_sorting_algorithms[bubble_sort] PASSED [ 16%]
Dashboard/tests/test_algorithms.py::test_sorting_algorithms[insertion_sort] PASSED [ 22%]
Dashboard/tests/test_algorithms.py::test_sorting_algorithms[selection_sort] PASSED [ 27%]
Dashboard/tests/test_algorithms.py::test_sorting_algorithms[binary_insertion_sort] PASSED [ 33%]
Dashboard/tests/test_algorithms.py::test_sorting_steps PASSED            [ 38%]
Dashboard/tests/test_algorithms.py::test_naive_string_match PASSED       [ 44%]
Dashboard/tests/test_algorithms.py::test_cashiers_algorithm PASSED       [ 50%]
Dashboard/tests/test_algorithms.py::test_activity_selection PASSED       [ 55%]
Dashboard/tests/test_algorithms.py::test_boyer_moore_majority PASSED     [ 61%]
Dashboard/tests/test_algorithms.py::test_gale_shapley PASSED             [ 66%]
Dashboard/tests/test_algorithms.py::test_data_generator PASSED           [ 72%]
Dashboard/tests/test_analysis.py::test_complexity_metadata PASSED        [ 77%]
Dashboard/tests/test_analysis.py::test_asymptotic_notations PASSED       [ 83%]
Dashboard/tests/test_analysis.py::test_growth_data_calculation PASSED    [ 88%]
Dashboard/tests/test_analysis.py::test_sorting_benchmark PASSED          [ 94%]
Dashboard/tests/test_analysis.py::test_searching_benchmark PASSED        [100%]

============================= 18 passed in 0.97s ==============================
```

---

## 📊 Summary of Theoretical Complexity

| Algorithm | Category | Best Time | Average Time | Worst Time | Space Complexity | Stable | In-Place |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Linear Search** | Searching | $O(1)$ | $O(n)$ | $O(n)$ | $O(1)$ | N/A | Yes |
| **Binary Search** | Searching | $O(1)$ | $O(\log n)$ | $O(\log n)$ | $O(1)$ | N/A | Yes |
| **Bubble Sort** | Sorting | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Yes | Yes |
| **Insertion Sort** | Sorting | $O(n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Yes | Yes |
| **Selection Sort** | Sorting | $O(n^2)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | No | Yes |
| **Binary Insertion Sort** | Sorting | $O(n \log n)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ | Yes | Yes |
| **Naive String Matching** | String Matching | $O(n)$ | $O(n+m)$ | $O(n \cdot m)$ | $O(1)$ | N/A | Yes |
| **Cashier's Algorithm** | Greedy | $O(k)$ | $O(k)$ | $O(k)$ | $O(1)$ | N/A | Yes |
| **Activity Selection** | Greedy | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ | N/A | No |
| **Boyer-Moore Majority** | Supplementary | $O(n)$ | $O(n)$ | $O(n)$ | $O(1)$ | N/A | Yes |
| **Gale-Shapley Matching** | Supplementary | $O(n)$ | $O(n \log n)$ | $O(n^2)$ | $O(n^2)$ | Stable | No |

---

## 👥 Coursework Information
- **Course**: Discrete Mathematics (DA-IICT)
- **Topic**: Algorithm Execution, Asymptotic Analysis, and Visualization Platform
- **Textbook**: Kenneth H. Rosen, *Discrete Mathematics and Its Applications* (8th Edition)
