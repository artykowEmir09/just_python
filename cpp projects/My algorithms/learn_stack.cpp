#include <stack>
#include <iostream>
using namespace std ;
int main(){
stack<char> mystack;
mystack.push('C');      // [C]
mystack.push('A');      // [C, A]   top is A
mystack.top();          // returns A
mystack.empty();        // returns false
mystack.pop();          // removes A → [C]
mystack.emplace('D');   // [C, D]  
}
