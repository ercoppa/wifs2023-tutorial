import os
import sys
import random
import subprocess
import time

start = time.time()
errors = set()
while True:
    # step 1: we know something about the input prefix
    prefix_choice = random.randrange(1, 4)
    if prefix_choice == 1: input = b"\x01\x02"
    elif prefix_choice == 2: input = b"\x02\x03"
    elif prefix_choice == 3: input = b"\x03\x04"
    input += os.urandom(random.randrange(1, 64 - len(input)))
    
    # step 2
    try: 
        # print("Using input: %s" % input)
        p = subprocess.run(sys.argv[1:], input=input, timeout=10, capture_output=True)
        if p.returncode < 0: # step 3a
            # print("Error with input: %s" % input)
            if p.stderr not in errors:
                print("Discovered bug (elapsed=%.1fs): %s" 
                    % (time.time() - start, p.stderr.decode("ascii").strip("\n").strip(" ")))
                errors.add(p.stderr)
    except subprocess.TimeoutExpired as t:
        print("Timeout with input: %s" % input)
    # step 3b