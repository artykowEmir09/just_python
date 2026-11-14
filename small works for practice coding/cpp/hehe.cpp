#include <iostream>
using namespace std;

class MyClass {
    struct Node {
        int data;
        Node* next;
    };

    Node* life;
    int skill;

public:
    MyClass() {
        life = NULL;
        skill = 0;
    }

    void addNode(int value) {
        Node* n = new Node();

        n->data = value;
        n->next = NULL;

        if (life == NULL) {
            life = n;
        }
        else {
            Node* temp = life;

            while (temp->next != NULL) {
                temp = temp->next;
            }

            temp->next = n;
        }
    }

    void fight() {
        while (life != NULL) {
            skill++;

            cout << "Bring it on!!" << endl;

            life = life->next;
        }

        cout << "Skill: " << skill << endl;
    }
};

int main() {
    MyClass player;

    player.addNode(10);
    player.addNode(20);
    player.addNode(30);
    player.addNode(40);

    player.fight();

    return 0;
}
