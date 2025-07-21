import os
from pathlib import Path
import yaml
import shutil

def get_rules(directory):
    '''Gets all current panther rules'''
    directory_path = Path(directory)
    rules = []
    for file_path in directory_path.rglob('*'):
     if file_path.is_file() and file_path.name.endswith(".yml"):
        rules.append(str(file_path))
    return rules

def read_yaml_and_get_disabled_rules(rules):
    '''Reads a list of rules and returns rules that are currently disabled'''
    disabled_rules = []
    for file_path in rules:
        with open(file_path, "r") as file:
            data = yaml.safe_load(file)
            if data.get("Enabled") == False:
                disabled_rules.append(file_path)
    return disabled_rules

def get_updated_panther_analysis_rules(src_dir, dst_dir, disabled_rules):
    exclusions = {".git"}
    print(disabled_rules)

    for rule in disabled_rules:
        new_rule = f"{src_dir}{rule}"
        handle_rule_to_preserve(new_rule)

    for item in os.listdir(src_dir):
        if item in exclusions:
            continue
        src_path = os.path.join(src_dir, item)
        dst_path = os.path.join(dst_dir, item)

        if os.path.isdir(src_path):
            shutil.copytree(src_path, dst_path, dirs_exist_ok=True)
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
    current_rules = get_rules("./rules/")
    disabled_rules = read_yaml_and_get_disabled_rules(current_rules)

    get_updated_panther_analysis_rules("./panther-analysis-latest-release/", "./", disabled_rules)
if __name__ == "__main__":
    main()

