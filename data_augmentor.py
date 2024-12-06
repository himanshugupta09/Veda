import os
import cv2
import numpy as np
import random
from tqdm import tqdm

input_directory = 'E:\\mlproject\\train\\my_images'
output_directory = 'E:\\mlproject\\Augmented_data'

os.makedirs(output_directory, exist_ok=True)

input_images = os.listdir(input_directory)

def rotate_image(image, angle):
    rows, cols, _ = image.shape
    M = cv2.getRotationMatrix2D((cols / 2, rows / 2), angle, 1)
    return cv2.warpAffine(image, M, (cols, rows))

for image_name in tqdm(input_images):
    image_path = os.path.join(input_directory, image_name)
    image = cv2.imread(image_path)

    augmented_image = rotate_image(image, random.randint(-15, 15))

    output_path = os.path.join(output_directory, image_name)
    cv2.imwrite(output_path, augmented_image)

print("Data augmentation completed.")
