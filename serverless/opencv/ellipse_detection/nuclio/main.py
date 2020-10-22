import base64
import io
import json

import numpy as np
import yaml
from PIL import Image

from model_loader import ModelLoader


def init_context(context):
    context.logger.info("Init context...  0%")

    functionconfig = yaml.safe_load(open("/opt/nuclio/function.yaml"))
    labels_spec = functionconfig['metadata']['annotations']['spec']
    context.logger.info(f"labels_spec {labels_spec}")
    labels = {item['id']: item['name'] for item in json.loads(labels_spec)}

    model_handler = ModelLoader(labels)
    setattr(context.user_data, 'model_handler', model_handler)

    context.logger.info("Init context...100%")


def handler(context, event):
    context.logger.info("Run OpenCV Ellipse Detector")
    data = event.body
    buf = io.BytesIO(base64.b64decode(data["image"].encode('utf-8')))
    threshold = float(data.get("threshold", 0.65))
    image = Image.open(buf)

    results = context.user_data.model_handler.infer(np.array(image), threshold)

    return context.Response(
        body=json.dumps(results),
        headers={},
        content_type='application/json',
        status_code=200
    )
