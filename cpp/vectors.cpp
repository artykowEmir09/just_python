#include <vector>
#include <iostream>

int main()
{
    std::vector<int> numbers = {10, 20, 30};

    for(auto it = numbers.begin(); it != numbers.end(); ++it)
    {
        std::cout << *it << std::endl;
    }

    return 0;
}