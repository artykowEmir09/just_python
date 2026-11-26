#include <iostream>
#include <stack>
using namespace std;
int main()
{
stack<char> mystack;

    mystack.push('C');
    mystack.push('A');

    cout << "Top element: " << mystack.top() <<endl;

    cout << "Is empty? "
              << (mystack.empty() ? "Yes" : "No")
              << endl;

    mystack.pop();

    cout << "After pop, top element: "
              << mystack.top() << endl;

    mystack.emplace('D');

    cout << "After emplace, top element: "
              << mystack.top() << endl;

    return 0;
}