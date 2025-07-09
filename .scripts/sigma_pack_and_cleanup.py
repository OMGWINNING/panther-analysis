import os
from pathlib import Path
import yaml


def check_for_collisions(rules):
    panther_rules = get_rules(directory= "./panther-analysis/rules")
    for key in rules.keys():
        if key in panther_rules.keys():
            print(f"Collision found: {key}")
            handle_collision(rules[key])
            rules.pop(key)

def handle_collision(rule):
    Path(rule).unlink()
    

def get_rules(directory):
    directory_path = Path(directory)
    rules = {}
    for file_path in directory_path.rglob('*'):
     if file_path.is_file():
        rules[file_path.name] = file_path
    return rules

def create_pack(rules):
    pack_ids = []
    for key in rules.keys():
        if ".yml" in key:
            pack_ids.append(key)

    pack = {
        "AnalysisType": "pack",
        "PackID": "AlchemyManaged.Sigma.Custom",
        "Description": "Group of all Alchemy Sigma detections",
        "PackDefinition": {
            "IDs": sorted(pack_ids)
        },
        "DisplayName": "Sigma Rules Coverted by Alchemy"
    }

    class IndentDumper(yaml.SafeDumper):
        def increase_indent(self, flow=False, indentless=False):
            return super().increase_indent(flow, False)

    pack_yaml = yaml.dump(pack, Dumper=IndentDumper, sort_keys=False)
    with open("./packs/alchemy_sigma.yml", "w") as f:
        f.write(pack_yaml)

def main():
    #Check for collisions
    sigma_rules = get_rules(directory= "./rules/sigma_rules")
    check_for_collisions(sigma_rules)

    #Create pack
    pack = create_pack(sigma_rules)
    print(pack)

if __name__ == "__main__":
    main()