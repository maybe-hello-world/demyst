import os
import csv
import sys
from tqdm import tqdm

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <root_folder> <output_file>")
        sys.exit(1)
    
    root_folder = sys.argv[1]
    output_file = sys.argv[2]
    
    csv_files = []
    for subdir, dirs, files in os.walk(root_folder):
        for file in files:
            if file.lower().endswith('.csv'):
                csv_files.append(os.path.join(subdir, file))
    
    with open(output_file, 'w', newline='', encoding='utf-8') as outfile:
        writer = None 
        
        for file_path in tqdm(csv_files, desc="Processing CSV files"):
            with open(file_path, 'r', newline='', encoding='utf-8') as infile:
                reader = csv.reader(infile)
                try:
                    header = next(reader)
                except StopIteration:
                    continue  

                try:
                    data_row = next(reader)
                except StopIteration:
                    continue  

                if writer is None:
                    new_header = header + ["filename"]
                    writer = csv.writer(outfile)
                    writer.writerow(new_header)
                
                full_path = os.path.abspath(file_path)
                writer.writerow(data_row + [full_path])

if __name__ == '__main__':
    main()
