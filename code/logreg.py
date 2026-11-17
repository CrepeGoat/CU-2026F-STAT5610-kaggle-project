from itertools import combinations
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

train = pd.read_csv("./data/train.csv", index_col="ID")
test = pd.read_csv("./data/test.csv", index_col="ID")

X = train.drop(columns="Y")
y = train["Y"]

cat_cols = ["x4", "x5", "x10"]

best_score, best_cols = -1, None
for k in range(1, X.shape[1] + 1):
    for cols in combinations(X.columns, k):
        cols = list(cols)
        X_sub = pd.get_dummies(X[cols], columns=[c for c in cols if c in cat_cols])
        model = LogisticRegression(max_iter=1000, class_weight="balanced")
        score = cross_val_score(model, X_sub, y, cv=5, scoring="f1").mean()
        if score > best_score:
            best_score, best_cols = score, cols

print(best_cols, best_score)

both = pd.concat([X[best_cols], test[best_cols]])
both = pd.get_dummies(both, columns=[c for c in best_cols if c in cat_cols])
X_best = both.iloc[:len(X)]
test_best = both.iloc[len(X):]

model = LogisticRegression(max_iter=1000, class_weight="balanced")
model.fit(X_best, y)
preds = pd.Series(model.predict(test_best), index=test.index, name="Y")
preds.to_csv("logreg_submission.csv")