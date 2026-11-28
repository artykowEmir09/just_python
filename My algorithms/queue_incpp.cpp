#include <iostream>
#include <queue>

using namespace std;

int main()
{
    // declare a queue
    queue<int> myQ1;

    cout << "Q1 size: " << myQ1.size() << endl;

    if (myQ1.empty())
    {
        cout << "Q1 is empty\n";
    }

    cout << "Append 10\n";
    myQ1.push(10);

    cout << "Append 20\n";
    myQ1.push(20);

    cout << "Q1 size: " << myQ1.size() << endl;

    cout << "Append 30\n";
    myQ1.push(30);

    cout << "Q1 size: " << myQ1.size() << endl;
    cout << "Q1 front: " << myQ1.front() << endl;
    cout << "Q1 rear: " << myQ1.back() << endl;

    cout << "Append 50\n";
    myQ1.push(50);

    cout << "Serve Q1: " << myQ1.front() << endl;
    myQ1.pop();

    cout << "Q1 size: " << myQ1.size() << endl;
    cout << "Q1 front: " << myQ1.front() << endl;
    cout << "Q1 rear: " << myQ1.back() << endl;

    if (myQ1.empty())
    {
        cout << "Q1 is empty\n";
    }
    else
    {
        cout << "Serve Q1: " << myQ1.front() << endl;
        myQ1.pop();
    }

    return 0;
}