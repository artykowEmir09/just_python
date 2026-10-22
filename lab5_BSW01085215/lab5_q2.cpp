
/*Subject code : CSEB3213 Data Structures and Algorithms
  Section      : 01B
  Student name : Artykov Emir
  Student ID no: BSW01085215
  Question no  : 2 */

#include <iostream>
#include <string>
using namespace std;
 
struct Node {
    string studentID;
    Node* next;
};
 
void pushScript(Node*& top, string id) {
    Node* newNode = new Node;

    newNode->studentID = id;
    newNode->next = top;
    top = newNode;
}
 
string popScript(Node*& top) {
    if (top == nullptr) {
        return "";
    }

    Node* temp = top;
    string id = temp->studentID;

    top = top->next;
    delete temp;

    return id;
}


int countScripts(Node* top) {
    int count = 0;

    while (top != nullptr) {
        count++;
        top = top->next;
    }

    return count;
}


void displayScripts(Node* top) {
    if (top == nullptr) {
        cout << "No scripts remaining.";
        return;
    }

    while (top != nullptr) {
        cout << top->studentID << " ";
        top = top->next;
    }
}

int main() {
    Node* top = nullptr;
    string studentID;
    int total, markCount;

    cout << "Enter number of answer scripts: ";
    cin >> total;

    for (int i = 0; i < total; i++) {
        cout << "Enter student ID: ";
        cin >> studentID;
        pushScript(top, studentID);
    }

    if (top != nullptr) {
        cout << "\nTop answer script: ";
        cout << top->studentID << endl;
    }
    else {
        cout << "\nNo answer scripts available." << endl;
    }

    cout << "\nEnter number of scripts to mark: ";
    cin >> markCount;

    cout << "\nScripts selected for marking: ";

    for (int i = 0; i < markCount && top != nullptr; i++) {
        cout << popScript(top) << " ";
    }

    cout << "\nRemaining scripts: ";
    displayScripts(top);

  
    while (top != nullptr) {
        popScript(top);
    }

    cout << endl;
    return 0;
}
