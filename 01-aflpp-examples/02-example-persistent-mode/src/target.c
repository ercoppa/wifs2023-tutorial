#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

#define INPUTSIZE 100

int process(char *input)
{
	char *out;
	char *rest;
	int len;
	if (strncmp(input, "u ", 2) == 0)
	{ // upper case command
		char *rest;
		len = strtol(input + 2, &rest, 10); // how many characters of the string to upper-case
		rest += 1;							// skip the first char (should be a space)
		out = malloc(len + strlen(input));	// could be shorter, but play it safe
		if (len > (int)strlen(input))
		{
			printf("Specified length %d was larger than the input!\n", len);
			return 1;
		}
		else if (out == NULL)
		{
			printf("Failed to allocate memory\n");
			return 1;
		}
		for (int i = 0; i != len; i++)
		{
			char c = rest[i];
			if (c > 96 && c < 123) // ascii a-z
			{
				c -= 32;
			}
			out[i] = c;
		}
		out[len] = 0;
		strcat(out, rest + len); // append the remaining text
		printf("%s", out);
		free(out);
	}
	else if (strncmp(input, "head ", 5) == 0)
	{ // head command
		if (strlen(input) > 6)
		{
			len = strtol(input + 4, &rest, 10);
			rest += 1;		  // skip the first char (should be a space)
			rest[len] = '\0'; // truncate string at specified offset
			printf("%s\n", rest);
		}
		else
		{
			fprintf(stderr, "head input was too small\n");
		}
	}
	else if (strcmp(input, "surprise!\n") == 0)
	{
		// easter egg!
		*(char *)1 = 2;
	}
	else
	{
		return 1;
	}
	return 0;
}

__AFL_FUZZ_INIT();

int main(int argc, char *argv[])
{
#ifdef __AFL_HAVE_MANUAL_CONTROL
	__AFL_INIT();
#endif

	unsigned char *input = __AFL_FUZZ_TESTCASE_BUF; // must be after __AFL_INIT
                                                    // and before __AFL_LOOP!
	while (__AFL_LOOP(10000)) {
		int len = __AFL_FUZZ_TESTCASE_LEN;
		process(input);
	}

	return 0;
}
