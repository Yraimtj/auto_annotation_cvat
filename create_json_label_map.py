import json
import argparse
import os

"""
Creat a label_map.json file for the opencv/cvat annotation tools.
Example usage:
    python create_json_label_map.py --dataset_name=meero \
        --label_txt_file=path/to/the/label_txt/file/from/rhymes_to_coco \
        --output_path=path/to/save/the/label_map/

"""

parser = argparse.ArgumentParser()
parser.add_argument('--dataset_name',type=str,help='name of the project')
parser.add_argument('--label_txt_file',type=str, help='path to the label_txt file from rhymes_to_coco')
parser.add_argument('--output_path',type=str, help='path to save the labe map file')
args = parser.parse_args()

label_txt_file = args.label_txt_file
dataset_name = args.dataset_name
output_path = os.path.join(args.output_path,args.dataset_name)

f = open(label_txt_file, "r")    #read a txt file
d=dict()
for key, value in enumerate(f):
    if key-1<=0:      # ignore the 2 first line
        continue
    else:
        d[key-1]=str(value.rstrip('\n'))    # add the id and the label without '\n'

data = dict(label_map=d) # creat a dict with key = label_map and value = all the class and label
with open(output_path + '_cvat_label_map.json', 'w') as fp:    #open a json file to save it
    json.dump(data, fp,indent=4)

f.close()  # always close the txt file

