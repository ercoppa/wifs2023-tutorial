import os
import sys
import random
import subprocess
import glob
import time

os.system("cp -a ../seeds ../queue")

# warmup
errors = set()
behaviors = set()
for input in glob.glob("../queue/*"):
    p = subprocess.run(sys.argv[1:], input=open(input, 'rb').read(), timeout=10, capture_output=True)
    behaviors.add(p.stdout)

start = time.time()
errors = set()
while True:
    # step 1: pick an input
    queue = glob.glob("../queue/*")
    input = bytearray(open(queue[random.randrange(0, len(queue))], "rb").read())

    # step 2: apply a random mutation
    offset = random.randrange(0, len(input))
    mutation = random.randrange(0, 3)
    if mutation == 0: input[offset] = os.urandom(1)[0]
    elif mutation == 1: input[offset] += 1
    elif mutation == 2: input = input[:offset] + os.urandom(random.randrange(1, 64))

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
    
        else: # step 4b
            if p.stdout not in behaviors:
                # print("Adding input with stdout: %s" % p.stdout)
                behaviors.add(p.stdout)
                open("../queue/%05d" % len(queue), 'wb').write(input)
    except subprocess.TimeoutExpired as t:
        print("Timeout with input: %s" % input)
    # step 5