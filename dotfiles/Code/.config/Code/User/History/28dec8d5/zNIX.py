import os
import numpy as np
import cv2
from pathlib import Path
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import shutil

def load_and_preprocess_images(data_dir, img_size=(224, 224)):
    """Load images from dataset directory and preprocess them."""
    data_dir = Path(data_dir)
    images = []
    labels = []
    
    # Expected class names (adjust based on your dataset)
    class_names = ['unripe', 'ripe', 'overripe']  # Update with actual classes
    
    for class_idx, class_name in enumerate(class_names):
        class_dir = data_dir / class_name
        if not class_dir.exists():
            print(f"Warning: {class_dir} not found")
            continue
            
        for img_path in class_dir.glob('*.jpg'):
            # Load and resize image
            img = cv2.imread(str(img_path))
            if img is None:
                continue
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, img_size)
            img = img.astype(np.float32) / 255.0  # Normalize to 0-1
            
            images.append(img)
            labels.append(class_idx)
    
    return np.array(images), np.array(labels), class_names

def create_data_generators(data_dir, batch_size=32, img_size=(224, 224)):
    """Create ImageDataGenerators for training/validation with augmentation."""
    datagen_args = {
        'rescale': 1./255,
        'rotation_range': 20,
        'width_shift_range': 0.2,
        'height_shift_range': 0.2,
        'horizontal_flip': True,
        'fill_mode': 'nearest'
    }
    
    train_datagen = ImageDataGenerator(**datagen_args)
    val_datagen = ImageDataGenerator(rescale=1./255)
    
    train_generator = train_datagen.flow_from_directory(
        data_dir / 'train',
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical'
    )
    
    val_generator = val_datagen.flow_from_directory(
        data_dir / 'val',
        target_size=img_size,
        batch_size=batch_size,
        class_mode='categorical'
    )
    
    return train_generator, val_generator

def main():
    # Paths
    raw_data_dir = Path('data/raw')
    processed_dir = Path('data')
    
    # Create directories
    for split in ['train', 'val', 'test']:
        for class_name in ['unripe', 'ripe', 'overripe']:  # Update classes
            (processed_dir / split / class_name).mkdir(parents=True, exist_ok=True)
    
    # Load raw data
    print("Loading and preprocessing images...")
    images, labels, class_names = load_and_preprocess_images(raw_data_dir)
    print(f"Loaded {len(images)} images across {len(class_names)} classes")
    
    # Split data 80/10/10
    X_temp, X_test, y_temp, y_test = train_test_split(
        images, labels, test_size=0.1, stratify=labels, random_state=42
    )
    X_train, X_val, y_train, y_val = train_test_split(
        X_temp, y_temp, test_size=0.111, stratify=y_temp, random_state=42  # 10/90
    )
    
    print(f"Train: {len(X_train)}, Val: {len(X_val)}, Test: {len(X_test)}")
    
    # Save split data (optional: save as numpy arrays)
    np.save(processed_dir / 'X_train.npy', X_train)
    np.save(processed_dir / 'y_train.npy', y_train)
    np.save(processed_dir / 'X_val.npy', X_val)
    np.save(processed_dir / 'y_val.npy', y_val)
    np.save(processed_dir / 'X_test.npy', X_test)
    np.save(processed_dir / 'y_test.npy', y_test)
    
    print("Data preprocessing complete! Ready for model training.")

if __name__ == "__main__":
    main()
