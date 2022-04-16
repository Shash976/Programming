#include <iostream>
#include <fstream>
#include <string>
#include <chrono>
#include <thread>

using namespace std;

string filename, filecontent;

int main(){
    cout << "File name: ";
    getline(cin, filename);
    ifstream MyReadFile(filename);
    while (getline (MyReadFile, filecontent)) {
        // Output the text from the file
        cout << filecontent << '\n';
        }

        // Close the file
        MyReadFile.close();
    this_thread::sleep_for(chrono::milliseconds(5000));
}
