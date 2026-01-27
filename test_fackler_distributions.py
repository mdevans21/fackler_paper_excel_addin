"""
Test and Visualization Script for Fackler Distributions

Generates PNG visualizations for each distribution showing:
- PDF (Probability Density Function)
- CDF (Cumulative Distribution Function)
- Description and parameters
- References

Usage:
    python test_fackler_distributions.py

Output:
    PNG files in the 'output/' directory

References:
    - Fackler (2013): "Reinventing Pareto: Fits for both small and large losses"
    - Original paper: reference/Fackler_Paper_Hague2013.pdf
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from typing import Tuple, Optional
import textwrap

from fackler_distributions import (
    Distribution,
    Pareto, GPD, Lomax, Burr,
    LognormalPareto, LognormalGPD, WeibullPareto, ExponentialPareto, PowerPareto,
    FourParameterPareto, FiveParameterPareto, RightTruncated,
    local_pareto_alpha, limited_expected_value
)


# Output directory for PNG files
OUTPUT_DIR = "output"


def setup_output_dir():
    """Create output directory if it doesn't exist."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"Created output directory: {OUTPUT_DIR}/")


def create_distribution_figure(
    dist: Distribution,
    x_range: Tuple[float, float],
    title: str,
    description: str,
    references: list[str],
    filename: str,
    num_points: int = 500,
    log_scale_x: bool = False,
    log_scale_y_pdf: bool = False,
    show_local_alpha: bool = False,
    alpha_points: Optional[list[float]] = None,
):
    """
    Create a comprehensive figure for a distribution.

    Parameters:
        dist: The distribution to visualize
        x_range: (x_min, x_max) range for plotting
        title: Main title for the figure
        description: Text description of the distribution
        references: List of reference strings
        filename: Output filename (without path)
        num_points: Number of points for plotting
        log_scale_x: Use logarithmic x-axis
        log_scale_y_pdf: Use logarithmic y-axis for PDF
        show_local_alpha: Show local Pareto alpha plot
        alpha_points: Points at which to compute local alpha
    """
    # Generate x values
    x_min, x_max = x_range
    if log_scale_x:
        x = np.logspace(np.log10(max(x_min, 1e-6)), np.log10(x_max), num_points)
    else:
        x = np.linspace(x_min, x_max, num_points)

    # Compute PDF and CDF
    pdf_vals = dist.pdf(x)
    cdf_vals = dist.cdf(x)
    sf_vals = dist.sf(x)

    # Create figure with custom layout
    fig = plt.figure(figsize=(14, 10))
    gs = GridSpec(3, 2, height_ratios=[1, 1, 0.8], hspace=0.3, wspace=0.3)

    # Color scheme
    pdf_color = '#2E86AB'  # Blue
    cdf_color = '#A23B72'  # Magenta
    sf_color = '#F18F01'   # Orange
    alpha_color = '#C73E1D' # Red

    # Plot 1: PDF
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.plot(x, pdf_vals, color=pdf_color, linewidth=2, label='PDF f(x)')
    ax1.fill_between(x, pdf_vals, alpha=0.3, color=pdf_color)
    ax1.set_xlabel('x', fontsize=11)
    ax1.set_ylabel('f(x)', fontsize=11)
    ax1.set_title('Probability Density Function (PDF)', fontsize=12, fontweight='bold')
    ax1.legend(loc='upper right')
    ax1.grid(True, alpha=0.3)
    if log_scale_x:
        ax1.set_xscale('log')
    if log_scale_y_pdf:
        ax1.set_yscale('log')
    ax1.set_xlim(x_min, x_max)

    # Plot 2: CDF
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.plot(x, cdf_vals, color=cdf_color, linewidth=2, label='CDF F(x)')
    ax2.plot(x, sf_vals, color=sf_color, linewidth=2, linestyle='--', label='SF F̄(x)')
    ax2.set_xlabel('x', fontsize=11)
    ax2.set_ylabel('F(x) / F̄(x)', fontsize=11)
    ax2.set_title('Cumulative Distribution Function (CDF) & Survival Function (SF)', fontsize=12, fontweight='bold')
    ax2.legend(loc='right')
    ax2.grid(True, alpha=0.3)
    if log_scale_x:
        ax2.set_xscale('log')
    ax2.set_xlim(x_min, x_max)
    ax2.set_ylim(-0.05, 1.05)

    # Plot 3: Log-Log Survival (characteristic of Pareto-like tails)
    ax3 = fig.add_subplot(gs[1, 0])
    # Filter positive values for log plot
    mask = (sf_vals > 0) & (x > 0)
    if np.any(mask):
        ax3.plot(x[mask], sf_vals[mask], color=sf_color, linewidth=2, label='Survival F̄(x)')
        ax3.set_xscale('log')
        ax3.set_yscale('log')
    ax3.set_xlabel('x (log scale)', fontsize=11)
    ax3.set_ylabel('F̄(x) (log scale)', fontsize=11)
    ax3.set_title('Log-Log Survival Plot (Linear = Pareto Tail)', fontsize=12, fontweight='bold')
    ax3.legend(loc='upper right')
    ax3.grid(True, alpha=0.3, which='both')

    # Plot 4: Local Pareto Alpha or LEV
    ax4 = fig.add_subplot(gs[1, 1])
    if show_local_alpha and alpha_points:
        alphas = [local_pareto_alpha(dist, d) for d in alpha_points]
        ax4.plot(alpha_points, alphas, color=alpha_color, linewidth=2, marker='o', markersize=4)
        ax4.set_xlabel('x', fontsize=11)
        ax4.set_ylabel('α(x)', fontsize=11)
        ax4.set_title('Local Pareto Alpha α(x) = x·f(x)/F̄(x)', fontsize=12, fontweight='bold')
        ax4.grid(True, alpha=0.3)
        if log_scale_x:
            ax4.set_xscale('log')
    else:
        # Show Limited Expected Value
        lev_limits = np.linspace(x_min + 0.01, x_max * 0.8, 50)
        lev_limits = lev_limits[lev_limits > 0]
        lev_vals = [limited_expected_value(dist, c, num_points=200) for c in lev_limits]
        ax4.plot(lev_limits, lev_vals, color=alpha_color, linewidth=2)
        ax4.set_xlabel('Policy Limit C', fontsize=11)
        ax4.set_ylabel('LEV(C)', fontsize=11)
        ax4.set_title('Limited Expected Value LEV(C) = E[min(X,C)]', fontsize=12, fontweight='bold')
        ax4.grid(True, alpha=0.3)
        if log_scale_x:
            ax4.set_xscale('log')

    # Text panel: Description and Parameters
    ax_text = fig.add_subplot(gs[2, :])
    ax_text.axis('off')

    # Format parameters
    params_str = "\n".join([f"  • {k}: {v}" for k, v in dist.params_dict().items()])

    # Wrap description
    wrapped_desc = textwrap.fill(description, width=100)

    # Format references
    refs_str = "\n".join([f"  • {ref}" for ref in references])

    info_text = f"""
{dist.description}

Parameters:
{params_str}

Description:
{wrapped_desc}

References:
{refs_str}
    """

    ax_text.text(0.02, 0.95, info_text, transform=ax_text.transAxes,
                 fontsize=10, verticalalignment='top', fontfamily='monospace',
                 bbox=dict(boxstyle='round', facecolor='#f8f9fa', edgecolor='#dee2e6', alpha=0.8))

    # Main title
    fig.suptitle(title, fontsize=16, fontweight='bold', y=0.98)

    # Save figure
    filepath = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white', edgecolor='none')
    plt.close()
    print(f"  Saved: {filepath}")


def test_pareto():
    """Test and visualize Pareto distribution."""
    print("\nTesting Pareto distribution...")

    dist = Pareto(alpha=2.0, theta=1.0)

    create_distribution_figure(
        dist=dist,
        x_range=(0.5, 10),
        title="Pareto Type I Distribution (Single-Parameter Pareto)",
        description=(
            "The classic reinsurance tail model. The survival function F̄(x) = (θ/x)^α has "
            "a 'memoryless' property where α remains invariant when modeling higher tails. "
            "This makes it ideal for comparing tails across different reporting thresholds. "
            "For α > 1, the mean exists and equals αθ/(α-1). A straight line on the log-log "
            "survival plot indicates perfect Pareto behavior."
        ),
        references=[
            "Fackler (2013), Section 2: 'Pareto – Reinsurer's old love'",
            "https://en.wikipedia.org/wiki/Pareto_distribution",
        ],
        filename="01_pareto.png",
        show_local_alpha=True,
        alpha_points=np.linspace(1.1, 10, 50).tolist(),
    )

    # Test with different alpha
    dist2 = Pareto(alpha=1.5, theta=1.0)
    create_distribution_figure(
        dist=dist2,
        x_range=(0.5, 20),
        title="Pareto Type I Distribution (α=1.5, heavier tail)",
        description=(
            "Pareto with α=1.5 has a heavier tail than α=2. Lower α means heavier tail. "
            "For α ≤ 1, the mean is infinite. For α ≤ 2, the variance is infinite. "
            "This distribution is often used for modeling large insurance losses where "
            "extreme events have significant probability."
        ),
        references=[
            "Fackler (2013), Section 2",
            "https://en.wikipedia.org/wiki/Pareto_distribution",
        ],
        filename="01b_pareto_heavy.png",
        show_local_alpha=True,
        alpha_points=np.linspace(1.1, 20, 50).tolist(),
    )


def test_gpd():
    """Test and visualize GPD distribution."""
    print("\nTesting GPD distribution...")

    # Standard GPD
    dist = GPD(alpha=2.0, lambda_=1.0, theta=1.0)

    create_distribution_figure(
        dist=dist,
        x_range=(0.5, 10),
        title="Generalized Pareto Distribution (GPD)",
        description=(
            "GPD generalizes Pareto with survival function F̄(x|X>θ) = ((θ+λ)/(x+λ))^α. "
            "Both α and λ are invariant when modeling higher tails, making GPD ideal for "
            "tail comparisons. The parameter λ acts as a 'shift' from Pareto. When λ=0, "
            "GPD reduces to Pareto. When λ>0 and θ=0, it becomes Lomax. The local Pareto "
            "alpha varies as α_d = (d/(d+λ))·α, approaching α as d→∞."
        ),
        references=[
            "Fackler (2013), Section 3: 'Generalized Pareto – Reinsurer's new love?'",
            "https://en.wikipedia.org/wiki/Generalized_Pareto_distribution",
            "Brazauskas & Kleefeld (2009)",
        ],
        filename="02_gpd.png",
        show_local_alpha=True,
        alpha_points=np.linspace(1.1, 10, 50).tolist(),
    )


def test_lomax():
    """Test and visualize Lomax distribution."""
    print("\nTesting Lomax distribution...")

    dist = Lomax(alpha=2.0, lambda_=1.0)

    create_distribution_figure(
        dist=dist,
        x_range=(0, 10),
        title="Lomax Distribution (Pareto Type II / American Pareto)",
        description=(
            "Lomax is a special case of GPD with θ=0, giving F̄(x) = (λ/(x+λ))^α. "
            "Unlike Pareto Type I, Lomax is a ground-up distribution starting at 0, "
            "making it suitable for modeling losses of any size without a gap. "
            "The mean (for α>1) is λ/(α-1). Lomax is also known as American Pareto "
            "or Two-parameter Pareto."
        ),
        references=[
            "Fackler (2013), Sections 3-4",
            "https://en.wikipedia.org/wiki/Lomax_distribution",
        ],
        filename="03_lomax.png",
        show_local_alpha=True,
        alpha_points=np.linspace(0.1, 10, 50).tolist(),
    )


def test_burr():
    """Test and visualize Burr distribution."""
    print("\nTesting Burr distribution...")

    # Burr with τ > 1 (bell-shaped)
    dist = Burr(alpha=2.0, lambda_=1.0, tau=2.0)

    create_distribution_figure(
        dist=dist,
        x_range=(0, 8),
        title="Burr Distribution (τ=2, bell-shaped density)",
        description=(
            "Burr is a three-parameter generalization of Lomax with F̄(x) = (1/(1+(x/λ)^τ))^α. "
            "For τ>1, the density has a unimodal bell shape (positive mode), making it suitable "
            "for modeling losses with a characteristic 'typical' size. For large x, Burr "
            "asymptotically tends to Pareto with exponent α·τ. This provides flexibility in "
            "the body while maintaining heavy-tail behavior."
        ),
        references=[
            "Fackler (2013), Section 4",
            "https://en.wikipedia.org/wiki/Burr_distribution",
            "Klugman et al. (2008)",
        ],
        filename="04_burr_bellshaped.png",
    )

    # Burr with τ < 1 (decreasing density)
    dist2 = Burr(alpha=2.0, lambda_=1.0, tau=0.5)

    create_distribution_figure(
        dist=dist2,
        x_range=(0, 10),
        title="Burr Distribution (τ=0.5, decreasing density)",
        description=(
            "Burr with τ<1 has a strictly decreasing density with mode at 0, similar to "
            "Lomax (τ=1). The asymptotic Pareto exponent is α·τ = 1.0, indicating a heavier "
            "tail than the τ=2 case. This parametrization is useful when small losses are "
            "most frequent but large losses still have significant probability."
        ),
        references=[
            "Fackler (2013), Section 4",
            "https://en.wikipedia.org/wiki/Burr_distribution",
        ],
        filename="04b_burr_decreasing.png",
    )


def test_lognormal_pareto():
    """Test and visualize Lognormal-Pareto spliced distribution."""
    print("\nTesting Lognormal-Pareto distribution...")

    dist = LognormalPareto(mu=1.0, sigma=0.8, theta=10.0)

    create_distribution_figure(
        dist=dist,
        x_range=(0.01, 50),
        title="Lognormal-Pareto Spliced Distribution (Czeledin)",
        description=(
            "The Czeledin distribution (pLN-Par-1) splices a Lognormal body with a Pareto tail. "
            "Below θ, losses follow a Lognormal distribution. Above θ, losses follow Pareto. "
            "The PDF is continuous (C1) at θ, with α determined by the smoothness condition: "
            "α = φ_θ/(σ·(1-Φ_θ)). This model is popular in reinsurance for fitting both "
            "small/medium losses (bell-shaped body) and large losses (heavy tail)."
        ),
        references=[
            "Fackler (2013), Section 5: 'The Lognormal-Pareto world'",
            "Knecht & Küttel (2003), 'The Czeledin distribution function'",
            "Scollnik (2007), 'On composite Lognormal-Pareto models'",
        ],
        filename="05_lognormal_pareto.png",
        log_scale_x=True,
    )


def test_lognormal_gpd():
    """Test and visualize Lognormal-GPD spliced distribution."""
    print("\nTesting Lognormal-GPD distribution...")

    dist = LognormalGPD(mu=1.0, sigma=0.8, theta=10.0, lambda_=2.0, r=0.7)

    create_distribution_figure(
        dist=dist,
        x_range=(0.01, 50),
        title="Lognormal-GPD Spliced Distribution (LN-GPD-1)",
        description=(
            "LN-GPD-1 extends Lognormal-Pareto with the additional λ parameter from GPD. "
            "The body may be 'distorted' from a proper Lognormal via the weight r. "
            "The tail follows GPD: F̄(x) = (1-r)·((θ+λ)/(x+λ))^α. This provides more "
            "flexibility than the Czeledin distribution, allowing different tail behaviors "
            "through the λ parameter (rising or falling local Pareto alpha)."
        ),
        references=[
            "Fackler (2013), Section 5",
            "Scollnik (2007), 'On composite Lognormal-Pareto models'",
        ],
        filename="06_lognormal_gpd.png",
        log_scale_x=True,
    )


def test_weibull_pareto():
    """Test and visualize Weibull-Pareto spliced distribution."""
    print("\nTesting Weibull-Pareto distribution...")

    dist = WeibullPareto(k=2.0, scale=5.0, theta=10.0, r=0.7)

    create_distribution_figure(
        dist=dist,
        x_range=(0, 40),
        title="Weibull-Pareto Spliced Distribution (Wei-Par-1)",
        description=(
            "Wei-Par-1 splices a Weibull body with a Pareto tail. The Weibull shape parameter k "
            "controls the body geometry: k<1 gives decreasing density, k=1 gives Exponential, "
            "k>1 gives bell-shaped density. The Pareto tail α is derived from the C1 condition. "
            "This model was applied to the famous Danish fire data by Scollnik & Sun (2012)."
        ),
        references=[
            "Fackler (2013), Section 6",
            "Scollnik & Sun (2012), 'Modeling with Weibull-Pareto models'",
            "https://en.wikipedia.org/wiki/Weibull_distribution",
        ],
        filename="07_weibull_pareto.png",
    )


def test_exponential_pareto():
    """Test and visualize Exponential-Pareto spliced distribution."""
    print("\nTesting Exponential-Pareto distribution...")

    dist = ExponentialPareto(rate=0.2, theta=10.0)

    create_distribution_figure(
        dist=dist,
        x_range=(0, 40),
        title="Exponential-Pareto Spliced Distribution (pExp-Par-1)",
        description=(
            "pExp-Par-1 is a simpler spliced model with only 2 free parameters. The Exponential "
            "body always has decreasing density. A notable property: the local Pareto alpha "
            "increases linearly from 0 at x=0 to α at x=θ, then remains constant in the tail. "
            "The derived α = θ·rate, and r = 1 - exp(-rate·θ). Used by ISO for some data."
        ),
        references=[
            "Fackler (2013), Section 6",
            "Teodorescu & Vernic (2009)",
            "Riegel (2010)",
        ],
        filename="08_exponential_pareto.png",
        show_local_alpha=True,
        alpha_points=np.linspace(0.1, 40, 80).tolist(),
    )


def test_power_pareto():
    """Test and visualize Power-Pareto spliced distribution."""
    print("\nTesting Power-Pareto distribution...")

    dist = PowerPareto(alpha=2.0, beta=1.5, theta=5.0)

    create_distribution_figure(
        dist=dist,
        x_range=(0.01, 20),
        title="Power-Pareto Spliced Distribution (Log-Laplace / Double Pareto)",
        description=(
            "Pow-Par-1 splices a power function body with Pareto tail. The body CDF is (x/θ)^β. "
            "For β<1: decreasing density; β=1: uniform on [0,θ]; β>1: increasing density. "
            "The C1 condition requires r = α/(α+β). This is related to the Log-Laplace or "
            "double Pareto distribution. It has been studied extensively in statistics and "
            "economics beyond actuarial applications."
        ),
        references=[
            "Fackler (2013), Section 6",
            "Kozubowski & Podgórski (2003), 'Log-Laplace distributions'",
            "https://en.wikipedia.org/wiki/Log-Laplace_distribution",
        ],
        filename="09_power_pareto.png",
    )


def test_four_parameter_pareto():
    """Test and visualize 4-Parameter Pareto distribution."""
    print("\nTesting 4-Parameter Pareto distribution...")

    dist = FourParameterPareto(alpha2=1.5, lambda1=2.0, lambda2=10.0, r=0.6)

    create_distribution_figure(
        dist=dist,
        x_range=(0, 50),
        title="4-Parameter Pareto Distribution (Constrained Lomax Mixture)",
        description=(
            "A mixture of two Lomax distributions with constraint α₁ = α₂ + 2. "
            "F̄(x) = r·(λ₁/(x+λ₁))^α₁ + (1-r)·(λ₂/(x+λ₂))^α₂. "
            "The constraint reduces parameters while maintaining flexibility. "
            "This model has been successfully applied by ISO (Insurance Services Office) "
            "to general liability business in the USA."
        ),
        references=[
            "Fackler (2013), Section 4",
            "Klugman et al. (2008), 'Loss models'",
        ],
        filename="10_four_parameter_pareto.png",
        log_scale_x=False,
    )


def test_five_parameter_pareto():
    """Test and visualize 5-Parameter Pareto distribution."""
    print("\nTesting 5-Parameter Pareto distribution...")

    dist = FiveParameterPareto(alpha1=3.0, alpha2=1.5, lambda1=2.0, lambda2=15.0, r=0.7)

    create_distribution_figure(
        dist=dist,
        x_range=(0, 80),
        title="5-Parameter Pareto Distribution (Unconstrained Lomax Mixture)",
        description=(
            "An unconstrained mixture of two Lomax distributions. "
            "F̄(x) = r·(λ₁/(x+λ₁))^α₁ + (1-r)·(λ₂/(x+λ₂))^α₂. "
            "The first component (with higher α₁) dominates for smaller losses, "
            "while the second (with lower α₂) dominates the tail. This can model "
            "two types of losses (e.g., material damage vs. bodily injury in MTPL)."
        ),
        references=[
            "Fackler (2013), Section 4",
        ],
        filename="11_five_parameter_pareto.png",
        log_scale_x=False,
    )


def test_right_truncated():
    """Test and visualize right-truncated distributions."""
    print("\nTesting Right-Truncated distributions...")

    # Right-truncated Pareto
    base = Pareto(alpha=1.5, theta=1.0)
    dist = RightTruncated(base_dist=base, max_value=20.0)

    create_distribution_figure(
        dist=dist,
        x_range=(0.5, 25),
        title="Right-Truncated Pareto Distribution",
        description=(
            "Right truncation conditions on X ≤ Max, useful when losses are bounded "
            "(e.g., by policy limits or sum insured). F̄_tr(x) = (F̄(x)-F̄(Max))/(1-F̄(Max)). "
            "Crucially, truncation makes the expected value finite even when the base "
            "distribution has α<1 (infinite mean). The memoryless property of GPD/Pareto "
            "is preserved: each truncated tail has the same parameters α, λ, and Max."
        ),
        references=[
            "Fackler (2013), Section 4: 'With or without a knife'",
            "Klugman et al. (2008)",
        ],
        filename="12_right_truncated_pareto.png",
    )


def test_comparison_plot():
    """Create a comparison plot of different tail behaviors."""
    print("\nCreating comparison plots...")

    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # Define distributions for comparison
    distributions = [
        (Pareto(alpha=2.0, theta=1.0), "Pareto (α=2)", '#2E86AB'),
        (Pareto(alpha=1.5, theta=1.0), "Pareto (α=1.5)", '#A23B72'),
        (GPD(alpha=2.0, lambda_=1.0, theta=1.0), "GPD (α=2, λ=1)", '#F18F01'),
        (Lomax(alpha=2.0, lambda_=1.0), "Lomax (α=2, λ=1)", '#C73E1D'),
        (Burr(alpha=2.0, lambda_=1.0, tau=1.5), "Burr (α=2, τ=1.5)", '#6B2D5C'),
    ]

    x = np.linspace(0.01, 15, 500)
    x_log = np.logspace(-1, 2, 500)

    # Plot 1: PDF comparison
    ax1 = axes[0, 0]
    for dist, name, color in distributions:
        pdf_vals = dist.pdf(x)
        ax1.plot(x, pdf_vals, label=name, color=color, linewidth=2)
    ax1.set_xlabel('x', fontsize=11)
    ax1.set_ylabel('f(x)', fontsize=11)
    ax1.set_title('PDF Comparison', fontsize=12, fontweight='bold')
    ax1.legend(loc='upper right', fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 15)
    ax1.set_ylim(0, 1.5)

    # Plot 2: CDF comparison
    ax2 = axes[0, 1]
    for dist, name, color in distributions:
        cdf_vals = dist.cdf(x)
        ax2.plot(x, cdf_vals, label=name, color=color, linewidth=2)
    ax2.set_xlabel('x', fontsize=11)
    ax2.set_ylabel('F(x)', fontsize=11)
    ax2.set_title('CDF Comparison', fontsize=12, fontweight='bold')
    ax2.legend(loc='lower right', fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 15)

    # Plot 3: Log-Log Survival comparison
    ax3 = axes[1, 0]
    for dist, name, color in distributions:
        sf_vals = dist.sf(x_log)
        mask = sf_vals > 0
        ax3.plot(x_log[mask], sf_vals[mask], label=name, color=color, linewidth=2)
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    ax3.set_xlabel('x (log scale)', fontsize=11)
    ax3.set_ylabel('F̄(x) (log scale)', fontsize=11)
    ax3.set_title('Log-Log Survival Comparison', fontsize=12, fontweight='bold')
    ax3.legend(loc='lower left', fontsize=9)
    ax3.grid(True, alpha=0.3, which='both')

    # Plot 4: Local Pareto Alpha comparison
    ax4 = axes[1, 1]
    alpha_points = np.linspace(1.1, 15, 100)
    for dist, name, color in distributions:
        alphas = [local_pareto_alpha(dist, d) for d in alpha_points]
        ax4.plot(alpha_points, alphas, label=name, color=color, linewidth=2)
    ax4.set_xlabel('x', fontsize=11)
    ax4.set_ylabel('α(x)', fontsize=11)
    ax4.set_title('Local Pareto Alpha Comparison', fontsize=12, fontweight='bold')
    ax4.legend(loc='lower right', fontsize=9)
    ax4.grid(True, alpha=0.3)
    ax4.set_xlim(1, 15)
    ax4.set_ylim(0, 4)

    fig.suptitle('Comparison of Pareto Family Distributions', fontsize=14, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    filepath = os.path.join(OUTPUT_DIR, "00_comparison_pareto_family.png")
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Saved: {filepath}")


def test_spliced_comparison():
    """Create a comparison plot of spliced distributions."""
    print("\nCreating spliced distribution comparison...")

    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # Define spliced distributions
    distributions = [
        (LognormalPareto(mu=1.0, sigma=0.8, theta=10.0), "Lognormal-Pareto", '#2E86AB'),
        (WeibullPareto(k=2.0, scale=5.0, theta=10.0, r=0.7), "Weibull-Pareto", '#A23B72'),
        (ExponentialPareto(rate=0.15, theta=10.0), "Exponential-Pareto", '#F18F01'),
        (PowerPareto(alpha=2.0, beta=1.5, theta=10.0), "Power-Pareto", '#C73E1D'),
    ]

    x = np.linspace(0.01, 50, 500)
    x_log = np.logspace(-1, 2, 500)

    # Plot 1: PDF comparison
    ax1 = axes[0, 0]
    for dist, name, color in distributions:
        pdf_vals = dist.pdf(x)
        ax1.plot(x, pdf_vals, label=name, color=color, linewidth=2)
    ax1.axvline(x=10, color='gray', linestyle='--', alpha=0.5, label='θ=10')
    ax1.set_xlabel('x', fontsize=11)
    ax1.set_ylabel('f(x)', fontsize=11)
    ax1.set_title('PDF Comparison (Spliced Models)', fontsize=12, fontweight='bold')
    ax1.legend(loc='upper right', fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 50)

    # Plot 2: CDF comparison
    ax2 = axes[0, 1]
    for dist, name, color in distributions:
        cdf_vals = dist.cdf(x)
        ax2.plot(x, cdf_vals, label=name, color=color, linewidth=2)
    ax2.axvline(x=10, color='gray', linestyle='--', alpha=0.5, label='θ=10')
    ax2.set_xlabel('x', fontsize=11)
    ax2.set_ylabel('F(x)', fontsize=11)
    ax2.set_title('CDF Comparison (Spliced Models)', fontsize=12, fontweight='bold')
    ax2.legend(loc='lower right', fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.set_xlim(0, 50)

    # Plot 3: Log-Log Survival comparison
    ax3 = axes[1, 0]
    for dist, name, color in distributions:
        sf_vals = dist.sf(x_log)
        mask = sf_vals > 0
        ax3.plot(x_log[mask], sf_vals[mask], label=name, color=color, linewidth=2)
    ax3.axvline(x=10, color='gray', linestyle='--', alpha=0.5, label='θ=10')
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    ax3.set_xlabel('x (log scale)', fontsize=11)
    ax3.set_ylabel('F̄(x) (log scale)', fontsize=11)
    ax3.set_title('Log-Log Survival (Spliced Models)', fontsize=12, fontweight='bold')
    ax3.legend(loc='lower left', fontsize=9)
    ax3.grid(True, alpha=0.3, which='both')

    # Plot 4: Local Pareto Alpha comparison
    ax4 = axes[1, 1]
    alpha_points = np.linspace(0.5, 50, 200)
    for dist, name, color in distributions:
        alphas = [local_pareto_alpha(dist, d) for d in alpha_points]
        ax4.plot(alpha_points, alphas, label=name, color=color, linewidth=2)
    ax4.axvline(x=10, color='gray', linestyle='--', alpha=0.5, label='θ=10')
    ax4.set_xlabel('x', fontsize=11)
    ax4.set_ylabel('α(x)', fontsize=11)
    ax4.set_title('Local Pareto Alpha (Spliced Models)', fontsize=12, fontweight='bold')
    ax4.legend(loc='upper right', fontsize=9)
    ax4.grid(True, alpha=0.3)
    ax4.set_xlim(0, 50)

    fig.suptitle('Comparison of Spliced Distributions (Body + Pareto Tail)',
                 fontsize=14, fontweight='bold')
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    filepath = os.path.join(OUTPUT_DIR, "13_comparison_spliced.png")
    plt.savefig(filepath, dpi=150, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  Saved: {filepath}")


def run_all_tests():
    """Run all tests and generate visualizations."""
    print("=" * 60)
    print("Fackler Distributions - Test and Visualization Suite")
    print("=" * 60)
    print("\nGenerating PNG visualizations for all distributions...")
    print("Reference: Fackler (2013), 'Reinventing Pareto'")
    print("-" * 60)

    setup_output_dir()

    # Run all tests
    test_comparison_plot()
    test_pareto()
    test_gpd()
    test_lomax()
    test_burr()
    test_lognormal_pareto()
    test_lognormal_gpd()
    test_weibull_pareto()
    test_exponential_pareto()
    test_power_pareto()
    test_four_parameter_pareto()
    test_five_parameter_pareto()
    test_right_truncated()
    test_spliced_comparison()

    print("\n" + "=" * 60)
    print(f"All visualizations saved to: {OUTPUT_DIR}/")
    print("=" * 60)


if __name__ == "__main__":
    run_all_tests()
