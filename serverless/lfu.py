import threading,time,subprocess,shlex
import argparse
import time
import random
from readerwriterlock import rwlock
from collections import defaultdict

time_dict = []
workload = ""
capacity = 0
freq = defaultdict(int)
big_lock = threading.Lock()

def deploy(workload, id):
    return "sudo ./deploy_gpu.sh {0} {0}{1} > /dev/null;".format(workload, id)

def invoke(workload, id):
    return "cat /tmp/input.json | sudo nuctl invoke {0}{1} -c 'application/json' > /dev/null;".format(workload, id)

def delete(workload, id):
    return "sudo nuctl delete functions {0}{1} > /dev/null;".format(workload, id)

def infer(id):
    global freq, rw
    with rw[id].gen_rlock():
        if id in freq: # deployed
            freq[id] += 1
            command = invoke(workload, id)
            subprocess.run([command], shell=True)
            # print("id: {}, freq: {}".format(id, freq.keys()))
            return True
        else:
            return False

def build(id):
    global freq, rw, big_lock
    if id in freq:
        return True
    with rw[id].gen_wlock():
        if len(freq) > capacity: # memory full
            lfu_fn = min(freq, key=lambda fn: freq[fn] * nr_fn + fn)
            with rw[lfu_fn].gen_wlock(): # deadlock warning!
                if lfu_fn in freq:
                    freq.pop(lfu_fn, None)
                    command = delete(workload, lfu_fn)
                    subprocess.run([command], shell=True)
        
        if id not in freq:
            with big_lock:
                if len(freq) > capacity:
                    return False
                freq[id] += 1
            command = deploy(workload, id)
            command += "sleep 2;"
            subprocess.run([command], shell=True)
        
        return True

def time_me(id):
    global time_dict
    start_time = time.time()
    if infer(id):
        time_dict.append(time.time() - start_time)
        return
    while build(id) == False:
        pass
    assert infer(id)
    time_dict.append(time.time() - start_time)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='.')
    parser.add_argument('--workload', default="torch-vgg", type=str, help='Workload name.')
    parser.add_argument('--requests', default=20, type=int, help='Number of requests.')
    parser.add_argument('--nr_fn', default=10, type=int, help='Number of functions.')
    parser.add_argument('--capacity', default=6, type=int, help='Capacity of functions')
    args = parser.parse_args()

    # Examle run:
    # time python lfu.py --requests 20 --workload torch-vgg --nr_fn 10 > output.log

    workload = args.workload
    requests = args.requests
    nr_fn = args.nr_fn
    capacity = args.capacity
    rw = [rwlock.RWLockFairD() for _ in range(nr_fn)]

    commands = []
    threads = []

    for _ in range(requests):
        j = random.randrange(nr_fn)
        commands.append(j)
    
    # print(commands)

    start = time.time()
    for command in commands:
        t = threading.Thread(target=time_me,args=(command,))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    end = time.time()

    for value in time_dict:
        print(value)
    print('Total spent time is: ', end - start)

    command = ""
    for r in freq:
        command += delete(workload, r)
    subprocess.run([command], shell=True)

