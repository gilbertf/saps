/** Initializing parser **/
Parser parser;
parser.init(argc, argv);
parser.set_silentmode();
char cwdstr[500];
string appname = "bin";
string fullpath = get_exepath();

appname = fullpath.substr(fullpath.rfind("/")+1,-1);
string fnexample = fullpath + ".saps.template";

if (!file_exists(fnexample.c_str())) {
	ofstream example(fnexample.c_str());

	/**Show .saps example **/
	example << "# This is a template for " << appname << " showing all accepted input and output parameters. Furthermore some example plot options are shown. Have fun:)" << endl << endl;
	example << "Program: " << replace_home_by_tilde(fullpath) << endl << endl;

	example << "# Gnuplot options" << endl;
	example << "PlotSet: grid" << endl;
	example << "PlotSet: size square" << endl;
	example << "PlotSet: xtics 0.2" << endl;
	example << "PlotSet: ytics 0.2" << endl;
	example << "PlotSet: xrange [0:1]" << endl;
	example << "PlotSet: yrange [0:1]" << endl << endl;

	example << "# Input variables" << endl;
	#define X(a,b) example << #b << ": " << endl;
		INPUTVARS
	#undef X
	
	#ifdef OPTINPUTVARS
		example << endl << "# Optional input variables" << endl;
	#define X(a,b) example << "#" << #b << ": " << endl;
		OPTINPUTVARS
	#undef X
	#endif
	
	example << endl;
	example << "Figure Example application:" << endl;
	example << "  Set First parameter set:" << endl;
	example << "    PlotOpt: w lines" << endl;
	example << "    Analyse: integrate.py, y" << endl;
	example << "    # Output variables that can be used for Axis: ";
	#define X(a,b) example << #b << ", ";
		OUTPUTVARS
		X(double, Duration)
		X(double, Complete)
	#undef X
	example << endl << "    Axis: x, y" << endl;
	example.close();
	cout << "Created template file: " << fnexample << " for your joy" << endl;
}

/** Parse input variables **/
#define X(a,b) a b = parser.get_##a(#b); inputvarcnt++;
	int inputvarcnt = 0;
	INPUTVARS
	X(string, DirResults)
#undef X

#ifdef OPTINPUTVARS
	#define X(a,b) a b; bool specified_##b = false; if (parser.exist(#b)) { specified_##b = true; b = parser.get_##a(#b); };
		OPTINPUTVARS
	#undef X
#endif

#define X(a,b) if (strncmp(argv[i], #b, strlen( #b )) == 0) continue;
	for (int i=1; i<argc;i++) {
		INPUTVARS
		X(string, DirResults)
		#ifdef OPTINPUTVARS
			OPTINPUTVARS
		#endif
		stringstream err_ss;
		err_ss << argv[0] << ": You specified " << strtok(argv[i],"=") << " which is a irrelevant input variable";
#undef X
#define X(a,b) #b " "
		err_ss << ", we only accept: " INPUTVARS ;
		it_error(err_ss.str());
	}
#undef X

/** Initalizing output variables **/
#define X(a,b) a b;
	OUTPUTVARS
	X(double, Duration)
	X(double, Complete)
#undef X
int Version = VERSION;
Complete = -1; //Default value -1 to detect if complete is not updated by program
Duration = -1;

/** Printing input variables **/
#ifdef debug
	cout << "===== Input variables =====" << endl;
	cout.width(20); cout << left << "Type";
	cout.width(20); cout << left << "Name";
	cout.width(20); cout << left << "Value" << endl;
	#define X(a,b) cout.width(20); cout << #a; cout.width(20); cout << #b; cout.width(20); cout << b << endl;
		INPUTVARS
	#undef X
	cout << endl;
	#ifdef OPTINPUTVARS
		cout << "===== Optional Input variables =====" << endl;
		cout.width(20); cout << left << "Type";
		cout.width(20); cout << left << "Name";
		cout.width(20); cout << left << "Value" << endl;
		#define X(a,b) if ( specified_##b == true) { cout.width(20); cout << #a; cout.width(20); cout << #b; cout.width(20); cout << b << endl;}
			OPTINPUTVARS
		#undef X
		cout << endl;
	#endif
	
	cout << "===== Simulation =====" << endl;
#endif


/**Initializing results file **/
string outfilename = construct_result_it_filename(argc, argv, DirResults);
check_path(outfilename);
check_file(outfilename, Version);

#ifdef debug
	cout << "Saving results to: " << outfilename << endl;
#endif

it_file it;
ofstream it_plaintxt;

Real_Timer timer;
timer.start();
int LastTime = timer.get_time();

int Time;
#include "WriteOutputVars.inc"
