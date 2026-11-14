#include <iostream>
#include <string>
using namespace std;

class Node {
public:
    string name;
    int id;
    Node *next;
};

int main() {
    Node *n = new Node();

    n->name = "Ali";
    n->id = 103;
    n->next = NULL;

    return 0;
}