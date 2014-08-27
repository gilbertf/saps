#include "param.h"

string param::getName() {
	return this->name;
}

void* param::getValue() const {
	return this->value;
}

param::param(string name, void* value, string type) {
	this->value = value;
	this->name = name;
	this->type = type;
}
