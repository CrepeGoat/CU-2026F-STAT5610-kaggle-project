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

    result = min(expr(i), probs.iloc[i - 1])
    probs = probs.sort_index()

    return result


def test_estimate_optimal_threshold():
    probs = pd.Series([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9])

    result = estimate_optimal_threshold(probs)
    print(result)


if __name__ == "__main__":
    test_estimate_optimal_threshold()
