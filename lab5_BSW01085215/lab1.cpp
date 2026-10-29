 

#include <iostream>
#include <queue>
#include <string>
using namespace std;

void displayScripts(queue<string> scripts) {
    if (scripts.empty()) {
        cout << "No scripts remaining.";
        return;
    }

    while (!scripts.empty()) {
        cout << scripts.front() << " ";
        scripts.pop();
    }
}

int main() {
    queue<string> scripts;
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
        cout << "\nRecent answer script added: ";
        cout << scripts.back() << endl;
    }
    else {
        cout << "\nNo answer scripts available." << endl;
    }

    cout << "\nEnter number of scripts to mark: ";
    cin >> markCount;

    cout << "\nScripts selected for marking: ";

    for (int i = 0; i < markCount && !scripts.empty(); i++) {
        cout << scripts.front() << " ";
        scripts.pop();
    }

    cout << "\nRemaining scripts: ";
    displayScripts(scripts);

    cout << endl;
    return 0;
}
