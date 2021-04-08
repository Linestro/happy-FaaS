#!/bin/bash
# Sample commands to deploy nuclio functions on GPU

fn_name=$2

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"

nuctl create project cvat

if [ "$1" = "tf-faster-rcnn-inception-v2-coco" ]; then
  nuctl deploy $fn_name --project-name cvat \
    --path "$SCRIPT_DIR/tensorflow/faster_rcnn_inception_v2_coco/nuclio" \
    --platform local --base-image tensorflow/tensorflow:2.1.1-gpu \
    --desc "GPU based Faster RCNN from Tensorflow Object Detection API" \
    --image cvat/tf.faster_rcnn_inception_v2_coco_gpu \
    --triggers '{"myHttpTrigger": {"maxWorkers": 1}}' \
    --resource-limit nvidia.com/gpu=1 --verbose

elif [ "$1" = 'tf-matterport-mask-rcnn' ]; then
  nuctl deploy $fn_name --project-name cvat \
    --path "$SCRIPT_DIR/tensorflow/matterport/mask_rcnn/nuclio" \
    --platform local --base-image tensorflow/tensorflow:1.15.5-gpu-py3 \
    --desc "GPU based implementation of Mask RCNN on Python 3, Keras, and TensorFlow." \
    --image cvat/tf.matterport.mask_rcnn_gpu --triggers '{"myHttpTrigger": {"maxWorkers": 1}}' \
    --resource-limit nvidia.com/gpu=1 --verbose

fi

nuctl get function
