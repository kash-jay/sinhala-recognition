import cv2
import numpy as np
import math

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

    resized_image = cv2.resize(image, target_shape)                                                 # resize to 80x80
    # cv2.imwrite('1resized.jpg', resized_image)

    gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)                                          # grayscale
    # cv2.imwrite('2gray.jpg', gray)

    block_size = 11
    constant = 2
    binarized_image = cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,block_size,constant)

    contours, _ = cv2.findContours(binarized_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)         # find contours
    copy = cv2.cvtColor(binarized_image, cv2.COLOR_GRAY2BGR)                                        # change to color
    black_background = np.empty_like(binarized_image)                                               # create new image
    black_background.fill(255)                                                                      # fill with white
    black_background = cv2.cvtColor(black_background, cv2.COLOR_GRAY2BGR)                           # convert to color
    cv2.drawContours(black_background, contours, -1, (0, 0, 0), -1)                                 # add contour and invert color
    # cv2.imwrite('7contours.jpg', black_background)

    gray2 = cv2.cvtColor(black_background, cv2.COLOR_BGR2GRAY)
    th, binarized_image2 = cv2.threshold(gray2, 128, 255, cv2.THRESH_BINARY)

    thin_img = cv2.ximgproc.thinning(binarized_image2)                                               # thinning
    # cv2.imwrite('8thinned.jpg', thin_img)

    thinned_skeleton = cv2.ximgproc.thinning(thin_img, thinningType=cv2.ximgproc.THINNING_GUOHALL)  # skeletonization
    # cv2.imwrite('9skeletonized.jpg', thinned_skeleton)

    # centered = filter_and_center(thinned_skeleton)                                                  # filter contours and center

    # cv2.imwrite('10preprocessed.jpg', centered)                                                     # save image

    normalized = cv2.normalize(thinned_skeleton, None, 0, 1.0, cv2.NORM_MINMAX, dtype=cv2.CV_32F)           # normalize
    final_image = normalized.reshape(80, 80, 1)
    return final_image