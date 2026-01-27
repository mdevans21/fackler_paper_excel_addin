"""
Fackler Distributions: Implementation of loss severity distributions from:

Fackler, M. (2013). "Reinventing Pareto: Fits for both small and large losses."
ASTIN Colloquium, The Hague.

This module implements the Pareto family of distributions and their extensions,
including spliced models that combine different body distributions with heavy tails.

References:
- Original paper: reference/Fackler_Paper_Hague2013.pdf
- Pareto: https://en.wikipedia.org/wiki/Pareto_distribution
- GPD: https://en.wikipedia.org/wiki/Generalized_Pareto_distribution
- Lomax: https://en.wikipedia.org/wiki/Lomax_distribution
- Burr: https://en.wikipedia.org/wiki/Burr_distribution
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, Tuple
import numpy as np
from scipy import stats
from scipy.special import ndtr  # Standard normal CDF (Phi)


def phi(z: np.ndarray) -> np.ndarray:
    """Standard normal PDF."""
    return np.exp(-0.5 * z**2) / np.sqrt(2 * np.pi)


def Phi(z: np.ndarray) -> np.ndarray:
    """Standard normal CDF."""
    return ndtr(z)


class Distribution(ABC):
    """Abstract base class for probability distributions."""

    name: str = "Distribution"
    description: str = ""
    wikipedia_url: str = ""

    @abstractmethod
    def pdf(self, x: np.ndarray) -> np.ndarray:
        """Probability density function."""
        pass

    @abstractmethod
    def cdf(self, x: np.ndarray) -> np.ndarray:
        """Cumulative distribution function."""
        pass

    def sf(self, x: np.ndarray) -> np.ndarray:
        """Survival function F̄(x) = 1 - F(x) = P(X > x)."""
        return 1 - self.cdf(x)

    @abstractmethod
    def params_dict(self) -> dict:
        """Return parameters as a dictionary."""
        pass

    def __repr__(self) -> str:
        params = ", ".join(f"{k}={v}" for k, v in self.params_dict().items())
        return f"{self.name}({params})"


# =============================================================================
# Core Pareto Family
# =============================================================================

@dataclass
class Pareto(Distribution):
    """
    Pareto Type I (Single-parameter Pareto / European Pareto)

    The classic reinsurance tail model with survival function:
        F̄(x) = (θ/x)^α for x ≥ θ

    Key property: Parameter α is invariant when modeling higher tails.
    This "memoryless" property makes it ideal for comparing tails across
    different reporting thresholds.

    Parameters:
        alpha (α): Shape parameter (tail index), α > 0
        theta (θ): Scale parameter (minimum value), θ > 0

    References:
        - https://en.wikipedia.org/wiki/Pareto_distribution
        - Fackler (2013), Section 2
    """
    alpha: float
    theta: float

    name: str = "Pareto"
    description: str = "Pareto Type I (Single-parameter Pareto)"
    wikipedia_url: str = "https://en.wikipedia.org/wiki/Pareto_distribution"

    def __post_init__(self):
        if self.alpha <= 0:
            raise ValueError("alpha must be positive")
        if self.theta <= 0:
            raise ValueError("theta must be positive")

    def pdf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.zeros_like(x)
        mask = x >= self.theta
        result[mask] = (self.alpha * self.theta**self.alpha) / x[mask]**(self.alpha + 1)
        return result

    def cdf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.zeros_like(x)
        mask = x >= self.theta
        result[mask] = 1 - (self.theta / x[mask])**self.alpha
        return result

    def sf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.ones_like(x)
        mask = x >= self.theta
        result[mask] = (self.theta / x[mask])**self.alpha
        return result

    def mean(self) -> float:
        """Expected value (only exists for α > 1)."""
        if self.alpha <= 1:
            return np.inf
        return (self.alpha * self.theta) / (self.alpha - 1)

    def params_dict(self) -> dict:
        return {"alpha": self.alpha, "theta": self.theta}


@dataclass
class GPD(Distribution):
    """
    Generalized Pareto Distribution (GPD)

    A generalization of Pareto with survival function:
        F̄(x|X > θ) = ((θ + λ) / (x + λ))^α for x ≥ θ

    The parametrization follows Scollnik's approach where both α and λ
    are invariant when modeling higher tails. This makes GPD ideal for
    tail comparisons across different thresholds.

    Parameters:
        alpha (α): Shape parameter, α > 0
        lambda_ (λ): Shift parameter, λ > -θ
        theta (θ): Threshold parameter, θ ≥ 0

    Special cases:
        - λ = 0: Reduces to Pareto
        - λ > 0, θ = 0: Lomax distribution

    References:
        - https://en.wikipedia.org/wiki/Generalized_Pareto_distribution
        - Fackler (2013), Section 3
    """
    alpha: float
    lambda_: float
    theta: float = 0.0

    name: str = "GPD"
    description: str = "Generalized Pareto Distribution"
    wikipedia_url: str = "https://en.wikipedia.org/wiki/Generalized_Pareto_distribution"

    def __post_init__(self):
        if self.alpha <= 0:
            raise ValueError("alpha must be positive")
        if self.lambda_ <= -self.theta:
            raise ValueError("lambda must be greater than -theta")

    def pdf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.zeros_like(x)
        mask = x >= self.theta
        x_shifted = x[mask] + self.lambda_
        theta_shifted = self.theta + self.lambda_
        result[mask] = (self.alpha * theta_shifted**self.alpha) / x_shifted**(self.alpha + 1)
        return result

    def cdf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.zeros_like(x)
        mask = x >= self.theta
        x_shifted = x[mask] + self.lambda_
        theta_shifted = self.theta + self.lambda_
        result[mask] = 1 - (theta_shifted / x_shifted)**self.alpha
        return result

    def sf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.ones_like(x)
        mask = x >= self.theta
        x_shifted = x[mask] + self.lambda_
        theta_shifted = self.theta + self.lambda_
        result[mask] = (theta_shifted / x_shifted)**self.alpha
        return result

    def local_pareto_alpha(self, d: float) -> float:
        """
        Local Pareto alpha at point d.

        α_d = (d / (d + λ)) * α

        For GPD, this shows how the effective tail index varies with threshold.
        """
        return (d / (d + self.lambda_)) * self.alpha

    def params_dict(self) -> dict:
        return {"alpha": self.alpha, "lambda": self.lambda_, "theta": self.theta}


@dataclass
class Lomax(Distribution):
    """
    Lomax Distribution (Pareto Type II / American Pareto / Two-parameter Pareto)

    A special case of GPD with θ = 0, giving survival function:
        F̄(x) = (λ / (x + λ))^α = (1 / (1 + x/λ))^α for x ≥ 0

    Unlike Pareto Type I, Lomax is a ground-up distribution starting at 0,
    making it suitable for modeling losses of any size.

    Parameters:
        alpha (α): Shape parameter, α > 0
        lambda_ (λ): Scale parameter, λ > 0

    References:
        - https://en.wikipedia.org/wiki/Lomax_distribution
        - Fackler (2013), Section 3-4
    """
    alpha: float
    lambda_: float

    name: str = "Lomax"
    description: str = "Lomax (Pareto Type II)"
    wikipedia_url: str = "https://en.wikipedia.org/wiki/Lomax_distribution"

    def __post_init__(self):
        if self.alpha <= 0:
            raise ValueError("alpha must be positive")
        if self.lambda_ <= 0:
            raise ValueError("lambda must be positive")

    def pdf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.zeros_like(x)
        mask = x >= 0
        result[mask] = (self.alpha / self.lambda_) * (1 + x[mask] / self.lambda_)**(-(self.alpha + 1))
        return result

    def cdf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.zeros_like(x)
        mask = x >= 0
        result[mask] = 1 - (1 + x[mask] / self.lambda_)**(-self.alpha)
        return result

    def sf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.ones_like(x)
        mask = x >= 0
        result[mask] = (1 + x[mask] / self.lambda_)**(-self.alpha)
        return result

    def mean(self) -> float:
        """Expected value (only exists for α > 1)."""
        if self.alpha <= 1:
            return np.inf
        return self.lambda_ / (self.alpha - 1)

    def params_dict(self) -> dict:
        return {"alpha": self.alpha, "lambda": self.lambda_}


@dataclass
class Burr(Distribution):
    """
    Burr Distribution (Burr Type XII)

    A three-parameter generalization of Lomax with survival function:
        F̄(x) = (1 / (1 + (x/λ)^τ))^α for x ≥ 0

    The Burr distribution provides more flexibility than Lomax:
    - τ < 1: Strictly decreasing density (mode at 0)
    - τ = 1: Reduces to Lomax
    - τ > 1: Unimodal bell-curve density (positive mode)

    For large x, asymptotically tends to Pareto with exponent ατ.

    Parameters:
        alpha (α): Shape parameter, α > 0
        lambda_ (λ): Scale parameter, λ > 0
        tau (τ): Shape parameter, τ > 0

    References:
        - https://en.wikipedia.org/wiki/Burr_distribution
        - Fackler (2013), Section 4
    """
    alpha: float
    lambda_: float
    tau: float

    name: str = "Burr"
    description: str = "Burr Type XII Distribution"
    wikipedia_url: str = "https://en.wikipedia.org/wiki/Burr_distribution"

    def __post_init__(self):
        if self.alpha <= 0:
            raise ValueError("alpha must be positive")
        if self.lambda_ <= 0:
            raise ValueError("lambda must be positive")
        if self.tau <= 0:
            raise ValueError("tau must be positive")

    def pdf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.zeros_like(x)
        mask = x > 0
        z = (x[mask] / self.lambda_)**self.tau
        result[mask] = (self.alpha * self.tau / self.lambda_) * \
                       (x[mask] / self.lambda_)**(self.tau - 1) * \
                       (1 + z)**(-(self.alpha + 1))
        return result

    def cdf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.zeros_like(x)
        mask = x >= 0
        z = (x[mask] / self.lambda_)**self.tau
        result[mask] = 1 - (1 + z)**(-self.alpha)
        return result

    def sf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.ones_like(x)
        mask = x >= 0
        z = (x[mask] / self.lambda_)**self.tau
        result[mask] = (1 + z)**(-self.alpha)
        return result

    def asymptotic_pareto_alpha(self) -> float:
        """The asymptotic Pareto exponent for large x."""
        return self.alpha * self.tau

    def params_dict(self) -> dict:
        return {"alpha": self.alpha, "lambda": self.lambda_, "tau": self.tau}


# =============================================================================
# Spliced Distributions
# =============================================================================

@dataclass
class LognormalPareto(Distribution):
    """
    Lognormal-Pareto Spliced Distribution (pLN-Par-1 / Czeledin Distribution)

    A spliced model combining:
    - Body: Lognormal distribution for small/medium losses (x < θ)
    - Tail: Pareto distribution for large losses (x ≥ θ)

    The survival function is:
        F̄(x) = 1 - Φ((ln(x) - μ) / σ)  for x < θ
        F̄(x) = (1 - Φ_θ) * (θ/x)^α     for x ≥ θ

    where α is determined by the C1 (continuous PDF) condition:
        α = φ_θ / (σ * (1 - Φ_θ))

    This is the "Czeledin distribution" introduced by Knecht & Küttel (2003).

    Parameters:
        mu (μ): Lognormal location parameter
        sigma (σ): Lognormal scale parameter, σ > 0
        theta (θ): Splicing threshold, θ > 0

    References:
        - Fackler (2013), Section 5
        - Knecht & Küttel (2003), "The Czeledin distribution function"
        - Scollnik (2007), "On composite Lognormal-Pareto models"
    """
    mu: float
    sigma: float
    theta: float

    name: str = "LognormalPareto"
    description: str = "Lognormal-Pareto Spliced (Czeledin)"
    wikipedia_url: str = "https://en.wikipedia.org/wiki/Log-normal_distribution"

    def __post_init__(self):
        if self.sigma <= 0:
            raise ValueError("sigma must be positive")
        if self.theta <= 0:
            raise ValueError("theta must be positive")

        # Compute derived parameters
        self._z_theta = (np.log(self.theta) - self.mu) / self.sigma
        self._Phi_theta = Phi(self._z_theta)
        self._phi_theta = phi(self._z_theta)

        # Alpha from C1 condition (continuous PDF)
        self._alpha = self._phi_theta / (self.sigma * (1 - self._Phi_theta))

    @property
    def alpha(self) -> float:
        """The Pareto tail index (derived from smoothness condition)."""
        return self._alpha

    def pdf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.zeros_like(x)

        # Body: Lognormal PDF
        mask_body = (x > 0) & (x < self.theta)
        if np.any(mask_body):
            z = (np.log(x[mask_body]) - self.mu) / self.sigma
            result[mask_body] = phi(z) / (x[mask_body] * self.sigma)

        # Tail: Pareto PDF
        mask_tail = x >= self.theta
        if np.any(mask_tail):
            result[mask_tail] = (1 - self._Phi_theta) * self._alpha * \
                               self.theta**self._alpha / x[mask_tail]**(self._alpha + 1)

        return result

    def cdf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.zeros_like(x)

        # Body: Lognormal CDF
        mask_body = (x > 0) & (x < self.theta)
        if np.any(mask_body):
            z = (np.log(x[mask_body]) - self.mu) / self.sigma
            result[mask_body] = Phi(z)

        # Tail: Spliced Pareto CDF
        mask_tail = x >= self.theta
        if np.any(mask_tail):
            result[mask_tail] = 1 - (1 - self._Phi_theta) * \
                               (self.theta / x[mask_tail])**self._alpha

        return result

    def params_dict(self) -> dict:
        return {"mu": self.mu, "sigma": self.sigma, "theta": self.theta,
                "alpha (derived)": round(self._alpha, 4)}


@dataclass
class LognormalGPD(Distribution):
    """
    Lognormal-GPD Spliced Distribution (LN-GPD-1)

    A spliced model combining:
    - Body: Lognormal distribution (possibly distorted) for x < θ
    - Tail: GPD distribution for x ≥ θ

    More flexible than LognormalPareto due to the additional λ parameter.

    Parameters:
        mu (μ): Lognormal location parameter
        sigma (σ): Lognormal scale parameter, σ > 0
        theta (θ): Splicing threshold, θ > 0
        lambda_ (λ): GPD shift parameter, λ > -θ
        r: Body weight (probability of X ≤ θ), 0 < r < 1

    References:
        - Fackler (2013), Section 5
        - Scollnik (2007), "On composite Lognormal-Pareto models"
    """
    mu: float
    sigma: float
    theta: float
    lambda_: float
    r: float

    name: str = "LognormalGPD"
    description: str = "Lognormal-GPD Spliced Distribution"
    wikipedia_url: str = "https://en.wikipedia.org/wiki/Generalized_Pareto_distribution"

    def __post_init__(self):
        if self.sigma <= 0:
            raise ValueError("sigma must be positive")
        if self.theta <= 0:
            raise ValueError("theta must be positive")
        if self.lambda_ <= -self.theta:
            raise ValueError("lambda must be greater than -theta")
        if not (0 < self.r < 1):
            raise ValueError("r must be between 0 and 1")

        # Compute derived parameters
        self._z_theta = (np.log(self.theta) - self.mu) / self.sigma
        self._Phi_theta = Phi(self._z_theta)
        self._phi_theta = phi(self._z_theta)

        # Alpha from C1 condition
        self._alpha = ((self.theta + self.lambda_) / self.theta) * \
                      (self._phi_theta / (self.sigma * self._Phi_theta)) * \
                      (self.r / (1 - self.r))

    @property
    def alpha(self) -> float:
        """The GPD tail index (derived from smoothness condition)."""
        return self._alpha

    def pdf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.zeros_like(x)

        # Body: Distorted Lognormal PDF
        mask_body = (x > 0) & (x < self.theta)
        if np.any(mask_body):
            z = (np.log(x[mask_body]) - self.mu) / self.sigma
            # Distortion factor: r / Phi_theta
            result[mask_body] = (self.r / self._Phi_theta) * \
                               phi(z) / (x[mask_body] * self.sigma)

        # Tail: GPD PDF
        mask_tail = x >= self.theta
        if np.any(mask_tail):
            theta_shifted = self.theta + self.lambda_
            x_shifted = x[mask_tail] + self.lambda_
            result[mask_tail] = (1 - self.r) * self._alpha * \
                               theta_shifted**self._alpha / x_shifted**(self._alpha + 1)

        return result

    def cdf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.zeros_like(x)

        # Body: Distorted Lognormal CDF
        mask_body = (x > 0) & (x < self.theta)
        if np.any(mask_body):
            z = (np.log(x[mask_body]) - self.mu) / self.sigma
            result[mask_body] = (self.r / self._Phi_theta) * Phi(z)

        # Tail: Spliced GPD CDF
        mask_tail = x >= self.theta
        if np.any(mask_tail):
            theta_shifted = self.theta + self.lambda_
            x_shifted = x[mask_tail] + self.lambda_
            result[mask_tail] = 1 - (1 - self.r) * \
                               (theta_shifted / x_shifted)**self._alpha

        return result

    def params_dict(self) -> dict:
        return {"mu": self.mu, "sigma": self.sigma, "theta": self.theta,
                "lambda": self.lambda_, "r": self.r,
                "alpha (derived)": round(self._alpha, 4)}


@dataclass
class WeibullPareto(Distribution):
    """
    Weibull-Pareto Spliced Distribution (Wei-Par-1)

    A spliced model combining:
    - Body: Weibull distribution for small/medium losses (x < θ)
    - Tail: Pareto distribution for large losses (x ≥ θ)

    The Weibull body provides flexibility:
    - k < 1: Strictly decreasing density
    - k = 1: Exponential distribution
    - k > 1: Unimodal bell-curve density

    Parameters:
        k: Weibull shape parameter, k > 0
        scale (λ): Weibull scale parameter, λ > 0
        theta (θ): Splicing threshold, θ > 0
        r: Body weight (probability of X ≤ θ), 0 < r < 1

    References:
        - Fackler (2013), Section 6
        - Scollnik & Sun (2012), "Modeling with Weibull-Pareto models"
    """
    k: float
    scale: float
    theta: float
    r: float

    name: str = "WeibullPareto"
    description: str = "Weibull-Pareto Spliced Distribution"
    wikipedia_url: str = "https://en.wikipedia.org/wiki/Weibull_distribution"

    def __post_init__(self):
        if self.k <= 0:
            raise ValueError("k must be positive")
        if self.scale <= 0:
            raise ValueError("scale must be positive")
        if self.theta <= 0:
            raise ValueError("theta must be positive")
        if not (0 < self.r < 1):
            raise ValueError("r must be between 0 and 1")

        # Weibull CDF at theta
        self._F_theta = 1 - np.exp(-(self.theta / self.scale)**self.k)

        # Weibull PDF at theta
        self._f_theta = (self.k / self.scale) * (self.theta / self.scale)**(self.k - 1) * \
                        np.exp(-(self.theta / self.scale)**self.k)

        # Alpha from C1 condition
        self._alpha = (self.r / (1 - self.r)) * (self._f_theta / self._F_theta) * self.theta

    @property
    def alpha(self) -> float:
        """The Pareto tail index (derived from smoothness condition)."""
        return self._alpha

    def pdf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.zeros_like(x)

        # Body: Distorted Weibull PDF
        mask_body = (x > 0) & (x < self.theta)
        if np.any(mask_body):
            z = x[mask_body] / self.scale
            weibull_pdf = (self.k / self.scale) * z**(self.k - 1) * np.exp(-z**self.k)
            result[mask_body] = (self.r / self._F_theta) * weibull_pdf

        # Tail: Pareto PDF
        mask_tail = x >= self.theta
        if np.any(mask_tail):
            result[mask_tail] = (1 - self.r) * self._alpha * \
                               self.theta**self._alpha / x[mask_tail]**(self._alpha + 1)

        return result

    def cdf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.zeros_like(x)

        # Body: Distorted Weibull CDF
        mask_body = (x > 0) & (x < self.theta)
        if np.any(mask_body):
            weibull_cdf = 1 - np.exp(-(x[mask_body] / self.scale)**self.k)
            result[mask_body] = (self.r / self._F_theta) * weibull_cdf

        # Tail: Spliced Pareto CDF
        mask_tail = x >= self.theta
        if np.any(mask_tail):
            result[mask_tail] = 1 - (1 - self.r) * \
                               (self.theta / x[mask_tail])**self._alpha

        return result

    def params_dict(self) -> dict:
        return {"k": self.k, "scale": self.scale, "theta": self.theta, "r": self.r,
                "alpha (derived)": round(self._alpha, 4)}


@dataclass
class ExponentialPareto(Distribution):
    """
    Exponential-Pareto Spliced Distribution (pExp-Par-1)

    A spliced model combining:
    - Body: Exponential distribution for small/medium losses (x < θ)
    - Tail: Pareto distribution for large losses (x ≥ θ)

    This is a simpler alternative to Lognormal-Pareto with one fewer parameter.
    The Exponential body always has strictly decreasing density.

    A notable property: the local Pareto alpha increases linearly from 0 to α
    across the body region.

    Parameters:
        rate (λ): Exponential rate parameter, λ > 0
        theta (θ): Splicing threshold, θ > 0

    References:
        - Fackler (2013), Section 6
        - Teodorescu & Vernic (2009)
        - Riegel (2010)
    """
    rate: float
    theta: float

    name: str = "ExponentialPareto"
    description: str = "Exponential-Pareto Spliced Distribution"
    wikipedia_url: str = "https://en.wikipedia.org/wiki/Exponential_distribution"

    def __post_init__(self):
        if self.rate <= 0:
            raise ValueError("rate must be positive")
        if self.theta <= 0:
            raise ValueError("theta must be positive")

        # Exponential CDF at theta (this is r, the body weight)
        self._r = 1 - np.exp(-self.rate * self.theta)

        # Alpha from C1 condition for proper Exponential body
        # f(θ-) = λ * exp(-λθ), and we need f(θ-) = (1-r) * α / θ
        # This gives α = θ * λ * exp(-λθ) / (1-r) = θ * λ
        self._alpha = self.theta * self.rate

    @property
    def alpha(self) -> float:
        """The Pareto tail index (derived from smoothness condition)."""
        return self._alpha

    @property
    def r(self) -> float:
        """Body weight (probability of X ≤ θ)."""
        return self._r

    def pdf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.zeros_like(x)

        # Body: Exponential PDF
        mask_body = (x >= 0) & (x < self.theta)
        if np.any(mask_body):
            result[mask_body] = self.rate * np.exp(-self.rate * x[mask_body])

        # Tail: Pareto PDF
        mask_tail = x >= self.theta
        if np.any(mask_tail):
            result[mask_tail] = (1 - self._r) * self._alpha * \
                               self.theta**self._alpha / x[mask_tail]**(self._alpha + 1)

        return result

    def cdf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.zeros_like(x)

        # Body: Exponential CDF
        mask_body = (x >= 0) & (x < self.theta)
        if np.any(mask_body):
            result[mask_body] = 1 - np.exp(-self.rate * x[mask_body])

        # Tail: Spliced Pareto CDF
        mask_tail = x >= self.theta
        if np.any(mask_tail):
            result[mask_tail] = 1 - (1 - self._r) * \
                               (self.theta / x[mask_tail])**self._alpha

        return result

    def params_dict(self) -> dict:
        return {"rate": self.rate, "theta": self.theta,
                "alpha (derived)": round(self._alpha, 4),
                "r (derived)": round(self._r, 4)}


@dataclass
class PowerPareto(Distribution):
    """
    Power Function-Pareto Spliced Distribution (Pow-Par-1 / Log-Laplace / Double Pareto)

    A spliced model combining:
    - Body: Power function for small/medium losses (x < θ)
    - Tail: Pareto distribution for large losses (x ≥ θ)

    The body CDF is (x/θ)^β, providing flexibility:
    - β < 1: Decreasing density
    - β = 1: Uniform distribution on [0, θ]
    - β > 1: Increasing density

    For the C1 (smooth) case with r = α/(α+β), this is the Log-Laplace
    or double Pareto distribution.

    Parameters:
        alpha (α): Pareto tail index, α > 0
        beta (β): Power body exponent, β > 0
        theta (θ): Splicing threshold, θ > 0

    References:
        - Fackler (2013), Section 6
        - Kozubowski & Podgórski (2003), "Log-Laplace distributions"
    """
    alpha: float
    beta: float
    theta: float

    name: str = "PowerPareto"
    description: str = "Power-Pareto (Log-Laplace / Double Pareto)"
    wikipedia_url: str = "https://en.wikipedia.org/wiki/Log-Laplace_distribution"

    def __post_init__(self):
        if self.alpha <= 0:
            raise ValueError("alpha must be positive")
        if self.beta <= 0:
            raise ValueError("beta must be positive")
        if self.theta <= 0:
            raise ValueError("theta must be positive")

        # Body weight from C1 condition
        self._r = self.alpha / (self.alpha + self.beta)

    @property
    def r(self) -> float:
        """Body weight (probability of X ≤ θ)."""
        return self._r

    def pdf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.zeros_like(x)

        # Body: Power function PDF
        mask_body = (x > 0) & (x < self.theta)
        if np.any(mask_body):
            result[mask_body] = self._r * self.beta / self.theta * \
                               (x[mask_body] / self.theta)**(self.beta - 1)

        # Tail: Pareto PDF
        mask_tail = x >= self.theta
        if np.any(mask_tail):
            result[mask_tail] = (1 - self._r) * self.alpha * \
                               self.theta**self.alpha / x[mask_tail]**(self.alpha + 1)

        return result

    def cdf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.zeros_like(x)

        # Body: Power function CDF
        mask_body = (x > 0) & (x < self.theta)
        if np.any(mask_body):
            result[mask_body] = self._r * (x[mask_body] / self.theta)**self.beta

        # Tail: Spliced Pareto CDF
        mask_tail = x >= self.theta
        if np.any(mask_tail):
            result[mask_tail] = 1 - (1 - self._r) * \
                               (self.theta / x[mask_tail])**self.alpha

        return result

    def params_dict(self) -> dict:
        return {"alpha": self.alpha, "beta": self.beta, "theta": self.theta,
                "r (derived)": round(self._r, 4)}


# =============================================================================
# Mixed Distributions
# =============================================================================

@dataclass
class FourParameterPareto(Distribution):
    """
    4-Parameter Pareto Distribution

    A mixture of two Lomax distributions with the constraint α₁ = α₂ + 2.
    This constraint reduces the parameter count while maintaining flexibility.

    Survival function:
        F̄(x) = r * (λ₁/(x+λ₁))^α₁ + (1-r) * (λ₂/(x+λ₂))^α₂

    where α₁ = α₂ + 2.

    This model has been successfully applied by ISO to general liability business.

    Parameters:
        alpha2 (α₂): Shape parameter for second component, α₂ > 0
        lambda1 (λ₁): Scale parameter for first component, λ₁ > 0
        lambda2 (λ₂): Scale parameter for second component, λ₂ > 0
        r: Mixing weight, 0 < r < 1

    References:
        - Fackler (2013), Section 4
        - Klugman et al. (2008), "Loss models"
    """
    alpha2: float
    lambda1: float
    lambda2: float
    r: float

    name: str = "FourParameterPareto"
    description: str = "4-Parameter Pareto (Lomax Mixture)"
    wikipedia_url: str = "https://en.wikipedia.org/wiki/Lomax_distribution"

    def __post_init__(self):
        if self.alpha2 <= 0:
            raise ValueError("alpha2 must be positive")
        if self.lambda1 <= 0:
            raise ValueError("lambda1 must be positive")
        if self.lambda2 <= 0:
            raise ValueError("lambda2 must be positive")
        if not (0 < self.r < 1):
            raise ValueError("r must be between 0 and 1")

        self._alpha1 = self.alpha2 + 2

    @property
    def alpha1(self) -> float:
        """Shape parameter for first component (= α₂ + 2)."""
        return self._alpha1

    def pdf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.zeros_like(x)
        mask = x >= 0

        # Component 1: Lomax with α₁, λ₁
        pdf1 = (self._alpha1 / self.lambda1) * \
               (1 + x[mask] / self.lambda1)**(-(self._alpha1 + 1))

        # Component 2: Lomax with α₂, λ₂
        pdf2 = (self.alpha2 / self.lambda2) * \
               (1 + x[mask] / self.lambda2)**(-(self.alpha2 + 1))

        result[mask] = self.r * pdf1 + (1 - self.r) * pdf2
        return result

    def cdf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.zeros_like(x)
        mask = x >= 0

        # Component 1: Lomax CDF
        cdf1 = 1 - (1 + x[mask] / self.lambda1)**(-self._alpha1)

        # Component 2: Lomax CDF
        cdf2 = 1 - (1 + x[mask] / self.lambda2)**(-self.alpha2)

        result[mask] = self.r * cdf1 + (1 - self.r) * cdf2
        return result

    def sf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.ones_like(x)
        mask = x >= 0

        # Component 1: Lomax survival
        sf1 = (1 + x[mask] / self.lambda1)**(-self._alpha1)

        # Component 2: Lomax survival
        sf2 = (1 + x[mask] / self.lambda2)**(-self.alpha2)

        result[mask] = self.r * sf1 + (1 - self.r) * sf2
        return result

    def params_dict(self) -> dict:
        return {"alpha2": self.alpha2, "alpha1 (=alpha2+2)": self._alpha1,
                "lambda1": self.lambda1, "lambda2": self.lambda2, "r": self.r}


@dataclass
class FiveParameterPareto(Distribution):
    """
    5-Parameter Pareto Distribution

    A mixture of two Lomax distributions without constraints.

    Survival function:
        F̄(x) = r * (λ₁/(x+λ₁))^α₁ + (1-r) * (λ₂/(x+λ₂))^α₂

    Parameters:
        alpha1 (α₁): Shape parameter for first component, α₁ > 0
        alpha2 (α₂): Shape parameter for second component, α₂ > 0
        lambda1 (λ₁): Scale parameter for first component, λ₁ > 0
        lambda2 (λ₂): Scale parameter for second component, λ₂ > 0
        r: Mixing weight, 0 < r < 1

    References:
        - Fackler (2013), Section 4
    """
    alpha1: float
    alpha2: float
    lambda1: float
    lambda2: float
    r: float

    name: str = "FiveParameterPareto"
    description: str = "5-Parameter Pareto (Lomax Mixture)"
    wikipedia_url: str = "https://en.wikipedia.org/wiki/Lomax_distribution"

    def __post_init__(self):
        if self.alpha1 <= 0:
            raise ValueError("alpha1 must be positive")
        if self.alpha2 <= 0:
            raise ValueError("alpha2 must be positive")
        if self.lambda1 <= 0:
            raise ValueError("lambda1 must be positive")
        if self.lambda2 <= 0:
            raise ValueError("lambda2 must be positive")
        if not (0 < self.r < 1):
            raise ValueError("r must be between 0 and 1")

    def pdf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.zeros_like(x)
        mask = x >= 0

        # Component 1
        pdf1 = (self.alpha1 / self.lambda1) * \
               (1 + x[mask] / self.lambda1)**(-(self.alpha1 + 1))

        # Component 2
        pdf2 = (self.alpha2 / self.lambda2) * \
               (1 + x[mask] / self.lambda2)**(-(self.alpha2 + 1))

        result[mask] = self.r * pdf1 + (1 - self.r) * pdf2
        return result

    def cdf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.zeros_like(x)
        mask = x >= 0

        cdf1 = 1 - (1 + x[mask] / self.lambda1)**(-self.alpha1)
        cdf2 = 1 - (1 + x[mask] / self.lambda2)**(-self.alpha2)

        result[mask] = self.r * cdf1 + (1 - self.r) * cdf2
        return result

    def sf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.ones_like(x)
        mask = x >= 0

        sf1 = (1 + x[mask] / self.lambda1)**(-self.alpha1)
        sf2 = (1 + x[mask] / self.lambda2)**(-self.alpha2)

        result[mask] = self.r * sf1 + (1 - self.r) * sf2
        return result

    def params_dict(self) -> dict:
        return {"alpha1": self.alpha1, "alpha2": self.alpha2,
                "lambda1": self.lambda1, "lambda2": self.lambda2, "r": self.r}


# =============================================================================
# Truncated Distributions
# =============================================================================

@dataclass
class RightTruncated(Distribution):
    """
    Right-Truncated Distribution Wrapper

    Applies right truncation to any distribution, conditioning on X ≤ Max.

    Survival function:
        F̄_tr(x) = (F̄(x) - F̄(Max)) / (1 - F̄(Max))  for x < Max
        F̄_tr(x) = 0                                  for x ≥ Max

    Right truncation is useful when:
    - Losses are bounded (e.g., by policy limits or sum insured)
    - The original distribution has infinite expectation (α < 1)

    Parameters:
        base_dist: The underlying distribution to truncate
        max_value: The truncation point (maximum possible value)

    References:
        - Fackler (2013), Section 4
        - Klugman et al. (2008)
    """
    base_dist: Distribution
    max_value: float

    name: str = "RightTruncated"
    description: str = "Right-Truncated Distribution"
    wikipedia_url: str = ""

    def __post_init__(self):
        if self.max_value <= 0:
            raise ValueError("max_value must be positive")

        # Compute normalizing constant
        self._F_max = self.base_dist.cdf(np.array([self.max_value]))[0]
        if self._F_max <= 0:
            raise ValueError("max_value must be in the support of the distribution")

        self.name = f"RightTruncated({self.base_dist.name})"
        self.description = f"Right-Truncated {self.base_dist.description}"

    def pdf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.zeros_like(x)
        mask = x < self.max_value
        result[mask] = self.base_dist.pdf(x[mask]) / self._F_max
        return result

    def cdf(self, x: np.ndarray) -> np.ndarray:
        x = np.asarray(x, dtype=float)
        result = np.ones_like(x)
        mask = x < self.max_value
        result[mask] = self.base_dist.cdf(x[mask]) / self._F_max
        return result

    def sf(self, x: np.ndarray) -> np.ndarray:
        return 1 - self.cdf(x)

    def params_dict(self) -> dict:
        base_params = self.base_dist.params_dict()
        return {**base_params, "max_value": self.max_value}


# =============================================================================
# Utility Functions
# =============================================================================

def local_pareto_alpha(dist: Distribution, d: float, epsilon: float = 1e-6) -> float:
    """
    Compute the local Pareto alpha at point d for any distribution.

    α_d = d * f(d) / F̄(d)

    This measures the "local heaviness" of the tail at point d.
    For a true Pareto distribution, this equals α everywhere in the tail.
    For GPD, α_d = (d/(d+λ)) * α.

    Parameters:
        dist: The distribution
        d: The point at which to compute the local alpha
        epsilon: Small value to avoid division by zero

    Returns:
        The local Pareto alpha at d

    References:
        - Fackler (2013), Section 2
        - Riegel (2008)
    """
    d_arr = np.array([d])
    f_d = dist.pdf(d_arr)[0]
    sf_d = dist.sf(d_arr)[0]

    if sf_d < epsilon:
        return np.inf

    return d * f_d / sf_d


def limited_expected_value(dist: Distribution, limit: float,
                           num_points: int = 1000) -> float:
    """
    Compute the Limited Expected Value (LEV) using numerical integration.

    LEV(C) = E[min(X, C)] = integral_0^C F̄(x) dx

    This is fundamental to exposure rating in insurance.

    Parameters:
        dist: The distribution
        limit: The policy limit C
        num_points: Number of points for numerical integration

    Returns:
        The limited expected value at the given limit

    References:
        - Fackler (2013), Section 7
        - Mack & Fackler (2003)
    """
    x = np.linspace(0, limit, num_points)
    sf_values = dist.sf(x)
    return np.trapezoid(sf_values, x)


# =============================================================================
# Registry of all distributions
# =============================================================================

DISTRIBUTIONS = {
    "Pareto": Pareto,
    "GPD": GPD,
    "Lomax": Lomax,
    "Burr": Burr,
    "LognormalPareto": LognormalPareto,
    "LognormalGPD": LognormalGPD,
    "WeibullPareto": WeibullPareto,
    "ExponentialPareto": ExponentialPareto,
    "PowerPareto": PowerPareto,
    "FourParameterPareto": FourParameterPareto,
    "FiveParameterPareto": FiveParameterPareto,
    "RightTruncated": RightTruncated,
}


if __name__ == "__main__":
    # Quick demonstration
    print("Fackler Distributions Module")
    print("=" * 50)

    # Create example distributions
    pareto = Pareto(alpha=2.0, theta=1.0)
    gpd = GPD(alpha=2.0, lambda_=0.5, theta=1.0)
    lomax = Lomax(alpha=2.0, lambda_=1.0)
    burr = Burr(alpha=2.0, lambda_=1.0, tau=1.5)

    print(f"\n{pareto}")
    print(f"  Mean: {pareto.mean():.4f}")

    print(f"\n{gpd}")
    print(f"  Local alpha at d=2: {gpd.local_pareto_alpha(2):.4f}")

    print(f"\n{lomax}")
    print(f"  Mean: {lomax.mean():.4f}")

    print(f"\n{burr}")
    print(f"  Asymptotic Pareto alpha: {burr.asymptotic_pareto_alpha():.4f}")

    # Spliced distributions
    ln_par = LognormalPareto(mu=0, sigma=1, theta=5)
    print(f"\n{ln_par}")
    print(f"  Derived alpha: {ln_par.alpha:.4f}")

    print("\n" + "=" * 50)
    print("Run test_fackler_distributions.py for visualizations")
