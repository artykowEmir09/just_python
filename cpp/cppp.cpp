#include <iostream>
#include <vector>
#include <string>

int main() {
    std::vector<std::string> vec = {"apple", "banana"};

    // emplace_back() appends directly to the end
    vec.emplace_back("cherry"); 
    // Container: ["apple", "banana", "cherry"]

    // emplace() inserts at a specified iterator position
    vec.emplace(vec.begin() + 1, "mango"); 
    // Container: ["apple", "mango", "banana", "cherry"]

    return 0;
}