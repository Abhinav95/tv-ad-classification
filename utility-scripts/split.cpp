#include <bits/stdc++.h>

using namespace std;

int main(int argc, char *argv[]){
	if(argc < 2){
		cout << "Usage: ./split <filename> <every how many lines> <train/test>" << endl;
		return 0;
	}
	ifstream myfile;
	string line;
	myfile.open(argv[1]);
	int cur = 1;
	int max = atoi(argv[2]);
	if(myfile.is_open()){
		while(getline(myfile,line)){
			if(cur<max-1&&!strcmp(argv[3],"train")){
				cout << line << endl;
			}
			else if(cur==max-1&&!strcmp(argv[3],"test")){
				cout << line << endl;
			}
			cur++;
			if(cur >= max){
				cur = 1;
			}
		}
		myfile.close();
	}
	return 0;
}