#include <iostream>
#include <stack>
using namespace std;

int main()
{
    stack<int> myStack;
    int num;

    // Accept 5 integers from user
    for (int i = 1; i <= 5; i++)
    {
        cout << "Enter value " << i << ": ";
        cin >> num;
        myStack.push(num);
    }

    // Display total data in stack
    cout << "\nTotal data in stack : " << myStack.size() << endl;

    // Remove data one by one
    cout << "\n::Deletion process::" << endl;

    while (!myStack.empty())
    {
        cout << "Top value: " << myStack.top() << endl;
        myStack.pop();
    }

    cout << "Stack is empty" << endl;

    return 0;
}