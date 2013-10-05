/** Initializing parser **/
Parser parser;
parser.init(argc, argv);
parser.set_silentmode();
char cwdstr[500];
string Program = "bin";
string NamePathProgram = get_exepath();

Program = NamePathProgram.substr(NamePathProgram.rfind("/")+1,-1);
string NameFileTemplate = NamePathProgram + "Template.saps";

if (!file_exists(NameFileTemplate.c_str())) {
	ofstream FileTemplate(NameFileTemplate.c_str());

	FileTemplate << "# This is a template for " << Program << " showing all accepted input and output parameters. Furthermore some FileTemplate plot options are shown. Have fun:)" << endl << endl;
	FileTemplate << "Program: " << replace_home_by_tilde(NamePathProgram) << endl << endl;

	FileTemplate << "# Gnuplot options" << endl;
	FileTemplate << "PlotSet: grid" << endl;
	FileTemplate << "#PlotSet: size square" << endl;
	FileTemplate << "#PlotSet: xtics 0.2" << endl;
	FileTemplate << "#PlotSet: ytics 0.2" << endl;
	FileTemplate << "#PlotSet: xrange [0:1]" << endl;
	FileTemplate << "#PlotSet: yrange [0:1]" << endl << endl;

	FileTemplate << "# Input variables" << endl;
	#define X(a,b) FileTemplate << #b << ": " << endl;
		INPUTVARS
	#undef X
	
	#ifdef OPTINPUTVARS
		FileTemplate << endl << "# Optional input variables" << endl;
	#define X(a,b) FileTemplate << "#" << #b << ": " << endl;
		OPTINPUTVARS
	#undef X
	#endif
	
	FileTemplate << endl;
	FileTemplate << "Figure Example application:" << endl;
	FileTemplate << "  Set First parameter set:" << endl;
	FileTemplate << "    PlotOpt: w lines" << endl;
	FileTemplate << "    #Analyse: integrate.py, y" << endl;
	FileTemplate << "    #Output variables that can be used for Axis: ";
	#define X(a,b) FileTemplate << #b << ", ";
		OUTPUTVARS
	#undef X
	FileTemplate << "Duration" << endl;
	FileTemplate << "    Axis: , " << endl;
	FileTemplate.close();
	cout << "Created template file: " << NameFileTemplate << " for your joy" << endl;
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
string NameFileItppResults = construct_result_it_filename(argc, argv, DirResults);
check_path(NameFileItppResults);
check_file(NameFileItppResults, Version);

#ifdef debug
	cout << "Saving results to: " << NameFileItppResults << endl;
#endif

it_file FileItppResults;
ofstream FilePlainResults;

Real_Timer timer;
timer.start();
int LastTime = timer.get_time();

int Time;
#include "WriteOutputVars.inc"
