#include <iostream>
#include <vector>
using namespace std;

int main() {

    int data[] = {1, 2, 3, 4, 5};

    vector<int> no1;
    vector<int> no2;
    vector<int> no3;

    // 2
    no1.assign(5, 10);

    cout << "no1: ";
    for (int x : no1)
        cout << x << " ";
    cout << endl;

    // 3
    no2.assign(data, data + 3);

    cout << "no2: ";
    for (int x : no2)
        cout << x << " ";
    cout << endl;

    // 4
    no3.assign(no1.begin(), no1.begin() + 3);

    cout << "no3: ";
    for (int x : no3)
        cout << x << " ";
    cout << endl;

    // 5
    no3.assign({7, 8, 9, 1});

    cout << "no3: ";
    for (int x : no3)
        cout << x << " ";
    cout << endl;

    // 6. Add 8 at the end of no3
    no3.push_back(8);

    cout << "no3: ";
    for (int x : no3)
        cout << x << " ";
    cout << endl;

    // 7. Delete the last value of no2
    no2.pop_back();

    cout << "no2: ";
    for (int x : no2)
        cout << x << " ";
    cout << endl;

    // 8. Add 4 as the 3rd data of no3
    no3.insert(no3.begin() + 2, 4);

    cout << "no3: ";
    for (int x : no3)
        cout << x << " ";
    cout << endl;

    // 9. Delete the 5th value of no3
    no3.erase(no3.begin() + 4);

    cout << "no3: ";
    for (int x : no3)
        cout << x << " ";
    cout << endl;

    // 10. Exchange no1 and no3
    no1.swap(no3);

    cout << "no1: ";
    for (int x : no1)
        cout << x << " ";
    cout << endl;

    cout << "no3: ";
    for (int x : no3)
        cout << x << " ";
    cout << endl;

    // 11. Empty no2
    no2.clear();

    cout << "no2: ";
    for (int x : no2)
        cout << x << " ";
    cout << endl;

    return 0;
}