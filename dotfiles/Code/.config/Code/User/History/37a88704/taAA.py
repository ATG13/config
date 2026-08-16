import sys
import os
from pathlib import Path

current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
sys.path.append(str(project_root))

from tensorflow.keras.models import load_model
from src.data_processing import load_data
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import time

def plot_confusion_matrix(model, generator, set_name):
    print(f"Generating confusion matrix for {set_name} data...")
    # Reset generator to start
    generator.reset()
    
    # Get predictions
    y_pred = model.predict(generator)
    y_pred_classes = np.argmax(y_pred, axis=1)
    
    # Get true labels
    y_true = generator.classes
    
    # Compute confusion matrix
    cm = confusion_matrix(y_true, y_pred_classes)
    
    # Plot
    plt.figure(figsize=(10, 8))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=list(generator.class_indices.keys()),
                yticklabels=list(generator.class_indices.keys()))
    plt.title(f'Confusion Matrix - {set_name} Data')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    
    # Save plot
    output_dir = project_root / "reports" / "confusion_matrices"
    output_dir.mkdir(parents=True, exist_ok=True)
    save_path = output_dir / f"confusion_matrix_{set_name}.png"
    plt.savefig(save_path)
    plt.close()
    print(f"Confusion matrix saved to {save_path}")
    print("\nConfusion Matrix:")
    print(cm)
    
def test_main():
    # Load best model
    model_path = project_root / "models" / "banana_model_best.keras"
    
    # Putting the correct path
    if Path.cwd().name != 'src':
        print(f"Changing working directory to {current_file.parent} to support data loading...")
        os.chdir(current_file.parent)

    # Load data
    print("Loading data...")
    train_generator, valid_generator, test_generator = load_data(shuffle_train=False)
    
    if not model_path.exists():
        print(f"Error: Model file not found at {model_path}")
        return

    print(f"Loading model from {model_path}...")
    try:
        model = load_model(model_path)
    except Exception as e:
        print(f"Failed to load model: {e}")
        return

    # Evaluate on Train Data
    print("\n" + "="*30)
    print("Evaluating on Train Data...")
    print("="*30)
    train_loss, train_acc = model.evaluate(train_generator)
    print(f"Train Loss: {train_loss:.4f}")
    print(f"Train Accuracy: {train_acc:.4f}")
    plot_confusion_matrix(model, train_generator, "Train")

    # Evaluate on Validation Data
    print("\n" + "="*30)
    print("Evaluating on Validation Data...")
    print("="*30)
    val_loss, val_acc = model.evaluate(valid_generator)
    print(f"Validation Loss: {val_loss:.4f}")
    print(f"Validation Accuracy: {val_acc:.4f}")
    plot_confusion_matrix(model, valid_generator, "Validation")
    
    # Evaluate on Test Data
    print("\n" + "="*30)
    print("Evaluating on Test Data...")
    print("="*30)
    test_loss, test_acc = model.evaluate(test_generator)
    print(f"Test Loss: {test_loss:.4f}")
    print(f"Test Accuracy: {test_acc:.4f}")
    plot_confusion_matrix(model, test_generator, "Test")

if __name__ == "__main__":
    test_main()
