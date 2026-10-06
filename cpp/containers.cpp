#include <iostream>
using namespace std;

class MyClass{
    struct Node{
        int data;
        Node *next;
    };

    Node *head;

public:
    MyClass(){
        head = NULL;
    }

    Node* createNode(){
        Node *n = new Node();

        cout << "Enter a number: ";
        cin >> n->data;

        n->next = NULL;

        return n;
    }
};