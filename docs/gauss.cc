#include "saps.hh"
#include <cmath>
#include "saps.cc"

using namespace itpp;
using namespace std;

#define VERSION 3

#define INPUTVARS \
X(double, x) \
X(double, Expectation) \
X(double, Variance)

#define OPTINPUTVARS \
X(int, Verbose)

#define OUTPUTVARS \
X(double, cdf) \
X(double, pdf) \
X(double, Sigma)

int main(int argc, char *argv[]) {
	#include "ParseParameters.inc"
	Complete = 0; //special variable defined in the include to communicate the processing progress
	Sigma = sqrt(Variance);
	Complete = 0.1;
	#include "WriteInLoop.inc"
	pdf = (1/(Sigma*sqrt(2*pi))) * exp(-pow(x-Expectation,2)/(2*Variance));
	Complete = 0.5;
	#include "WriteInLoop.inc"
	cdf = 0.5 * (1+erf((x-Expectation)/sqrt(2*Variance)));
	Complete = 1;
	#include "WriteOutputVars.inc"
}
	
	
