import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import Rectangle

COLORS = dict(
    sampled="darkgray",
    simulated="lightgray",
    empirical="darkorange",
    optimal="darkviolet",
    true_good="green",
    true_bad="red",
)


def estimate_optimal_threshold(probs):
    # check that input is a pd.Series object
    _ = probs.index

    probs_count = len(probs)
    probs_sum = probs.sum()
    probs = probs.sort_values(ascending=False)

    probs_acc = 0

    def expr(i):
        return (probs_acc) / (probs_sum + i)

    i = 0
    for i in range(1, probs_count - 1):
        probs_acc += probs.iloc[i - 1]
        if expr(i) >= probs.iloc[i]:
            break
    else:
        i += 1

    result = (i, min(expr(i), probs.iloc[i - 1]))
    probs = probs.sort_index()

    return result


def test_estimate_optimal_threshold():
    probs = pd.Series([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])

    result = estimate_optimal_threshold(probs)
    print(result)


def plot_probs(probs, expt_prob, threshold, pos_pred_count):
    ax = sns.ecdfplot(probs, color=COLORS["sampled"])

    neg_pred_prop = 1 - (pos_pred_count / len(probs))
    ax.hlines(
        neg_pred_prop,
        0,
        min(threshold + 0.05, 1),
        linestyles="--",
        colors=COLORS["optimal"],
        label='"optimal" decision threshold',
    )
    ax.vlines(
        threshold,
        0,
        min(neg_pred_prop + 0.05, 1),
        linestyles="--",
        colors=COLORS["optimal"],
    )
    ax.add_patch(
        Rectangle(
            xy=(1, 1),
            width=1,
            height=1 - neg_pred_prop,
            angle=180,
            # facecolor=COLORS["empirical"],
            alpha=0.1,
            hatch="//",
            facecolor="none",
            hatchcolor=COLORS["optimal"],
            hatch_linewidth=2,
        )
    )

    ax.hlines(
        1 - expt_prob,
        0,
        1,
        colors=COLORS["empirical"],
        linestyle="-",
        linewidth=0.5,
        label="positive response rate in training",
    )
    ax.add_patch(
        Rectangle(
            xy=(1, 1),
            width=1,
            height=expt_prob,
            angle=180,
            # facecolor=COLORS["empirical"],
            alpha=0.1,
            hatch="/",
            facecolor="none",
            hatchcolor=COLORS["empirical"],
            hatch_linewidth=8,
        )
    )

    ax.set_title("Estimated CDF of Pr(Y = 1)", loc="left")
    ax.set_ylabel("")
    ax.set_xticks([0.25, 0.5, 0.75])
    ax.set_yticks([0.25, 0.5, 0.75])
    # ax.axis("equal")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend()

    sns.despine(left=True, right=True, top=False, bottom=False)

    return ax


def calc_f_score(n, tp_count, tn_count):
    return (2 * tp_count) / (tp_count + n - tn_count)


def sample_probable_f_scores(rng, n, probs, pp_count):
    # check that input is a pd.Series object
    _ = probs.index

    probs = probs.sort_values(ascending=False)

    tp = np.zeros(n)
    tn = np.zeros(n)

    for i in range(pp_count):
        tp += rng.binomial(n=1, p=probs.iloc[i], size=n)
    for i in range(pp_count, len(probs)):
        tn += rng.binomial(n=1, p=1 - probs.iloc[i], size=n)

    probs = probs.sort_index()

    return calc_f_score(len(probs), tp, tn)


def pos_in_sorted(a, x):
    return np.count_nonzero(x > a)


def plot_f_scores(empiricals, calculated, reported, rng=np.random.default_rng(1)):
    ax = sns.violinplot(
        y=empiricals,
        inner=None,
        linewidth=0,
        color=COLORS["simulated"],
        # fill=False,
        label=f"simulated (n = {len(empiricals)})",
    )
    ax.hlines(
        np.quantile(empiricals, [0.025, 0.5, 0.975]),
        xmin=-0.5,
        xmax=0.5,
        colors="white",
        linestyles="-",
        linewidth=0.75,
    )

    def quantile_text(i, n):
        if i <= 0:
            return f"< ~{1 / n:.1%}"
        if i >= n:
            return f"> ~{1 - (1 / n):.1%}"
        else:
            return f"~{i / n:.1%}"

    ax.hlines(
        calculated,
        xmin=-0.5,
        xmax=0,
        colors=COLORS["optimal"],
        linestyles="--",
        linewidth=1,
        label="theoretical optimal",
    )
    i_calc = pos_in_sorted(empiricals, calculated)
    ax.text(
        s=f"{calculated:.3f} ({quantile_text(i_calc, len(empiricals))})",
        x=0,
        horizontalalignment="right",
        y=calculated,
        verticalalignment="bottom",
        color=COLORS["optimal"],
    )
    if reported is not None:
        ax.hlines(
            reported,
            xmin=0,
            xmax=0.5,
            colors=COLORS["true_good"],
            linestyles="-",
            linewidth=1,
            label="actual (from Kaggle)",
        )
        i_rept = pos_in_sorted(empiricals, reported)
        ax.text(
            s=f"{reported:.3f} ({quantile_text(i_rept, len(empiricals))})",
            x=0,
            horizontalalignment="left",
            y=reported,
            verticalalignment="bottom",
            color=COLORS["true_good"],
        )

    ax.set_title("Comparison of F-scores", loc="left")
    ax.set_xlabel("")
    ax.set_ylabel("")
    ax.set_xticks([])
    ax.locator_params(axis="y", nbins=3)
    ax.set_xlim(-0.5, 0.5)
    ax.legend()

    sns.despine(left=True, right=True, top=False, bottom=False)

    return ax


if __name__ == "__main__":
    test_estimate_optimal_threshold()
