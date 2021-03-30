import threading,time,subprocess,shlex
import argparse
import time

time_dict = []

def time_me(command):
    start_time = time.time()
    # cmd = shlex.split(command)
    subprocess.run([command], shell=True)
    time_dict.append(time.time() - start_time)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='.')
    parser.add_argument('--workload', default="tf-faster-rcnn-inception-v2-coco", type=str, help='Workload name.')
    parser.add_argument('--repeat', default=10, type=int, help='Number of repeat to train.')
    parser.add_argument('--blocking', action='store_true', default=False, help='Blocking for latency, non-blocking for throughput.')
    args = parser.parse_args()

    # Examle run:
    # time python process.py --repeat 10 --workload tf-matterport-mask-rcnn --blocking > output.log

    workload = args.workload
    repeat = args.repeat

    # Blocking
    if args.blocking == True:
        commands = [("cat /tmp/input.json | sudo nuctl invoke " +
            workload
            + " -c 'application/json'  >/dev/null;") * repeat]

    # Non-blocking
    else:
        commands = [("cat /tmp/input.json | sudo nuctl invoke " +
            workload
            + " -c 'application/json' >/dev/null;")] * repeat

    threads = []

    for command in commands:
        t = threading.Thread(target=time_me,args=(command,))
        time.sleep(1)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    for value in time_dict:
        print(value)


