fn_names=(
  "tf-faster-rcnn-inception-v2-coco"
  "tf-matterport-mask-rcnn"
)

repeat_num=$1

for ((i = 1; i <= repeat_num; ++i)); do
  for fn_name in ${fn_names[@]}; do
    time sudo ./deploy_gpu.sh $fn_name | grep real 2>>$fn_name.deploy.txt
    time cat /tmp/input.json | sudo nuctl invoke $fn_name -c 'application/json' | grep real 2>>$fn_name.invoke.txt
    sudo nuctl delete functions $fn_name
  done
done
