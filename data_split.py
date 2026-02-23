import os
import h5py
import shutil
from collections import defaultdict

directory_path = 'brain_tumor_411/'

train_dir = os.path.join(directory_path, 'train')
val_dir = os.path.join(directory_path, 'val')
test_dir = os.path.join(directory_path, 'test')

for directory in [train_dir, val_dir, test_dir]:
    if not os.path.exists(directory):
        os.makedirs(directory)

file_lists = defaultdict(list)

for label_folder in ['0', '1', '2']:
    label_path = os.path.join(directory_path, label_folder)
    if os.path.isdir(label_path):
        for filename in os.listdir(label_path):
            if filename.endswith('.mat'):
                file_lists[label_folder].append(os.path.join(label_path, filename))


train_ratio = 4
val_ratio = 1
test_ratio = 1

label_counts = defaultdict(int)

for label, files in file_lists.items():
    num_files = len(files)
    num_train = num_files * train_ratio // (train_ratio + val_ratio + test_ratio)
    num_val = num_files * val_ratio // (train_ratio + val_ratio + test_ratio)
    num_test = num_files - num_train - num_val

    label_counts[label] = {
        'train': 0,
        'val': 0,
        'test': 0
    }


    for i, file_path in enumerate(files):
        if i < num_train:
            dest_folder = train_dir
            label_counts[label]['train'] += 1
        elif num_train <= i < num_train + num_val:
            dest_folder = val_dir
            label_counts[label]['val'] += 1
        else:
            dest_folder = test_dir
            label_counts[label]['test'] += 1


        label_folder_path = os.path.join(dest_folder, label)
        if not os.path.exists(label_folder_path):
            os.makedirs(label_folder_path)

        shutil.move(file_path, label_folder_path)

for label, counts in label_counts.items():
    print(f"Label {label}: Train - {counts['train']}, Val - {counts['val']}, Test - {counts['test']}")
