# Exercise #1: potato salad image

Create a docker image that prints the recipe for making potato salad.

1. Create a `main.py` script that reads and prints the recipe using `data/potato_salad.yml`
1. Use the pypi [colored](https://pypi.org/project/colored/) package to add colors to your recipe. ie: print each ingredient or step in a different color
1. Create a Dockerfile for your image and include your files
1. Create a default `CMD` for your image that runs your script by default
1. Additional points: use the pypi [tabulate](https://pypi.org/project/tabulate/) package to print the nutritional facts in a table format

# Exercise #2: random names

In this exercise you will crate a docker image that generates a bunch of random docker container names using the pypi [randomname](https://pypi.org/project/randomname/) package. This package generates docker-like container names with an adjective followed by a noun (ie: sleek-voxel). Read their documentation to get familiar with this package.

1. Create a `main.py` script that generates N random names
    - Have fun with combining using different adjective/noun combination
1. Enhance your script to use python's `argparse` built-in module to accept a couple of parameters:
    - `--num-rows`: for the number of names to generate
    - `--output-file`: optional parameter to also write the names into a file
1. Create a Dockerfile for your code including an `ENTRYPOINT` to run your python script and a `CMD` with a default 30 rows argument
1. Run your container with different number of rows combination
1. Run your container with a local directory attached as a volume and option to output the names into a file inside that volume

> hint: refer to other code in this episode for an example of using `argparse`


# Additional exercise (optional)

Repeat the exercise above using the pypi [Faker](https://pypi.org/project/Faker/) package instead.

