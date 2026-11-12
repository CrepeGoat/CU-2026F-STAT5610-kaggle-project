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

## computing $F_{1}$

given:
- a sequence of points $\{\underline{x}_{i}\}$
- a partition for which we predict positively and negatively:
	- $\hat{S}_{0} = \{i \mid \hat{y}_{i} = 0\}$
	- $\hat{S}_{1} = \{i \mid \hat{y}_{i} = 1\}$
	- $\hat{S}_{0} \cup \hat{S}_{1} = \{1, \dots, n\}$
- a partition for which the response is positive and negative:
	- $S_{0} = \{i \mid y_{i} = 0\}$
	- $S_{1} = \{i \mid y_{i} = 1\}$
	- $S_{0} \cup S_{1} = \{1, \dots, n\}$

-> then the $F_{1}$-score is computed as:
$$
\begin{align}
F_{1}
	&= \frac{2 \text{TP}}{2 \text{TP} + \text{FP} + \text{FN}} \\
	&= \frac
		{2 \cdot \left|S_{1} \cap \hat{S}_{1}\right|}
		{
			2 \cdot \left|S_{1} \cap \hat{S}_{1}\right|
			+ \left|S_{0} \cap \hat{S}_{1}\right|
			+ \left|S_{1} \cap \hat{S}_{0}\right|
		}
		\\
\end{align}
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
		&= \lim_{n \to \infty} \frac{2 \text{TP}}{2 \text{TP} + \text{FP} + \text{FN}} \\
		&= \lim_{n \to \infty} \frac
			{2 (n p)}
			{2 (n p) + (n (1 - p)) + (0)}
			& \text{def. of probability}
			\\
		&= \lim_{n \to \infty} \frac
			{2 n p}
			{n p + \cancel{n p} + n (1 \cancel{- p})}
			\\
		&= \lim_{n \to \infty} \frac
			{2 \cancel{n} p}
			{\cancel{n} (1 + p)}
			\\
		&= 2 \frac{p}{1 + p} \\
	\end{align}
	$$

	<iframe src="https://www.desmos.com/calculator/pvt3c2gzai?embed" width="400" height="400" style="border: 1px solid #ccc" frameborder=0></iframe>

3. randomly choose at some rate $r$ - $\hat{y}_{i} \sim \text{Bernoulli}(r)$:
	(note that, since the probability $p$ is the same for each set of inputs $\underline{x}_{i}$, there is no effective difference among the points; thus choosing some percentage of the points for which to predict a positive $\hat{y}_{i} = 1 \ \forall i \in S_{1} \subseteq \{1, \dots, n\}$, is no different than choosing these points $S_{1}$ at random)
	$$
	\begin{align}
	&\lim_{n \to \infty} \left(F_{1} \mid \hat{y}_{i} \sim \text{Bernoulli} (r)\right) \\
		&= \lim_{n \to \infty} \frac{2 \text{TP}}{2 \text{TP} + \text{FP} + \text{FN}} \\
		&= \lim_{n \to \infty} \frac
			{2 (n p r)}
			{2 (n p r) + (n (1 - p) r) + (n p (1 - r))}
			\\
		&= \lim_{n \to \infty} \frac
			{2 n p r}
			{\cancel{2 n p r} + n r \cancel{- n p r} + n p \cancel{- n p r}}
			\\
		&= \lim_{n \to \infty} \frac{2 \cancel{n} p r}{\cancel{n} (r + p)} \\
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

the expected value has a lot of nice properties:

$$
\begin{align}
\text{for all $X, Y$:}
	&& E [X + Y] = E [X] + E [Y] \\
\\
\text{$X, Y$ independent:}
	&& \implies E [X Y] = E [X] E [Y] \\
\end{align}
$$

however, there is *no* such property for division or inversion:

$$
\exists X, Y \text{ independent s.t. }
	E \left[\frac{X}{Y}\right]
	\neq \frac{E [X]}{E [Y]}
$$

the only way to compute the expected value in this case would be to work from the integral definition. while possible, this is too intensive for just a conceptual understanding via "napkin-math".

conversely, taking the long-run result, which here is just some function of a set of averages (i.e., TP, FP, FN), allows us to do simpler math via convergence in probabilities:

$$
f \left(\bar{X}, \bar{Y}\right)
	\stackrel{p}{\longrightarrow}
	f \left(\mu_{X}, \mu_{Y}\right)
$$


# more complex case - points w/ variable $p_i$

given:
- a sequence of points $\{\underline{x}_{i}\}$
- a probability distribution for the probability of a positive response for a given data point:
	$$
	p_{i} := \Pr (y_{i} = 1)
	$$
	where $\{p_{i}\}_{i = 1}^{n}$ are i.i.d.
- we always predict a positive response $\hat{y}_{i} = 1$

-> then the long-run $F_{1}$-score is:

$$
\begin{align}
\lim_{n \to \infty} F_{1}
	&= \lim_{n \to \infty} \frac{2 \text{TP}}{2 \text{TP} + \text{FP} + \text{FN}} \\
	&= \lim_{n \to \infty} \frac{2 \text{TP}}{2 \text{TP} + \text{FP} + \text{FN}} \\
\end{align}
$$


TODO

## $\{\hat{y}_{i} = 0, \hat{y}_{j} = 1\} \to \{\hat{y}_{i} = 1, \hat{y}_{j} = 0\}$


> suppose we have some $F_{1}$ for which $\hat{y}_{i} = 0, \hat{y}_{j} = 1$ and for some $p_{i}, p_{j}$. what is the effect on $F_{1}$ of swapping these two predictions s.t. $\hat{y}_{i} = 1, \hat{y}_{j} = 0$?

given:
- a sequence of points $\{\underline{x}_{i}\}$
- a partition for which we predict positively and negatively:
	- $\hat{S}_{0} = \{i \mid \hat{y}_{i} = 0\}$
	- $\hat{S}_{1} = \{i \mid \hat{y}_{i} = 1\}$
	- $\hat{S}_{0} \cup \hat{S}_{1} = \{1, \dots, n\}$
- some UNKNOWN prediction measures $\text{TP}, \text{FP}, \text{FN}$, given our prediction partition stated above
	- specifically, we don't know the actual response values $\{y_{i}\}_{i = 1}^{n}$
- some probability of each response value being positive $p_{i} := \Pr (y_{i} = 1)$

now suppose we switch the predictions for two points at indices $i, j$
- assume our predictions are opposing; i.e. $\hat{y}_{i} = 0 \neq 1 = \hat{y}_{j}$
- -> switching predictions yields $\hat{y}_{i}' = 1 \neq 0 = \hat{y}_{j}'$

-> our new prediction measures are then:

$$
\begin{align}
\text{TP}'
	&= \text{TP} \\
		&\hspace{1cm} \cancel{- \mathbb{1} \left\{y_{i} = 1, \hat{y}_{i} = 1\right\}} \\
		&\hspace{1cm} - \mathbb{1} \left\{y_{j} = 1, \cancel{\hat{y}_{j} = 1}\right\} \\
		&\hspace{1cm} + \mathbb{1} \left\{y_{i} = 1, \cancel{\hat{y}_{i}' = 1}\right\} \\
		&\hspace{1cm} \cancel{+ \mathbb{1} \left\{y_{j} = 1, \hat{y}_{j}' = 1\right\}} \\
	&= \text{TP}
		- \mathbb{1} \left\{y_{j} = 1\right\}
		+ \mathbb{1} \left\{y_{i} = 1\right\}
		\\
	\\
	&= \left\{\begin{array}{ll}
			\text{TP} & y_{i} = y_{j} \\
			\text{TP} - 1 & y_{i} = 0, y_{j} = 1 \\
			\text{TP} + 1 & y_{i} = 1, y_{j} = 0 \\
		\end{array}\right.
		\\
\\
\text{FP}'
	&= \text{FP} \\
		&\hspace{1cm} \cancel{- \mathbb{1} \left\{y_{i} = 0, \hat{y}_{i} = 1\right\}} \\
		&\hspace{1cm} - \mathbb{1} \left\{y_{j} = 0, \cancel{\hat{y}_{j} = 1}\right\} \\
		&\hspace{1cm} + \mathbb{1} \left\{y_{i} = 0, \cancel{\hat{y}_{i}' = 1}\right\} \\
		&\hspace{1cm} \cancel{+ \mathbb{1} \left\{y_{j} = 0, \hat{y}_{j}' = 1\right\}} \\
	&= \text{FP}
		- \mathbb{1} \left\{y_{j} = 0\right\}
		+ \mathbb{1} \left\{y_{i} = 0\right\}
		\\
	\\
	&= \left\{\begin{array}{ll}
			\text{FP} & y_{i} = y_{j} \\
			\text{FP} + 1 & y_{i} = 0, y_{j} = 1 \\
			\text{FP} - 1 & y_{i} = 1, y_{j} = 0 \\
		\end{array}\right.
		\\
\\
\text{FN}'
	&= \text{FN} \\
		&\hspace{1cm} - \mathbb{1} \left\{y_{i} = 1, \cancel{\hat{y}_{i} = 0}\right\} \\
		&\hspace{1cm} \cancel{- \mathbb{1} \left\{y_{j} = 1, \hat{y}_{j} = 0\right\}} \\
		&\hspace{1cm} \cancel{+ \mathbb{1} \left\{y_{i} = 1, \hat{y}_{i}' = 0\right\}} \\
		&\hspace{1cm} + \mathbb{1} \left\{y_{j} = 1, \cancel{\hat{y}_{j}' = 0}\right\} \\
	&= \text{FN}
		- \mathbb{1} \left\{y_{i} = 1\right\}
		+ \mathbb{1} \left\{y_{j} = 1\right\}
		\\
	\\
	&= \left\{\begin{array}{ll}
			\text{FN} & y_{i} = y_{j} \\
			\text{FN} + 1 & y_{i} = 0, y_{j} = 1 \\
			\text{FN} - 1 & y_{i} = 1, y_{j} = 0 \\
		\end{array}\right.
		\\
\end{align}
$$


-> the expectation of our new score $F_{1}'$ would then be:

$$
\begin{align}
E \left[F_{1}'\right]
	&= E \left[\frac{2 \text{TP}'}{2 \text{TP}' + \text{FP}' + \text{FN}'}\right] \\
	&= \sum_{y_{i}, y_{j} \in \{0, 1\}} \Pr(y_{i}, y_{j})
		\cdot \left(\frac
			{2 \text{TP}'}
			{2 \text{TP}' + \text{FP}' + \text{FN}'}
			\mid y_{i}, y_{j}
			\right)
		\\
	&=
		\Pr(y_{i} = 0, y_{j} = 0)
			\cdot \left(
				\frac{2 \text{TP}'}{2 \text{TP}' + \text{FP}' + \text{FN}'}
				\mid y_{i} = 0, y_{j} = 0
				\right)
			\\
		&\hspace{1cm} + \Pr(y_{i} = 0, y_{j} = 1)
			\cdot \left(
				\frac{2 \text{TP}'}{2 \text{TP}' + \text{FP}' + \text{FN}'}
				\mid y_{i} = 0, y_{j} = 1
				\right)
			\\
		&\hspace{1cm} + \Pr(y_{i} = 1, y_{j} = 0)
			\cdot \left(
				\frac{2 \text{TP}'}{2 \text{TP}' + \text{FP}' + \text{FN}'}
				\mid y_{i} = 1, y_{j} = 0
				\right)
			\\
		&\hspace{1cm} + \Pr(y_{i} = 1, y_{j} = 1)
			\cdot \left(
				\frac{2 \text{TP}'}{2 \text{TP}' + \text{FP}' + \text{FN}'}
				\mid y_{i} = 1, y_{j} = 1
			\right)
			\\
		\\
	&=
		(1 - p_{i}) (1 - p_{j})
			\cdot \left(\frac
				{2 (\text{TP})}
				{2 (\text{TP}) + (\text{FP}) + (\text{FN})}
			\right)
			\\
		&\hspace{1cm} + (1 - p_{i}) (p_{j})
			\cdot \left(\frac
				{2 (\text{TP} - 1)}
				{2 (\text{TP} \cancel{- 1}) + (\text{FP} \cancel{+ 1}) + (\text{FN} \cancel{+ 1})}
			\right)
			\\
		&\hspace{1cm} + (p_{i}) (1 - p_{j})
			\cdot \left(\frac
				{2 (\text{TP} + 1)}
				{2 (\text{TP} \cancel{+ 1}) + (\text{FP} \cancel{- 1}) + (\text{FN} \cancel{- 1})}
			\right)
			\\
		&\hspace{1cm} + (p_{i}) (p_{j})
			\cdot \left(\frac
				{2 (\text{TP})}
				{2 (\text{TP}) + (\text{FP}) + (\text{FN})}
			\right)
			\\
		\\
	&=
		(1 - p_{i} - p_{j})
			\cdot \left(\frac
				{2 \text{TP}}
				{2 \text{TP} + \text{FP} + \text{FN}}
			\right)
			\\
		&\hspace{1cm} + (1 - p_{i}) (p_{j})
			\cdot \left(\frac
				{2 \text{TP} - 2}
				{2 \text{TP} + \text{FP} + \text{FN}}
			\right)
			\\
		&\hspace{1cm} + (p_{i}) (1 - p_{j})
			\cdot \left(\frac
				{2 \text{TP} + 2}
				{2 \text{TP} + \text{FP} + \text{FN}}
				\right)
			\\
		\\
	&= \frac{2 \left(
			(1 - p_{i} - p_{j}) (\text{TP})
			+ (p_{j} - p_{i} p_{j}) (\text{TP} - 1)
			+ (p_{i} - p_{i} p_{j}) (\text{TP} + 1)
		\right)}
		{2 \text{TP} + \text{FP} + \text{FN}}
		\\
	&= \frac{2 \left(
			\text{TP}
			+ p_{i} (\cancel{-\text{TP} + \text{TP}} + 1)
			+ p_{j} (\cancel{-\text{TP} + \text{TP}} - 1)
			- p_{i} p_{j} (\text{TP} \cancel{- 1} + \text{TP} \cancel{+ 1})
		\right)}
		{2 \text{TP} + \text{FP} + \text{FN}}
		\\
	&= \frac{2 \left(
			\text{TP} (1 - 2 p_{i} p_{j}) + p_{i} - p_{j}
		\right)}
		{2 \text{TP} + \text{FP} + \text{FN}}
		\\
\end{align}
$$


TODO

