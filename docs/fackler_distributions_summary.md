# Summary of Distributions in the Fackler Paper

**Source:** Fackler, M. (2013). "Reinventing Pareto: Fits for both small and large losses." ASTIN Colloquium, The Hague.

The paper discusses distributions for modeling insurance losses, focusing on fitting both small/medium losses and heavy tails simultaneously.

## Core Pareto Family

| Distribution | Description |
|-------------|-------------|
| **Pareto (Type I / Single-parameter)** | The classic reinsurance tail model: F̄(x) = (θ/x)^α. Has a "memoryless" property where α remains invariant across different thresholds. |
| **GPD (Generalized Pareto Distribution)** | F̄(x\|X>θ) = ((θ+λ)/(x+λ))^α. Adds parameter λ (a "shift" from Pareto). Both α and λ are invariant when modeling higher tails. |
| **Lomax (Pareto Type II / American Pareto)** | Special case of GPD with λ>0 and θ=0. A ground-up model for losses of any size. |
| **Burr** | Three-parameter generalization: (1/(1+(x/λ)^τ))^α. Allows unimodal bell-curve densities when τ>1. |

## Spliced Models (Body + GPD/Pareto Tail)

The paper develops a framework of spliced distributions combining different "body" distributions for small losses with GPD/Pareto tails:

| Body Distribution | Variants |
|-------------------|----------|
| **Lognormal-GPD/Pareto** | LN-GPD-0/1/2, LN-Par-0/1/2, pLN-GPD-0/1, pLN-Par-0/1. The **pLN-Par-1 (Czeledin distribution)** is popular in reinsurance. |
| **Weibull-GPD/Pareto** | Wei-GPD-1/2/3, Wei-Par-1/2 |
| **Exponential-GPD/Pareto** | Exp-GPD-2, Exp-Par-2, pExp-Par-1 |
| **Power function-GPD/Pareto** | Pow-GPD-0/1/2, Pow-Par-0/1 (related to **Log-Laplace / double Pareto**) |

## Mixed Distributions

- **4-parameter Pareto** and **5-parameter Pareto**: Mixtures of Lomax distributions

## Modifications

- **Right censoring/truncation**: For bounded losses (X ≤ Max)
- **Local Pareto alpha**: α_d = d·f(d)/F̄(d) — allows Pareto-like analysis of any smooth distribution

## Key Insights

1. All models with GPD/Pareto tails remain comparable via the threshold-invariant parameters α and λ
2. Spliced models allow fitting both the body (small/medium losses) and tail (large losses) accurately
3. The smoothness level (C0, C1, C2) determines how many parameters are needed
4. Market benchmarks for α values can be established across different data sources

## References

- [Pareto Distribution (Wikipedia)](https://en.wikipedia.org/wiki/Pareto_distribution)
- [Generalized Pareto Distribution (Wikipedia)](https://en.wikipedia.org/wiki/Generalized_Pareto_distribution)
- [Lomax Distribution (Wikipedia)](https://en.wikipedia.org/wiki/Lomax_distribution)
- [Burr Distribution (Wikipedia)](https://en.wikipedia.org/wiki/Burr_distribution)
- [Log-normal Distribution (Wikipedia)](https://en.wikipedia.org/wiki/Log-normal_distribution)
- [Weibull Distribution (Wikipedia)](https://en.wikipedia.org/wiki/Weibull_distribution)
