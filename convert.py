import csv

input_file = 'source files/Zh_En_GPT.csv'
output_file = 'Zh_En_GPT.csv'

with open(input_file, mode='r', encoding='utf-8') as infile, \
     open(output_file, mode='w', newline='', encoding='utf-8') as outfile:
    
    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    # Read header and write new header with "index"
    header = next(reader)
    writer.writerow(['index'] + header)

    # Write each row with a new index
    for idx, row in enumerate(reader):
        writer.writerow([idx] + row)

print(f"Saved with index to: {output_file}")
