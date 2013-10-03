#include "saps.hh"

string get_exepath() {
	char result[ PATH_MAX ];
	ssize_t count = readlink( "/proc/self/exe", result, PATH_MAX );
	string path = std::string( result, (count > 0) ? count : 0 );
	return path;
}

string replace_home_by_tilde(string path) {
	struct passwd *pw = getpwuid(getuid());
	string home_path = pw->pw_dir;
	int pos =  path.find(home_path);
	if (pos != -1) {
		path.replace(pos, home_path.length(),"~");
	}
	return path;
}

string replace_tilde_by_home(string path) {
	struct passwd *pw = getpwuid(getuid());
	string home_path = pw->pw_dir;
	int pos =  path.find("~");
	if (pos != -1) {
		path.replace(pos, 1, home_path);
	}
	return path;
}

bool check_file(string filename, int Version) {
	bool exists = file_exists(filename);
	if (exists) {
		int VersionFile = GetVersionFile(filename);
		if (VersionFile == Version) {
			it_error("File " + filename + " was created before and same program version used.");
		} else if (VersionFile > Version) {
			it_error("File " + filename + " was created with a newer version, strange.");
		}
	}
	return false;
}

int GetVersionFile(string filename) {
	it_file itversion(filename);
	if (itversion.exists("Version")) {
		int VersionFile;
		itversion >> Name("Version") >> VersionFile;
		return VersionFile;
	}
	it_error("No version variable found.");
}

bool file_exists(string filename) {
	ifstream ifile(filename.c_str());
	bool exists = false;;
	if (ifile) {
		exists = true;
		ifile.close();
	}
	return exists;
}

bool check_path( string filename) {
	int pos = filename.find_last_of('/');
	string path = filename.substr(0,pos);
	return mkpath(path);
}

bool mkpath( std::string path ) {
    bool bSuccess = false;
    int nRC = ::mkdir( path.c_str(), 0775 );
    if( nRC == -1 )
    {
        switch( errno )
        {
            case ENOENT:
                //parent didn't exist, try to create it
                if( mkpath( path.substr(0, path.find_last_of('/')) ) )
                    //Now, try to create again.
                    bSuccess = 0 == ::mkdir( path.c_str(), 0775 );
                else
                    bSuccess = false;
                break;
            case EEXIST:
                //Done!
                bSuccess = true;
                break;
            default:
                bSuccess = false;
                break;
        }
    }
    else
        bSuccess = true;
    return bSuccess;
}

string construct_result_it_filename(int argc, char** argv) {
	string bn = argv[0];
	int spos = bn.find_last_of("/");
	if (spos != -1) {
		int slen = bn.length();
		bn = bn.substr(spos+1,slen-spos);
	}
	stringstream filename_it;
	filename_it << replace_tilde_by_home(RAW_RESULTS_DIR) << bn << "/";
	for (int i=1;i<argc;i++) {
		filename_it << argv[i];
		if (i < argc-1) filename_it << "_";
	}
	#ifdef debug
		cout << "Opened file: " << filename_it.str() << endl;
	#endif
	return filename_it.str();
}
