#include <iostream>
#include <vector>
using namespace std;

int main() {

    vector<int> numbers = {10, 20, 30};

    // 1. size()
    cout << "Size: " << numbers.size() << endl;

    // 2. max_size()
    cout << "Max size: " << numbers.max_size() << endl;

    // 3. capacity()
    cout << "Capacity: " << numbers.capacity() << endl;

    // 4. resize()
    numbers.resize(5);

    cout << "After resize: ";
    for (int x : numbers) {
        cout << x << " ";
    }
    cout << endl;

    // 5. empty()
    cout << "Is empty? " << numbers.empty() << endl;

    // 6. reserve()
    numbers.reserve(10);

    cout << "Capacity after reserve(10): "
         << numbers.capacity() << endl;

    // 7. shrink_to_fit()
    numbers.shrink_to_fit();

    cout << "Capacity after shrink_to_fit(): "
         << numbers.capacity() << endl;

    return 0;
}