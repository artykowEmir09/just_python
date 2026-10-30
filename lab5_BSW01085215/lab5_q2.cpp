
#include <iostream>
#include <string>
using namespace std;

struct Node {
    string studentID;
    Node* next;
};

void enqueueScript(Node*& front, Node*& rear, string id) {
    Node* newNode = new Node{id, nullptr};

    if (front == nullptr)
        front = rear = newNode;
    else {
        rear->next = newNode;
        rear = newNode;
    }
}

string dequeueScript(Node*& front, Node*& rear) {
    if (front == nullptr)
        return "";

    Node* temp = front;
    string id = temp->studentID;
    front = front->next;

    if (front == nullptr)
        rear = nullptr;

    delete temp;
    return id;
}

int countScripts(Node* front) {
    int count = 0;

    while (front != nullptr) {
        count++;
        front = front->next;
    }

    return count;
}

void displayScripts(Node* front) {
    if (front == nullptr) {
        cout << "No scripts remaining.";
        return;
    }

    while (front != nullptr) {
        cout << front->studentID << " ";
        front = front->next;
    }
}                
                                   
int main() {
    Node* front = nullptr;
    Node* rear = nullptr;
    string id;
    int total, markCount;

    cout << "Enter number of answer scripts: ";
    cin >> total;

    for (int i = 0; i < total; i++) {
        cout << "Enter student ID: ";
        cin >> id;
        enqueueScript(front, rear, id);
    }

    if (front != nullptr)
        cout << "\nFront answer script: " << front->studentID << endl;
    else
        cout << "\nNo answer scripts available." << endl;

    cout << "\nEnter number of scripts to mark: ";
    cin >> markCount;

    cout << "\nScripts selected for marking: ";

    for (int i = 0; i < markCount && front != nullptr; i++)
        cout << dequeueScript(front, rear) << " ";

    cout << "\nRemaining scripts: ";
    displayScripts(front);

    cout << "\nTotal scripts remaining: " << countScripts(front) << endl;

    while (front != nullptr)
        dequeueScript(front, rear);

    return 0;
}
