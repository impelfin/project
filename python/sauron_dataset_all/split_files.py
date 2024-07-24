import os
import shutil
import random
from collections import defaultdict

def split_files(base_path='train', valid_ratio=0.2, test_ratio=0.2):
    images_dir = os.path.join(base_path, 'images')
    labels_dir = os.path.join(base_path, 'labels')
    
    valid_images_dir = 'valid/images'
    valid_labels_dir = 'valid/labels'
    test_images_dir = 'test/images'
    test_labels_dir = 'test/labels'
    
    os.makedirs(valid_images_dir, exist_ok=True)
    os.makedirs(valid_labels_dir, exist_ok=True)
    os.makedirs(test_images_dir, exist_ok=True)
    os.makedirs(test_labels_dir, exist_ok=True)
    
    files = os.listdir(images_dir)
    
    base_name_files = defaultdict(list)
    for file in files:
        base_name = file.split('_')[0]
        base_name_files[base_name].append(file)
    
    for base_name, file_list in base_name_files.items():
        random.shuffle(file_list)
        
        total = len(file_list)
        train_count = int(total * 0.6)
        valid_count = int(total * valid_ratio)
        test_count = total - train_count - valid_count
        
        train_files = file_list[:train_count]
        valid_files = file_list[train_count:train_count + valid_count]
        test_files = file_list[train_count + valid_count:]
        
        for file in valid_files:
            src_image_path = os.path.join(images_dir, file)
            src_label_path = os.path.join(labels_dir, file.replace('.jpg', '.txt'))
            shutil.move(src_image_path, os.path.join(valid_images_dir, file))
            shutil.move(src_label_path, os.path.join(valid_labels_dir, file.replace('.jpg', '.txt')))
        
        for file in test_files:
            src_image_path = os.path.join(images_dir, file)
            src_label_path = os.path.join(labels_dir, file.replace('.jpg', '.txt'))
            shutil.move(src_image_path, os.path.join(test_images_dir, file))
            shutil.move(src_label_path, os.path.join(test_labels_dir, file.replace('.jpg', '.txt')))

if __name__ == '__main__':
    split_files()
