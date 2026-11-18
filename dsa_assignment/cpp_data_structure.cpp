#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <iomanip>

using namespace std;

// --- ANSI Color Codes ---
const string RESET   = "\033[0m";
const string BOLD    = "\033[1m";
const string RED     = "\033[31m";
const string GREEN   = "\033[32m";
const string YELLOW  = "\033[33m";
const string BLUE    = "\033[34m";
const string MAGENTA = "\033[35m";
const string CYAN    = "\033[36m";
const string WHITE   = "\033[37m";

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

    // Helper to promote waitlisted user for a specific event when a slot frees up
    void checkAndPromoteWaitlist(string eventName) {
        EventInfo* ev = findEvent(eventName);
        if (!ev || ev->registeredCount >= ev->capacity) return;

        WaitNode* waitTemp = front;
        WaitNode* prevWait = NULL;
        while(waitTemp) {
            if(waitTemp->eventName == eventName) {
                int promotedId = waitTemp->participantId;
                Participant* promotedParticipant = searchByIdInternal(promotedId);
                if(promotedParticipant) {
                    promotedParticipant->registered = true;
                    promotedParticipant->waitlisted = false;
                    ev->registeredCount++;
                    cout << CYAN << "\n┌────────────────────────────────────────────────────────┐\n";
                    cout << "│ [⚡] AUTO-PROMOTION FROM WAITLIST                      │\n";
                    cout << "│ " << left << setw(53) << (promotedParticipant->name + " promoted to Registered for '" + eventName + "'") << " │\n";
                    cout << "└────────────────────────────────────────────────────────┘" << RESET << "\n";
                }

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
            cout << RED << "\n[✖] Error: Participant ID [P" << id << "] already exists in the system." << RESET << "\n"; 
            return; 
        }
        
        EventInfo* ev = findEvent(eventName);
        if(!ev) {
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

            cout << YELLOW << "\n┌────────────────────────────────────────────────────────┐\n";
            cout << "│ [!] NOTICE: Event '" << eventName << "' is at Full Capacity!      │\n";
            cout << "│ [✔] " << left << setw(50) << (name + " added to waitlist queue.") << " │\n";
            cout << "└────────────────────────────────────────────────────────┘" << RESET << "\n";
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
        cout << GREEN << "\n[✔] Success: [" << name << "] successfully registered for '" << eventName << "'." << RESET << "\n";
    }

    void removeParticipant(int id) {
        if(!head) { cout << YELLOW << "\n[ℹ] System Notice: No participants registered currently." << RESET << "\n"; return; }
        
        Participant* target = searchByIdInternal(id);
        if(!target) { cout << RED << "\n[✖] Error: Participant ID [P" << id << "] Not Found." << RESET << "\n"; return; }

        string eventName = target->eventName;
        bool wasRegistered = target->registered;

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
            checkAndPromoteWaitlist(eventName);
        } else {
            removeFromWaitlistQueue(id);
        }

        cout << GREEN << "[✔] Success: Participant P" << id << " removed and capacity updated." << RESET << "\n";
    }

    void updateParticipant(int id, string newName, string newEventName) {
        Participant* p = searchByIdInternal(id);
        if(!p) { 
            cout << RED << "\n[✖] Error: Participant P" << id << " Not Found." << RESET << "\n"; 
            return; 
        }
        
        string oldEventName = p->eventName;
        bool wasRegistered = p->registered;

        // Update Name
        p->name = newName;

        // If event is changing, adjust counts and statuses
        if (oldEventName != newEventName) {
            // 1. Handle old event adjustment
            if (wasRegistered) {
                EventInfo* oldEv = findEvent(oldEventName);
                if (oldEv && oldEv->registeredCount > 0) oldEv->registeredCount--;
                checkAndPromoteWaitlist(oldEventName);
            } else {
                removeFromWaitlistQueue(id);
            }

            // 2. Handle new event placement
            EventInfo* newEv = findEvent(newEventName);
            if (!newEv) {
                events.push_back({newEventName, 5, 0});
                newEv = findEvent(newEventName);
            }

            p->eventName = newEventName;

            if (newEv->registeredCount >= newEv->capacity) {
                p->registered = false;
                p->waitlisted = true;
                addToWaitlistQueue(id, newName, newEventName);
                cout << YELLOW << "\n[!] Notice: New event '" << newEventName << "' is full. Participant moved to waitlist." << RESET << "\n";
            } else {
                p->registered = true;
                p->waitlisted = false;
                newEv->registeredCount++;
                cout << GREEN << "[✔] Success: Participant successfully transferred and registered for '" << newEventName << "'." << RESET << "\n";
            }
        } else {
            cout << GREEN << "[✔] Success: Participant name updated successfully." << RESET << "\n";
        }
    }

    void displaySingle(Participant* p) {
        EventInfo* ev = findEvent(p->eventName);
        int cap = ev ? ev->capacity : 0;
        int reg = ev ? ev->registeredCount : 0;
        int waitCount = getWaitlistCountForEvent(p->eventName);

        cout << CYAN << "\n╔════════════════════════════════════════╗\n";
        cout << "║          PARTICIPANT PROFILE           ║\n";
        cout << "╠════════════════════════════════════════╣\n";
        cout << "║ ID           : P" << left << setw(22) << p->id << " ║\n";
        cout << "║ Name         : " << left << setw(23) << p->name << " ║\n";
        cout << "║ Event        : " << left << setw(23) << p->eventName << " ║\n";
        cout << "║ Status       : " << left << setw(23) << (p->registered ? "Registered [✔]" : "Waitlisted [⏳]") << " ║\n";
        cout << "║ Slot Usage   : " << reg << " / " << left << setw(19) << cap << " ║\n";
        cout << "║ Event Waitlist: " << left << setw(22) << waitCount << " ║\n";
        cout << "╚════════════════════════════════════════╝" << RESET << "\n";
    }

    void searchParticipant() {
        int choice;
        cout << CYAN << "\n--- Search Menu ---\n" << RESET;
        cout << "1. Search by ID\n2. Search by Name\nChoice: "; 
        cin >> choice;
        if(choice == 1) {
            int id; cout << "Enter ID: "; cin >> id;
            Participant* p = searchByIdInternal(id);
            if(p) displaySingle(p); else cout << RED << "\n[✖] Participant ID P" << id << " Not Found." << RESET << "\n";
        } else if(choice == 2) {
            string name; cout << "Enter Name: "; cin.ignore(); getline(cin, name);
            bool found = false;
            for(Participant* t = head; t; t = t->next) {
                if(t->name == name) { displaySingle(t); found = true; }
            }
            if(!found) cout << RED << "\n[✖] No participants found matching '" << name << "'." << RESET << "\n";
        } else {
            cout << RED << "[✖] Invalid choice." << RESET << "\n";
        }
    }

    void processWaitlist() {
        if(!front) {
            cout << YELLOW << "\n[ℹ] Waitlist Queue is currently empty." << RESET << "\n";
            return;
        }

        WaitNode* temp = front;
        Participant* p = searchByIdInternal(temp->participantId);
        EventInfo* ev = findEvent(temp->eventName);

        if(p && ev && ev->registeredCount < ev->capacity) {
            p->registered = true;
            p->waitlisted = false;
            ev->registeredCount++;

            cout << GREEN << "\n╔═══════════════════════════════════════════════════════════╗\n";
            cout << "║          MANUALLY PROCESSED FROM WAITLIST QUEUE           ║\n";
            cout << "╠═══════════════════════════════════════════════════════════╣\n";
            cout << "║ ID    : P" << left << setw(48) << temp->participantId << "║\n";
            cout << "║ Name  : " << left << setw(49) << temp->participantName << "║\n";
            cout << "║ Event : " << left << setw(49) << temp->eventName << "║\n";
            cout << "╚═══════════════════════════════════════════════════════════╝" << RESET << "\n";

            front = front->next;
            if(!front) rear = NULL;
            delete temp;
        } else {
            cout << YELLOW << "\n[!] Notice: Event '" << temp->eventName << "' is still at full capacity. Promotion deferred." << RESET << "\n";
        }
    }

    void displayWaitlist() {
        if(front == NULL) {
            cout << YELLOW << "\n┌────────────────────────────────────────┐\n";
            cout << "│          WAITLIST QUEUE IS EMPTY       │\n";
            cout << "└────────────────────────────────────────┘" << RESET << "\n";
            return;
        }

        cout << CYAN << "\n";
        cout << "┌──────┬──────┬──────────────────────────┬──────────────────────────┐\n";
        cout << "│ POS  │ ID   │ NAME                     │ EVENT                    │\n";
        cout << "├──────┼──────┼──────────────────────────┼──────────────────────────┤\n";

        WaitNode* temp = front;
        int position = 1;

        while(temp != NULL) {
            cout << "│ " << left << setw(4) << position 
                 << " │ P" << left << setw(4) << temp->participantId 
                 << " │ " << left << setw(24) << temp->participantName 
                 << " │ " << left << setw(24) << temp->eventName << " │\n";
            temp = temp->next;
            position++;
        }

        cout << "└──────┴──────┴──────────────────────────┴──────────────────────────┘" << RESET << "\n";
    }

    void bubbleSortDisplay() {
        if(!head) { 
            cout << YELLOW << "\n┌────────────────────────────────────────┐\n";
            cout << "│      NO PARTICIPANTS FOUND IN SYSTEM   │\n";
            cout << "└────────────────────────────────────────┘" << RESET << "\n"; 
            return; 
        }

        vector<ParticipantView> arr;
        for(Participant* t = head; t; t = t->next) {
            arr.push_back({t->id, t->name, t->eventName, t->registered, t->waitlisted});
        }
        
        for(size_t i = 0; i < arr.size() - 1; i++)
            for(size_t j = 0; j < arr.size() - i - 1; j++)
                if(arr[j].name > arr[j+1].name) swap(arr[j], arr[j+1]);

        cout << CYAN << "\n";
        cout << "=================================================================================\n";
        cout << "                         ALL REGISTERED PARTICIPANTS                             \n";
        cout << "=================================================================================\n" << RESET;
        cout << left << setw(10) << "ID" << setw(26) << "Name" << setw(28) << "Event" << setw(18) << "Status" << endl;
        cout << "---------------------------------------------------------------------------------\n";
        for(const auto& p : arr) {
            string status = p.registered ? (GREEN + "Registered [✔]" + RESET) : (YELLOW + "Waitlisted [⏳]" + RESET);
            cout << left << setw(10) << ("P" + to_string(p.id)) 
                 << setw(26) << p.name 
                 << setw(28) << p.eventName 
                 << setw(28) << status << endl;
        }
        cout << CYAN << "=================================================================================\n" << RESET;
    }

    void binarySearchParticipant() {
        if(!head) { cout << YELLOW << "\n[ℹ] No participants found in system." << RESET << "\n"; return; }
        vector<int> ids;
        for(Participant* t = head; t; t = t->next) ids.push_back(t->id);
        mergeSort(ids, 0, ids.size() - 1);

        int target; 
        cout << "\n[Binary Search] Enter Participant ID to check: P"; 
        cin >> target;
        
        int low = 0, high = ids.size() - 1;
        while(low <= high) {
            int mid = low + (high - low) / 2;
            if(ids[mid] == target) { 
                cout << GREEN << "[✔] Result: Participant [P" << target << "] exists in the system registry." << RESET << "\n"; 
                return; 
            }
            if(ids[mid] < target) low = mid + 1; else high = mid - 1;
        }
        cout << RED << "[✖] Result: Participant [P" << target << "] Not Found." << RESET << "\n";
    }
};

int getValidInt() {
    int input;
    while (!(cin >> input)) {
        cin.clear(); 
        cin.ignore(10000, '\n');
        cout << RED << "[✖] Invalid input! Please enter a valid number: " << RESET;
    }
    return input;
}

int main() {
    EventSystem sys;
    int choice;

    // Default entry
    sys.registerParticipant(101, "Alice Smith", "AI Seminar");

    do {
        cout << "\n";
        cout << CYAN << BOLD << "╔═══════════════════════════════════════════════════╗\n";
        cout << "║         CAMPUS EVENT REGISTRATION SYSTEM          ║\n";
        cout << "╠═══════════════════════════════════════════════════╣\n";
        cout << "║ 1. Register Participant                           ║\n";
        cout << "║ 2. Remove Participant & Update Capacity           ║\n";
        cout << "║ 3. Update Participant Name & Event                ║\n";
        cout << "║ 4. Search Participant (ID or Name)                ║\n";
        cout << "║ 5. Display All Participants (Sorted Table)        ║\n";
        cout << "║ 6. Manually Process Waitlist Queue                ║\n";
        cout << "║ 7. Display Waitlist Queue                         ║\n";
        cout << "║ 8. Binary Search Participant by ID                ║\n";
        cout << "║ 0. Exit System                                    ║\n";
        cout << "╚═══════════════════════════════════════════════════╝\n" << RESET;
        cout << YELLOW << " Select Option ➔ " << RESET;
        
        choice = getValidInt();

        switch(choice) {
            case 1: {
                int id;
                string name;
                cout << CYAN << "\n--- New Registration --- \n" << RESET;
                cout << "Enter Participant ID (numeric): P"; 
                id = getValidInt();
                cin.ignore(); 
                cout << "Enter Full Name: "; 
                getline(cin, name);

                cout << CYAN << "\n┌────────────────────────────────────────┐\n";
                cout << "│        AVAILABLE CAMPUS EVENTS         │\n";
                cout << "└────────────────────────────────────────┘\n" << RESET;
                vector<EventInfo>& events = sys.getEvents();
                for (size_t i = 0; i < events.size(); i++) {
                    int available = events[i].capacity - events[i].registeredCount;
                    cout << " " << i + 1 << ". " << events[i].name 
                         << " \n    [Capacity: " << events[i].capacity 
                         << " | Registered: " << events[i].registeredCount 
                         << " | Available: " << (available > 0 ? available : 0) << "]\n";
                }
                cout << " 0. Enter Custom Event Name\n";
                cout << YELLOW << " Select option ➔ " << RESET;
                
                int eventChoice = getValidInt();
                string eventName = "";

                if (eventChoice > 0 && eventChoice <= (int)events.size()) {
                    eventName = events[eventChoice - 1].name;
                } else {
                    cin.ignore();
                    cout << " Enter Custom Event Name: ";
                    getline(cin, eventName);
                }

                sys.registerParticipant(id, name, eventName);
                break;
            }
            case 2: {
                cout << "\n[Removal Tool] Enter Participant ID to remove: P"; 
                sys.removeParticipant(getValidInt()); 
                break;
            }
            case 3: {
                int id;
                cout << "\n[Update Tool] Enter Participant ID to update: P"; 
                id = getValidInt();
                cin.ignore();

                string newName;
                cout << "Enter New Name: ";
                getline(cin, newName);

                cout << CYAN << "\n┌────────────────────────────────────────┐\n";
                cout << "│        SELECT NEW EVENT TARGET         │\n";
                cout << "└────────────────────────────────────────┘\n" << RESET;
                vector<EventInfo>& events = sys.getEvents();
                for (size_t i = 0; i < events.size(); i++) {
                    int available = events[i].capacity - events[i].registeredCount;
                    cout << " " << i + 1 << ". " << events[i].name 
                         << " \n    [Capacity: " << events[i].capacity 
                         << " | Registered: " << events[i].registeredCount 
                         << " | Available: " << (available > 0 ? available : 0) << "]\n";
                }
                cout << " 0. Enter Custom Event Name\n";
                cout << YELLOW << " Select option ➔ " << RESET;

                int eventChoice = getValidInt();
                string newEventName = "";

                if (eventChoice > 0 && eventChoice <= (int)events.size()) {
                    newEventName = events[eventChoice - 1].name;
                } else {
                    cin.ignore();
                    cout << " Enter Custom Event Name: ";
                    getline(cin, newEventName);
                }

                sys.updateParticipant(id, newName, newEventName);
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
                cout << GREEN << "\n[ℹ] Exiting program. Have a great day!\n\n" << RESET; 
                break;
            default: 
                cout << RED << "\n[✖] Invalid choice! Please select an option between 0 and 8." << RESET << "\n";
        }
    } while(choice != 0);

    return 0;
}