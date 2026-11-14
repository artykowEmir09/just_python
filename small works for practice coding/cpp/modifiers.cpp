#include <iostream>
#include <vector>
using namespace std;

int main() {

    vector<int> numbers = {10, 20, 30};

    // assign()
    numbers.assign({1, 2, 3});
    // {1, 2, 3}


    // push_back()
    numbers.push_back(4);
    // {1, 2, 3, 4}


    // pop_back()
    numbers.pop_back();
    // {1, 2, 3}


    // insert()
    numbers.insert(numbers.begin() + 1, 99);
    // {1, 99, 2, 3}


    // erase()
    numbers.erase(numbers.begin() + 1);
    // {1, 2, 3}


    // swap()
    vector<int> other = {100, 200};

    numbers.swap(other);

    // numbers = {100, 200}
    // other = {1, 2, 3}


    // clear()
    numbers.clear();
    // numbers = {}


    // emplace()
    numbers.emplace(numbers.begin(), 50);
    // {50}


    // emplace_back()
    numbers.emplace_back(60);
    // {50, 60}


    for (int x : numbers) {
        cout << x << " ";
    }

    return 0;
}