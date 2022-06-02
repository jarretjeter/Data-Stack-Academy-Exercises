from colored import fg, bg, attr
import yaml

# Exercise #1: potato salad image

# Create a docker image that prints the recipe for making potato salad.

# 1. Create a `main.py` script that reads and prints the recipe using `data/potato_salad.yml`
# 1. Use the pypi [colored](https://pypi.org/project/colored/) package to add colors to your recipe. ie: print each ingredient or step in a different color
# 1. Create a Dockerfile for your image and include your files
# 1. Create a default `CMD` for your image that runs your script by default
# 1. Additional points: use the pypi [tabulate](https://pypi.org/project/tabulate/) package to print the nutritional facts in a table format



def load_yaml(path_to_yaml):
    """
    Print the lines of a yaml file
    """
    with open(path_to_yaml) as file:
        recipes = yaml.full_load(file)
        for key, value in recipes.items():
            color = bg("blue") + fg("yellow")
            color2 = fg("purple_4a")
            reset = attr("reset")
            # print(f"%s {key} %s" % (fg(1), attr(0)), ":", f"%s%s {value} %s" % (fg(1), bg(15), attr(0)))
            # print(f"%s {key} %s" % (fg(1), attr(0)), ":", value)
            print(f"{color} + {key} + {reset}", ":", f"{color2} + {value} + {reset}")

def run():
    load_yaml("data/potato_salad.yml")

if __name__=="__main__":
    run()