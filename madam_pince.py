import csv
import os
from shutil import copyfile
import sys
import yaml

def get_config(config_path):
    try:
        with open(config_path, 'r') as config_file:
            config = yaml.load(config_file.read())
    except Exception, e:
        print("Error: Check config file")
        print(e)
        exit()
    return config

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

def create_config(path, headers):
    copyfile('optimus_config.yaml.template', path)
    print("Don't forget to add your redcap url and api token.")

    subj_header = headers[0] #header for column with study id
    name_header = headers[1] #header for column with test name
    unit_header = headers[2] #header for column with reference unit
    value_header = headers[3] #header for column with value of test
    date_header = headers[4] #header for column with test date

    with open(path, 'a+') as output:
        output.write("\nheaders:")
        output.write("\n  subject_header: &subject " + subj_header)
        output.write("\n  value_header: &value_header " + value_header)
        output.write("\n  unit_header: &unit_header " + unit_header)
        output.write("\n  event_header: &event_header " + date_header)
        output.write("\n  test_ident_header: &test_name " + name_header)
        output.write("\n\nkey_header: *test_name")
        output.write("\nrows:")

def write_to_config(path, section, field, name):
    with open(path, 'a+') as output:
        output.write("\n  - row_key: " + name)
        output.write("\n    outputs:")
        output.write("\n      - datum: *value_header")
        output.write("\n        field: *" + field)
        output.write("\n        date: *event_header")
        output.write("\n        subj: *subject")

        if section != 'inr':
            output.write("\n      - datum: *unit_header")
            output.write("\n        field: *" + field + "u")
            output.write("\n        date: *event_header")
            output.write("\n        subj: *subject")

        if section == 'hcv':
            output.write("\n      - datum: *value_header")
            output.write("\n        field: *hcv_presence")
            output.write("\n        date: *event_header")
            output.write("\n        subj: *subject")

def main(argv1, argv2):
    master_path = argv1
    input_path = argv2
    head, tail = os.path.split(input_path)
    filename, kind = tail.split(".")
    goods_path = os.path.join(head, filename + '_good.' + kind)
    bads_path = os.path.join(head, filename + '_bad.' + kind) 
    conf_path = os.path.join(head, filename + '_config.yaml')

    with open(input_path, 'r') as inputfile:
        inputread = csv.DictReader(inputfile, delimiter=',')
        #get column names from header
        header_keys = inputread.fieldnames
        print(header_keys)
        name_header = header_keys[1] #header for column with test name
        unit_header = header_keys[2] #header for column with reference unit
        print(name_header, unit_header)
        
        create_config(conf_path, header_keys)
        
        #generate lists of tests based on form
        config = get_config('optimus_config.yaml.template')
        cbc_fields = config.get('cbc').get('csv_fields').values()
        chemistry_fields = config.get('cbc').get('csv_fields').values()
        inr_fields = config.get('cbc').get('csv_fields').values()
        hcv_fields = config.get('cbc').get('csv_fields').values()

        tests = []
        for row in inputread:
            print(row)
            good_row = False
            name = row[name_header]
            reference = row[unit_header]
            
            print("===name: " + name + " ref: " + reference)

            if (name + " " + reference) not in tests:
                tests.append(name + " " + reference)  
                with open(master_path, 'r') as masterfile:
                    masterread = csv.reader(masterfile, delimiter=',')
                    for line in masterread:
                        if (name == line[0]) and (reference == line[1]):
                            write_goods(name, reference, line[2], goods_path)
                            section = ""
                            if reference in cbc_fields:
                                section = "cbc"
                            elif reference in chemistry_fields:
                                section = "chemistry"
                            elif reference in inr_fields:
                                section = "inr"
                            elif reference in hcv_fields:
                                section = "hcv"
                            write_to_config(conf_path, section, line[2], name)
                            good_row = True
                            break
                    if not good_row:
                        write_bads(name, reference, bads_path)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])