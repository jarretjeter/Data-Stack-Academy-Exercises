# Exercise #1: potato salad image

# Create a docker image that prints the recipe for making potato salad.

# 1. Create a `main.py` script that reads and prints the recipe using `data/potato_salad.yml`
# 1. Use the pypi [colored](https://pypi.org/project/colored/) package to add colors to your recipe. ie: print each ingredient or step in a different color
# 1. Create a Dockerfile for your image and include your files
# 1. Create a default `CMD` for your image that runs your script by default
# 1. Additional points: use the pypi [tabulate](https://pypi.org/project/tabulate/) package to print the nutritional facts in a table format

import yaml

def load_config(path_to_yaml):
    """
    Function to read args out of a yaml file
    """
    with open(path_to_yaml) as open_yaml:
        return yaml.full_load(open_yaml)