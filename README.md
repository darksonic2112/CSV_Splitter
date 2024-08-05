# CSV Splitter

This program splits a large CSV file into multiple smaller CSV files based on a specified number of rows and a keyword found in a specific column.

## Features
- Automatically detects the CSV delimiter.
- Splits the file after a specified number of rows.
- Ensures that values belonging together are not broken across files by splitting at the next occurrence of a specified keyword.

## Requirements
- Python 3.x

## Installation
1. Clone this repository or download the script directly.
2. Ensure you have Python 3 installed on your system.

## Usage
The program can be run from the command line. Use the following syntax:

```sh
python <file_path\csv_splitter.py> <file_path\file_name.csv> <output_dir> <chunk_size> <keyword_index> <keyword_value>
```
Args: 
- file_path (str): Path to the input CSV file.
- output_dir (str): Directory to save the output CSV files.
- chunk_size (int): Number of rows to include in each CSV file.
- keyword_index (int): Column index to check for the keyword [Optional].
- keyword_value (str): Keyword to look for in the specified column [Optional].

## Notes
- Works only with CSV files.
- The amount of rows inside a CSV file is always chunk_size + 1 (for the headder). Make sure that the total number of rows does not exceed 1.048.576.
  
