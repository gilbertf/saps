#ifndef PARAM_H_
#define PARAM_H_

#include <string>
#include <iostream>
#include <itpp/base/binfile.h>
#include <itpp/base/itfile.h>
#include <typeinfo>

using namespace std;
using namespace itpp;

class param {
private:
	string name;
	void* value;
	string type;

public:
	string getName();
	void* getValue() const;
	param(string name, void* value, string type);


	template<typename T>
	friend T& operator<<(T &f, param const& p) {
		#define customcast(x) if (p.type == typeid(x).name()) {f << * (x*) p.value;}
			customcast(int)
			else customcast(double)
			else customcast(string)
			else customcast(mat)
			else customcast(bmat)
			else customcast(cmat)
			else customcast(vec)
			else customcast(bvec)
			else customcast(cvec)
		#undef customcast
		else {
			it_error("Unsupported type: " + p.type);
		}

		return f;
	}
};
#endif /* PARAM_H_ */
