#include "saps.h"
#include "param.h"

saps::saps(int argc, char** argv, bool SaveOnExit) {
	ArgNames = new string[argc];
	ArgUsed = new bool[argc];

	for (int a=0;a<argc;a++) {
		ArgUsed[a] = false;
		ArgNames[a] = argv[a];
		int EqPos = ArgNames[a].find("=");
		if (EqPos>0) {
			ArgNames[a] = ArgNames[a].substr(0,EqPos);
		} else if (a>0) {
			it_error("Parameter string " + ArgNames[a] + " is not valid one");
		}
	}

	ArgCnt = argc;

	pars = new Parser();
	pars->init(argc, argv);
	pars->set_silentmode(true);

	in = new vector<param*>;
	out = new vector<param*>;

	this->reg<string>("NameFileResult", &NameFileResult, true);

	itf = new it_file(NameFileResult);

	this->SaveOnExit = SaveOnExit;
}

saps::~saps() {
	if (SaveOnExit) {
		this->write_file();
	}

	delete pars;

	this->clean();
	delete in;
	delete out;

	itf->close();
	delete itf;
	delete[] ArgUsed;
	delete[] ArgNames;
}

void saps::CheckComplete() const {
	for (int i=1; i<this->ArgCnt; i++) {
		if (!this->ArgUsed[i]) {
			it_error("Argument " + this->ArgNames[i] + " is not used.");
		}
	}
}

void saps::clean() {
	this->clean(this->in);
	this->clean(this->out);
}

void saps::clean(vector<param*> *paramvec) {
	for (vector<param*>::iterator it = paramvec->begin(); it != paramvec->end(); ++it) {
		delete *it;
	}
}

void saps::write_file() {
	this->CheckComplete();
	write_file(this->in);
	write_file(this->out);
}

void saps::write_file(vector<param*> *paramvec) {
	for (vector<param*>::iterator it = paramvec->begin(); it != paramvec->end(); ++it) {
				param *p = *it;
				*(this->itf) << Name(p->getName()) << *p;
			}
}


void saps::write_out(vector<param*> *paramvec, ostream& o) const {
	for (vector<param*>::iterator it = paramvec->begin(); it != paramvec->end(); ++it) {
		param *p = *it;
		o << "\t" << p->getName() << ": " << *p << endl;
	}
}

void saps::write_out(ostream& o) const {
	this->CheckComplete();
	o << "In:" << endl;
	write_out(this->in, o);
	o << "Out:" << endl;
	write_out(this->out, o);
}

bool saps::NameUsed(string name, vector<param*>* paramvec) {
	for (vector<param*>::iterator it = paramvec->begin(); it != paramvec->end(); ++it) {
		param *p = *it;
		if (p->getName() == name) {
			return true;
		}
	}
	return false;
}

bool saps::NameUsed(string name) {
	return this->NameUsed(name, this->in) | this->NameUsed(name, this->out);
}

ostream& operator<<(std::ostream& o, saps const& s) {
	s.write_out(o);
	return o;
}
