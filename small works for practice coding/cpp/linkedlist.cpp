#include <iostream>
using namespace std;

struct Node
{
    int data;
    Node *next;
};

void display(Node *head)
{
    Node *current = head;

    while (current != NULL)
    {
        cout << current->data << " ";
        current = current->next;
    }

    cout << endl;
}

void insertBeginning(Node *&head, int value)
{
    Node *newNode = new Node();

    newNode->data = value;
    newNode->next = head;

    head = newNode;
}

void insertEnd(Node *&head, int value)
{
    Node *newNode = new Node();

    newNode->data = value;
    newNode->next = NULL;

    if (head == NULL)
    {
        head = newNode;
        return;
    }

    Node *current = head;

    while (current->next != NULL)
    {
        current = current->next;
    }

    current->next = newNode;
}

void deleteBeginning(Node *&head)
{
    if (head == NULL)
        return;

    Node *temp = head;

    head = head->next;

    delete temp;
}

void deleteEnd(Node *&head)
{
    if (head == NULL)
        return;

    if (head->next == NULL)
    {
        delete head;
        head = NULL;
        return;
    }

    Node *current = head;

    while (current->next->next != NULL)
    {
        current = current->next;
    }

    delete current->next;
    current->next = NULL;
}

int main()
{
    Node *head = NULL;

    insertEnd(head, 10);
    insertEnd(head, 20);
    insertEnd(head, 30);

    display(head);

    insertBeginning(head, 5);

    display(head);

    deleteBeginning(head);

    display(head);

    deleteEnd(head);

    display(head);
}