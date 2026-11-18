import numpy as np
import pandas as pd


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


if __name__ == "__main__":
    test_estimate_optimal_threshold()
