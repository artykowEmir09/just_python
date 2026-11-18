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
            Participant* p = searchByIdInternal(temp->participantId);
            if(p && p->eventName == eventName) count++;
            temp = temp->next;
        }
        return count;
    }

public:
    EventSystem() : head(NULL), front(NULL), rear(NULL) {
        // Initialize default events with capacities
        events = {
            {"Programming Workshop", 5, 0},
            {"AI Seminar", 5, 1}, // Alice Smith registered by default
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
        if(searchByIdInternal(id)) { cout << "Error: ID already exists.\n"; return; }
        
        EventInfo* ev = findEvent(eventName);
        if(ev && ev->registeredCount >= ev->capacity) {
            cout << "Error: Event '" << eventName << "' is at full capacity (" << ev->capacity << "). Please join the waitlist.\n";
            return;
        }

        Participant* newNode = new Participant(id, name, eventName);
        if(!head) head = newNode;
        else {
            Participant* temp = head;
            while(temp->next) temp = temp->next;
            temp->next = newNode;
        }

        if(ev) ev->registeredCount++;
        cout << "Success: Participant Registered for '" << eventName << "'.\n";
    }

    void removeParticipant(int id) {
        if(!head) { cout << "No participants found.\n"; return; }
        
        Participant* target = searchByIdInternal(id);
        if(!target) { cout << "Error: Participant Not Found.\n"; return; }

        string eventName = target->eventName;

        if(head->id == id) {
            Participant* t = head; head = head->next; delete t;
        } else {
            Participant* temp = head;
            while(temp->next && temp->next->id != id) temp = temp->next;
            Participant* t = temp->next; temp->next = temp->next->next; delete t;
        }

        EventInfo* ev = findEvent(eventName);
        if(ev && ev->registeredCount > 0) ev->registeredCount--;

        cout << "Success: Participant Removed & Capacity Updated.\n";
    }

    void updateParticipant(int id) {
        Participant* p = searchByIdInternal(id);
        if(!p) { cout << "Error: Not Found.\n"; return; }
        
        string oldEvent = p->eventName;
        cout << "Current Name: " << p->name << " | Event: " << p->eventName << "\nEnter New Name: ";
        cin.ignore(); getline(cin, p->name);
        
        cout << "Success: Updated.\n";
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
        cout << "Capacity       : " << cap << "\n";
        cout << "Registered     : " << reg << "\n";
        cout << "Waitlist       : " << waitCount << "\n";
        cout << "----------------------------------------\n";
    }

    void searchParticipant() {
        int choice;
        cout << "1. By ID\n2. By Name\nChoice: "; cin >> choice;
        if(choice == 1) {
            int id; cout << "ID: "; cin >> id;
 