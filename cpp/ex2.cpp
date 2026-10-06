#include <iostream>
#include <vector>
using namespace std;

int main() {

    vector<int> no3 = {10, 10, 9, 9, 9, 9, 0, 0, 0, 0};

    // 15. Update 3rd element to 8
    no3[2] = 8;

    cout << "no3: ";
    for (int x : no3)
        cout << x << " ";
    cout << endl;

    // 16. Display first and last element
    cout << "First element: " << no3.front() << endl;
    cout << "Last element: " << no3.back() << endl;

    return 0;
}