#include <iostream>
#include <vector>
using namespace std;

int main() {

    int data[] = {1, 2, 3, 4, 5};

    // 1. Declare three vectors
    vector<int> no1;
    vector<int> no2;
    vector<int> no3;

    // 2. Assign five values of 10 to no1
    no1.assign(5, 10);

    cout << "no1: ";
    for (int x : no1) {
        cout << x << " ";
    }
    cout << endl;


    // 3. Assign first three values from data[] to no2
    no2.assign(data, data + 3);

    cout << "no2: ";
    for (int x : no2) {
        cout << x << " ";
    }
    cout << endl;


    // 4. Assign first three values from no1 to no3
    no3.assign(no1.begin(), no1.begin() + 3);

    cout << "no3: ";
    for (int x : no3) {
        cout << x << " ";
    }
    cout << endl;


    // 5. Assign 7, 8, 9 and 1 to no3
    no3.assign({7, 8, 9, 1});

    cout << "no3 after assigning new values: ";
    for (int x : no3) {
        cout << x << " ";
    }
    cout << endl;

    return 0;
}