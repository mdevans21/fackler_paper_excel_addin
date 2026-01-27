using System;

namespace FacklerDistributions
{
    /// <summary>
    /// Core distribution implementations based on Fackler (2013):
    /// "Reinventing Pareto: Fits for both small and large losses"
    /// </summary>
    public static class Distributions
    {
        #region Helper Functions - Standard Normal Distribution

        /// <summary>Standard normal PDF: φ(z) = exp(-z²/2) / √(2π)</summary>
        public static double Phi(double z)
        {
            return Math.Exp(-0.5 * z * z) / Math.Sqrt(2 * Math.PI);
        }

        /// <summary>
        /// Standard normal CDF using Abramowitz and Stegun approximation.
        /// Accurate to about 7.5 decimal places.
        /// </summary>
        public static double PhiCDF(double z)
        {
            // Handle extreme values
            if (z < -8.0) return 0.0;
            if (z > 8.0) return 1.0;

            // Constants for approximation
            double p = 0.2316419;
            double b1 = 0.319381530;
            double b2 = -0.356563782;
            double b3 = 1.781477937;
            double b4 = -1.821255978;
            double b5 = 1.330274429;

            double absZ = Math.Abs(z);
            double t = 1.0 / (1.0 + p * absZ);
            double t2 = t * t;
            double t3 = t2 * t;
            double t4 = t3 * t;
            double t5 = t4 * t;

            double pdf = Phi(absZ);
            double cdf = 1.0 - pdf * (b1 * t + b2 * t2 + b3 * t3 + b4 * t4 + b5 * t5);

            return z >= 0 ? cdf : 1.0 - cdf;
        }

        #endregion

        #region Pareto Type I

        /// <summary>
        /// Pareto Type I PDF: f(x) = α * θ^α / x^(α+1) for x >= θ
        /// </summary>
        public static double ParetoPDF(double x, double alpha, double theta)
        {
            if (alpha <= 0 || theta <= 0) return double.NaN;
            if (x < theta) return 0;
            return alpha * Math.Pow(theta, alpha) / Math.Pow(x, alpha + 1);
        }

        /// <summary>
        /// Pareto Type I CDF: F(x) = 1 - (θ/x)^α for x >= θ
        /// </summary>
        public static double ParetoCDF(double x, double alpha, double theta)
        {
            if (alpha <= 0 || theta <= 0) return double.NaN;
            if (x < theta) return 0;
            return 1 - Math.Pow(theta / x, alpha);
        }

        /// <summary>
        /// Pareto Type I Survival Function: F̄(x) = (θ/x)^α for x >= θ
        /// </summary>
        public static double ParetoSF(double x, double alpha, double theta)
        {
            if (alpha <= 0 || theta <= 0) return double.NaN;
            if (x < theta) return 1;
            return Math.Pow(theta / x, alpha);
        }

        /// <summary>
        /// Pareto Type I Mean: E[X] = αθ/(α-1) for α > 1
        /// </summary>
        public static double ParetoMean(double alpha, double theta)
        {
            if (alpha <= 1 || theta <= 0) return double.PositiveInfinity;
            return alpha * theta / (alpha - 1);
        }

        #endregion

        #region Generalized Pareto Distribution (GPD)

        /// <summary>
        /// GPD PDF using Fackler's parametrization
        /// </summary>
        public static double GPDPDF(double x, double alpha, double lambda, double theta)
        {
            if (alpha <= 0 || lambda <= -theta) return double.NaN;
            if (x < theta) return 0;
            double thetaShifted = theta + lambda;
            double xShifted = x + lambda;
            return alpha * Math.Pow(thetaShifted, alpha) / Math.Pow(xShifted, alpha + 1);
        }

        /// <summary>
        /// GPD CDF using Fackler's parametrization
        /// </summary>
        public static double GPDCDF(double x, double alpha, double lambda, double theta)
        {
            if (alpha <= 0 || lambda <= -theta) return double.NaN;
            if (x < theta) return 0;
            double thetaShifted = theta + lambda;
            double xShifted = x + lambda;
            return 1 - Math.Pow(thetaShifted / xShifted, alpha);
        }

        /// <summary>
        /// GPD Survival Function
        /// </summary>
        public static double GPDSF(double x, double alpha, double lambda, double theta)
        {
            if (alpha <= 0 || lambda <= -theta) return double.NaN;
            if (x < theta) return 1;
            double thetaShifted = theta + lambda;
            double xShifted = x + lambda;
            return Math.Pow(thetaShifted / xShifted, alpha);
        }

        /// <summary>
        /// GPD Local Pareto Alpha at point d
        /// </summary>
        public static double GPDLocalAlpha(double d, double alpha, double lambda)
        {
            return (d / (d + lambda)) * alpha;
        }

        #endregion

        #region Lomax (Pareto Type II)

        /// <summary>
        /// Lomax PDF: f(x) = (α/λ) * (1 + x/λ)^(-(α+1)) for x >= 0
        /// </summary>
        public static double LomaxPDF(double x, double alpha, double lambda)
        {
            if (alpha <= 0 || lambda <= 0) return double.NaN;
            if (x < 0) return 0;
            return (alpha / lambda) * Math.Pow(1 + x / lambda, -(alpha + 1));
        }

        /// <summary>
        /// Lomax CDF: F(x) = 1 - (1 + x/λ)^(-α) for x >= 0
        /// </summary>
        public static double LomaxCDF(double x, double alpha, double lambda)
        {
            if (alpha <= 0 || lambda <= 0) return double.NaN;
            if (x < 0) return 0;
            return 1 - Math.Pow(1 + x / lambda, -alpha);
        }

        /// <summary>
        /// Lomax Survival Function
        /// </summary>
        public static double LomaxSF(double x, double alpha, double lambda)
        {
            if (alpha <= 0 || lambda <= 0) return double.NaN;
            if (x < 0) return 1;
            return Math.Pow(1 + x / lambda, -alpha);
        }

        /// <summary>
        /// Lomax Mean: E[X] = λ/(α-1) for α > 1
        /// </summary>
        public static double LomaxMean(double alpha, double lambda)
        {
            if (alpha <= 1 || lambda <= 0) return double.PositiveInfinity;
            return lambda / (alpha - 1);
        }

        #endregion

        #region Burr Distribution

        /// <summary>
        /// Burr PDF: f(x) = (α*τ/λ) * (x/λ)^(τ-1) * (1 + (x/λ)^τ)^(-(α+1)) for x > 0
        /// </summary>
        public static double BurrPDF(double x, double alpha, double lambda, double tau)
        {
            if (alpha <= 0 || lambda <= 0 || tau <= 0) return double.NaN;
            if (x <= 0) return 0;
            double z = Math.Pow(x / lambda, tau);
            return (alpha * tau / lambda) * Math.Pow(x / lambda, tau - 1) * Math.Pow(1 + z, -(alpha + 1));
        }

        /// <summary>
        /// Burr CDF: F(x) = 1 - (1 + (x/λ)^τ)^(-α) for x >= 0
        /// </summary>
        public static double BurrCDF(double x, double alpha, double lambda, double tau)
        {
            if (alpha <= 0 || lambda <= 0 || tau <= 0) return double.NaN;
            if (x < 0) return 0;
            double z = Math.Pow(x / lambda, tau);
            return 1 - Math.Pow(1 + z, -alpha);
        }

        /// <summary>
        /// Burr Survival Function
        /// </summary>
        public static double BurrSF(double x, double alpha, double lambda, double tau)
        {
            if (alpha <= 0 || lambda <= 0 || tau <= 0) return double.NaN;
            if (x < 0) return 1;
            double z = Math.Pow(x / lambda, tau);
            return Math.Pow(1 + z, -alpha);
        }

        #endregion

        #region Lognormal-Pareto (Czeledin Distribution)

        /// <summary>
        /// Calculate derived alpha for Lognormal-Pareto from C1 condition
        /// </summary>
        public static double LognormalParetoAlpha(double mu, double sigma, double theta)
        {
            double zTheta = (Math.Log(theta) - mu) / sigma;
            double phiTheta = Phi(zTheta);
            double cdfTheta = PhiCDF(zTheta);
            return phiTheta / (sigma * (1 - cdfTheta));
        }

        /// <summary>
        /// Lognormal-Pareto PDF (Czeledin distribution)
        /// </summary>
        public static double LognormalParetoPDF(double x, double mu, double sigma, double theta)
        {
            if (sigma <= 0 || theta <= 0) return double.NaN;
            if (x <= 0) return 0;

            double zTheta = (Math.Log(theta) - mu) / sigma;
            double cdfTheta = PhiCDF(zTheta);
            double alpha = LognormalParetoAlpha(mu, sigma, theta);

            if (x < theta)
            {
                // Lognormal PDF
                double z = (Math.Log(x) - mu) / sigma;
                return Phi(z) / (x * sigma);
            }
            else
            {
                // Pareto PDF
                return (1 - cdfTheta) * alpha * Math.Pow(theta, alpha) / Math.Pow(x, alpha + 1);
            }
        }

        /// <summary>
        /// Lognormal-Pareto CDF (Czeledin distribution)
        /// </summary>
        public static double LognormalParetoCDF(double x, double mu, double sigma, double theta)
        {
            if (sigma <= 0 || theta <= 0) return double.NaN;
            if (x <= 0) return 0;

            double zTheta = (Math.Log(theta) - mu) / sigma;
            double cdfTheta = PhiCDF(zTheta);
            double alpha = LognormalParetoAlpha(mu, sigma, theta);

            if (x < theta)
            {
                // Lognormal CDF
                double z = (Math.Log(x) - mu) / sigma;
                return PhiCDF(z);
            }
            else
            {
                // Spliced Pareto CDF
                return 1 - (1 - cdfTheta) * Math.Pow(theta / x, alpha);
            }
        }

        /// <summary>
        /// Lognormal-Pareto Survival Function
        /// </summary>
        public static double LognormalParetoSF(double x, double mu, double sigma, double theta)
        {
            return 1 - LognormalParetoCDF(x, mu, sigma, theta);
        }

        #endregion

        #region Weibull-Pareto

        /// <summary>
        /// Calculate derived alpha for Weibull-Pareto
        /// </summary>
        public static double WeibullParetoAlpha(double k, double scale, double theta, double r)
        {
            double FTheta = 1 - Math.Exp(-Math.Pow(theta / scale, k));
            double fTheta = (k / scale) * Math.Pow(theta / scale, k - 1) * Math.Exp(-Math.Pow(theta / scale, k));
            return (r / (1 - r)) * (fTheta / FTheta) * theta;
        }

        /// <summary>
        /// Weibull-Pareto PDF
        /// </summary>
        public static double WeibullParetoPDF(double x, double k, double scale, double theta, double r)
        {
            if (k <= 0 || scale <= 0 || theta <= 0 || r <= 0 || r >= 1) return double.NaN;
            if (x <= 0) return 0;

            double FTheta = 1 - Math.Exp(-Math.Pow(theta / scale, k));
            double alpha = WeibullParetoAlpha(k, scale, theta, r);

            if (x < theta)
            {
                // Distorted Weibull PDF
                double z = x / scale;
                double weibullPdf = (k / scale) * Math.Pow(z, k - 1) * Math.Exp(-Math.Pow(z, k));
                return (r / FTheta) * weibullPdf;
            }
            else
            {
                // Pareto PDF
                return (1 - r) * alpha * Math.Pow(theta, alpha) / Math.Pow(x, alpha + 1);
            }
        }

        /// <summary>
        /// Weibull-Pareto CDF
        /// </summary>
        public static double WeibullParetoCDF(double x, double k, double scale, double theta, double r)
        {
            if (k <= 0 || scale <= 0 || theta <= 0 || r <= 0 || r >= 1) return double.NaN;
            if (x <= 0) return 0;

            double FTheta = 1 - Math.Exp(-Math.Pow(theta / scale, k));
            double alpha = WeibullParetoAlpha(k, scale, theta, r);

            if (x < theta)
            {
                // Distorted Weibull CDF
                double weibullCdf = 1 - Math.Exp(-Math.Pow(x / scale, k));
                return (r / FTheta) * weibullCdf;
            }
            else
            {
                // Spliced Pareto CDF
                return 1 - (1 - r) * Math.Pow(theta / x, alpha);
            }
        }

        /// <summary>
        /// Weibull-Pareto Survival Function
        /// </summary>
        public static double WeibullParetoSF(double x, double k, double scale, double theta, double r)
        {
            return 1 - WeibullParetoCDF(x, k, scale, theta, r);
        }

        #endregion

        #region Exponential-Pareto

        /// <summary>
        /// Exponential-Pareto PDF
        /// Alpha is derived as θ * rate, r is derived as 1 - exp(-rate * θ)
        /// </summary>
        public static double ExponentialParetoPDF(double x, double rate, double theta)
        {
            if (rate <= 0 || theta <= 0) return double.NaN;
            if (x < 0) return 0;

            double r = 1 - Math.Exp(-rate * theta);
            double alpha = theta * rate;

            if (x < theta)
            {
                // Exponential PDF
                return rate * Math.Exp(-rate * x);
            }
            else
            {
                // Pareto PDF
                return (1 - r) * alpha * Math.Pow(theta, alpha) / Math.Pow(x, alpha + 1);
            }
        }

        /// <summary>
        /// Exponential-Pareto CDF
        /// </summary>
        public static double ExponentialParetoCDF(double x, double rate, double theta)
        {
            if (rate <= 0 || theta <= 0) return double.NaN;
            if (x < 0) return 0;

            double r = 1 - Math.Exp(-rate * theta);
            double alpha = theta * rate;

            if (x < theta)
            {
                // Exponential CDF
                return 1 - Math.Exp(-rate * x);
            }
            else
            {
                // Spliced Pareto CDF
                return 1 - (1 - r) * Math.Pow(theta / x, alpha);
            }
        }

        /// <summary>
        /// Exponential-Pareto Survival Function
        /// </summary>
        public static double ExponentialParetoSF(double x, double rate, double theta)
        {
            return 1 - ExponentialParetoCDF(x, rate, theta);
        }

        /// <summary>
        /// Get derived alpha for Exponential-Pareto
        /// </summary>
        public static double ExponentialParetoAlpha(double rate, double theta)
        {
            return theta * rate;
        }

        /// <summary>
        /// Get derived r for Exponential-Pareto
        /// </summary>
        public static double ExponentialParetoR(double rate, double theta)
        {
            return 1 - Math.Exp(-rate * theta);
        }

        #endregion

        #region Power-Pareto (Log-Laplace / Double Pareto)

        /// <summary>
        /// Power-Pareto PDF
        /// r is derived as α/(α+β) from C1 condition
        /// </summary>
        public static double PowerParetoPDF(double x, double alpha, double beta, double theta)
        {
            if (alpha <= 0 || beta <= 0 || theta <= 0) return double.NaN;
            if (x <= 0) return 0;

            double r = alpha / (alpha + beta);

            if (x < theta)
            {
                // Power function PDF
                return r * beta / theta * Math.Pow(x / theta, beta - 1);
            }
            else
            {
                // Pareto PDF
                return (1 - r) * alpha * Math.Pow(theta, alpha) / Math.Pow(x, alpha + 1);
            }
        }

        /// <summary>
        /// Power-Pareto CDF
        /// </summary>
        public static double PowerParetoCDF(double x, double alpha, double beta, double theta)
        {
            if (alpha <= 0 || beta <= 0 || theta <= 0) return double.NaN;
            if (x <= 0) return 0;

            double r = alpha / (alpha + beta);

            if (x < theta)
            {
                // Power function CDF
                return r * Math.Pow(x / theta, beta);
            }
            else
            {
                // Spliced Pareto CDF
                return 1 - (1 - r) * Math.Pow(theta / x, alpha);
            }
        }

        /// <summary>
        /// Power-Pareto Survival Function
        /// </summary>
        public static double PowerParetoSF(double x, double alpha, double beta, double theta)
        {
            return 1 - PowerParetoCDF(x, alpha, beta, theta);
        }

        /// <summary>
        /// Get derived r for Power-Pareto
        /// </summary>
        public static double PowerParetoR(double alpha, double beta)
        {
            return alpha / (alpha + beta);
        }

        #endregion

        #region Four-Parameter Pareto (Constrained Lomax Mixture)

        /// <summary>
        /// Four-Parameter Pareto PDF (α₁ = α₂ + 2)
        /// </summary>
        public static double FourParamParetoPDF(double x, double alpha2, double lambda1, double lambda2, double r)
        {
            if (alpha2 <= 0 || lambda1 <= 0 || lambda2 <= 0 || r <= 0 || r >= 1) return double.NaN;
            if (x < 0) return 0;

            double alpha1 = alpha2 + 2;

            double pdf1 = (alpha1 / lambda1) * Math.Pow(1 + x / lambda1, -(alpha1 + 1));
            double pdf2 = (alpha2 / lambda2) * Math.Pow(1 + x / lambda2, -(alpha2 + 1));

            return r * pdf1 + (1 - r) * pdf2;
        }

        /// <summary>
        /// Four-Parameter Pareto CDF
        /// </summary>
        public static double FourParamParetoCDF(double x, double alpha2, double lambda1, double lambda2, double r)
        {
            if (alpha2 <= 0 || lambda1 <= 0 || lambda2 <= 0 || r <= 0 || r >= 1) return double.NaN;
            if (x < 0) return 0;

            double alpha1 = alpha2 + 2;

            double cdf1 = 1 - Math.Pow(1 + x / lambda1, -alpha1);
            double cdf2 = 1 - Math.Pow(1 + x / lambda2, -alpha2);

            return r * cdf1 + (1 - r) * cdf2;
        }

        /// <summary>
        /// Four-Parameter Pareto Survival Function
        /// </summary>
        public static double FourParamParetoSF(double x, double alpha2, double lambda1, double lambda2, double r)
        {
            return 1 - FourParamParetoCDF(x, alpha2, lambda1, lambda2, r);
        }

        #endregion

        #region Five-Parameter Pareto (Unconstrained Lomax Mixture)

        /// <summary>
        /// Five-Parameter Pareto PDF
        /// </summary>
        public static double FiveParamParetoPDF(double x, double alpha1, double alpha2, double lambda1, double lambda2, double r)
        {
            if (alpha1 <= 0 || alpha2 <= 0 || lambda1 <= 0 || lambda2 <= 0 || r <= 0 || r >= 1) return double.NaN;
            if (x < 0) return 0;

            double pdf1 = (alpha1 / lambda1) * Math.Pow(1 + x / lambda1, -(alpha1 + 1));
            double pdf2 = (alpha2 / lambda2) * Math.Pow(1 + x / lambda2, -(alpha2 + 1));

            return r * pdf1 + (1 - r) * pdf2;
        }

        /// <summary>
        /// Five-Parameter Pareto CDF
        /// </summary>
        public static double FiveParamParetoCDF(double x, double alpha1, double alpha2, double lambda1, double lambda2, double r)
        {
            if (alpha1 <= 0 || alpha2 <= 0 || lambda1 <= 0 || lambda2 <= 0 || r <= 0 || r >= 1) return double.NaN;
            if (x < 0) return 0;

            double cdf1 = 1 - Math.Pow(1 + x / lambda1, -alpha1);
            double cdf2 = 1 - Math.Pow(1 + x / lambda2, -alpha2);

            return r * cdf1 + (1 - r) * cdf2;
        }

        /// <summary>
        /// Five-Parameter Pareto Survival Function
        /// </summary>
        public static double FiveParamParetoSF(double x, double alpha1, double alpha2, double lambda1, double lambda2, double r)
        {
            return 1 - FiveParamParetoCDF(x, alpha1, alpha2, lambda1, lambda2, r);
        }

        #endregion

        #region Utility Functions

        /// <summary>
        /// Local Pareto Alpha for any distribution (numerical approximation)
        /// α_d = d * f(d) / F̄(d)
        /// </summary>
        public static double LocalParetoAlpha(double pdf, double sf, double x)
        {
            if (sf <= 0) return double.PositiveInfinity;
            return x * pdf / sf;
        }

        #endregion
    }
}
