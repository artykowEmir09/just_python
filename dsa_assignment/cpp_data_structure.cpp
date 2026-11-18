#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <iomanip>

using namespace std;

struct Participant {
    int id;
    string name, eventName;
    bool registered;
    Participant* next;
    Participant(int i, string n, string e) : id(i), name(n), eventName(e), registered(true), next(NULL) {}
};

struct WaitNode {
    int participantId;
    WaitNode* next;
    WaitNode(int id) : participantId(id), next(NULL) {}
};

struct ParticipantView {
    int id;
    string name, eventName;
};

class EventSystem {
private:
    Participant* head;
    WaitNode *front, *rear;

    Participant* searchByIdInternal(int id) {
        Participant* temp = head;
        while(temp) {
            if(temp->id == id) return temp;
            temp = temp->next;
        }
        return NULL;
    }

    void merge(vector<int>& arr, int left, int mid, int right) {
        int n1 = mid - left + 1, n2 = right - mid;
        vector<int> L(n1), R(n2);
        for(int i = 0; i < n1; i++) L[i] = arr[left + i];
        for(int j = 0; j < n2; j++) R[j] = arr[mid + 1 + j];
        int i = 0, j = 0, k = left;
        while(i < n1 && j < n2) arr[k++] = (L[i] <= R[j]) ? L[i++] : R[j++];
        while(i < n1) arr[k++] = L[i++];
        while(j < n2) arr[k++] = R[j++];
    }

    void mergeSort(vector<int>& arr, int left, int right) {
        if(left < right) {
            int mid = left + (right - left) / 2;
            mergeSort(arr, left, mid);
            mergeSort(arr, mid + 1, right);
            merge(arr, left, mid, right);
        }
    }

public:
    EventSystem() : head(NULL), front(NULL), rear(NULL) {}

    ~EventSystem() {
        while(head) { Participant* t = head; head = head->next; delete t; }
        while(front) { WaitNode* t = front; front = front->next; delete t; }
    }

    void registerParticipant(int id, string name, string eventName) {
        if(searchByIdInternal(id)) { cout << "Error: ID already exists.\n"; return; }
        Participant* newNode = new Participant(id, name, eventName);
        if(!head) head = newNode;
        else {
            Participant* temp = head;
            while(temp->next) temp = temp->next;
            temp->next = newNode;
        }
        cout << "Success: Participant Registered for '" << eventName << "'.\n";
    }

    void removeParticipant(int id) {
        if(!head) { cout << "No participants found.\n"; return; }
        if(head->id == id) {
            Participant* t = head; head = head->next; delete t;
            cout << "Success: Participant Removed.\n";
            return;
        }
        Participant* temp = head;
        while(temp->next && temp->next->id != id) temp = temp->next;
        if(!temp->next) cout << "Error: Not Found.\n";
        else {
            Participant* t = temp->next; temp->next = temp->next->next; delete t;
            cout << "Success: Participant Removed.\n";
        }
    }

    void updateParticipant(int id) {
        Participant* p = searchByIdInternal(id);
        if(!p) { cout << "Error: Not Found.\n"; return; }
        cout << "Current: " << p->name << " | " << p->eventName << "\nEnter New Name: ";
        cin.ignore(); getline(cin, p->name);
        cout << "Enter New Event: "; getline(cin, p->eventName);
        cout << "Success: Updated.\n";
    }

    void displaySingle(Participant* p) {
        cout << "\nID: " << p->id << "\nName: " << p->name << "\nEvent: " << p->eventName 
             << "\nStatus: " << (p->registered ? "Registered" : "Unregistered") << "\n";
    }

    void searchParticipant() {
        int choice;
        cout << "1. By ID\n2. By Name\nChoice: "; cin >> choice;
        if(choice == 1) {
            int id; cout << "ID: "; cin >> id;
            Participant* p = searchByIdInternal(id);
            if(p) displaySingle(p); else cout << "Not Found.\n";
        } else if(choice == 2) {
            string name; cout << "Name: "; cin.ignore(); getline(cin, name);
            bool found = false;
            for(Participant* t = head; t; t = t->next) {
                if(t->name == name) { displaySingle(t); found = true; }
            }
            if(!found) cout << "Not Found.\n";
        }
    }

    void joinWaitlist(int id) {
        WaitNode* newNode = new WaitNode(id);
        if(!rear) front = rear = newNode;
        else { rear->next = newNode; rear = newNode; }
        cout << "Added To Waitlist.\n";
    }

    void processWaitlist() {
        if(!front) { cout << "Waitlist Empty.\n"; return; }
        cout << "Processed ID: " << front->participantId << endl;
        WaitNode* t = front; front = front->next; delete t;
        if(!front) rear = NULL;
    }

    void bubbleSortDisplay() {
        if(!head) { cout << "No participants found.\n"; return; }
        vector<ParticipantView> arr;
        for(Participant* t = head; t; t = t->next) arr.push_back({t->id, t->name, t->eventName});
        
        for(size_t i = 0; i < arr.size() - 1; i++)
            for(size_t j = 0; j < arr.size() - i - 1; j++)
                if(arr[j].name > arr[j+1].name) swap(arr[j], arr[j+1]);

        cout << "\n--- Sorted By Name ---\n";
        for(const auto& p : arr) cout << p.id << " | " << p.name << " | " << p.eventName << endl;
    }

    void binarySearchParticipant() {
        if(!head) { cout << "No participants found.\n"; return; }
        vector<int> ids;
        for(Participant* t = head; t; t = t->next) ids.push_back(t->id);
        mergeSort(ids, 0, ids.size() - 1);

        int target; cout << "Enter ID to search: "; cin >> target;
        int low = 0, high = ids.size() - 1;
        while(low <= high) {
            int mid = low + (high - low) / 2;
            if(ids[mid] == target) { cout << "Participant Exists.\n"; return; }
            if(ids[mid] < target) low = mid + 1; else high = mid - 1;
        }
        cout << "Participant Not Found.\n";
    }
};

int getValidInt() {
    int input;
    while (!(cin >> input)) {
        cin.clear(); cin.ignore(10000, '\n');
        cout << "Invalid input! Enter number: ";
    }
    return input;
}

int main() {
    EventSystem sys;
    int choice;
    sys.registerParticipant(101, "Alice Smith", "AI Seminar");

    // Predefined available events list matching the provided reference
    vector<string> availableEvents = {
        "Programming Workshop",
        "AI Seminar",
        "Cybersecurity Bootcamp",
        "Data Science Workshop",
        "Final Year Project Exhibition",
        "Tech Talk Series",
        "Coding Competition",
        "Hackathon",
        "Blood Donation Drive"
    };

    do {
        cout << "\n1. Register\n2. Remove\n3. Update\n4. Search\n5. Display Sorted\n6. Join Waitlist\n7. Process Waitlist\n8. Binary Search\n0. Exit\nChoice: ";
        choice = getValidInt();
        int id; string name;

        switch(choice) {
            case 1: {
                cout << "ID: "; id = getValidInt();
                cin.ignore(); 
                cout << "Name: "; getline(cin, name);

                cout << "\n--- Available Events ---" << endl;
                for (size_t i = 0; i < availableEvents.size(); i++) {
                    cout << i + 1 << ". " << availableEvents[i] << endl;
                }
                cout << "0. Enter Custom Event Name\n";
                cout << "Select event option: ";
                
                int eventChoice = getValidInt();
                string eventName = "";

                if (eventChoice > 0 && eventChoice <= (int)availableEvents.size()) {
                    eventName = availableEvents[eventChoice - 1];
                } else {
                    cin.ignore();
                    cout << "Enter Custom Event Name: ";
                    getline(cin, eventName);
                }

                sys.registerParticipant(id, name, eventName);
                break;
            }
            case 2: cout << "ID: "; sys.removeParticipant(getValidInt()); break;
            case 3: cout << "ID: "; sys.updateParticipant(getValidInt()); break;
            case 4: sys.searchParticipant(); break;
            case 5: sys.bubbleSortDisplay(); break;
            case 6: cout << "ID: "; sys.joinWaitlist(getValidInt()); break;
            case 7: sys.processWaitlist(); break;
            case 8: sys.binarySearchParticipant(); break;
            case 0: cout << "Exiting...\n"; break;
            default: cout << "Invalid choice!\n";
        }
    } while(choice != 0);

    return 0;
}