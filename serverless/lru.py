import threading,time,subprocess,shlex
import argparse
import time
import random
from readerwriterlock import rwlock

time_dict = []
workload = ""
capacity = 0
ts = {}
big_lock = threading.Lock()

def deploy(workload, id):
    return "sudo ./deploy_gpu.sh {0} {0}{1} > /dev/null;".format(workload, id)

def invoke(workload, id):
    return "cat /tmp/input.json | sudo nuctl invoke {0}{1} -c 'application/json' > /dev/null;".format(workload, id)

def delete(workload, id):
    return "sudo nuctl delete functions {0}{1} > /dev/null;".format(workload, id)

def infer(id):
    global ts, rw
    with rw[id].gen_rlock():
        print('infer {}; ts: {}'.format(id, ts.keys()))
        if id in ts: # deployed
            ts[id] = time.time()
            command = invoke(workload, id)
            print('infer {}'.format(id))
            subprocess.run([command], shell=True)
            print('infer {} success'.format(id))
            ts[id] = time.time()
            return True
        else:
            print('infer {} failed'.format(id))
            return False

def build(id):
    global ts, rw, big_lock
    with rw[id].gen_wlock():
        print('build {}'.format(id))
        if len(ts) >= capacity: # memory full
            to_replace = min(ts, key=lambda fn: ts[fn])
            with rw[to_replace].gen_wlock(): # deadlock warning!
                if to_replace in ts:
                    ts.pop(to_replace, None)
                    command = delete(workload, to_replace)
                    print('delete {}'.format(to_replace))
                    subprocess.run([command], shell=True)
                    print('delete {} success'.format(to_replace))
                    print('ts: {}'.format(ts.keys()))
        
        if id not in ts:
            with big_lock:
                if len(ts) > capacity:
                    print('ejected but full ({})'.format(id))
                    return False
                ts[id] = time.time()
            command = deploy(workload, id)
            command += "sleep 2;"
            print('deploy {}'.format(id))
            subprocess.run([command], shell=True)
            print('deploy {} success'.format(id))
            ts[id] = time.time()
            print('ts: {}'.format(ts.keys()))
        
        return True

def time_me(id):
    global time_dict
    start_time = time.time()
    if infer(id):
        time_dict.append(time.time() - start_time)
        return
    while build(id) == False:
        pass
    if infer(id) == False:
        print('=== second infer {} failed'.format(id))
    time_dict.append(time.time() - start_time)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='.')
    parser.add_argument('--workload', default="torch-vgg", type=str, help='Workload name.')
    parser.add_argument('--requests', default=20, type=int, help='Number of requests.')
    parser.add_argument('--nr_fn', default=10, type=int, help='Number of functions.')
    parser.add_argument('--capacity', default=5, type=int, help='Capacity of functions')
    parser.add_argument('--rate', default=-1, type=float, help='Capacity of functions')
    args = parser.parse_args()

    # Examle run:
    # time python lru.py --requests 20 --workload torch-vgg --nr_fn 10 > output.log

    workload = args.workload
    requests = args.requests
    nr_fn = args.nr_fn
    capacity = args.capacity
    rate = args.rate
    rw = [rwlock.RWLockFairD() for _ in range(nr_fn)]

    commands = []
    threads = []
    
    if rate == 0.75:
        commands = [0, 1, 2, 3, 4,       0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4] # 75%
    elif rate == 0.5:
        commands = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,       6, 7, 8, 9, 6, 5, 6, 7, 8, 9] # 50%
    elif rate == 0.25:
        commands = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4,       3, 4, 1, 2, 0] # 25%
    elif rate == 0:
        commands = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9      ] # 0%
    elif rate == -1:
        for _ in range(requests):
            j = random.randrange(nr_fn)
            commands.append(j)
    else:
        print('error rate')
        exit(-1)
    print(commands)

    start = time.time()
    if rate == -1:
        for command in commands:
            t = threading.Thread(target=time_me,args=(command,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()
    else:
        for command in commands:
            time_me(command)

    end = time.time()


    for value in time_dict:
        print(value)
    print('Total spent time is: ', end - start)

    command = ""
    for r in ts:
        command += delete(workload, r)
    subprocess.run([command], shell=True)

