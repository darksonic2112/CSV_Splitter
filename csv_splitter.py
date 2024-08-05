# CSV splitter in case of very large csv files over ~1.04 million rows and over ~16k columns
import csv
import argparse
import os


def split_csv(file_path, output_dir, chunk_size, keyword_index, keyword_value):
    with open(file_path, 'r') as file:
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
