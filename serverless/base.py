import threading,time,subprocess,shlex
import argparse
import time
import random

time_dict = []
workload = ""
capacity = 0
cnt = 0
cv = threading.Condition()

def deploy(workload, id):
    return "sudo ./deploy_gpu.sh {0} {0}{1} > /dev/null;".format(workload, id)

def invoke(workload, id):
    return "cat /tmp/input.json | sudo nuctl invoke {0}{1} -c 'application/json' > /dev/null;".format(workload, id)

def delete(workload, id):
    return "sudo nuctl delete functions {0}{1} > /dev/null;".format(workload, id)

def time_me(id):
    global time_dict, cnt
    start_time = time.time()
    with cv:
        while cnt > capacity:
            cv.wait()
    command = ""
    command += deploy(workload, id)
    command += "sleep 2;"
    command += invoke(workload, id)

    with cv:
        cnt += 1

    subprocess.run([command], shell=True)
    time_dict.append(time.time() - start_time)
    command = delete(workload, id)
    subprocess.run([command], shell=True)

    with cv:
        cnt -= 1
        cv.notify()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='.')
    parser.add_argument('--workload', default="torch-vgg", type=str, help='Workload name.')
    parser.add_argument('--requests', default=20, type=int, help='Number of requests.')
    parser.add_argument('--nr_fn', default=10, type=int, help='Number of functions.')
    parser.add_argument('--capacity', default=6, type=int, help='Capacity of functions')
    args = parser.parse_args()

    # Examle run:
    # time python base.py --requests 20 --workload torch-vgg --nr_fn 10 > output.log

    workload = args.workload
    requests = args.requests
    nr_fn = args.nr_fn
    capacity = args.capacity

    commands = []
    threads = []

    for i in range(requests):
        commands.append(i)
    
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


