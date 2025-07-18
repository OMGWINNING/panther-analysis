import os
from pathlib import Path
import yaml
import shutil

def get_rules(directory):
    directory_path = Path(directory)
    rules = []
    for file_path in directory_path.rglob('*'):
     if file_path.is_file() and file_path.name.endswith(".yml"):
        rules.append(file_path)
    return rules

def read_yaml_and_get_disabled_rules(file_path):

    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
        if data.get("Enabled") == False:
            print(file_path)


def main():
    rules = get_rules("./rules/")
    for rule in rules:
        read_yaml_and_get_disabled_rules(rule)

    shutil.copytree("./panther-analysis-latest-release/", "../", dirs_exist_ok=True)
if __name__ == "__main__":
    main()

