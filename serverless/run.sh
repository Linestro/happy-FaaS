#!/bin/bash
fn_names=("tf-faster-rcnn-inception-v2-coco" "tf-matterport-mask-rcnn")

repeat_num=$1

function run() {
  fn_name=$1
  i=$2
  { time sudo ./deploy_gpu.sh $fn_name $fn_name$i; } 2>&1 >/dev/null | grep real | awk '{print $2}' | sudo tee -a $fn_name.deploy.txt
  { time cat /tmp/input.json | sudo nuctl invoke $fn_name$i -c 'application/json'; } 2>&1 >/dev/null | grep real | awk '{print $2}' | sudo tee -a $fn_name.invoke.txt
  sudo nuctl delete functions $fn_name$i >/dev/null
}

for ((i = 1; i <= repeat_num; ++i)); do
  for fn_name in ${fn_names[@]}; do
    run $fn_name $i &
  done
done

wait