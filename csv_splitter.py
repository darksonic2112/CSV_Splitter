# CSV splitter in case of very large csv files over ~1.04 million rows and over ~16k columns
import csv
import argparse


def split_csv(file_path, output_dir, chunk_size):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        chunk_number = 1
        file_part = open(f"{output_dir}/part_{chunk_number}.csv", 'w', newline='')
        writer = csv.writer(file_part)
        writer.writerow(headers)

        for i, row in enumerate(reader, start=1):
            if i % chunk_size == 0:
                file_part.close()
                chunk_number += 1
                file_part = open(f"{output_dir}/part_{chunk_number}.csv", 'w', newline='')
                writer = csv.writer(file_part)
                writer.writerow(headers)

            writer.writerow(row)

        file_part.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Split CSV file based on a specific value in a column.')
    parser.add_argument('file_path', type=str, help='Path to the input CSV file')
    parser.add_argument('output_dir', type=str, help='Directory to save the output CSV files')

    args = parser.parse_args()

    split_csv(args.file_path, args.output_dir, 2)
