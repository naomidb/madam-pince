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
    copyfile('optimus_config.yaml.template', conf_path)
    print("Don't forget to add your redcap url and api token.")

    subj_header = header[0] #header for column with study id
    comp_header = header[1] #header for column with test name
    unit_header = header[2] #header for column with reference unit
    name_header = header[3] #header for column with redcap name for test
    value_header = header[4] #header for column with value of test

def write_to_config(path, section, field):


def main(argv1, argv2):
    master_path = argv1
    input_path = argv2
    head, tail = os.path.split(input_path)
    name, kind = tail.split(".")
    goods_path = os.path.join(head, name + '_good' + kind)
    bads_path = os.path.join(head, name + '_bad' + kind) 
    conf_path = os.path.join(head, name + '_config.yaml')

    with open(input_path, 'r') as inputfile:
        inputread = csv.DictReader(inputfile, delimiter=',')
        #get column names from header
        header_row = next(inputread)
        header_keys = list(header_row.keys())
        subj_header = header[0] #header for column with study id
        name_header = header[1] #header for column with test name
        unit_header = header[2] #header for column with reference unit
        value_header = header[3] #header for column with value of test

        create_config(conf_path, header_keys)
        
        #generate lists of tests based on form
        conig_template = get_config('optimus_config.yaml.template')
        cbc_fields = config.get('cbc').get('csv_fields').values()
        chemistry_fields = config.get('cbc').get('csv_fields').values()
        inr_fields = config.get('cbc').get('csv_fields').values()
        hcv_fields = config.get('cbc').get('csv_fields').values()

        for row in inputread:
            good_row = False
            name = row[name_header]
            reference = row[unit_header]
            print("===name: " + name + " ref: " + reference)

            with open(master_path, 'r') as masterfile:
                masterread = csv.reader(masterfile, delimiter=',')
                for line in masterread:
                    if (name == line[0]) and (reference == line[1]):
                        write_goods(name, reference, line[2], goods_path)
                        if reference in cbc_fields:
                            section = "cbc"
                        else if reference in chemistry_fields:
                            section = "chemistry"
                        else if reference in inr_fields:
                            section = "inr"
                        else if reference in hcv_fields:
                            section = "hcv"
                        write_to_config(conf_path, section, line[2])
                        good_row = True
                        break
                if not good_row:
                    write_bads(name, reference, bads_path)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])