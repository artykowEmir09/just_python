// Create a stack program that accepts five (5) integer values from user.
// Display total data in stack.
// Remove the data in stack, one by one until the stack is empty. Display the data before you remove it.


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