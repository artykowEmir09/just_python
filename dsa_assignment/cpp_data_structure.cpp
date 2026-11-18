#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <iomanip>

using namespace std;

struct EventInfo {
    string name;
    int capacity;
    int registeredCount;
};

struct Participant {
    int id;
    string name;
    string eventName;
    bool registered;
    bool waitlisted;
    Participant* next;

    Participant(int i, string n, string e, bool reg = true, bool wait = false) {
        id = i;
        name = n;
        eventName = e;
        registered = reg;
        waitlisted = wait;
        next = NULL;
    }
};

struct WaitNode {
    int participantId;
    string participantName;
    string eventName;
    WaitNode* next;

    WaitNode(int id, string name, string event) {
        participantId = id;
        participantName = name;
        eventName = event;
        next = NULL;
    }
};

struct ParticipantView {
    int id;
    string name, eventName;
    bool registered;
    bool waitlisted;
};

class EventSystem {
private:
    Participant* head;
    WaitNode *front, *rear;
    vector<EventInfo> events;

    Participant* searchByIdInternal(int id) {
        Participant* temp = head;
        while(temp) {
            if(temp->id == id) return temp;
            temp = temp->next;
        }
        return NULL;
    }

    EventInfo* findEvent(string eventName) {
        for(auto& ev : events) {
            if(ev.name == eventName) return &ev;
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

    int getWaitlistCountForEvent(string eventName) {
        int count = 0;
        WaitNode* temp = front;
        while(temp) {
            if(temp->eventName == eventName) count++;
            temp = temp->next;
        }
        return count;
    }

    void addToWaitlistQueue(int id, string name, string eventName) {
        WaitNode* newNode = new WaitNode(id, name, eventName);
        if(!rear) {
            front = rear = newNode;
        } else {
            rear->next = newNode;
            rear = newNode;
        }
    }

    void removeFromWaitlistQueue(int id) {
        if(!front) return;
        if(front->participantId == id) {
            WaitNode* t = front;
            front = front->next;
            if(!front) rear = NULL;
            delete t;
            return;
        }
        WaitNode* temp = front;
        while(temp->next && temp->next->participantId != id) {
            temp = temp->next;
        }
        if(temp->next) {
            WaitNode* t = temp->next;
            temp->next = t->next;
            if(t == rear) rear = temp;
            delete t;
        }
    }

public:
    EventSystem() : head(NULL), front(NULL), rear(NULL) {
        events = {
            {"Programming Workshop", 5, 0},
            {"AI Seminar", 5, 0},
            {"Cybersecurity Bootcamp", 5, 0},
            {"Data Science Workshop", 5, 0},
            {"Final Year Project Exhibition", 5, 0},
            {"Tech Talk Series", 5, 0},
            {"Coding Competition", 5, 0},
            {"Hackathon", 5, 0},
            {"Blood Donation Drive", 80, 0}
        };
    }

    ~EventSystem() {
        while(head) { Participant* t = head; head = head->next; delete t; }
        while(front) { WaitNode* t = front; front = front->next; delete t; }
    }

    vector<EventInfo>& getEvents() { return events; }

    void registerParticipant(int id, string name, string eventName) {
        if(searchByIdInternal(id)) { 
            cout << "Error: ID already exists in the system.\n"; 
            return; 
        }
        
        EventInfo* ev = findEvent(eventName);
        if(!ev) {
            // If custom event, add it dynamically with capacity 5
            events.push_back({eventName, 5, 0});
            ev = findEvent(eventName);
        }

        if(ev->registeredCount >= ev->capacity) {
            Participant* newNode = new Participant(id, name, eventName, false, true);
            if(!head) head = newNode;
            else {
                Participant* temp = head;
                while(temp->next) temp = temp->next;
                temp->next = newNode;
            }

            addToWaitlistQueue(id, name, eventName);

            cout << "Event '" << eventName << "' is Full.\n";
            cout << "Success: " << name << " automatically added to the waitlist.\n";
            return;
        }

        Participant* newNode = new Participant(id, name, eventName, true, false);
        if(!head) head = newNode;
        else {
            Participant* temp = head;
            while(temp->next) temp = temp->next;
            temp->next = newNode;
        }

        ev->registeredCount++;
        cout << "Success: Participant Registered for '" << eventName << "'.\n";
    }

    void removeParticipant(int id) {
        if(!head) { cout << "No participants found in the system.\n"; return; }
        
        Participant* target = searchByIdInternal(id);
        if(!target) { cout << "Error: Participant Not Found.\n"; return; }

        string eventName = target->eventName;
        bool wasRegistered = target->registered;

        // Remove from linked list
        if(head->id == id) {
            Participant* t = head; head = head->next; delete t;
        } else {
            Participant* temp = head;
            while(temp->next && temp->next->id != id) temp = temp->next;
            Participant* t = temp->next; temp->next = temp->next->next; delete t;
        }

        EventInfo* ev = findEvent(eventName);

        if(wasRegistered) {
            if(ev && ev->registeredCount > 0) ev->registeredCount--;

            // Check if there is someone waiting in the queue for this event
            WaitNode* waitTemp = front;
            WaitNode* prevWait = NULL;
            while(waitTemp) {
                if(waitTemp->eventName == eventName) {
                    // Found first person on waitlist for this event! Promote them.
                    int promotedId = waitTemp->participantId;
                    Participant* promotedParticipant = searchByIdInternal(promotedId);
                    if(promotedParticipant) {
                        promotedParticipant->registered = true;
                        promotedParticipant->waitlisted = false;
                        if(ev) ev->registeredCount++;
                        cout << "Promotion: " << promotedParticipant->name 
                             << " has been moved from the waitlist to Registered for '" << eventName << "'.\n";
                    }

                    // Remove from waitlist queue
                    if(prevWait == NULL) {
                        front = waitTemp->next;
                        if(!front) rear = NULL;
                    } else {
                        prevWait->next = waitTemp->next;
                        if(waitTemp == rear) rear = prevWait;
                    }
                    delete waitTemp;
                    break;
                }
                prevWait = waitTemp;
                waitTemp = waitTemp->next;
            }
        } else {
            // Was on waitlist only
            removeFromWaitlistQueue(id);
        }

        cout << "Success: Participant Removed & System Updated.\n";
    }

    void updateParticipant(int id) {
        Participant* p = searchByIdInternal(id);
        if(!p) { cout << "Error: Participant Not Found.\n"; return; }
        
        cout << "Current Name: " << p->name << " | Event: " << p->eventName << "\nEnter New Name: ";
        cin.ignore(); 
        getline(cin, p->name);
        
        cout << "Success: Participant Name Updated.\n";
    }

    void displaySingle(Participant* p) {
        EventInfo* ev = findEvent(p->eventName);
        int cap = ev ? ev->capacity : 0;
        int reg = ev ? ev->registeredCount : 0;
        int waitCount = getWaitlistCountForEvent(p->eventName);

        cout << "\n----------------------------------------\n";
        cout << "PARTICIPANT ID : P" << p->id << "\n";
        cout << "Name           : " << p->name << "\n";
        cout << "Event Name     : " << p->eventName << "\n";
        cout << "Status         : " << (p->registered ? "Registered" : "Waitlisted") << "\n";
        cout << "Event Capacity : " << cap << "\n";
        cout << "Registered     : " << reg << "\n";
        cout << "Waitlist Total : " << waitCount << "\n";
        cout << "----------------------------------------\n";
    }

    void searchParticipant() {
        int choice;
        cout << "1. Search by ID\n2. Search by Name\nChoice: "; 
        cin >> choice;
        if(choice == 1) {
            int id; cout << "Enter ID: "; cin >> id;
            Participant* p = searchByIdInternal(id);
            if(p) displaySingle(p); else cout << "Participant Not Found.\n";
        } else if(choice == 2) {
            string name; cout << "Enter Name: "; cin.ignore(); getline(cin, name);
            bool found = false;
            for(Participant* t = head; t; t = t->next) {
                if(t->name == name) { displaySingle(t); found = true; }
            }
            if(!found) cout << "No participants found with that name.\n";
        } else {
            cout << "Invalid choice.\n";
        }
    }

    void processWaitlist() {
        if(!front) {
            cout << "Waitlist Queue is Empty.\n";
            return;
        }

        WaitNode* temp = front;
        // Promote front waitlist member
        Participant* p = searchByIdInternal(temp->participantId);
        EventInfo* ev = findEvent(temp->eventName);

        if(p && ev && ev->registeredCount < ev->capacity) {
            p->registered = true;
            p->waitlisted = false;
            ev->registeredCount++;

            cout << "\n=============================================================\n";
            cout << "               PROCESSED & REGISTERED FROM WAITLIST\n";
            cout << "=============================================================\n";
            cout << left << setw(15) << "ID: P" + to_string(temp->participantId)
                 << setw(25) << "NAME: " + temp->participantName
                 << setw(30) << "EVENT: " + temp->eventName << endl;
            cout << "=============================================================\n";

            front = front->next;
            if(!front) rear = NULL;
            delete temp;
        } else {
            cout << "Cannot process waitlist: Event '" << temp->eventName << "' is still at full capacity.\n";
        }
    }

    void displayWaitlist() {
        if(front == NULL) {
            cout << "\nWaitlist Queue is Empty.\n";
            return;
        }

        cout << "\n";
        cout << "========================================================================\n";
        cout << "                            WAITLIST QUEUE\n";
        cout << "========================================================================\n";

        cout << left
             << setw(10) << "POS"
             << setw(10) << "ID"
             << setw(25) << "NAME"
             << setw(25) << "EVENT"
             << endl;

        cout << "------------------------------------------------------------------------\n";

        WaitNode* temp = front;
        int position = 1;

        while(temp != NULL) {
            cout << left
                 << setw(10) << position
                 << setw(10) << ("P" + to_string(temp->participantId))
                 << setw(25) << temp->participantName
                 << setw(25) << temp->eventName
                 << endl;

            temp = temp->next;
            position++;
        }

        cout << "========================================================================\n";
    }

    void bubbleSortDisplay() {
        if(!head) { cout << "No participants found in the system.\n"; return; }
        vector<ParticipantView> arr;
        for(Participant* t = head; t; t = t->next) {
            arr.push_back({t->id, t->name, t->eventName, t->registered, t->waitlisted});
        }
        
        for(size_t i = 0; i < arr.size() - 1; i++)
            for(size_t j = 0; j < arr.size() - i - 1; j++)
                if(arr[j].name > arr[j+1].name) swap(arr[j], arr[j+1]);

        cout << "\n--- Participants Sorted By Name ---\n";
        cout << left << setw(10) << "ID" << setw(25) << "Name" << setw(28) << "Event" << setw(15) << "Status" << endl;
        cout << "---------------------------------------------------------------------------------\n";
        for(const auto& p : arr) {
            cout << left << setw(10) << ("P" + to_string(p.id)) 
                 << setw(25) << p.name 
                 << setw(28) << p.eventName 
                 << setw(15) << (p.registered ? "Registered" : "Waitlisted") << endl;
        }
    }

    void binarySearchParticipant() {
        if(!head) { cout << "No participants found in the system.\n"; return; }
        vector<int> ids;
        for(Participant* t = head; t; t = t->next) ids.push_back(t->id);
        mergeSort(ids, 0, ids.size() - 1);

        int target; cout << "Enter ID to search: "; cin >> target;
        int low = 0, high = ids.size() - 1;
        while(low <= high) {
            int mid = low + (high - low) / 2;
            if(ids[mid] == target) { 
                cout << "Result: Participant ID P" << target << " exists in the system.\n"; 
                return; 
            }
            if(ids[mid] < target) low = mid + 1; else high = mid - 1;
        }
        cout << "Result: Participant ID P" << target << " Not Found.\n";
    }
};

int getValidInt() {
    int input;
    while (!(cin >> input)) {
        cin.clear(); 
        cin.ignore(10000, '\n');
        cout << "Invalid input! Enter a valid number: ";
    }
    return input;
}

int main() {
    EventSystem sys;
    int choice;

    // Register initial default participant safely
    sys.registerParticipant(101, "Alice Smith", "AI Seminar");

    do {
        cout << "\n";
        cout << "=====================================================\n";
        cout << "        CAMPUS EVENT REGISTRATION SYSTEM\n";
        cout << "=====================================================\n";
        cout << "1. Register Participant\n";
        cout << "2. Remove Participant\n";
        cout << "3. Update Participant Name\n";
        cout << "4. Search Participant\n";
        cout << "5. Display All Participants (Sorted by Name)\n";
        cout << "6. Manually Process Waitlist Queue\n";
        cout << "7. Display Waitlist Queue\n";
        cout << "8. Binary Search Participant by ID\n";
        cout << "0. Exit\n";
        cout << "=====================================================\n";
        cout << "Choice: ";
        
        choice = getValidInt();

        switch(choice) {
            case 1: {
                int id;
                string name;
                cout << "Enter Participant ID (numeric): "; 
                id = getValidInt();
                cin.ignore(); 
                cout << "Enter Full Name: "; 
                getline(cin, name);

                cout << "\n--- Available Events & Capacity ---" << endl;
                vector<EventInfo>& events = sys.getEvents();
                for (size_t i = 0; i < events.size(); i++) {
                    int available = events[i].capacity - events[i].registeredCount;
                    cout << i + 1 << ". " << events[i].name 
                         << " [Capacity: " << events[i].capacity 
                         << ", Registered: " << events[i].registeredCount 
                         << ", Available Spots: " << (available > 0 ? available : 0) << "]\n";
                }
                cout << "0. Enter Custom Event Name\n";
                cout << "Select event option: ";
                
                int eventChoice = getValidInt();
                string eventName = "";

                if (eventChoice > 0 && eventChoice <= (int)events.size()) {
                    eventName = events[eventChoice - 1].name;
                } else {
                    cin.ignore();
                    cout << "Enter Custom Event Name: ";
                    getline(cin, eventName);
                }

                sys.registerParticipant(id, name, eventName);
                break;
            }
            case 2: {
                cout << "Enter Participant ID to remove: "; 
                sys.removeParticipant(getValidInt()); 
                break;
            }
            case 3: {
                cout << "Enter Participant ID to update: "; 
                sys.updateParticipant(getValidInt()); 
                break;
            }
            case 4: 
                sys.searchParticipant(); 
                break;
            case 5: 
                sys.bubbleSortDisplay(); 
                break;
            case 6: 
                sys.processWaitlist(); 
                break;
            case 7:
                sys.displayWaitlist();
                break;
            case 8: 
                sys.binarySearchParticipant(); 
                break;
            case 0: 
                cout << "Exiting program. Thank you!\n"; 
                break;
            default: 
                cout << "Invalid choice! Please choose between 0 and 8.\n";
        }
    } while(choice != 0);

    return 0;
}