#include <iostream>
#include <vector>
using namespace std;

int main() {

    int arr[] = {10, 20, 30, 40, 50};

    vector<int> numbers;

    numbers.assign(arr, arr + 3);

    for (int x : numbers) {
        cout << x << " ";
    }

    return 0;
}