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

# simple case - optimize for a given $p$

suppose that we have:
- a set of points $\{\underline{x}_{i}\}$
- some conditional probability of a positive response $p = \Pr (y_{i} = 1 \mid \underline{x}_{i})$

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
			{2 (n p)}
			{2 (n p) + (n (1 - p)) + (0)}
			& \text{def. of probability}
			\\
		&= \frac
			{2 n p}
			{n p + \cancel{n p} + n (1 \cancel{- p})}
			\\
		&= \frac
			{2 \cancel{n} p}
			{\cancel{n} (1 + p)}
			\\
		&= 2 \frac{p}{1 + p} \\
	\end{align}
	$$

	<iframe src="https://www.desmos.com/calculator/pvt3c2gzai?embed" width="400" height="400" style="border: 1px solid #ccc" frameborder=0></iframe>

3. randomly choose at some rate $r$ - $\hat{y}_{i} \sim \text{Bernoulli}(r)$:
	$$
	\begin{align}
	&\lim_{n \to \infty} \left(F_{1} \mid \hat{y}_{i} \sim \text{Bernoulli} (r)\right) \\
		&= \frac{2 \text{TP}}{2 \text{TP} + \text{FP} + \text{FN}} \\
		&= \frac
			{2 (n p r)}
			{2 (n p r) + (n (1 - p) r) + (n p (1 - r))}
			\\
		&= \frac
			{2 n p r}
			{\cancel{2 n p r} + n r \cancel{- n p r} + n p \cancel{- n p r}}
			\\
		&= \frac{2 \cancel{n} p r}{\cancel{n} (r + p)} \\
		&= \frac{2 p r}{r + p} \\
	\end{align}
	$$

	(note that this is consistent with the prior two results, when setting $r = 0, r = 1$, respectively)

	we then want to choose $r$ s.t. we maximize this quantity:
	$$
	\begin{align}
	&\arg \max_{r \in [0, 1]} \lim_{n \to \infty} \left(F_{1} \mid \hat{y}_{i} \sim \text{Bernoulli} (r)\right) \\
		&= \arg \max_{r \in [0, 1]} \left(\frac{2 p r}{r + p}\right) \\
		&= \arg \max_{r \in [0, 1]} \left(\frac{2 p}{1 + p / r}\right)
			& \text{$1 / f(r)$ is decreasing w.r.t. $f(r)$}
			\\
		&= \arg \min_{r \in [0, 1]} \left(1 + \frac{p}{r}\right)
			& \text{$1 + f(r)$ is increasing w.r.t. $f(r)$}
			\\
		&= \arg \min_{r \in [0, 1]} \left(\frac{p}{r}\right)
			& \text{$1 / f(r)$ is decreasing w.r.t. $f(r)$}
			\\
		&= \arg \max_{r \in [0, 1]} \left(r\right) \\
		&= 1 \\
	\end{align}
	$$

	**-> the optimal case is when $r = 1$; i.e., case 2 - always choose $\hat{y}_{i} = 1$.**


## note on expected values

> Why did we take the long-run value $\lim_{n \to \infty} (\dots)$ instead of just taking the expected value $E [\dots]$?

The expected value has a lot of nice properties:

$$
\begin{align}
\text{for all $X, Y$:}
	&& E [X + Y] = E [X] + E [Y] \\
\\
\text{$X, Y$ independent:}
	&& \implies E [X Y] = E [X] E [Y] \\
\end{align}
$$

However, there is *no* such property for division or inversion:

$$
\exists X, Y \text{ independent s.t. }
	E \left[\frac{X}{Y}\right]
	\neq \frac{E [X]}{E [Y]}
$$

the only way to compute the expected value in this case would be to work from the integral definition. while possible, this is too intensive for just a conceptual understanding via "napkin-math".

Conversely, taking the long-run result, which here is just some function of a set of averages (i.e., TP, FP, FN) allows us to do simpler math via convergence in probabilities:

$$
f \left(\bar{X}, \bar{Y}\right)
	\stackrel{p}{\longrightarrow}
	f \left(\mu_{X}, \mu_{Y}\right)
$$
