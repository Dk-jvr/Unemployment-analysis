from csv import writer
from csv import reader

with open('World_Population_2020.csv', 'r') as cooord, \
        open('result.csv', 'r') as r, \
        open('result2.csv', 'w', newline='') as write_obj:
    code_by_iso3 = dict()
    for row in reader(cooord):
        code_by_iso3[row[2]] = row[3]

    csv_reader = reader(unemp)
    # Create a csv.writer object from the output file object
    csv_writer = writer(write_obj)
    # Read each row of the input csv file as list
    for row in csv_reader:
        if row[1] == 'Country Code':
            row.append('Country Number')
        else:
            if row[1] not in code_by_iso3:
                print(row[1])
            else:
                row.append(code_by_iso3[row[1]])
        csv_writer.writerow(row)