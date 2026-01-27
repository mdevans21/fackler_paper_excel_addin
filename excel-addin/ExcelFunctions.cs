using ExcelDna.Integration;

namespace FacklerDistributions
{
    /// <summary>
    /// Excel UDF functions for Fackler distributions.
    /// Based on Fackler (2013): "Reinventing Pareto: Fits for both small and large losses"
    /// </summary>
    public static class ExcelFunctions
    {
        private const string CATEGORY = "Fackler Distributions";

        #region Pareto Type I

        [ExcelFunction(
            Name = "FACKLER.PARETO.PDF",
            Description = "Pareto Type I probability density function. f(x) = α·θ^α / x^(α+1) for x ≥ θ",
            Category = CATEGORY,
            HelpTopic = "https://en.wikipedia.org/wiki/Pareto_distribution")]
        public static double ParetoPDF(
            [ExcelArgument(Description = "Value at which to evaluate the PDF")] double x,
            [ExcelArgument(Description = "Shape parameter α (alpha), must be > 0")] double alpha,
            [ExcelArgument(Description = "Scale parameter θ (theta), minimum value, must be > 0")] double theta)
        {
            return Distributions.ParetoPDF(x, alpha, theta);
        }

        [ExcelFunction(
            Name = "FACKLER.PARETO.CDF",
            Description = "Pareto Type I cumulative distribution function. F(x) = 1 - (θ/x)^α for x ≥ θ",
            Category = CATEGORY)]
        public static double ParetoCDF(
            [ExcelArgument(Description = "Value at which to evaluate the CDF")] double x,
            [ExcelArgument(Description = "Shape parameter α (alpha)")] double alpha,
            [ExcelArgument(Description = "Scale parameter θ (theta)")] double theta)
        {
            return Distributions.ParetoCDF(x, alpha, theta);
        }

        [ExcelFunction(
            Name = "FACKLER.PARETO.SF",
            Description = "Pareto Type I survival function. F̄(x) = (θ/x)^α for x ≥ θ",
            Category = CATEGORY)]
        public static double ParetoSF(
            [ExcelArgument(Description = "Value at which to evaluate the SF")] double x,
            [ExcelArgument(Description = "Shape parameter α (alpha)")] double alpha,
            [ExcelArgument(Description = "Scale parameter θ (theta)")] double theta)
        {
            return Distributions.ParetoSF(x, alpha, theta);
        }

        [ExcelFunction(
            Name = "FACKLER.PARETO.MEAN",
            Description = "Pareto Type I expected value. E[X] = αθ/(α-1) for α > 1",
            Category = CATEGORY)]
        public static double ParetoMean(
            [ExcelArgument(Description = "Shape parameter α (alpha)")] double alpha,
            [ExcelArgument(Description = "Scale parameter θ (theta)")] double theta)
        {
            return Distributions.ParetoMean(alpha, theta);
        }

        #endregion

        #region GPD

        [ExcelFunction(
            Name = "FACKLER.GPD.PDF",
            Description = "Generalized Pareto Distribution PDF using Fackler's parametrization",
            Category = CATEGORY,
            HelpTopic = "https://en.wikipedia.org/wiki/Generalized_Pareto_distribution")]
        public static double GPDPDF(
            [ExcelArgument(Description = "Value at which to evaluate the PDF")] double x,
            [ExcelArgument(Description = "Shape parameter α (alpha)")] double alpha,
            [ExcelArgument(Description = "Shift parameter λ (lambda)")] double lambda,
            [ExcelArgument(Description = "Threshold parameter θ (theta), default 0")] double theta = 0)
        {
            return Distributions.GPDPDF(x, alpha, lambda, theta);
        }

        [ExcelFunction(
            Name = "FACKLER.GPD.CDF",
            Description = "Generalized Pareto Distribution CDF. F(x) = 1 - ((θ+λ)/(x+λ))^α",
            Category = CATEGORY)]
        public static double GPDCDF(
            [ExcelArgument(Description = "Value at which to evaluate the CDF")] double x,
            [ExcelArgument(Description = "Shape parameter α (alpha)")] double alpha,
            [ExcelArgument(Description = "Shift parameter λ (lambda)")] double lambda,
            [ExcelArgument(Description = "Threshold parameter θ (theta), default 0")] double theta = 0)
        {
            return Distributions.GPDCDF(x, alpha, lambda, theta);
        }

        [ExcelFunction(
            Name = "FACKLER.GPD.SF",
            Description = "Generalized Pareto Distribution survival function",
            Category = CATEGORY)]
        public static double GPDSF(
            [ExcelArgument(Description = "Value at which to evaluate the SF")] double x,
            [ExcelArgument(Description = "Shape parameter α (alpha)")] double alpha,
            [ExcelArgument(Description = "Shift parameter λ (lambda)")] double lambda,
            [ExcelArgument(Description = "Threshold parameter θ (theta), default 0")] double theta = 0)
        {
            return Distributions.GPDSF(x, alpha, lambda, theta);
        }

        [ExcelFunction(
            Name = "FACKLER.GPD.LOCALALPHA",
            Description = "GPD local Pareto alpha at point d: α_d = (d/(d+λ))·α",
            Category = CATEGORY)]
        public static double GPDLocalAlpha(
            [ExcelArgument(Description = "Point at which to compute local alpha")] double d,
            [ExcelArgument(Description = "Shape parameter α (alpha)")] double alpha,
            [ExcelArgument(Description = "Shift parameter λ (lambda)")] double lambda)
        {
            return Distributions.GPDLocalAlpha(d, alpha, lambda);
        }

        #endregion

        #region Lomax

        [ExcelFunction(
            Name = "FACKLER.LOMAX.PDF",
            Description = "Lomax (Pareto Type II) PDF. f(x) = (α/λ)·(1 + x/λ)^(-(α+1))",
            Category = CATEGORY,
            HelpTopic = "https://en.wikipedia.org/wiki/Lomax_distribution")]
        public static double LomaxPDF(
            [ExcelArgument(Description = "Value at which to evaluate the PDF")] double x,
            [ExcelArgument(Description = "Shape parameter α (alpha)")] double alpha,
            [ExcelArgument(Description = "Scale parameter λ (lambda)")] double lambda)
        {
            return Distributions.LomaxPDF(x, alpha, lambda);
        }

        [ExcelFunction(
            Name = "FACKLER.LOMAX.CDF",
            Description = "Lomax (Pareto Type II) CDF. F(x) = 1 - (1 + x/λ)^(-α)",
            Category = CATEGORY)]
        public static double LomaxCDF(
            [ExcelArgument(Description = "Value at which to evaluate the CDF")] double x,
            [ExcelArgument(Description = "Shape parameter α (alpha)")] double alpha,
            [ExcelArgument(Description = "Scale parameter λ (lambda)")] double lambda)
        {
            return Distributions.LomaxCDF(x, alpha, lambda);
        }

        [ExcelFunction(
            Name = "FACKLER.LOMAX.SF",
            Description = "Lomax (Pareto Type II) survival function",
            Category = CATEGORY)]
        public static double LomaxSF(
            [ExcelArgument(Description = "Value at which to evaluate the SF")] double x,
            [ExcelArgument(Description = "Shape parameter α (alpha)")] double alpha,
            [ExcelArgument(Description = "Scale parameter λ (lambda)")] double lambda)
        {
            return Distributions.LomaxSF(x, alpha, lambda);
        }

        [ExcelFunction(
            Name = "FACKLER.LOMAX.MEAN",
            Description = "Lomax expected value. E[X] = λ/(α-1) for α > 1",
            Category = CATEGORY)]
        public static double LomaxMean(
            [ExcelArgument(Description = "Shape parameter α (alpha)")] double alpha,
            [ExcelArgument(Description = "Scale parameter λ (lambda)")] double lambda)
        {
            return Distributions.LomaxMean(alpha, lambda);
        }

        #endregion

        #region Burr

        [ExcelFunction(
            Name = "FACKLER.BURR.PDF",
            Description = "Burr Type XII PDF. Asymptotically Pareto with exponent α·τ",
            Category = CATEGORY,
            HelpTopic = "https://en.wikipedia.org/wiki/Burr_distribution")]
        public static double BurrPDF(
            [ExcelArgument(Description = "Value at which to evaluate the PDF")] double x,
            [ExcelArgument(Description = "Shape parameter α (alpha)")] double alpha,
            [ExcelArgument(Description = "Scale parameter λ (lambda)")] double lambda,
            [ExcelArgument(Description = "Shape parameter τ (tau)")] double tau)
        {
            return Distributions.BurrPDF(x, alpha, lambda, tau);
        }

        [ExcelFunction(
            Name = "FACKLER.BURR.CDF",
            Description = "Burr Type XII CDF. F(x) = 1 - (1 + (x/λ)^τ)^(-α)",
            Category = CATEGORY)]
        public static double BurrCDF(
            [ExcelArgument(Description = "Value at which to evaluate the CDF")] double x,
            [ExcelArgument(Description = "Shape parameter α (alpha)")] double alpha,
            [ExcelArgument(Description = "Scale parameter λ (lambda)")] double lambda,
            [ExcelArgument(Description = "Shape parameter τ (tau)")] double tau)
        {
            return Distributions.BurrCDF(x, alpha, lambda, tau);
        }

        [ExcelFunction(
            Name = "FACKLER.BURR.SF",
            Description = "Burr Type XII survival function",
            Category = CATEGORY)]
        public static double BurrSF(
            [ExcelArgument(Description = "Value at which to evaluate the SF")] double x,
            [ExcelArgument(Description = "Shape parameter α (alpha)")] double alpha,
            [ExcelArgument(Description = "Scale parameter λ (lambda)")] double lambda,
            [ExcelArgument(Description = "Shape parameter τ (tau)")] double tau)
        {
            return Distributions.BurrSF(x, alpha, lambda, tau);
        }

        #endregion

        #region Lognormal-Pareto (Czeledin)

        [ExcelFunction(
            Name = "FACKLER.LNPARETO.PDF",
            Description = "Lognormal-Pareto (Czeledin) PDF. Lognormal body, Pareto tail, continuous at θ",
            Category = CATEGORY)]
        public static double LognormalParetoPDF(
            [ExcelArgument(Description = "Value at which to evaluate the PDF")] double x,
            [ExcelArgument(Description = "Lognormal location parameter μ (mu)")] double mu,
            [ExcelArgument(Description = "Lognormal scale parameter σ (sigma)")] double sigma,
            [ExcelArgument(Description = "Splicing threshold θ (theta)")] double theta)
        {
            return Distributions.LognormalParetoPDF(x, mu, sigma, theta);
        }

        [ExcelFunction(
            Name = "FACKLER.LNPARETO.CDF",
            Description = "Lognormal-Pareto (Czeledin) CDF",
            Category = CATEGORY)]
        public static double LognormalParetoCDF(
            [ExcelArgument(Description = "Value at which to evaluate the CDF")] double x,
            [ExcelArgument(Description = "Lognormal location parameter μ (mu)")] double mu,
            [ExcelArgument(Description = "Lognormal scale parameter σ (sigma)")] double sigma,
            [ExcelArgument(Description = "Splicing threshold θ (theta)")] double theta)
        {
            return Distributions.LognormalParetoCDF(x, mu, sigma, theta);
        }

        [ExcelFunction(
            Name = "FACKLER.LNPARETO.SF",
            Description = "Lognormal-Pareto (Czeledin) survival function",
            Category = CATEGORY)]
        public static double LognormalParetoSF(
            [ExcelArgument(Description = "Value at which to evaluate the SF")] double x,
            [ExcelArgument(Description = "Lognormal location parameter μ (mu)")] double mu,
            [ExcelArgument(Description = "Lognormal scale parameter σ (sigma)")] double sigma,
            [ExcelArgument(Description = "Splicing threshold θ (theta)")] double theta)
        {
            return Distributions.LognormalParetoSF(x, mu, sigma, theta);
        }

        [ExcelFunction(
            Name = "FACKLER.LNPARETO.ALPHA",
            Description = "Derived Pareto tail index for Lognormal-Pareto from C1 condition",
            Category = CATEGORY)]
        public static double LognormalParetoAlpha(
            [ExcelArgument(Description = "Lognormal location parameter μ (mu)")] double mu,
            [ExcelArgument(Description = "Lognormal scale parameter σ (sigma)")] double sigma,
            [ExcelArgument(Description = "Splicing threshold θ (theta)")] double theta)
        {
            return Distributions.LognormalParetoAlpha(mu, sigma, theta);
        }

        #endregion

        #region Weibull-Pareto

        [ExcelFunction(
            Name = "FACKLER.WEIPARETO.PDF",
            Description = "Weibull-Pareto spliced PDF. Weibull body, Pareto tail",
            Category = CATEGORY)]
        public static double WeibullParetoPDF(
            [ExcelArgument(Description = "Value at which to evaluate the PDF")] double x,
            [ExcelArgument(Description = "Weibull shape parameter k")] double k,
            [ExcelArgument(Description = "Weibull scale parameter")] double scale,
            [ExcelArgument(Description = "Splicing threshold θ (theta)")] double theta,
            [ExcelArgument(Description = "Body weight r (probability X ≤ θ)")] double r)
        {
            return Distributions.WeibullParetoPDF(x, k, scale, theta, r);
        }

        [ExcelFunction(
            Name = "FACKLER.WEIPARETO.CDF",
            Description = "Weibull-Pareto spliced CDF",
            Category = CATEGORY)]
        public static double WeibullParetoCDF(
            [ExcelArgument(Description = "Value at which to evaluate the CDF")] double x,
            [ExcelArgument(Description = "Weibull shape parameter k")] double k,
            [ExcelArgument(Description = "Weibull scale parameter")] double scale,
            [ExcelArgument(Description = "Splicing threshold θ (theta)")] double theta,
            [ExcelArgument(Description = "Body weight r")] double r)
        {
            return Distributions.WeibullParetoCDF(x, k, scale, theta, r);
        }

        [ExcelFunction(
            Name = "FACKLER.WEIPARETO.SF",
            Description = "Weibull-Pareto spliced survival function",
            Category = CATEGORY)]
        public static double WeibullParetoSF(
            [ExcelArgument(Description = "Value at which to evaluate the SF")] double x,
            [ExcelArgument(Description = "Weibull shape parameter k")] double k,
            [ExcelArgument(Description = "Weibull scale parameter")] double scale,
            [ExcelArgument(Description = "Splicing threshold θ (theta)")] double theta,
            [ExcelArgument(Description = "Body weight r")] double r)
        {
            return Distributions.WeibullParetoSF(x, k, scale, theta, r);
        }

        [ExcelFunction(
            Name = "FACKLER.WEIPARETO.ALPHA",
            Description = "Derived Pareto tail index for Weibull-Pareto",
            Category = CATEGORY)]
        public static double WeibullParetoAlpha(
            [ExcelArgument(Description = "Weibull shape parameter k")] double k,
            [ExcelArgument(Description = "Weibull scale parameter")] double scale,
            [ExcelArgument(Description = "Splicing threshold θ (theta)")] double theta,
            [ExcelArgument(Description = "Body weight r")] double r)
        {
            return Distributions.WeibullParetoAlpha(k, scale, theta, r);
        }

        #endregion

        #region Exponential-Pareto

        [ExcelFunction(
            Name = "FACKLER.EXPPARETO.PDF",
            Description = "Exponential-Pareto spliced PDF. α = θ·rate, r = 1-exp(-rate·θ)",
            Category = CATEGORY)]
        public static double ExponentialParetoPDF(
            [ExcelArgument(Description = "Value at which to evaluate the PDF")] double x,
            [ExcelArgument(Description = "Exponential rate parameter λ")] double rate,
            [ExcelArgument(Description = "Splicing threshold θ (theta)")] double theta)
        {
            return Distributions.ExponentialParetoPDF(x, rate, theta);
        }

        [ExcelFunction(
            Name = "FACKLER.EXPPARETO.CDF",
            Description = "Exponential-Pareto spliced CDF",
            Category = CATEGORY)]
        public static double ExponentialParetoCDF(
            [ExcelArgument(Description = "Value at which to evaluate the CDF")] double x,
            [ExcelArgument(Description = "Exponential rate parameter λ")] double rate,
            [ExcelArgument(Description = "Splicing threshold θ (theta)")] double theta)
        {
            return Distributions.ExponentialParetoCDF(x, rate, theta);
        }

        [ExcelFunction(
            Name = "FACKLER.EXPPARETO.SF",
            Description = "Exponential-Pareto spliced survival function",
            Category = CATEGORY)]
        public static double ExponentialParetoSF(
            [ExcelArgument(Description = "Value at which to evaluate the SF")] double x,
            [ExcelArgument(Description = "Exponential rate parameter λ")] double rate,
            [ExcelArgument(Description = "Splicing threshold θ (theta)")] double theta)
        {
            return Distributions.ExponentialParetoSF(x, rate, theta);
        }

        [ExcelFunction(
            Name = "FACKLER.EXPPARETO.ALPHA",
            Description = "Derived alpha for Exponential-Pareto: α = θ·rate",
            Category = CATEGORY)]
        public static double ExponentialParetoAlpha(
            [ExcelArgument(Description = "Exponential rate parameter λ")] double rate,
            [ExcelArgument(Description = "Splicing threshold θ (theta)")] double theta)
        {
            return Distributions.ExponentialParetoAlpha(rate, theta);
        }

        [ExcelFunction(
            Name = "FACKLER.EXPPARETO.R",
            Description = "Derived r for Exponential-Pareto: r = 1-exp(-rate·θ)",
            Category = CATEGORY)]
        public static double ExponentialParetoR(
            [ExcelArgument(Description = "Exponential rate parameter λ")] double rate,
            [ExcelArgument(Description = "Splicing threshold θ (theta)")] double theta)
        {
            return Distributions.ExponentialParetoR(rate, theta);
        }

        #endregion

        #region Power-Pareto (Log-Laplace)

        [ExcelFunction(
            Name = "FACKLER.POWPARETO.PDF",
            Description = "Power-Pareto (Log-Laplace) PDF. r = α/(α+β) from C1 condition",
            Category = CATEGORY)]
        public static double PowerParetoPDF(
            [ExcelArgument(Description = "Value at which to evaluate the PDF")] double x,
            [ExcelArgument(Description = "Pareto tail index α (alpha)")] double alpha,
            [ExcelArgument(Description = "Power body exponent β (beta)")] double beta,
            [ExcelArgument(Description = "Splicing threshold θ (theta)")] double theta)
        {
            return Distributions.PowerParetoPDF(x, alpha, beta, theta);
        }

        [ExcelFunction(
            Name = "FACKLER.POWPARETO.CDF",
            Description = "Power-Pareto (Log-Laplace) CDF",
            Category = CATEGORY)]
        public static double PowerParetoCDF(
            [ExcelArgument(Description = "Value at which to evaluate the CDF")] double x,
            [ExcelArgument(Description = "Pareto tail index α (alpha)")] double alpha,
            [ExcelArgument(Description = "Power body exponent β (beta)")] double beta,
            [ExcelArgument(Description = "Splicing threshold θ (theta)")] double theta)
        {
            return Distributions.PowerParetoCDF(x, alpha, beta, theta);
        }

        [ExcelFunction(
            Name = "FACKLER.POWPARETO.SF",
            Description = "Power-Pareto (Log-Laplace) survival function",
            Category = CATEGORY)]
        public static double PowerParetoSF(
            [ExcelArgument(Description = "Value at which to evaluate the SF")] double x,
            [ExcelArgument(Description = "Pareto tail index α (alpha)")] double alpha,
            [ExcelArgument(Description = "Power body exponent β (beta)")] double beta,
            [ExcelArgument(Description = "Splicing threshold θ (theta)")] double theta)
        {
            return Distributions.PowerParetoSF(x, alpha, beta, theta);
        }

        [ExcelFunction(
            Name = "FACKLER.POWPARETO.R",
            Description = "Derived r for Power-Pareto: r = α/(α+β)",
            Category = CATEGORY)]
        public static double PowerParetoR(
            [ExcelArgument(Description = "Pareto tail index α (alpha)")] double alpha,
            [ExcelArgument(Description = "Power body exponent β (beta)")] double beta)
        {
            return Distributions.PowerParetoR(alpha, beta);
        }

        #endregion

        #region Four-Parameter Pareto

        [ExcelFunction(
            Name = "FACKLER.PARETO4.PDF",
            Description = "4-Parameter Pareto (Lomax mixture with α₁ = α₂ + 2)",
            Category = CATEGORY)]
        public static double FourParamParetoPDF(
            [ExcelArgument(Description = "Value at which to evaluate the PDF")] double x,
            [ExcelArgument(Description = "Shape parameter α₂")] double alpha2,
            [ExcelArgument(Description = "Scale parameter λ₁")] double lambda1,
            [ExcelArgument(Description = "Scale parameter λ₂")] double lambda2,
            [ExcelArgument(Description = "Mixing weight r")] double r)
        {
            return Distributions.FourParamParetoPDF(x, alpha2, lambda1, lambda2, r);
        }

        [ExcelFunction(
            Name = "FACKLER.PARETO4.CDF",
            Description = "4-Parameter Pareto CDF",
            Category = CATEGORY)]
        public static double FourParamParetoCDF(
            [ExcelArgument(Description = "Value at which to evaluate the CDF")] double x,
            [ExcelArgument(Description = "Shape parameter α₂")] double alpha2,
            [ExcelArgument(Description = "Scale parameter λ₁")] double lambda1,
            [ExcelArgument(Description = "Scale parameter λ₂")] double lambda2,
            [ExcelArgument(Description = "Mixing weight r")] double r)
        {
            return Distributions.FourParamParetoCDF(x, alpha2, lambda1, lambda2, r);
        }

        [ExcelFunction(
            Name = "FACKLER.PARETO4.SF",
            Description = "4-Parameter Pareto survival function",
            Category = CATEGORY)]
        public static double FourParamParetoSF(
            [ExcelArgument(Description = "Value at which to evaluate the SF")] double x,
            [ExcelArgument(Description = "Shape parameter α₂")] double alpha2,
            [ExcelArgument(Description = "Scale parameter λ₁")] double lambda1,
            [ExcelArgument(Description = "Scale parameter λ₂")] double lambda2,
            [ExcelArgument(Description = "Mixing weight r")] double r)
        {
            return Distributions.FourParamParetoSF(x, alpha2, lambda1, lambda2, r);
        }

        #endregion

        #region Five-Parameter Pareto

        [ExcelFunction(
            Name = "FACKLER.PARETO5.PDF",
            Description = "5-Parameter Pareto (unconstrained Lomax mixture)",
            Category = CATEGORY)]
        public static double FiveParamParetoPDF(
            [ExcelArgument(Description = "Value at which to evaluate the PDF")] double x,
            [ExcelArgument(Description = "Shape parameter α₁")] double alpha1,
            [ExcelArgument(Description = "Shape parameter α₂")] double alpha2,
            [ExcelArgument(Description = "Scale parameter λ₁")] double lambda1,
            [ExcelArgument(Description = "Scale parameter λ₂")] double lambda2,
            [ExcelArgument(Description = "Mixing weight r")] double r)
        {
            return Distributions.FiveParamParetoPDF(x, alpha1, alpha2, lambda1, lambda2, r);
        }

        [ExcelFunction(
            Name = "FACKLER.PARETO5.CDF",
            Description = "5-Parameter Pareto CDF",
            Category = CATEGORY)]
        public static double FiveParamParetoCDF(
            [ExcelArgument(Description = "Value at which to evaluate the CDF")] double x,
            [ExcelArgument(Description = "Shape parameter α₁")] double alpha1,
            [ExcelArgument(Description = "Shape parameter α₂")] double alpha2,
            [ExcelArgument(Description = "Scale parameter λ₁")] double lambda1,
            [ExcelArgument(Description = "Scale parameter λ₂")] double lambda2,
            [ExcelArgument(Description = "Mixing weight r")] double r)
        {
            return Distributions.FiveParamParetoCDF(x, alpha1, alpha2, lambda1, lambda2, r);
        }

        [ExcelFunction(
            Name = "FACKLER.PARETO5.SF",
            Description = "5-Parameter Pareto survival function",
            Category = CATEGORY)]
        public static double FiveParamParetoSF(
            [ExcelArgument(Description = "Value at which to evaluate the SF")] double x,
            [ExcelArgument(Description = "Shape parameter α₁")] double alpha1,
            [ExcelArgument(Description = "Shape parameter α₂")] double alpha2,
            [ExcelArgument(Description = "Scale parameter λ₁")] double lambda1,
            [ExcelArgument(Description = "Scale parameter λ₂")] double lambda2,
            [ExcelArgument(Description = "Mixing weight r")] double r)
        {
            return Distributions.FiveParamParetoSF(x, alpha1, alpha2, lambda1, lambda2, r);
        }

        #endregion

        #region Utility Functions

        [ExcelFunction(
            Name = "FACKLER.LOCALALPHA",
            Description = "Local Pareto alpha: α(x) = x·f(x)/F̄(x). Pass PDF and SF values.",
            Category = CATEGORY)]
        public static double LocalParetoAlpha(
            [ExcelArgument(Description = "PDF value at x")] double pdf,
            [ExcelArgument(Description = "Survival function value at x")] double sf,
            [ExcelArgument(Description = "Value x")] double x)
        {
            return Distributions.LocalParetoAlpha(pdf, sf, x);
        }

        [ExcelFunction(
            Name = "FACKLER.VERSION",
            Description = "Returns the version of the Fackler Distributions add-in",
            Category = CATEGORY)]
        public static string Version()
        {
            return "Fackler Distributions v1.0.0 - Based on Fackler (2013)";
        }

        [ExcelFunction(
            Name = "FACKLER.HELP",
            Description = "Returns help information about available functions",
            Category = CATEGORY)]
        public static string Help()
        {
            return @"Fackler Distributions Excel Add-in
================================
Based on: Fackler (2013) 'Reinventing Pareto: Fits for both small and large losses'

Available function prefixes:
- FACKLER.PARETO.*   : Pareto Type I
- FACKLER.GPD.*      : Generalized Pareto Distribution
- FACKLER.LOMAX.*    : Lomax (Pareto Type II)
- FACKLER.BURR.*     : Burr Type XII
- FACKLER.LNPARETO.* : Lognormal-Pareto (Czeledin)
- FACKLER.WEIPARETO.*: Weibull-Pareto
- FACKLER.EXPPARETO.*: Exponential-Pareto
- FACKLER.POWPARETO.*: Power-Pareto (Log-Laplace)
- FACKLER.PARETO4.*  : 4-Parameter Pareto
- FACKLER.PARETO5.*  : 5-Parameter Pareto

Each distribution has .PDF, .CDF, and .SF functions.
Use Excel's Insert Function dialog for detailed help.";
        }

        #endregion
    }
}
