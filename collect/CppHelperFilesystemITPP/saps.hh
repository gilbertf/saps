#ifndef GJML_HH
#define GJML_HH

#include <string>
#include "itpp/itcomm.h"
#include <unistd.h> //getcwd
#include <limits.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <pwd.h>
#include <errno.h>

using namespace std;
using namespace itpp;

string construct_result_it_filename(int,char**);
bool file_exists(string);
string get_exepath();
string replace_tilde_by_home(string);
string replace_home_by_tilde(string);
int GetVersionFile(string);
bool check_file(string filename, int Version);
bool check_path( string filename);
bool mkpath( std::string path );

#endif
