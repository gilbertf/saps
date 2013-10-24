FileItppResults.open(NameFileItppResults);

FilePlainResults.open((NameFileItppResults + (string)".plaintxt").c_str());

Duration = timer.get_time(); 	

/** Printing output variables **/
#ifdef debug
	cout << endl << "===== Output variables =====" << endl;
	cout.width(10);
	cout << left << "Type";
	cout.width(20);
	cout << left << "Name";
	cout.width(15);
	cout << left << "Value" << endl;
	#define X(a,b) cout.width(10); cout << #a; cout.width(20); cout << #b; cout.width(15); cout << b << endl;
		#ifdef OUTPUTVARS
			OUTPUTVARS
		#endif
		X(double, Duration)
		X(double, Complete)
	#undef X
#endif

/** Save values to Itpp results file **/
#define X(a,b) FileItppResults << Name(#b) << b;
	#ifdef INPUTVARS
		INPUTVARS
	#endif
	#ifdef OPTINPUTVARS
		OPTINPUTVARS
	#endif
	#ifdef OUTPUTVARS
		OUTPUTVARS
	#endif
	X(double, Duration)
	X(double, Complete)
	X(int , Version)
#undef X
FileItppResults.close();

/** Save values to plaintxt results file **/
#define X(a,b) FilePlainResults << #b << "\t" << b << endl;
	#ifdef INPUTVARS
		INPUTVARS
	#endif
	#ifdef OPTINPUTVARS
		OPTINPUTVARS
	#endif
	#ifdef OUTPUTVARS
		OUTPUTVARS
	#endif
	X(double, Duration)
	X(double, Complete)
	X(int , Version)
#undef X
FilePlainResults.close();
