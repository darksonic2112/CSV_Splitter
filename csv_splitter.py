import csv
import argparse
import os
from typing import Optional

"""
This program splits one CSV file into multiple CSV files based on a number of rows and optionally a keyword after 
this number has been reached. 
'keyword_index' represents the column number of the column where the program looks for the 'keyword_value', a string.
The 'chunk_size' indicates the number of rows to include in a CSV file.
In order to not break values that belong together, after the 'chunk_size' has been reached, the program checks for the
'keyword_value'. When it is found, the CSV file is split and the program begins with a new file. 
If no keyword is provided, the program simply splits the file into chunks of the specified size.
"""


def split_csv(file_path: str, output_dir: str, chunk_size: int, keyword_index: Optional[int] = None,
              keyword_value: Optional[str] = None) -> None:
    """
    Splits a CSV file into multiple CSV files based on chunk size and optionally a keyword.

    Args:
        file_path (str): Path to the input CSV file.
        output_dir (str): Directory to save the output CSV files.
        chunk_size (int): Number of rows to include in each CSV file.
        keyword_index (Optional[int]): Column index to check for the keyword (0-based).
        keyword_value (Optional[str]): Keyword to look for in the specified column.

    Returns:
        None
    """
    with open(file_path, 'r', newline='') as file:
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

        def open_new_file(chunk_number: int) -> csv.writer:
            """
            Closes the current file and opens a new file for writing.

            Args:
                chunk_number (int): The current chunk number.

            Returns:
                csv.writer: A writer object for the new file.
            """
            nonlocal file_part
            if file_part:
                file_part.close()
            new_file_path = f"{output_dir}/{filename}_{chunk_number}.csv"
            file_part = open(new_file_path, 'w', newline='')
            new_writer = csv.writer(file_part)
            new_writer.writerow(headers)
            return new_writer

        # Iterate over rows and write them to new CSV files based on chunk size and optional keyword
        for i, row in enumerate(reader, start=1):
            if wrap_up_file and keyword_index is not None and row[keyword_index] == keyword_value:
                writer = open_new_file(chunk_number + 1)
                chunk_number += 1
                wrap_up_file = False

            writer.writerow(row)

            if i % chunk_size == 0:
                if keyword_index is None:
                    writer = open_new_file(chunk_number + 1)
                    chunk_number += 1
                else:
                    wrap_up_file = True

        if file_part:
            file_part.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Split CSV file based on chunk size and optionally a specific value in a column.')
    parser.add_argument('file_path', type=str, help='Path to the input CSV file')
    parser.add_argument('output_dir', type=str, help='Directory to save the output CSV files')
    parser.add_argument('chunk_size', type=int, help='Number of rows inside each CSV file')
    parser.add_argument('keyword_index', nargs='?', type=int, help='Column index where keyword appears (0-based)', default=None)
    parser.add_argument('keyword_value', nargs='?', type=str, help='Keyword to look for', default=None)

    args = parser.parse_args()

    split_csv(args.file_path, args.output_dir, args.chunk_size, args.keyword_index, args.keyword_value)
