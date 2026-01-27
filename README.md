# Fackler Distributions Excel Add-in

An Excel add-in implementing the heavy-tailed probability distributions from Fackler (2013) "Reinventing Pareto: Fits for Both Small and Large Losses".

Corroborating python functions are also included in the project.

This project is in beta. Code was produced using AI coding tools and is offered without any warranty. Please report any bugs.

## Distribution Visualizations

### Pareto Family Comparison
![Pareto Family Comparison](output/00_comparison_pareto_family.png)

### Core Distributions

| Pareto Type I | GPD | Lomax |
|:---:|:---:|:---:|
| ![Pareto](output/01_pareto.png) | ![GPD](output/02_gpd.png) | ![Lomax](output/03_lomax.png) |

### Burr Distribution

| Bell-shaped | Decreasing |
|:---:|:---:|
| ![Burr Bell](output/04_burr_bellshaped.png) | ![Burr Decreasing](output/04b_burr_decreasing.png) |

### Spliced Distributions

| Lognormal-Pareto | Lognormal-GPD |
|:---:|:---:|
| ![LN-Pareto](output/05_lognormal_pareto.png) | ![LN-GPD](output/06_lognormal_gpd.png) |

| Weibull-Pareto | Exponential-Pareto | Power-Pareto |
|:---:|:---:|:---:|
| ![Weibull-Pareto](output/07_weibull_pareto.png) | ![Exp-Pareto](output/08_exponential_pareto.png) | ![Power-Pareto](output/09_power_pareto.png) |

### Mixture Distributions

| Four-Parameter Pareto | Five-Parameter Pareto |
|:---:|:---:|
| ![4-Param](output/10_four_parameter_pareto.png) | ![5-Param](output/11_five_parameter_pareto.png) |

### Additional

| Right-Truncated Pareto | Spliced Comparison |
|:---:|:---:|
| ![Truncated](output/12_right_truncated_pareto.png) | ![Spliced Comparison](output/13_comparison_spliced.png) |

## Installation

1. Download the appropriate XLL file from the `dist` folder:
   - `FacklerDistributions64.xll` for 64-bit Excel
   - `FacklerDistributions.xll` for 32-bit Excel

2. If Windows blocks the file (common for downloads), right-click the XLL file → Properties → check "Unblock" → OK

3. In Excel: File → Options → Add-ins → Manage: Excel Add-ins → Go → Browse → select the XLL file

Alternatively, double-click the XLL file to load it for the current session.

## Available Functions

All functions use the `FACKLER.` prefix and are available in the "Fackler Distributions" category.

### Pareto Type I
| Function | Description |
|----------|-------------|
| `FACKLER.PARETO.PDF(x, alpha, theta)` | Probability density function |
| `FACKLER.PARETO.CDF(x, alpha, theta)` | Cumulative distribution function |
| `FACKLER.PARETO.SF(x, alpha, theta)` | Survival function |
| `FACKLER.PARETO.MEAN(alpha, theta)` | Expected value |

### Generalized Pareto Distribution (GPD)
| Function | Description |
|----------|-------------|
| `FACKLER.GPD.PDF(x, alpha, lambda, [theta])` | PDF using Fackler's parametrization |
| `FACKLER.GPD.CDF(x, alpha, lambda, [theta])` | CDF |
| `FACKLER.GPD.SF(x, alpha, lambda, [theta])` | Survival function |
| `FACKLER.GPD.LOCALALPHA(d, alpha, lambda)` | Local Pareto alpha at point d |

### Lomax (Pareto Type II)
| Function | Description |
|----------|-------------|
| `FACKLER.LOMAX.PDF(x, alpha, lambda)` | PDF |
| `FACKLER.LOMAX.CDF(x, alpha, lambda)` | CDF |
| `FACKLER.LOMAX.SF(x, alpha, lambda)` | Survival function |
| `FACKLER.LOMAX.MEAN(alpha, lambda)` | Expected value |

### Burr Type XII
| Function | Description |
|----------|-------------|
| `FACKLER.BURR.PDF(x, alpha, lambda, tau)` | PDF |
| `FACKLER.BURR.CDF(x, alpha, lambda, tau)` | CDF |
| `FACKLER.BURR.SF(x, alpha, lambda, tau)` | Survival function |

### Lognormal-Pareto (Czeledin)
Lognormal body with Pareto tail, continuously spliced at threshold.

| Function | Description |
|----------|-------------|
| `FACKLER.LNPARETO.PDF(x, mu, sigma, theta)` | PDF |
| `FACKLER.LNPARETO.CDF(x, mu, sigma, theta)` | CDF |
| `FACKLER.LNPARETO.SF(x, mu, sigma, theta)` | Survival function |
| `FACKLER.LNPARETO.ALPHA(mu, sigma, theta)` | Derived tail index from C1 condition |

### Weibull-Pareto
Weibull body with Pareto tail.

| Function | Description |
|----------|-------------|
| `FACKLER.WEIPARETO.PDF(x, k, scale, theta, r)` | PDF |
| `FACKLER.WEIPARETO.CDF(x, k, scale, theta, r)` | CDF |
| `FACKLER.WEIPARETO.SF(x, k, scale, theta, r)` | Survival function |
| `FACKLER.WEIPARETO.ALPHA(k, scale, theta, r)` | Derived tail index |

### Exponential-Pareto
Exponential body with Pareto tail (parameters derived from continuity conditions).

| Function | Description |
|----------|-------------|
| `FACKLER.EXPPARETO.PDF(x, rate, theta)` | PDF |
| `FACKLER.EXPPARETO.CDF(x, rate, theta)` | CDF |
| `FACKLER.EXPPARETO.SF(x, rate, theta)` | Survival function |
| `FACKLER.EXPPARETO.ALPHA(rate, theta)` | Derived alpha = theta * rate |
| `FACKLER.EXPPARETO.R(rate, theta)` | Derived r = 1 - exp(-rate * theta) |

### Power-Pareto (Log-Laplace)
Power function body with Pareto tail.

| Function | Description |
|----------|-------------|
| `FACKLER.POWPARETO.PDF(x, alpha, beta, theta)` | PDF |
| `FACKLER.POWPARETO.CDF(x, alpha, beta, theta)` | CDF |
| `FACKLER.POWPARETO.SF(x, alpha, beta, theta)` | Survival function |
| `FACKLER.POWPARETO.R(alpha, beta)` | Derived r = alpha / (alpha + beta) |

### Four-Parameter Pareto
Lomax mixture with constraint alpha1 = alpha2 + 2.

| Function | Description |
|----------|-------------|
| `FACKLER.PARETO4.PDF(x, alpha2, lambda1, lambda2, r)` | PDF |
| `FACKLER.PARETO4.CDF(x, alpha2, lambda1, lambda2, r)` | CDF |
| `FACKLER.PARETO4.SF(x, alpha2, lambda1, lambda2, r)` | Survival function |

### Five-Parameter Pareto
Unconstrained Lomax mixture.

| Function | Description |
|----------|-------------|
| `FACKLER.PARETO5.PDF(x, alpha1, alpha2, lambda1, lambda2, r)` | PDF |
| `FACKLER.PARETO5.CDF(x, alpha1, alpha2, lambda1, lambda2, r)` | CDF |
| `FACKLER.PARETO5.SF(x, alpha1, alpha2, lambda1, lambda2, r)` | Survival function |

### Utility Functions
| Function | Description |
|----------|-------------|
| `FACKLER.LOCALALPHA(pdf, sf, x)` | Local Pareto alpha: x * pdf / sf |
| `FACKLER.VERSION()` | Add-in version |
| `FACKLER.HELP()` | Help text |

## Project Structure

```
fackler_paper_excel_addin/
├── dist/                           # Distribution files (ready to use)
│   ├── FacklerDistributions.xll    # Excel add-in (32-bit)
│   ├── FacklerDistributions64.xll  # Excel add-in (64-bit)
│   └── FacklerDistributions_Demo.xlsx
│
├── excel-addin/                    # C# source code
│   ├── Distributions.cs            # Core distribution implementations
│   ├── ExcelFunctions.cs           # Excel UDF wrappers
│   ├── FacklerDistributions.csproj # Project file
│   ├── FacklerDistributions.dna    # Excel-DNA configuration
│   └── build.ps1                   # Build script
│
├── output/                         # Distribution visualizations (PNG)
│
├── docs/                           # Documentation
│   └── fackler_distributions_summary.md
│
├── reference/                      # Reference materials
│   └── Fackler_Paper_Hague2013.pdf # Original paper
│
├── fackler_distributions.py        # Python reference implementation
├── test_fackler_distributions.py   # Python tests
├── create_excel_demo.py            # Script to generate demo workbook
├── requirements.txt                # Python dependencies
└── agents.md                       # AI agent development notes
```

## Building from Source

Requirements:
- Windows
- .NET SDK 6.0 or later
- .NET Framework 4.8 targeting pack

```powershell
cd excel-addin
.\build.ps1
```

Output files are placed in the `dist` folder.

## Reference

Fackler, M. (2013). "Reinventing Pareto: Fits for Both Small and Large Losses". ASTIN Colloquium, The Hague.

## License

MIT
