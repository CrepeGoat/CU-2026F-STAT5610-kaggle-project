from itertools import combinations
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

train = pd.read_csv("./data/train.csv", index_col="ID")
test = pd.read_csv("./data/test.csv", index_col="ID")

X = train.drop(columns="Y")
y = train["Y"]

best_score, best_cols = -1, None
for k in range(1, X.shape[1] + 1):
    for cols in combinations(X.columns, k):
        model = LogisticRegression(max_iter=1000)
        score = cross_val_score(model, X[list(cols)], y, cv=5).mean()
        if score > best_score:
            best_score, best_cols = score, list(cols)

print(best_cols, best_score)

model = LogisticRegression(max_iter=1000)
model.fit(X[best_cols], y)
preds = pd.Series(model.predict(test[best_cols]), index=test.index, name="Y")
preds.to_csv("submission.csv")