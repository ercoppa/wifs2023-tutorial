#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

#define MAX_INPUT_SIZE 64
#define GOOD_BEHAVIOR(n) do { printf("OK %d\n", n); } while (0);
#define REACHED_BUG(n) do { fprintf(stderr, "BUG #%d\n", n); abort(); } while (0)

int main() {

    char input[MAX_INPUT_SIZE];
    int n = read(0, &input, sizeof(input));

    if (input[0] == 0) REACHED_BUG(0);
    if (input[0] == 1) REACHED_BUG(1); 

    if (input[0] == 2) { 
        if (input[1] == 3) REACHED_BUG(2); 
        else GOOD_BEHAVIOR(2); 
    } else {
        if (input[0] == 3) { 
            if(input[1] == input[0] + 1) REACHED_BUG(3); 
            else GOOD_BEHAVIOR(3); 
        } else {
            if (input[0] == 4) {
                if(input[1] == 5 && input[2] == 6) 
                    REACHED_BUG(4); 
                else GOOD_BEHAVIOR(4); 
            }
        }
    }

    return 0;
}