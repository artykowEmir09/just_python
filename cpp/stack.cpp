#include <iostream>
#include <stack>

using namespace std;

int main() {
    stack<int> myStack;
    int num;

    // 1. Accept five (5) integer values from user[cite: 2]
    cout << "Enter 5 integer values:" << endl;
    for (int i = 0; i < 5; i++) {
        cout << "Value " << (i + 1) << ": ";
        cin >> num;
        myStack.push(num);
    }

    // 2. Display total data in stack[cite: 2]
    cout << "\nTotal data in stack: " << myStack.size() << endl;

    // 3. Remove data one by one until empty, displaying each before removal[cite: 2]
    cout << "\nRemoving elements from stack:" << endl;
    while (!myStack.empty()) {
        cout << "Removing: " << myStack.top() << endl; // Display top element[cite: 2]
        myStack.pop();                                 // Remove top element[cite: 2]
    }

    return 0;
}