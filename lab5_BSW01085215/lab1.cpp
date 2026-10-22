 

#include <iostream>
#include <stack>
#include <string>
using namespace std;

void displayScripts(stack<string> scripts) {
    if (scripts.empty()) {
        cout << "No scripts remaining.";
        return;
    }

    while (!scripts.empty()) {
        cout << scripts.top() << " ";
        scripts.pop();
    }
}

int main() {
    stack<string> scripts;
    string studentID;
    int total, markCount;

    cout << "Enter number of answer scripts: ";
    cin >> total;

    for (int i = 0; i < total; i++) {
        cout << "Enter student ID: ";
        cin >> studentID;
        scripts.push(studentID);
    }

    if (!scripts.empty()) {
        cout << "\nTop answer script: ";
        cout << scripts.top() << endl;
    }
    else {
        cout << "\nNo answer scripts available." << endl;
    }

    cout << "\nEnter number of scripts to mark: ";
    cin >> markCount;

    cout << "\nScripts selected for marking: ";

    for (int i = 0; i < markCount && !scripts.empty(); i++) {
        cout << scripts.top() << " ";
        scripts.pop();
    }

    cout << "\nRemaining scripts: ";
    displayScripts(scripts);

    cout << endl;
    return 0;
}
