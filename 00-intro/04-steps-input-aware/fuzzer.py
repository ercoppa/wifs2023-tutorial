import os
import sys
import random
import subprocess
import glob
import time

start = time.time()
errors = set()
while True:
    # step 1: pick an input
    seeds = glob.glob("../seeds/*")
    input = bytearray(open(seeds[random.randrange(0, len(seeds))], "rb").read())

    # step 2: randomly mutate the current input exploiting its known structure
    change_prefix = random.randrange(0, 1)
    if change_prefix: 
        input[0] = random.randrange(0, 5)
        if input[0] == 2 or input[1] == 3: input[1] = input[0] + 1
        else: input[1] = os.urandom(1)[0]
    change_payload = random.randrange(0, 1)
    if change_payload: 
        offset = random.randrange(2, len(input))
        input = input[:offset] + os.urandom(random.randrange(1, 62))

    # step 3
    try: 
        # print("Using input: %s" % input)
        p = subprocess.run(sys.argv[1:], input=input, timeout=10, capture_output=True)
        if p.returncode < 0: # step 4a
            # print("Error with input: %s" % input)
            if p.stderr not in errors:
                print("Discovered bug (elapsed=%.1fs): %s" 
                    % (time.time() - start, p.stderr.decode("ascii").strip("\n").strip(" ")))
                errors.add(p.stderr)
    except subprocess.TimeoutExpired as t:
        print("Timeout with input: %s" % input)
    # step 4b