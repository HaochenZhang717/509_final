import json
import matplotlib.pyplot as plt

# ---------- 读取 JSON 数据 ----------
with open("dpll_results_parallel.json") as f:
    data = json.load(f)

heuristics = ["random", "2_clause_heuristics", "mine"]

# ---------- 图1: Compute Time vs L/N ----------
def plot_metric(metric_key, ylabel, title, filename):
    plt.figure(figsize=(8, 6))
    for heuristic in heuristics:
        xs = []
        ys = []
        for N in sorted(data.keys(), key=int):
            for L_N in sorted(data[N].keys(), key=float):
                val = data[N][L_N][heuristic][metric_key]
                xs.append(float(L_N))
                ys.append(val)
        plt.plot(xs, ys, marker='o', label=heuristic)
    plt.xlabel("L / N")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

plot_metric("median_time", "Median Time (s)", "Compute Time vs L/N", "plot1_time_vs_ln.png")
plot_metric("median_calls", "Median DPLL Calls", "DPLL Calls vs L/N", "plot2_calls_vs_ln.png")
plot_metric("sat_prob", "Satisfiability Probability", "Satisfiability Probability vs L/N", "plot3_satprob_vs_ln.png")

# ---------- 图4: Ratio 我的启发式 vs Baselines ----------
def plot_ratio(metric_key, baseline_heuristic, ylabel, title, filename):
    plt.figure(figsize=(8, 6))
    ratios = []
    xs = []

    for N in sorted(data.keys(), key=int):
        for L_N in sorted(data[N].keys(), key=float):
            mine = data[N][L_N]["mine"][metric_key]
            baseline = data[N][L_N][baseline_heuristic][metric_key]
            ratio = mine / baseline if baseline != 0 else float('nan')
            ratios.append(ratio)
            xs.append(float(L_N))

    plt.plot(xs, ratios, marker='o', label=f"mine / {baseline_heuristic}")
    plt.axhline(1.0, color='gray', linestyle='--')
    plt.xlabel("L / N")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

plot_ratio("median_time", "random", "Time Ratio", "Mine vs Random: Time Ratio", "plot4_mine_vs_random_time.png")
plot_ratio("median_calls", "random", "Calls Ratio", "Mine vs Random: Calls Ratio", "plot5_mine_vs_random_calls.png")
plot_ratio("median_time", "2_clause_heuristics", "Time Ratio", "Mine vs 2-Clause: Time Ratio", "plot6_mine_vs_2clause_time.png")
plot_ratio("median_calls", "2_clause_heuristics", "Calls Ratio", "Mine vs 2-Clause: Calls Ratio", "plot7_mine_vs_2clause_calls.png")