#include "saps.h"

using namespace std;

int main(int argc, char** argv) {


	try {
		saps *s = new saps(argc, argv);

		int more = 99;
		//s->reg("more", &more, false);
		s->saps_reg_out(more);

		double Es = 0.0781;
		s->reg("Es", &Es, false);

		string hi;
		s->reg("hi", &hi, true);

		//cmat *m = new cmat(10,10);
		//s->reg("m", m, false);

		bvec v(2);
		s->reg("v", &v, false);
		s->write_file();

		cout << *s << endl;

		delete s;
		//delete m;
	} catch (string* e) {
		cout << "Exception: " << *e << endl;
	}
}
