import os
import shutil
import random

root_directory = 'F:\\IT_IV_pro\\Data'

train_directory = 'F:\\IT_IV_pro\\train'
val_directory = 'F:\\IT_IV_pro\\validation'
test_directory = 'F:\\IT_IV_pro\\test'

train_ratio = 0.7  
val_ratio = 0.15  
test_ratio = 0.15 

os.makedirs(train_directory, exist_ok=True)
os.makedirs(val_directory, exist_ok=True)
os.makedirs(test_directory, exist_ok=True)

for class_name in os.listdir(root_directory):
    class_directory = os.path.join(root_directory, class_name)

    train_class_dir = os.path.join(train_directory, class_name)
    val_class_dir = os.path.join(val_directory, class_name)
    test_class_dir = os.path.join(test_directory, class_name)

    os.makedirs(train_class_dir, exist_ok=True)
    os.makedirs(val_class_dir, exist_ok=True)
    os.makedirs(test_class_dir, exist_ok=True)

    images = os.listdir(class_directory)

    random.shuffle(images)

    num_images = len(images)
    num_train = int(train_ratio * num_images)
    num_val = int(val_ratio * num_images)

    train_images = images[:num_train]
    val_images = images[num_train:num_train + num_val]
    test_images = images[num_train + num_val:]

    for image in train_images:
        src = os.path.join(class_directory, image)
        dst = os.path.join(train_class_dir, image)
        shutil.copy(src, dst)

    for image in val_images:
        src = os.path.join(class_directory, image)
        dst = os.path.join(val_class_dir, image)
        shutil.copy(src, dst)

    for image in test_images:
        src = os.path.join(class_directory, image)
        dst = os.path.join(test_class_dir, image)
        shutil.copy(src, dst)

print("Dataset split into training, validation, and test sets.")
