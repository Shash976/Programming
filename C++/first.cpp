#include <iostream>
#include <vector>
#include <string>

using namespace std;
string name;
int x, y, z;

int main()
{
    /*
    cout << "Number 1: ";
   cin >> x;
   cout << "Number2: ";
   cin >> y;
   z = x | y;
   cout << x << " | " << y << " equals " << z;
    */
   
    cout << "Name: ";
    getline (cin, name);
    cout << "Hi, " << name << " \nYour name is " << name.size() << " characters long";
    name[0] = '\nP';
    cout << name;
   
   return 0;
}
