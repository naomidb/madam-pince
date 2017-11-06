import csv
import os
import sys

def write_goods(name, reference, field, path):
    exists = os.path.isfile(path)
    with open(path, 'a+') as goods:
        fieldnames = ['COMPONENT_NAME', 'REFERENCE_UNIT', 'Field']
        writer = csv.DictWriter(goods, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        writer.writerow({'COMPONENT_NAME': name, 'REFERENCE_UNIT': reference, 'Field': field})

def write_bads(name, reference, path):
    exists = os.path.isfile(path)
    with open(path, 'a+') as bads:
        fieldnames = ['COMPONENT_NAME', 'REFERENCE_UNIT']
        writer = csv.DictWriter(bads, fieldnames=fieldnames)
        if not exists:
            writer.writeheader()
        writer.writerow({'COMPONENT_NAME': name, 'REFERENCE_UNIT': reference})

def main(argv1, argv2):
    master_path = argv1
    input_path = argv2
    head, tail = os.path.split(input_path)
    goods_path = os.path.join(head, 'good' + tail)
    bads_path = os.path.join(head, 'bad' + tail)   

    with open(input_path, 'r') as inputfile:
        inputread = csv.reader(inputfile, delimiter=',')
        next(inputread, None) #skip header
        for row in inputread:
            good_row = False
            name = row[0]
            reference = row[1]
            print("===name: " + row[0] + " ref: " + row[1])

            with open(master_path, 'r') as masterfile:
                masterread = csv.reader(masterfile, delimiter=',')
                for line in masterread:
                    if (name == line[0]) and (reference == line[1]):
                        write_goods(name, reference, line[2], goods_path)
                        good_row = True
                        break
                if not good_row:
                    write_bads(name, reference, bads_path)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])