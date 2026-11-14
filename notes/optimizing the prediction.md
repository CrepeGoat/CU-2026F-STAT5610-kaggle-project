# definitions

from the prompt:

> Evaluation of how well your classifier is doing will be based on [F1 score](https://en.wikipedia.org/wiki/F-score).

the F-score $F _{1}$ [is defined as](https://en.wikipedia.org/wiki/F-score#Definition):

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
	&:= |\lbrace \hat{y}_{i}, y_{i} \mid \hat{y}_{i} = 1 = y_{i}\rbrace| \\
\text{FP}
	&:= |\lbrace \hat{y}_{i}, y_{i} \mid \hat{y}_{i} = 1 \neq y_{i} = 0\rbrace| \\
\text{FN}
	&:= |\lbrace \hat{y}_{i}, y_{i} \mid \hat{y}_{i} = 0 \neq y_{i} = 1\rbrace| \\
\end{align}
$$

we also assume that there is some probability $p$ that governs the true response $y_{i}$ for some given predictors $\underline{x}_{i}$, s.t.:

$$
y_{i} \mid \underline{x}_{i}
	\sim \text{Bernoulli}(p)
$$

# computing $F_{1}$

given:
- a sequence of points $\lbrace \underline{x}_{i}\rbrace _{i = 1}^{n}$
- a partition for which we predict positively and negatively:
	- $\hat{S} _{0} = \lbrace i \mid \hat{y} _{i} = 0\rbrace$
	- $\hat{S} _{1} = \lbrace i \mid \hat{y} _{i} = 1\rbrace$
	- $\hat{S} _{0} \cup \hat{S} _{1} = \lbrace 1, \dots, n\rbrace$
	- $\hat{S} _{0} \cap \hat{S} _{1} = \varnothing$
- a partition for which the response is positive and negative:
	- $S _{0} = \lbrace i \mid y _{i} = 0\rbrace$
	- $S _{1} = \lbrace i \mid y _{i} = 1\rbrace$
	- $S _{0} \cup S _{1} = \lbrace 1, \dots, n\rbrace$
	- $S _{0} \cap S _{1} = \varnothing$

-> then the F-score is computed as:

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
- a set of points $\lbrace \underline{x}_{i}\rbrace _{i = 1}^{n}$
- some conditional probability of a positive response $p = \Pr (y_{i} = 1 \mid \underline{x}_{i})$

-> our F-score under different tactics:

## 1. **always choose $\hat{y} _{i} = 0$**

in this case $\text{TP} = 0$, so inherently:

$$
\lim_{n \to \infty} \left(F_{1} \mid \hat{y}_{i} = 0\right)
	= \frac{0}{(\dots)}
	= 0
$$
	
<iframe src="https://www.desmos.com/calculator/1pov1fpncp?embed" width="400" height="400" style="border: 1px solid #ccc" frameborder=0></iframe>

## 2. **always choose $\hat{y} _{i} = 1$**

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

## 3. randomly choose at some rate $r$

where $\hat{y} _{i} \sim \text{Bernoulli}(r)$:

(note that, since the probability $p$ is the same for each set of inputs $\underline{x}_{i}$, there is no effective difference among the points; thus choosing some percentage of the points for which to predict a positive $\hat{y} _{i} = 1 \ \forall i \in S _{1} \subseteq \lbrace 1, \dots, n\rbrace$, is no different than choosing these points $S_{1}$ at random)

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

**-> the optimal case is when $r = 1$; i.e., case 2 - always choose $\hat{y} _{i} = 1$.**

## note on expected values

> Why did we take the long-run value $\lim _{n \to \infty} (\dots)$ instead of just taking the expected value $E [\dots]$?

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

# increase F-score via prediction swap

> suppose we have some $F _{1}$ for which $\hat{y} _{i} = 0, \hat{y} _{j} = 1$ and for some $p _{i}, p _{j}$. what is the effect on $F _{1}$ of swapping these two predictions s.t. $\hat{y} _{i}' = 1, \hat{y} _{j}' = 0$?

given:
- a sequence of points $\lbrace \underline{x}_{i}\rbrace _{i = 1}^{n}$
- a partition for which we predict positively and negatively:
	- $\hat{S} _{0} = \lbrace i \mid \hat{y} _{i} = 0\rbrace$
	- $\hat{S} _{1} = \lbrace i \mid \hat{y} _{i} = 1\rbrace$
	- $\hat{S} _{0} \cup \hat{S} _{1} = \lbrace 1, \dots, n\rbrace$
	- $\hat{S} _{0} \cap \hat{S} _{1} = \varnothing$
- some UNKNOWN prediction measures $\text{TP}, \text{FP}, \text{FN}$, given our prediction partition stated above
	- specifically, we don't know the actual response values $\lbrace y _{i}\rbrace _{i = 1}^{n}$
- some probability of each response value being positive $p_{i} := \Pr (y _{i} = 1)$

suppose we switch the predictions for two points at indices $i, j$
- assume our predictions are opposing; i.e. $\hat{y} _{i} = 0 \neq 1 = \hat{y} _{j}$
- -> switching predictions yields $\hat{y} _{i}' = 1 \neq 0 = \hat{y} _{j}'$

-> our new prediction measures are then:

$$
\begin{align}
\text{TP}'
	&= \text{TP} \\
		&\hspace{1cm} \cancel{- \mathbb{1} \left\lbrace y_{i} = 1, \hat{y}_{i} = 1\right\rbrace} \\
		&\hspace{1cm} - \mathbb{1} \left\lbrace y_{j} = 1, \cancel{\hat{y}_{j} = 1}\right\rbrace \\
		&\hspace{1cm} + \mathbb{1} \left\lbrace y_{i} = 1, \cancel{\hat{y}_{i}' = 1}\right\rbrace \\
		&\hspace{1cm} \cancel{+ \mathbb{1} \left\lbrace y_{j} = 1, \hat{y}_{j}' = 1\right\rbrace} \\
	&= \text{TP}
		- \mathbb{1} \left\lbrace y_{j} = 1\right\rbrace
		+ \mathbb{1} \left\lbrace y_{i} = 1\right\rbrace
		\\
	\\
	&= \left\lbrace \begin{array}{ll}
			\text{TP} & y_{i} = y_{j} \\
			\text{TP} - 1 & y_{i} = 0, y_{j} = 1 \\
			\text{TP} + 1 & y_{i} = 1, y_{j} = 0 \\
		\end{array}\right.
		\\
\\
\text{FP}'
	&= \text{FP} \\
		&\hspace{1cm} \cancel{- \mathbb{1} \left\lbrace y_{i} = 0, \hat{y}_{i} = 1\right\rbrace} \\
		&\hspace{1cm} - \mathbb{1} \left\lbrace y_{j} = 0, \cancel{\hat{y}_{j} = 1}\right\rbrace \\
		&\hspace{1cm} + \mathbb{1} \left\lbrace y_{i} = 0, \cancel{\hat{y}_{i}' = 1}\right\rbrace \\
		&\hspace{1cm} \cancel{+ \mathbb{1} \left\lbrace y_{j} = 0, \hat{y}_{j}' = 1\right\rbrace} \\
	&= \text{FP}
		- \mathbb{1} \left\lbrace y_{j} = 0\right\rbrace
		+ \mathbb{1} \left\lbrace y_{i} = 0\right\rbrace
		\\
	\\
	&= \left\lbrace \begin{array}{ll}
			\text{FP} & y_{i} = y_{j} \\
			\text{FP} + 1 & y_{i} = 0, y_{j} = 1 \\
			\text{FP} - 1 & y_{i} = 1, y_{j} = 0 \\
		\end{array}\right.
		\\
\\
\text{FN}'
	&= \text{FN} \\
		&\hspace{1cm} - \mathbb{1} \left\lbrace y_{i} = 1, \cancel{\hat{y}_{i} = 0}\right\rbrace \\
		&\hspace{1cm} \cancel{- \mathbb{1} \left\lbrace y_{j} = 1, \hat{y}_{j} = 0\right\rbrace} \\
		&\hspace{1cm} \cancel{+ \mathbb{1} \left\lbrace y_{i} = 1, \hat{y}_{i}' = 0\right\rbrace} \\
		&\hspace{1cm} + \mathbb{1} \left\lbrace y_{j} = 1, \cancel{\hat{y}_{j}' = 0}\right\rbrace \\
	&= \text{FN}
		- \mathbb{1} \left\lbrace y_{i} = 1\right\rbrace
		+ \mathbb{1} \left\lbrace y_{j} = 1\right\rbrace
		\\
	\\
	&= \left\lbrace \begin{array}{ll}
			\text{FN} & y_{i} = y_{j} \\
			\text{FN} + 1 & y_{i} = 0, y_{j} = 1 \\
			\text{FN} - 1 & y_{i} = 1, y_{j} = 0 \\
		\end{array}\right.
		\\
\end{align}
$$


-> the expectation of our new score $F _{1}'$ would then be:

$$
\begin{align}
E \left[F_{1}'\right]
	&= E \left[\frac{2 \text{TP}'}{2 \text{TP}' + \text{FP}' + \text{FN}'}\right] \\
	&= \sum_{y_{i}, y_{j} \in \lbrace 0, 1\rbrace} \Pr(y_{i}, y_{j})
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
		(1 - p_{i} - p_{j} + 2 p_{i} p_{j})
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
			(1 - p_{i} - p_{j} + 2 p_{i} p_{j}) (\text{TP})
			+ (p_{j} - p_{i} p_{j}) (\text{TP} - 1)
			+ (p_{i} - p_{i} p_{j}) (\text{TP} + 1)
		\right)}
		{2 \text{TP} + \text{FP} + \text{FN}}
		\\
	&= \frac{2 \left(
			\text{TP}
			+ p_{i} (\cancel{-\text{TP} + \text{TP}} + 1)
			+ p_{j} (\cancel{-\text{TP} + \text{TP}} - 1)
			+ p_{i} p_{j} (\cancel{2 \text{TP}} - (\cancel{\text{TP}} \cancel{- 1}) - (\cancel{\text{TP}} \cancel{+ 1}))
		\right)}
		{2 \text{TP} + \text{FP} + \text{FN}}
		\\
	&= \frac
		{2 \left(\text{TP} + p_{i} - p_{j}\right)}
		{2 \text{TP} + \text{FP} + \text{FN}}
		\\
\end{align}
$$

compared to the original F-score:

$$
\begin{align}
&&E [F_{1}] &\lessgtr E \left[F_{1}'\right] \\
\iff &&\frac
	{2 \text{TP}}
	{2 \text{TP} + \text{FP} + \text{FN}}
	&\lessgtr \frac
		{2 \left(\text{TP} + p_{i} - p_{j}\right)}
		{2 \text{TP} + \text{FP} + \text{FN}}
	\\
\iff &&2 \text{TP}
	&\lessgtr 2 \left(\text{TP} + p_{i} - p_{j}\right)
	&& 2 \text{TP} + \text{FP} + \text{FN} > 0
	\\
\iff &&0
	&\lessgtr 2 \left(p_{i} - p_{j}\right)
	\\
\iff &&p_{j} &\lessgtr p_{i}
	&& 2 > 0
	\\
\end{align}
$$


thus:

$$
\to \boxed{
	p_{i} > p_{j}
	\implies E \left[F_{1}'\right] > E [F_{1}]
}
$$

where $F _{1}'$ is the F-score after switching predictions


specifically, we have shown that **we can increase the expectation of the F-score by switching predictions**:
- a point $i$ with a higher positive-response probability $p _{i}$ is reassigned a positive response $\cancel{\hat{y} _{i} = 0} \to \hat{y} _{i} = 1$
- a point $j$ with a lower positive-response probability $p _{j} < p _{i}$ is reassigned a negative response $\cancel{\hat{y} _{j} = 1} \to  \hat{y} _{j} = 0$

## implication - thresholds are optimal

given [[#increase F-score via prediction swap|the swap result]], we can show that **any optimal strategy can be described as some threshold on the positive response probabilities:**

$$
\hat{y} _{i} = \mathbb{1} \lbrace p _{i} \geq T _{p}\rbrace
$$

proof outline:
- start with [[#def - threshold strategy|the definition of a threshold strategy]]
- a strategy cannot be expressed as a threshold strategy iff, for some value $T_{p}$:
	- there exists a point indexed at $i$, where the probability is beneath the value $p_{i} < T_{p}$ and the prediction is positive $\hat{y} _{i} = 1$
		- to satisfy property 1, the threshold value must be *decreased* s.t. $T_{p} < p_{i}$
	- AND there also exists a point indexed at $j$, where the probability is above the value $p_{j} \geq T_{p}$ and the prediction is negative $\hat{y} _{i} = 0$
		- to satisfy property 2, the threshold value must be *increased* s.t. $T_{p} \geq p_{j}$
	- -> the threshold cannot be both increased and decreased
	- => the properties are not satisfiable
	- the reverse implication, shown [[#lemma - non-threshold strategy|here]]
- any strategy that is not a threshold strategy can swap predictions at $(i, j)$, where $p_{i} < T_{p} \leq p_{j}$ and $\hat{y} _{i} = 1, \hat{y} _{j} = 0$
- -> as shown in [[#increase F-score via prediction swap|the swap-increase property]], such a swap *must* increase (the expected value of) the F-score
- => the non-threshold strategy is NOT optimal
- => any optimal strategy MUST be a threshold strategy

### def - threshold strategy

a strategy for "thresholding" involves predictions $\lbrace \hat{y} _{i}\rbrace _{i = 1}^{n}$ s.t., for some threshold value $T_{p}$:
1. any point $i$ with a probability below the threshold $p_{i} < T_{p}$ gets a negative prediction $\hat{y} _{i} = 0$
2. any point $i$ with a probability above (or equal to) the threshold $p_{i} \geq T_{p}$ gets a positive prediction $\hat{y} _{i} = 1$

in short:

$$
\hat{y} _{i} = \mathbb{1} \lbrace p _{i} \geq T _{p}\rbrace
$$

### lemma - non-threshold strategy

if not a threshold strategy, then there is a negatively-predicted point $j$ with a higher (or equal) positive response probability than a positively-predicted point $i$

- to be a non-thresholding strategy, then for all $T$ one of the conditions must fail
	- the 1st condition fails for all thresholds above the lowest PRP of NP-points $\min _{j \in \hat{S} _{1}} p _{j} \leq T$
	- the 2nd condition fails for all thresholds below the highest NRP of PP-points $T < \max _{i \in \hat{S} _{0}} p _{i}$
1. for all $T$ to fail, these two failure conditions must cover the whole probability space $[0, 1]$:

$$
\begin{align}
T &\in
	\left[\min_{j \in \hat{S}_{1}} p_{j}, 1\right]
	\cap \left[0, \max_{i \in \hat{S}_{0}} p_{i}\right)
	\\
\to \min_{j \in \hat{S}_{1}} p_{j} &\leq \max_{i \in \hat{S}_{0}} p_{i} \\
\end{align}
$$

2. note also the two prediction sets are mutually exclusive $\hat{S} _{0} \cap \hat{S} _{1} = \varnothing$
- -> from 1. and 2., there must be two distinct points $i, j$ s.t.:
			
$$
\begin{align}
i \in \hat{S}_{0} \implies& \hat{y}_{i} = 0 \\
j \in \hat{S}_{1} \implies& \hat{y}_{j} = 1 \\
\\
p_{i} &\geq p_{j} \\
i &\neq j \\
\end{align}
$$

- lastly, we also assume that all points $i, j$ have unique predictions $p_{i} \neq p_{j}$ (which should be reasonable for any model incorporating non-categorical predictors):

$$
\exists i \neq j \text{ s.t. }
	\left\lbrace \begin{array}{ll}
		\hat{y}_{i} = 0 \\
		\hat{y}_{j} = 1 \\
		p_{i} > p_{j} \\
	\end{array}\right.
$$


# change in F-score from change in one prediction

> suppose we have some F-score over predictions. if we change our prediction $\hat{y} _{i} = 0 \to \hat{y} _{i}' = 1$ for one point $i$, how does the expected F-score change?

TODO make $y _{i}$ completely random ->:
- $\text{TP} \to \text{TP} + \mathbb{1} \lbrace y _{i} = 1, \hat{y} _{i} = 1\rbrace$
- $\text{FP} \to \text{FP} + \mathbb{1} \lbrace y _{i} = 0, \hat{y} _{i} = 1\rbrace$
- $\text{FN} \to \text{FN} + \mathbb{1} \lbrace y _{i} = 1, \hat{y} _{i} = 0\rbrace$

(same setup) given:
- a sequence of points $\lbrace \underline{x}_{i}\rbrace _{i = 1}^{n}$
- a partition for which we predict positively and negatively:
	- $\hat{S} _{0} = \lbrace i \mid \hat{y} _{i} = 0\rbrace$
	- $\hat{S} _{1} = \lbrace i \mid \hat{y} _{i} = 1\rbrace$
	- $\hat{S} _{0} \cup \hat{S} _{1} = \lbrace 1, \dots, n\rbrace$
	- $\hat{S} _{0} \cap \hat{S} _{1} = \varnothing$
- some UNKNOWN prediction measures $\text{TP}, \text{FP}, \text{FN}$, given our prediction partition stated above
	- specifically, we don't know the actual response values $\lbrace y_{i}\rbrace_{i = 1}^{n}$
- some probability of each response value being positive $p_{i} := \Pr (y_{i} = 1)$

suppose we change the prediction from negative to positive of exactly one data point $i$:

$$
\begin{align}
\hat{y}_{i} &= 0 \\
\hat{y}_{i}' &= 1 \\
\hat{y}_{j} &= \hat{y}_{j}' && \forall j \neq i
\end{align}
$$

-> our new prediction measures are then:

$$
\begin{align}
\text{TP}'
	&= \text{TP}
		\cancel{- \mathbb{1} \left\lbrace y_{i} = 1, \hat{y}_{i} = 1\right\rbrace}
		+ \mathbb{1} \left\lbrace y_{i} = 1, \cancel{\hat{y}_{i}' = 1}\right\rbrace
		\\
	&= \text{TP}
		+ \mathbb{1} \left\lbrace y_{i} = 1\right\rbrace
		\\
	\\
	&= \left\lbrace \begin{array}{ll}
			\text{TP} & y_{i} = 0 \\
			\text{TP} + 1 & y_{i} = 1 \\
		\end{array}\right.
		\\
\\
\text{FP}'
	&= \text{FP}
		\cancel{- \mathbb{1} \left\lbrace y_{i} = 0, \hat{y}_{i} = 1\right\rbrace}
		+ \mathbb{1} \left\lbrace y_{i} = 0, \cancel{\hat{y}_{i}' = 1}\right\rbrace
		\\
	&= \text{FP}
		+ \mathbb{1} \left\lbrace y_{i} = 0\right\rbrace
		\\
	\\
	&= \left\lbrace \begin{array}{ll}
			\text{FP} + 1 & y_{i} = 0 \\
			\text{FP} & y_{i} = 1 \\
		\end{array}\right.
		\\
\\
\text{FN}'
	&= \text{FN}
		- \mathbb{1} \left\lbrace y_{i} = 1, \cancel{\hat{y}_{i} = 0}\right\rbrace
		\cancel{+ \mathbb{1} \left\lbrace y_{i} = 1, \hat{y}_{i}' = 0\right\rbrace}
		\\
	&= \text{FN}
		- \mathbb{1} \left\lbrace y_{i} = 1\right\rbrace
		\\
	\\
	&= \left\lbrace \begin{array}{ll}
			\text{FN} & y_{i} = 0 \\
			\text{FN} - 1 & y_{i} = 1 \\
		\end{array}\right.
		\\
\end{align}
$$

-> the expected new F-score would then be:

$$
\begin{align}
E \left[F_{1}'\right]
	&= E \left[\frac{2 \text{TP}'}{2 \text{TP}' + \text{FP}' + \text{FN}'}\right] \\
	&= \sum_{y_{i} \in \lbrace 0, 1\rbrace} \Pr(y_{i})
		\cdot \left(\frac
			{2 \text{TP}'}
			{2 \text{TP}' + \text{FP}' + \text{FN}'}
			\mid y_{i}
			\right)
		\\
	&= \Pr(y_{i} = 0)
			\cdot \left(
				\frac{2 \text{TP}'}{2 \text{TP}' + \text{FP}' + \text{FN}'}
				\mid y_{i} = 0
				\right)
			\\
		&\hspace{1cm} + \Pr(y_{i} = 1)
			\cdot \left(
				\frac{2 \text{TP}'}{2 \text{TP}' + \text{FP}' + \text{FN}'}
				\mid y_{i} = 1
				\right)
			\\
		\\
	&= (1 - p_{i})
			\cdot \left(
				\frac{2 (\text{TP})}{2 (\text{TP}) + (\text{FP} + 1) + (\text{FN})}
			\right)
			\\
		&\hspace{1cm} + (p_{i})
			\cdot \left(
				\frac{2 (\text{TP} + 1)}{2 (\text{TP} + 1) + (\text{FP}) + (\text{FN} - 1)}
			\right)
			\\
		\\
	&= (1 \cancel{- p_{i}}) \left(
				\frac{2 \text{TP}}{2 \text{TP} + \text{FP} + \text{FN} + 1}
			\right)
			\\
		&\hspace{1cm} \cancel{+ p_{i} \left(
				\frac{2 \text{TP}}{2 \text{TP} + \text{FP} + \text{FN} + 1}
			\right)}
			\\
		&\hspace{1cm} + p_{i} \left(
				\frac{2}{2 \text{TP} + \text{FP} + \text{FN} + 1}
			\right)
			\\
		\\
	&= \frac
		{2 (\text{TP} + p_{i})}
		{2 \text{TP} + \text{FP} + \text{FN} + 1}
		\\
\end{align}
$$

-> compared to the old F-score:

$$
\begin{align}
&&E [F_{1}] &\lessgtr E \left[F_{1}'\right] \\
\iff &&\frac
	{2 \text{TP}}
	{2 \text{TP} + \text{FP} + \text{FN}}
	&\lessgtr \frac
		{2 (\text{TP} + p_{i})}
		{2 \text{TP} + \text{FP} + \text{FN} + 1}
	\\
\iff &&
	2 \text{TP} (\cancel{2 \text{TP} + \text{FP} + \text{FN}} + 1)
	&\lessgtr 2 (\cancel {\text{TP}} + p_{i}) (2 \text{TP} + \text{FP} + \text{FN})
	&& \text{denominators $> 0$}
	\\
\iff &&
	2 \text{TP}
	&\lessgtr 2 p_{i} (2 \text{TP} + \text{FP} + \text{FN})
	\\
\iff &&
	\frac{1}{2} F_{1} =
	\frac{\text{TP}}{2 \text{TP} + \text{FP} + \text{FN}}
	&\lessgtr p_{i}
	&& \text{denominator $> 0$}
	\\
\end{align}
$$

thus:

$$
\to \boxed{
	p_{i} > \frac{1}{2} F_{1}
	\implies E \left[F_{1}'\right] > E [F_{1}]
}
$$

where $F _{1}'$ is the F-score after switching predictions

## implication - $T _{p} = \frac{1}{2} F _{1}$

we have shown that converting a negative prediction to a positive prediction will increase the F-score iff that point's positive response probability is more than half of the current F-score.

more generally, applying this repeatedly yields that **the optimal threshold is half the optimal F-score**.

# optimal long-run threshold as a function of CDF

> suppose we have a cumulative distribution function (c.d.f.) $F$ that describes the long-run distribution of any given point's positive response probability:
> 
> $$
F(p)
	:= \Pr \left(\Pr \left(y_{i} = 1 \mid \underline{x}_{i}\right) < p \right)
$$
> 
> what is the optimal threshold for maximizing the long-run F-score for this prediction model?

given:
- a sequence of points $\lbrace \underline{x}_{i}\rbrace _{i = 1}^{n}$
- some probability of each response value being positive $p_{i} := \Pr (y_{i} = 1)$
- a c.d.f. characterizing the long-run distribution of positive response probabilities:

$$
F _{P}(p)
	:= \Pr \left(\Pr \left(y_{i} = 1 \mid \underline{x}_{i}\right) < p \right)
$$

- a threshold $T _{p}$ on the positive response probabilities $p _{i}$ that dictates the response prediction, s.t.:

$$
\hat{y} _{i} = \mathbb{1} \lbrace p _{i} \geq T _{p}\rbrace
$$

the long-run prediction measures are then:

$$
\begin{align}
\lim _{n \to \infty} \text{TP} / n
	&= \lim _{n \to \infty} (1 / n)
		\left|\lbrace i \mid y _{i} = 1, \hat{y} _{i} = 1\rbrace \right|
		\\
	&= \lim _{n \to \infty} \cancel{(1 / n) n} \Pr \left(y _{i} = 1, \hat{y} _{i} = 1\right) \\
	&= \Pr \left(y _{i} = 1 \mid \hat{y} _{i} = 1\right)
		\Pr \left(\hat{y} _{i} = 1\right)
		\\
	&= E \left[p _{i} \mid p _{i} \geq T _{p}\right] (1 - F _{P}(T _{p})) \\
	&= \cancel{(1 - F _{P}(T _{p}))}
		\int _{T _{p}}^{1} p \ \frac{f _{P} (p)}{\cancel{1 - F _{P}(T _{p})}} \ dp
		\\
	&= \int _{T _{p}}^{1} p \ f _{P} (p) \ dp \\
\\
\lim _{n \to \infty} \text{FP} / n
	&= \lim _{n \to \infty} (1 / n)
		\left|\lbrace i \mid y _{i} = 0, \hat{y} _{i} = 1\rbrace\right|
		\\
	&= \lim _{n \to \infty} \cancel{(1 / n) n} \Pr \left(y _{i} = 0, \hat{y} _{i} = 1\right)
		\\
	&= \Pr \left(y _{i} = 0 \mid \hat{y} _{i} = 1\right)
		\Pr \left(\hat{y} _{i} = 1\right)
		\\
	&= E \left[(1 - p _{i}) \mid p _{i} \geq T _{p}\right]
		\left(1 - F _{P} (T _{p})\right)
		\\
	&= \left(1 - E \left[p _{i} \mid p _{i} \geq T _{p}\right]\right)
		\left(1 - F _{P} (T _{p})\right)
		\\
	&= 1 - F _{P} (T _{p}) - \int _{T _{p}}^{1} p \ f _{P} (p) \ dp \\
\\
\lim _{n \to \infty} \text{FN} / n
	&= \lim _{n \to \infty} (1 / n) 
		\left|\lbrace i \mid y _{i} = 1, \hat{y} _{i} = 0\rbrace\right|
		\\
	&= \lim _{n \to \infty} \cancel{(1 / n) n}
		\Pr \left(y _{i} = 1, \hat{y} _{i} = 0\right)
		\\
	&= \Pr \left(y _{i} = 1 \mid \hat{y} _{i} = 0\right)
		\Pr \left(\hat{y} _{i} = 0\right)
		\\
	&= E \left[p _{i} \mid p _{i} < T _{p}\right] \left(F _{P} (T _{p})\right) \\
	&= \cancel{F _{P}(T _{p})} \int _{0}^{T _{p}} p \ \frac{f _{P} (p)}{\cancel{F _{P}(T _{p})}} \ dp \\
	&= \int _0^{T _{p}} p \ f _{P} (p) \ dp \\
\\
\end{align}
$$


the long-run F-score is then:

$$
\begin{align}
\lim _{n \to \infty} F _{1}
	&= \lim_{n \to \infty} \frac{2 \text{TP}}{2 \text{TP} + \text{FP} + \text{FN}} \\
	&= \frac
		{2 \left(\int _{T _{p}}^{1} p \ f _{P} (p) \ dp\right)}
		{
			\cancel{2} \left(\int _{T _{p}}^{1} p \ f _{P} (p) \ dp\right)
			+ \left(1 - F _{P}(T _{p}) \cancel{- \int _{T _{p}}^{1} p \ f _{P} (p) \ dp}\right)
			+ \left(\int _0^{T _{p}} p \ f _{P} (p) \ dp\right)
		}
		\\
	&= \frac
		{2 \int _{T _{p}}^{1} p \ f _{P} (p) \ dp}
		{1 - F _{P}(T _{p}) + \int _0^{T _{p}} p \ f _{P} (p) \ dp + \int _{T _{p}}^{1} p \ f _{P} (p) \ dp}
		\\
	&= \frac
		{2 \int _{T _{p}}^{1} p \ f _{P} (p) \ dp}
		{1 - F _{P}(T _{p}) + E [P]}
		\\
\end{align}
$$

the maximum of the long-run F-score will occur at an inflection point

-> calculate the derivative w.r.t. $T _{p}$ and set it to zero:

$$
\begin{align}
0 = \frac{d}{d T _{p}} \lim _{n \to \infty} F _{1}
	&= \frac{d}{d T _{p}} \left(\frac
		{2 \int _{T _{p}}^{1} p \ f _{P} (p) \ dp}
		{1 - F _{P}(T _{p}) + E [P]}
		\right)
		\\	
	&= 2 \frac
		{
			\frac{d}{d T _{p}} \left(\int _{T _{p}}^{1} p \ f _{P} (p) \ dp\right)
				\left(1 - F _{P}(T _{p}) + E [P]\right)
			- \left(\int _{T _{p}}^{1} p \ f _{P} (p) \ dp\right)
				\frac{d}{d T _{p}} \left(1 - F _{P}(T _{p}) + E [P]\right)
		}
		{\left(1 - F _{P}(T _{p}) + E [P]\right)^{2}}
		\\
	0 &= 2 \frac
		{
			- T _{p} \ f _{P} (T _{p})
				\left(1 - F _{P}(T _{p}) + E [P]\right)
			- \left(\int _{T _{p}}^{1} p \ f _{P} (p) \ dp\right)
				\left(-f _{P}(T _{p})\right)
		}
		{\left(1 - F _{P}(T _{p}) + E [P]\right)^{2}}
		\\
\to 0 &= - T _{p} \ f _{P} (T _{p})
			\left(1 - F _{P}(T _{p}) + E [P]\right)
		\cancel{-} \left(\int _{T _{p}}^{1} p \ f _{P} (p) \ dp\right)
			\left(\cancel{-}f _{P}(T _{p})\right)
		\\
\to T _{p} \ \cancel{f _{P} (T _{p})} \left(1 - F _{P}(T _{p}) + E [P]\right)
	&= \cancel{f _{P}(T _{p})} \left(\int _{T _{p}}^{1} p \ f _{P} (p) \ dp\right)
	\\
\to T _{p} \left(1 - F _{P}(T _{p}) + E [P]\right)
	&= \left(\int _{T _{p}}^{1} p \ f _{P} (p) \ dp\right)
	\\
\end{align}
$$

## for uniform distribution

$$
\begin{align}
f(p) &:= 1 \\
F (p) &= x \\
E[P] &= \frac{1}{2} \\
\end{align}
$$

->:

$$
\begin{align}
\to T _{p} \left(1 - F _{P}(T _{p}) + E [P]\right)
	&= \left(\int _{T _{p}}^{1} p \ f _{P} (p) \ dp\right)
	\\
\to T _{p} \left(1 - (T _{p}) + \frac{1}{2}\right)
	&= \left(\int _{T _{p}}^{1} p \ (1) \ dp\right)
	\\
\to T _{p} \left(\frac{3}{2} - T _{p}\right)
	&= \left(1 - T _{p}\right)
	\\
\to \frac{3}{2} T _{p} - T _{p}^{2} - 1 + T _{p}
	&= 0
	\\
\to T _{p}^{2} - \frac{5}{2} T _{p} + 1
	&= 0
	\\
\to T _{p}
	&= \frac{- \left(- \frac{5}{2}\right) \pm \sqrt{\left(- \frac{5}{2}\right)^{2} - 4 (1) (1)}}{2 (1)}
	\\
	&= \frac{\frac{5}{2} \pm \sqrt{\frac{25}{4} - \frac{16}{4}}}{2} \\
	&= \frac{\frac{5}{2} \pm \frac{3}{2}}{2} \\
	&= \frac{5}{4} \pm \frac{3}{4} \\
	&= \left\lbrace \cancel{\frac{8}{4}}, \frac{2}{4}\right\rbrace \\
	&= \frac{1}{2} \\
\end{align}
$$
