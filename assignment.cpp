#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <iomanip>
#include <windows.h>
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

    // Helper to update name in the waitlist queue if they are waitlisted
    void updateWaitlistNodeName(int id, string newName) {
        WaitNode* temp = front;
        while(temp) {
            if(temp->participantId == id) {
                temp->participantName = newName;
            }
            temp = temp->next;
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
                    cout << "\n┌────────────────────────────────────────────────────────┐\n";
                    cout << "│ [⚡] AUTO-PROMOTION FROM WAITLIST                      │\n";
                    cout << "│ " << left << setw(53) << (promotedParticipant->name + " promoted to Registered for '" + eventName + "'") << " │\n";
                    cout << "└────────────────────────────────────────────────────────┘\n";
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
            cout << "\n[✖] Error: Participant ID [P" << id << "] already exists in the system.\n"; 
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

            cout << "\n┌────────────────────────────────────────────────────────┐\n";
            cout << "│ [!] NOTICE: Event '" << eventName << "' is at Full Capacity!      │\n";
            cout << "│ [✔] " << left << setw(50) << (name + " added to waitlist queue.") << " │\n";
            cout << "└────────────────────────────────────────────────────────┘\n";
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
        cout << "\n[✔] Success: [" << name << "] successfully registered for '" << eventName << "'.\n";
    }

    void removeParticipant(int id) {
        if(!head) { cout << "\n[ℹ] System Notice: No participants registered currently.\n"; return; }
        
        Participant* target = searchByIdInternal(id);
        if(!target) { cout << "\n[✖] Error: Participant ID [P" << id << "] Not Found.\n"; return; }

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

        cout << "[✔] Success: Participant P" << id << " removed and capacity updated.\n";
    }

    void updateParticipant(int id, string newName, string newEventName) {
        Participant* p = searchByIdInternal(id);
        if(!p) { 
            cout << "\n[✖] Error: Participant P" << id << " Not Found.\n"; 
            return; 
        }
        
        string oldEventName = p->eventName;
        bool wasRegistered = p->registered;

        // Update Name in main record and in waitlist queue if they are waitlisted
        p->name = newName;
        updateWaitlistNodeName(id, newName);

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
                cout << "\n[!] Notice: New event '" << newEventName << "' is full. Participant moved to waitlist.\n";
            } else {
                p->registered = true;
                p->waitlisted = false;
                newEv->registeredCount++;
                cout << "\n[✔] Success: Participant successfully transferred and registered for '" << newEventName << "'.\n";
            }
        } else {
            cout << "\n[✔] Success: Participant details updated successfully.\n";
        }
    }

 