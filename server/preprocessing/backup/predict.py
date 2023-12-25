import sys
import cv2
import numpy as np
import math
import tensorflow as tf
from tensorflow import keras

from preprocess import preprocess
from sinhala_letters import sinhala_letters

sys.stdout.reconfigure(encoding='utf-8')
# -*- coding: utf-8 -*-

fileDest = sys.argv[1]
image = cv2.imread(fileDest)

final_image = preprocess(image)

# Load up model
with open("model.json", "r") as json_file:
    model_json = json_file.read()
model = keras.models.model_from_json(model_json)
model.load_weights("model_weights.h5")

x = np.expand_dims(final_image, axis=0)

pred = model.predict(x)
predicted_class = np.argmax(pred) + 1
print(sinhala_letters[predicted_class - 1])