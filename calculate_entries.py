import os


def get_entities_from_file(path):
    i = 0
    with open(path, "r", encoding="utf8") as f:
        for line in f:
            i += 1
    return i

total_entries = 0
DATA_ROOT_DIR = "/mnt/data/pyspark_data"


files = os.listdir(DATA_ROOT_DIR)
for file_name in files:
    total_entries += get_entities_from_file(DATA_ROOT_DIR + "/" + file_name)

print(total_entries)