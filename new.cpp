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
 