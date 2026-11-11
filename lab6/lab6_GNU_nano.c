#include <stdio.h>
#include <string.h>

int main() {
    char buffer[8];
    printf("Enter something: ");
    gets(buffer);
    printf("You entered: %s\n", buffer);
    return 0;
}     