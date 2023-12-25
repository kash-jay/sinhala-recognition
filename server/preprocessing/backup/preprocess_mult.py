import cv2
import numpy as np
import math
import imutils
from imutils.contours import sort_contours

from preprocess import preprocess

def filter_and_center(img):
  contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

  total_image_area = 80 * 80
  minimum_area_threshold = 0.002 * total_image_area   # 2% threshold

  #FILTER CONTOURS USING THRESHOLD
  result = img.copy()
  filtered_contours = []
  for ctn in contours:
    x, y, w, h = cv2.boundingRect(ctn)
    area = w*h
    if area > minimum_area_threshold:
      filtered_contours.append(ctn)
    else:
      # REMOVE FILTERED OUT CONTOURS
      result[y:y+h, x:x+w] = 0

  if filtered_contours:
    # PLOT FILTERED CONTOURS
    filt_contours = img.copy()
    x1, x2 = math.inf, 0
    y1, y2 = math.inf, 0
    for ctn in filtered_contours:
      x, y, w, h = cv2.boundingRect(ctn)
      x1 = min(x1, x)
      x2 = max(x2, x + w)
      y1 = min(y1, y)
      y2 = max(y2, y + h)
      filt_contours = cv2.cvtColor(filt_contours, cv2.COLOR_BGR2RGB)
      filt_contours = cv2.rectangle(filt_contours, (x, y), (x+w, y+h), (0, 255, 0), 1)

    # CENTER THE IMAGE USING MAX BOUNDING BOX
    char_center_x = x1 + (x2 - x1)/2
    char_center_y = y1 + (y2 - y1)/2
    target_center_x, target_center_y = 40, 40
    tx = target_center_x - char_center_x
    ty = target_center_y - char_center_y

    translation_matrix = np.float32([[1, 0, tx], [0, 1, ty]])
    centered = cv2.warpAffine(result, translation_matrix, (80, 80), flags=cv2.INTER_NEAREST, borderMode=cv2.BORDER_CONSTANT, borderValue=0)

    return centered
  else:
    return [0], [0], [0]

def preprocess(image):
    image = image.astype(np.uint8)

    target_shape = (80, 80)

    resized_image = cv2.resize(image, target_shape)                                                   # resize to 80x80
    # cv2.imwrite('1resized.jpg', resized_image)

    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)                                            # grayscale
    # cv2.imwrite('2gray.jpg', gray)

    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # perform edge detection, find contours in the edge map, and sort the
    # resulting contours from left-to-right
    edged = cv2.Canny(blurred, 30, 150)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sort_contours(cnts, method="left-to-right")[0]
    # initialize the list of contour bounding boxes and associated
    chars = []

    total_image_area = 80 * 80
    minimum_area_threshold = 0.002 * total_image_area   # 2% threshold
    for c in cnts:
      (x, y, w, h) = cv2.boundingRect(c)
      area = w*h
      if area > minimum_area_threshold:
        roi = gray[y:y + h, x:x + w]
        thresh = cv2.threshold(roi, 0, 255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        (tH, tW) = thresh.shape
        if tW > tH:
          thresh = imutils.resize(thresh, width=80)
        else:
          thresh = imutils.resize(thresh, height=80)

        (tH, tW) = thresh.shape
        dX = int(max(0, 80 - tW) / 2.0)
        dY = int(max(0, 80 - tH) / 2.0)
        padded = cv2.copyMakeBorder(thresh, top=dY, bottom=dY,
                                    left=dX, right=dX, borderType=cv2.BORDER_CONSTANT,
                                    value=(0, 0, 0))
        padded = cv2.resize(padded, (80, 80))

        # padded = padded.astype("float32") / 255.0
        padded = np.expand_dims(padded, axis=-1)
        chars.append((padded, (x, y, w, h)))

    chars = np.array([c[0] for c in chars], dtype="float32")

    i = 0
    for char in chars:
      i += 1
      cv2.imwrite(f'{i}.jpg', char)
      # char = char.astype('float32') / 255.0

    #   char = preprocess(char)

    #   gray = cv2.cvtColor(char, cv2.COLOR_BGR2GRAY) 
      block_size = 11
      constant = 2
    #   binarized_image = cv2.adaptiveThreshold(char,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,block_size,constant)
      # binarized_image = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,block_size,constant)
      # th, binarized_image = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)                          # binarize
      # cv2.imwrite('6binarized.jpg', binarized_image)

      # copy = binarized_image.copy()
      # kernel = np.ones((1,2), np.uint8)
      # copy = cv2.dilate(copy, kernel, iterations=1)
      # cv2.imwrite('4dilated.jpg', copy)
      # contours, _ = cv2.findContours(copy, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
      # copy = cv2.cvtColor(copy,cv2.COLOR_GRAY2RGB)
      # for contour in contours:
      #   x, y, w, h = cv2.boundingRect(contour)
      #   cv2.rectangle(copy, (x, y), (x + w, y + h), (0, 255, 0), 1)
      # cv2.imwrite('5bounding.jpg', copy)

      contours, _ = cv2.findContours(char, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)         # find contours
      copy = cv2.cvtColor(char, cv2.COLOR_GRAY2BGR)                                        # change to color
      black_background = np.empty_like(char)                                               # create new image
      black_background.fill(255)                                                                      # fill with white
      black_background = cv2.cvtColor(black_background, cv2.COLOR_GRAY2BGR)                           # convert to color
      cv2.drawContours(black_background, contours, -1, (0, 0, 0), -1)                                 # add contour and invert color
      # cv2.imwrite('7contours.jpg', black_background)

      gray2 = cv2.cvtColor(black_background, cv2.COLOR_BGR2GRAY)
      th, binarized_image2 = cv2.threshold(gray2, 128, 255, cv2.THRESH_BINARY)

      thin_img = cv2.ximgproc.thinning(binarized_image2)                                              # thinning
      # cv2.imwrite('8thinned.jpg', thin_img)

      thinned_skeleton = cv2.ximgproc.thinning(thin_img, thinningType=cv2.ximgproc.THINNING_GUOHALL)  # skeletonization
      # cv2.imwrite('9skeletonized.jpg', thinned_skeleton)

      centered = filter_and_center(thinned_skeleton)                                                  # filter contours and center

      # cv2.imwrite('10preprocessed.jpg', centered)                                                   # save image

      normalized = cv2.normalize(centered, None, 0, 1.0, cv2.NORM_MINMAX, dtype=cv2.CV_32F)           # normalize
      final_image = normalized.reshape(80, 80, 1)
      char = final_image

    return chars