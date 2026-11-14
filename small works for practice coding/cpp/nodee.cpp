#include <iostream>
using namespace std;

class Node {
public:
    int no;
    Node *next;
};

int main() {
    Node *n = new Node();

    n->no = 6;
    n->next = NULL;

    cout << n->no << endl;

    return 0;
}