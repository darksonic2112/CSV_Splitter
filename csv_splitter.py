# CSV splitter in case of very large csv files over ~1.04 million rows and over ~16k columns
import csv
import os
import argparse


def split_csv_by_value(file_path, output_dir, column_index, split_value, start_after_value=True):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)

        os.makedirs(output_dir, exist_ok=True)

        chunk_number = 1
        output_file_path = os.path.join(output_dir, f"part_{chunk_number}.csv")
        output_file = open(output_file_path, 'w', newline='')
        writer = csv.writer(output_file)
        writer.writerow(headers)

        for row in reader:
            if row[column_index] == split_value:
                output_file.close()
                chunk_number += 1
                output_file_path = os.path.join(output_dir, f"part_{chunk_number}.csv")
                output_file = open(output_file_path, 'w', newline='')
                writer = csv.writer(output_file)
                writer.writerow(headers)

                if start_after_value:
                    continue

            writer.writerow(row)

        output_file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split CSV file based on a specific value in a column.')
    parser.add_argument('file_path', type=str, help='Path to the input CSV file')
    parser.add_argument('output_dir', type=str, help='Directory to save the output CSV files')
    parser.add_argument('column_index', type=int, help='Index of the column to check for the split value (0-based)')
    parser.add_argument('split_value', type=str, help='Value in the specified column to split on')
    parser.add_argument('--start_after_value', action='store_true',
                        help='If set, the split value itself will be the start of the next file')

    args = parser.parse_args()

    split_csv_by_value(args.file_path, args.output_dir, args.column_index, args.split_value, args.start_after_value)
