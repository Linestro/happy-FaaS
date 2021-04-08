#!/bin/bash

fn_names=("tf-faster-rcnn-inception-v2-coco")

id=$1

function run() {
  fn_name=$1
  id=$2
  sudo ./deploy_cpu.sh ${id} >/dev/null
  time cat /tmp/input.json | sudo nuctl invoke ${fn_name}${id} -c 'application/json'
#   sudo nuctl delete functions $fn_name${id} >/dev/null
}


for fn_name in ${fn_names[@]}; do
    run $fn_name $id
done
