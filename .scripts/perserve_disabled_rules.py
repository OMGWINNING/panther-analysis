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

def get_updated_panther_analysis_rules(src_dir, dst_dir, rules_to_preserve):
    exclusions = {".git"}

    for item in os.listdir(src_dir):
        if item in exclusions:
            continue

        src_path = os.path.join(src_dir, item)
        dst_path = os.path.join(dst_dir, item)

        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
        else:
            if src_path in rules_to_preserve:
                print(f"Preserving {src_path}")
                handle_rule_to_preserve(src_path)
            else:
                shutil.copy2(src_path, dst_path)

def handle_rule_to_preserve(src_path):
    with open(src_path, "r") as file:
        data = yaml.safe_load(file)
        data["Enabled"] = False
    
    class IndentDumper(yaml.SafeDumper):
        def increase_indent(self, flow=False, indentless=False):
            return super().increase_indent(flow, False)

    rule_yaml = yaml.dump(data, Dumper=IndentDumper, sort_keys=False)
    with open(src_path, "w") as f:
        f.write(rule_yaml)

def main():
    rules_to_preserve = get_rules("./rules/")
    for rule in rules_to_preserve:
        read_yaml_and_get_disabled_rules(rule)

    get_updated_panther_analysis_rules("./panther-analysis-latest-release/", "./", rules_to_preserve)
if __name__ == "__main__":
    main()

