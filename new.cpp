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

 