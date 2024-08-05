import csv
import argparse
import os

"""
This program splits one CSV file into multiple CSV files based on a number of rows and a keyword after this number
has been reached. 
'keyword_index' represents the column number of the column, where the program looks for the 'keyword_value', a string.
The 'chunk_size' indicates the number of rows to include in a CSV file.
In order to not break values that belong together, after the 'chunk_size' has been reached, the program checks for the
'keyword_value'. When it is found, the CSV file is split and the program begins with a new file. 
"""


def split_csv(file_path: str, output_dir: str, chunk_size: int, keyword_index: int, keyword_value: str) -> None:
    """
    Splits a CSV file into multiple CSV files based on chunk size and keyword.

    Args:
        file_path (str): Path to the input CSV file.
        output_dir (str): Directory to save the output CSV files.
        chunk_size (int): Number of rows to include in each CSV file.
        keyword_index (int): Column index to check for the keyword.
        keyword_value (str): Keyword to look for in the specified column.

    Returns:
        None
    """
    with open(file_path, 'r') as file:
        # Automatically detect the delimiter
        dialect = csv.Sniffer().sniff(file.read(1024))
        file.seek(0)
        reader = csv.reader(file, dialect)

        headers = next(reader)
        chunk_number = 1
        wrap_up_file = False
        filename = os.path.splitext(os.path.basename(file_path))[0]
        file_part = open(f"{output_dir}/{filename}_{chunk_number}.csv", 'w', newline='')
        writer = csv.writer(file_part)
        writer.writerow(headers)

        # Iterate over rows and write them to new CSV files based on chunk size and keyword
        for i, row in enumerate(reader, start=1):
            if i % chunk_size == 0:
                wrap_up_file = True
            if wrap_up_file and row[keyword_index] == keyword_value:
                file_part.close()
                chunk_number += 1
                file_part = open(f"{output_dir}/{filename}_{chunk_number}.csv", 'w', newline='')
                writer = csv.writer(file_part)
                writer.writerow(headers)
                wrap_up_file = False

            writer.writerow(row)

        file_part.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split CSV file based on a specific value in a column.')
    parser.add_argument('file_path', type=str, help='Path to the input CSV file')
    parser.add_argument('output_dir', type=str, help='Directory to save the output CSV files')
    parser.add_argument('chunk_size', type=int, help='Amount of rows inside each CSV file')
    parser.add_argument('keyword_index', type=int, help='Colum where keyword appears')
    parser.add_argument('keyword_value', type=str, help='Keyword to look for')

    args = parser.parse_args()

    split_csv(args.file_path, args.output_dir, args.chunk_size, args.keyword_index, args.keyword_value)
