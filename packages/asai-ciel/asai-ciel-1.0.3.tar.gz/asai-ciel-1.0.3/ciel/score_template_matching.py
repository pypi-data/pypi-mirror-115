import numpy as np
from sklearn.cluster import KMeans
import cv2
import pickle
from typing import Any, List, Dict


def make_feature(image):
    resized_number_image = cv2.resize(image, (13, 17))
    ret, binary_number_image = cv2.threshold(
        np.average(resized_number_image, axis=2),
        200, 255, cv2.THRESH_BINARY)
    return binary_number_image


def train(number_images):
    kmeans = KMeans(30, random_state=1, n_jobs=-1)
    predicted = kmeans.fit_predict(number_images)

    label_images: Dict[Any, List[Any]] = {}
    for image, label in zip(number_images, predicted):
        if label not in label_images:
            label_images[label] = []
        label_images[label].append(image.reshape((17, 13)))

    # データが変わったら jupyter でクラスタを確認してアノテーションをつけなおす必要がある
    digit_cluster_annotations = {
        'x': [12],
        '0': [1, 9, 10, 14, 28],
        '1': [4],
        '2': [0],
        '3': [7],
        '4': [11, 25],
        '5': [21],
        '6': [3],
        '7': [8],
        '8': [19],
        '9': [15]
    }

    digit_average_images = {}
    for digit in digit_cluster_annotations:
        images = list(map(
            lambda l: label_images[l], digit_cluster_annotations[digit]))
        image = np.average(np.concatenate(images), axis=0)
        digit_average_images[digit] = image

    return digit_average_images


def digit_distance(a, b):
    return np.average(np.abs(a - b))


def predict(image, digit_average_images):
    feature = make_feature(image)
    score_digit = ' '
    min_dist = 50
    digits = list(digit_average_images.keys())

    for digit in digits:
        dist = digit_distance(feature, digit_average_images[digit])
        if dist < min_dist:
            score_digit = digit
            min_dist = dist

    return score_digit


def save(digit_average_images, path):
    with open(path, mode='wb') as f:
        pickle.dump(digit_average_images, f)


def load(path):
    with open(path, mode='rb') as f:
        digit_average_images = pickle.load(f)
    return digit_average_images
