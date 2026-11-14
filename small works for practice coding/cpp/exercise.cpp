#include <iostream>
#include <vector>
using namespace std;

int main() {

    vector<int> no3 = {10, 10, 10, 10, 10};

    // 12. Reduce to 2 elements
    no3.resize(2);

    cout << "12. no3: ";
    for (int x : no3)
        cout << x << " ";
    cout << endl;


    // 13. Expand to 6 elements, new elements = 9
    no3.resize(6, 9);

    cout << "13. no3: ";
    for (int x : no3)
        cout << x << " ";
    cout << endl;


    // 14. Expand to 10 elements
    no3.resize(10);

    cout << "14. no3: ";
    for (int x : no3)
        cout << x << " ";
    cout << endl;

    return 0;
}