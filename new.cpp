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
 