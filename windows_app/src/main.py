from file_ops import read_csv_files, save_results
from gui import create_gui
import torch
from PyQt5.QtWidgets import QMessageBox
import numpy as np
import pandas as pd
import os 
from model import CNN1D

def mean_intensity(temp_df, bin_resolution=0.5):
    bins = np.arange(899.9, 3500, bin_resolution)
    temp_df['bin'] = pd.cut(temp_df['mass'], bins=bins)
    return temp_df.groupby('bin')['intensity'].mean().values

def normalize(tensor):
    tensor[torch.isnan(tensor)] = 0
    mean = tensor.mean()
    std = tensor.std()
    return (tensor - mean) / (std + torch.finfo(torch.float32).eps)

def load_model(weight_path):
    model = torch.load(weight_path, map_location=torch.device('cpu'))
    model.eval()
    return model

def main(model_file_path, input_directory, output_directory):
    if not model_file_path or not input_directory or not output_directory:
        show_missing_paths_message()
        return
    
    model = load_model(model_file_path)
    file_paths, file_names = read_csv_files(input_directory)
    results, file_names, targets = make_predictions(file_paths, model)
    save_results(results, output_directory, file_names, targets)
    show_done_message()

def show_missing_paths_message():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle("Missing Path")
    msg.setText("Please provide all required paths (Model, Input Directory, Output Directory).")
    msg.exec_()

def show_done_message():
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Information)
    msg.setWindowTitle("Process Completed")
    msg.setText("The classification process is complete.")
    msg.exec_()

def make_predictions(file_paths, model):
    results = []
    file_names = []
    targets = []
    for i, file_path in enumerate(file_paths):
        temp_df = pd.read_csv(file_path)
        file_name = os.path.basename(file_path)
        file_names.append(file_name)
        
        intensities = mean_intensity(temp_df)
        tensor_data = torch.tensor(intensities, dtype=torch.float32)
        tensor_data = normalize(tensor_data)
        
        output = model(tensor_data.unsqueeze(0).unsqueeze(0))
        probabilities = torch.softmax(output, dim=1).detach().numpy().round(3)
        results.append(probabilities)
        
        target = np.argmax(probabilities)
        targets.append(target)
        
    return results, file_names, targets

if __name__ == "__main__":
    create_gui(main)
