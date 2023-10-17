import pandas as pd
import os
from datetime import datetime

def read_csv_files(directory):
    file_paths = []
    file_names = []
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            filepath = os.path.join(directory, filename)
            file_paths.append(filepath)
            file_names.append(filename)
    return file_paths, file_names



def save_results(results, output_directory, file_names, targets):
    # Column names
    column_names = [
        'Canidae', 'Cervidae', 'CervidaeGazellaSaiga', 'Ovis', 'Equidae',
        'CrocutaPanthera', 'BisonYak', 'Capra', 'Ursidae', 'Vulpes vulpes',
        'Elephantidae', 'Others', 'Rhinocerotidae', 'Rangifer tarandus', 'Hominins'
    ]
    
    # Updated the dataframe creation line to handle numpy arrays
    concatenated_df = pd.concat([pd.DataFrame(result) for result in results], ignore_index=True)
    
    concatenated_df.columns = column_names
    concatenated_df['Most Probable Class'] = [column_names[i] for i in targets]
    
    # Reorder columns to place 'Most Probable Class' as the second column
    cols = ['Most Probable Class'] + [col for col in concatenated_df.columns if col != 'Most Probable Class']
    concatenated_df = concatenated_df[cols]
    
    # Insert file names as the first column
    concatenated_df.insert(0, 'File Name', file_names)

    # Get current date and time
    current_datetime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    
    # Create a unique filename with current date and time
    output_path = os.path.join(output_directory, f'results_{current_datetime}.csv')
    
    # Save the concatenated dataframe to the unique output path
    concatenated_df.to_csv(output_path, index=False)
