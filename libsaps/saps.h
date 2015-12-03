#ifndef SAPS_H_
#define SAPS_H_

#include <vector>
#include <map>
#include <iostream>
#include "param.h"
#include <memory>
#include <itpp/base/parser.h>
#include <itpp/base/itfile.h>

using namespace std;
using namespace itpp;

#define saps_reg_in(x) reg(#x, &x, true)
#define saps_reg_out(x) reg(#x, &x, false)

class saps {
private:
	bool SaveOnExit;
	bool DoNotSave;
	bool* ArgUsed;
	int ArgCnt;
	string* ArgNames;
	void CheckComplete() const;
	it_file* itf;
	Parser* pars;
	vector<param*> *in;
	vector<param*> *out;
	string NameFileResult;
	void write_file(vector<param*> *paramvec);
	void write_out(vector<param*> *paramvec, ostream& o) const;
	void clean();
	void clean(vector<param*> *paramvec);
	bool NameUsed(string name, vector<param*> *paramvec);
	bool NameUsed(string name);

public:
	saps(int argc, char** argv, bool SaveOnExit = true);
	~saps();
	void DoSaveOnExit();

	void write_file();
	void write_out(ostream &o) const;

	bool exist(string name) {
		return pars->exist(name);
	}

	template <typename T>
	void reg(string name, T* v, bool is_in = false) {
		if (this->NameUsed(name)) {
			it_error("Duplicate variable name " + name);
		}
		if (is_in) {
			bool success = pars->get(*v, name);
			if (!success) {
				it_error("Missing parameter " + name);
			}

			for (int i=0; i<this->ArgCnt; i++) {
				if (!name.compare(this->ArgNames[i])) {
					if (ArgUsed[i] == true) {
						it_error("Duplicate parameter entry " + name);
					} else {
						ArgUsed[i] = true;
					}
				}
			}
		}

		param* p = new param(name, v, typeid(T).name());

		if (is_in) {
			this->in->insert(this->in->end(), p);
		} else {
			this->out->insert(this->out->end(), p);
		}
	}

	friend ostream& operator<< (std::ostream& o, saps const& s);
};

#endif /* SAPS_H_ */
