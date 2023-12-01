#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

#define MAX_INPUT_SIZE 64
#define GOOD_BEHAVIOR(n) do { printf("OK %d\n", n); } while (0);
#define REACHED_BUG(n) do { fprintf(stderr, "BUG #%d\n", n); abort(); } while (0)

#ifdef ENABLE_CMP_TRACK
#define TRACK_CMP(...) do { fprintf(stderr, __VA_ARGS__); } while (0);
#else
#define TRACK_CMP(...) ;
#endif

int main() {

    char input[MAX_INPUT_SIZE];
    int n = read(0, &input, sizeof(input));

    TRACK_CMP("input[0] == 0\n");
    if (input[0] == 0) REACHED_BUG(0);

    TRACK_CMP("input[0] == 1\n");
    if (input[0] == 1) REACHED_BUG(1); 

    TRACK_CMP("input[0] == 2\n");
    if (input[0] == 2) { 
        TRACK_CMP("input[1] == 3\n");
        if (input[1] == 3) REACHED_BUG(2); 
        else GOOD_BEHAVIOR(2); 
    } else {
        TRACK_CMP("input[0] == 3\n");
        if (input[0] == 3) { 
            TRACK_CMP("input[1] == %d\n", input[0] + 1);
            if(input[1] == input[0] + 1) REACHED_BUG(3); 
            else GOOD_BEHAVIOR(3); 
        } else {
            TRACK_CMP("input[0] == 4\n");
            if (input[0] == 4) {
                TRACK_CMP("input[1] == 5\n");
                TRACK_CMP("input[2] == 6\n");
                if(input[1] == 5 && input[2] == 6) 
                    REACHED_BUG(4); 
                else GOOD_BEHAVIOR(4); 
            }
        }
    }

    return 0;
}