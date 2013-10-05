function MatlabGauss(x, Expectation, Variance, FilenameResults)
    Sigma = sqrt(Variance);
    pdf = (1/(Sigma*sqrt(2*pi))) * exp(-(x-Expectation)^2/(2*Variance));
    cdf = 0.5 * (1+erf((x-Expectation)/sqrt(2*Variance)));
    Complete = 1;
    itsave(FilenameResults, x, Expectation, Variance, pdf, cdf, Sigma, Complete);
end
