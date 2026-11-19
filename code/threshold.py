import numpy as np
import pandas as pd
import seaborn as sns


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
    ax = sns.ecdfplot(probs)
    ax.set_xlim(0, 1)
    # ax.set_ylim(0, 1)

    neg_pred_prop = 1 - (pos_pred_count / len(probs))
    ax.hlines(neg_pred_prop, 0, threshold, linestyles="--", colors="darkorange")
    ax.vlines(threshold, 0, neg_pred_prop, linestyles="--", colors="darkorange")

    ax.vlines(np.mean(probs), 0, 1)
    ax.vlines(expt_prob, 0, 1, colors="green")

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
    for i in range(pp_count + 1, len(probs)):
        tn += rng.binomial(n=1, p=1 - probs.iloc[i], size=n)

    probs = probs.sort_index()

    return calc_f_score(len(probs), tp, tn)


def plot_f_scores(empiricals, calculated, reported, rng=np.random.default_rng(1)):
    # sns.set_theme(style="whitegrid")

    ax = sns.violinplot(y=empiricals)
    ax.yaxis.set_label_text("F-score")

    ax.hlines(calculated, xmin=-0.5, xmax=0.5, colors="darkorange", linestyles="--")
    if reported is not None:
        ax.hlines(reported, xmin=-0.5, xmax=0.5, colors="green", linestyles="-.")

    return ax


if __name__ == "__main__":
    test_estimate_optimal_threshold()
