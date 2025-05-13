import csv

input_file = 'source files/En_Zh_GPT.csv'
output_file = 'En_Zh_GPT.csv'

with open(input_file, newline='', encoding='utf-8') as infile, \
     open(output_file, 'w', newline='', encoding='utf-8') as outfile:
    
    reader = csv.DictReader(infile)
    fieldnames = [f for f in reader.fieldnames if f.lower() != 'index']
    fieldnames = ['index'] + fieldnames

    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for i, row in enumerate(reader):
        row = {k: v for k, v in row.items() if k.lower() != 'index'}
        row['index'] = i
        writer.writerow(row)
