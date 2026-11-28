#include <iostream>
#include <stack>
using namespace std;

int main(){
    stack<int>myStack;
    int num;

    for (int i = 1 ; i <=5; i++){
        cout << "Enter the value " <<i <<":";
        cin >> num;
        myStack.push(num);
    }
    cout<< "Total data in stack: "<< myStack.size()<< endl;

}