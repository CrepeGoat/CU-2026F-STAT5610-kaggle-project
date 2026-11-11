# definitions

from the prompt:

> Evaluation of how well your classifier is doing will be based on [F1 score](https://en.wikipedia.org/wiki/F-score).

the $F_{1}$-score [is defined as](https://en.wikipedia.org/wiki/F-score#Definition):

$$
\begin{align}
F_{1}
	&:= \frac{2}{\left(\text{recall}\right)^{-1} + \left(\text{precision}\right)^{-1}} \\
	&= \frac{2 \text{TP}}{2 \text{TP} + \text{FP} + \text{FN}}
\end{align}
$$

where the true positive, false positive, and false negative rates are defined as:

$$
\begin{align}
\text{TP}
	&:= |\{\hat{y}_{i}, y_{i} \mid \hat{y}_{i} = 1 = y_{i}\}| \\
\text{FP}
	&:= |\{\hat{y}_{i}, y_{i} \mid \hat{y}_{i} = 1 \neq y_{i} = 0\}| \\
\text{FN}
	&:= |\{\hat{y}_{i}, y_{i} \mid \hat{y}_{i} = 0 \neq y_{i} = 1\}| \\
\end{align}
$$

we also assume that there is some probability $p$ that governs the true response $y_{i}$ for some given predictors $\underline{x}_{i}$, s.t.:

$$
y_{i} \mid \underline{x}_{i}
	\sim \text{Bernoulli}(p)
$$

# simple case - optimize for a given predicted $p$ 

suppose that we have:
- a set of points $\{\underline{x}_{i}\}$
- some estimate for the probability $\hat{p} \approx \Pr (y_{i} = 1 \mid \underline{x}_{i})$

-> our $F_{1}$-score under different tactics:
1. **always choose $\hat{y}_{i} = 0$** - in this case $\text{TP} = 0$, so inherently:
	$$
	\lim_{n \to \infty} \left(F_{1} \mid \hat{y}_{i} = 0\right)
		= \frac{0}{(\dots)}
		= 0
	$$
	<iframe src="https://www.desmos.com/calculator/1pov1fpncp?embed" width="400" height="400" style="border: 1px solid #ccc" frameborder=0></iframe>

2. **always choose $\hat{y}_{i} = 1$**:
	$$
	\begin{align}
	\lim_{n \to \infty} \left(F_{1} \mid \hat{y}_{i} = 1\right)
		&= \frac{2 \text{TP}}{2 \text{TP} + \text{FP} + \text{FN}} \\
		&= \frac
			{2 (n \hat{p})}
			{2 (n \hat{p}) + (n (1 - \hat{p})) + (0)}
			\\
		&= \frac
			{2 n \hat{p}}
			{n \hat{p} + \cancel{n \hat{p}} + n (1 \cancel{- \hat{p}})}
			\\
		&= \frac
			{2 \cancel{n} \hat{p}}
			{\cancel{n} (1 + \hat{p})}
			\\
		&= 2 \frac{\hat{p}}{1 + \hat{p}} \\
	\end{align}
	$$

	<iframe src="https://www.desmos.com/calculator/pvt3c2gzai?embed" width="400" height="400" style="border: 1px solid #ccc" frameborder=0></iframe>

3. randomly choose at some rate $r$ - $\hat{y}_{i} \sim \text{Bernoulli}(p = r)$:
	$$
	\begin{align}
	&\lim_{n \to \infty} \left(F_{1} \mid \hat{y}_{i} \sim \text{Bernoulli} (r)\right) \\
		&= \frac{2 \text{TP}}{2 \text{TP} + \text{FP} + \text{FN}} \\
		&= \frac
			{2 (n \hat{p} r)}
			{2 (n \hat{p} r) + (n (1 - \hat{p}) r) + (n \hat{p} (1 - r))}
			\\
		&= \frac
			{2 n \hat{p} r}
			{\cancel{2 n \hat{p} r} + n r \cancel{- n \hat{p} r} + n \hat{p} \cancel{- n \hat{p} r}}
			\\
		&= \frac{2 \cancel{n} \hat{p} r}{\cancel{n} (r + \hat{p})} \\
		&= \frac{2 \hat{p} r}{r + \hat{p}} \\
	\end{align}
	$$

	(note that this is consistent with the prior two results, when setting $r = 0, r = 1$, respectively)

	we then want to choose $r$ s.t. we maximize this quantity:
	$$
	\begin{align}
	&\arg \max_{r \in [0, 1]} \lim_{n \to \infty} \left(F_{1} \mid \hat{y}_{i} \sim \text{Bern} (r)\right) \\
		&= \arg \max_{r \in [0, 1]} \left(\frac{2 \hat{p} r}{r + \hat{p}}\right) \\
		&= \arg \max_{r \in [0, 1]} \left(\frac{2 \hat{p}}{1 + \hat{p} / r}\right)
			& \text{$1 / f(r)$ is decreasing w.r.t. $f(r)$}
			\\
		&= \arg \min_{r \in [0, 1]} \left(1 + \frac{\hat{p}}{r}\right)
			& \text{$1 + f(r)$ is increasing w.r.t. $f(r)$}
			\\
		&= \arg \min_{r \in [0, 1]} \left(\frac{\hat{p}}{r}\right)
			& \text{$1 / f(r)$ is decreasing w.r.t. $f(r)$}
			\\
		&= \arg \max_{r \in [0, 1]} \left(r\right) \\
		&= 1 \\
	\end{align}
	$$

	**-> the optimal case is when $r = 1$; i.e., case 2.**
