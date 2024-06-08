# import csv

# # Function to remove duplicate rows from a CSV file
# def remove_duplicates(input_file_path, output_file_path):
#     unique_rows = set()
#     with open(input_file_path, mode='r') as infile, open(output_file_path, mode='w', newline='') as outfile:
#         csv_reader = csv.reader(infile)
#         csv_writer = csv.writer(outfile)
#         header = next(csv_reader)
#         csv_writer.writerow(header)  # Write the header to the output file
#         for row in csv_reader:
#             row_tuple = tuple(row)  # Convert the list to a tuple so it can be added to a set
#             if row_tuple not in unique_rows:
#                 csv_writer.writerow(row)
#                 unique_rows.add(row_tuple)

# # Define input and output file paths
# input_csv_file_path = 'data/csv/disc.csv'
# output_csv_file_path = 'data/csv/discn.csv'

# # Remove duplicates
# remove_duplicates(input_csv_file_path, output_csv_file_path)

# print(f"Duplicate rows have been removed and the output has been saved to {output_csv_file_path}.")


def search_in_sql_file(file_path, search_term):
    with open(file_path, 'r', encoding='latin1') as file:
        lines = file.readlines()

    matching_lines = [line.strip() for line in lines if search_term.lower() in line.lower()]
    
    return matching_lines

sql_file_path = 'data/sql/xakepok_xakepok.sql'
search_term = 'alrdsfdsfdsfsdfvaesi@gmail.com'

matching_lines = search_in_sql_file(sql_file_path, search_term)
if matching_lines:
    print(f"Lines matching '{search_term}':")

    for line in matching_lines:
        print(line)
