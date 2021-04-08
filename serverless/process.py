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
    parser.add_argument('--repeat', default=1, type=int, help='Number of repeat to train.')
    args = parser.parse_args()

    # Examle run:
    # time python process.py --repeat 10 --workload tf-matterport-mask-rcnn --blocking > output.log

    workload = args.workload
    repeat = args.repeat

    commands = []
    threads = []

    for i in range(repeat):
        commands.append("sudo ./measure.sh " + str(i) + ";")

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


