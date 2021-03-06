# Copyright (C) 2020 Intel Corporation
#
# SPDX-License-Identifier: MIT

import json
import base64
from PIL import Image
import io
from model_handler import ModelHandler

def init_context(context):
    context.logger.info("Init context...  0%")

    model = ModelHandler()
    setattr(context.user_data, 'model', model)

    context.logger.info("Init context...100%")

def handler(context, event):
    context.logger.info("call handler")
    data = event.body
    pos_points = [[0,0], [1,1], [2,2], [3,3], [4,4]]# data["pos_points"]
    neg_points = [[10,10], [11,11], [12,12], [13,13], [14,14]]# data["neg_points"]
    threshold = data.get("threshold", 0.5)
    buf = io.BytesIO(base64.b64decode(data["image"].encode('utf-8')))
    image = Image.open(buf)

    polygon = context.user_data.model.handle(image, pos_points,
        neg_points, threshold)
    return context.Response(body=json.dumps(polygon),
                            headers={},
                            content_type='application/json',
                            status_code=200)
