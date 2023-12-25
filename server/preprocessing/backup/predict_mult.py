import sys
import cv2
import numpy as np
import math
import tensorflow as tf
from tensorflow import keras

from preprocess_mult import preprocess
from sinhala_letters import sinhala_letters

sys.stdout.reconfigure(encoding='utf-8')
# -*- coding: utf-8 -*-

fileDest = sys.argv[1]
image = cv2.imread(fileDest)

char_images = preprocess(image)

# Load up model
with open("model.json", "r") as json_file:
    model_json = json_file.read()
model = keras.models.model_from_json(model_json)
model.load_weights("model_weights.h5")

for x in char_images:
    x = np.expand_dims(x, axis=0)

predictions = model.predict(char_images)
print(len(predictions))
word = ""

for pred in predictions:
    predicted_class = np.argmax(pred)
    prob = pred[predicted_class]
    letter = sinhala_letters[predicted_class]
    print(letter + str(prob) + "%")
    word += letter

print(word)