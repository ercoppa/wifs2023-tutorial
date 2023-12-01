import os
import sys
import random
import subprocess
import glob
import re
import time
import json

import tempfile

os.system("cp -a ../seeds ../queue")

# warmup
errors = set()
behaviors = set()
for input in glob.glob("../queue/*"):
    p = subprocess.run(sys.argv[1:], input=open(input, 'rb').read(), timeout=10, capture_output=True)
    behaviors.add(p.stdout)

cmp_dir_obj = tempfile.TemporaryDirectory()
cmp_dir = cmp_dir_obj.name
start = time.time()
errors = set()
while True:
    # step 1: pick an input
    queue = glob.glob("../queue/*")
    input_name = queue[random.randrange(0, len(queue))]
    input = bytearray(open(input_name, "rb").read())
    cmp_log = json.loads(open(cmp_dir + "/" + os.path.basename(input_name), 'r').read()) if os.path.exists(cmp_dir + "/" + os.path.basename(input_name)) else None
    # print(cmp_log)

    # step 2: apply a random mutation
    offset = random.randrange(0, len(input))
    mutation = random.randrange(0, 3 + (5 if cmp_log else 0))
    if mutation == 0: input[offset] = os.urandom(1)[0]
    elif mutation == 1: input[offset] = (input[offset] + 1) % 256
    elif mutation == 2: input = input[:offset] + os.urandom(random.randrange(1, 64))
    elif mutation == 3: 
        for p in list(dict(cmp_log).items()): input[int(p[0])] = int(p[1])
    elif mutation >= 4:
        p = cmp_log[random.randrange(0, len(cmp_log))]
        # print(p)
        input[int(p[0])] = int(p[1])

    # step 3
    try: 
        # print("Using input: %s" % input)
        p = subprocess.run(sys.argv[1:], input=input, timeout=10, capture_output=True)

        if p.returncode < 0: # step 4a
            bug_id = p.stderr.decode("ascii").strip().split("\n")[-1].strip(" ")
            if bug_id not in errors:
                print("Discovered bug (elapsed=%.1fs): %s" % (time.time() - start, bug_id))
                errors.add(bug_id)
    
        else: 
            # step 4b
            if p.stdout not in behaviors:
                # print("Adding input with stdout: %s" % p.stdout)
                behaviors.add(p.stdout)
                open("../queue/%05d" % len(queue), 'wb').write(input)
    

            # step 5
            if not os.path.exists(cmp_dir + "/" + os.path.basename(input_name)):
                cmp = re.findall("input\[(\d+)\] == (\d+)\n", p.stderr.decode("ascii"))
                # print(cmp)
                open("%s/%s" % (cmp_dir, os.path.basename(input_name),), 'w').write(json.dumps(cmp)) #list(dict(cmp).items())


    except subprocess.TimeoutExpired as t:
        print("Timeout with input: %s" % input)
    # step 6