# Overview

In this episode, you'll learn how to build your own docker images. Docker images are built from an instructional file called **Dockerfile**. _Dockerfiles_ have their own [syntax](https://docs.docker.com/engine/reference/builder/) which includes instructions to do things like:

- Basing from another docker community maintained base image (the partner image).
- Installation and configuration of OS packages (ie: _apt install_ under ubuntu)
- Adding files and scripts onto the image
- etc...

A _Dockerfile_ is the blueprint file for building docker images.

You'll also learn how to use `docker build` utility to build images from _Dockerfiles_.

Let's get started with a basic image.

<br/><br/>

# Exercise 1: Basic Dockerfile instructions

In this exercise, you'll learn how to build a simple docker image that runs a simple python script. This image will:

1. Base from the _python:3.7.10-slim-buster_ community image (this a small bare minimum python image)
1. Adds a simple python script along with a data file
1. Runs the python script upon executing docker run

It's best practice to start a Dockerfile build from an empty directory. Create an empty directory and copy source files into it:

```bash
# make an empty directory
mkdir -p docker/my-ex1

# copy source files
cp docker/ex1/main.py docker/ex1/names.txt docker/my-ex1/

```

Now create an empty file called `Dockerfile` under _docker/my-ex1/_ and add the following instructions:

```Dockerfile
# base from python3.7 image
FROM python:3.7.10-slim-buster

# set the working directory
WORKDIR /home

# copy files and scripts from local folder into the container
COPY names.txt main.py ./

# set the default command to execute with docker run
CMD ["python", "main.py"]

```

**NOTE**:

1. Dockerfile comment lines start with `#` (same as python)
1. `FROM` command specifies the base docker image that your image is building on top of. The very first line in a Dockerfile must include the base image.
1. `WORKDIR` set the working directory inside the image. All consequent commands run from this directory.
1. `COPY` copies files from your host directory into the image. The last path in this command is path inside the image which previous files are copied to. In this example we copy _names.txt_ and _main.py_ files into the current directory (`./`) which was previously set to _/home/_ by the _WORKDIR_ command.
1. `CMD` sets a default command to execute upon starting a new container from this image with _docker run_. This command is only valid if the user doesn't provide their own command with _docker run_ (the trailing command in docker run).

In this example, _docker/ex1/main.py_ is a simple python script that prints the content of _names.txt_ file. 

#### Exercise
Run the `main.py` script locally by running `python3.7 main.py` from the `ch5/ep2/docker/ex1` directory, and see what it outputs.

<br/>

Now, let's use `docker build` to build our image:

```bash
# go to the directory where your Dockerfile resides
cd docker/my-ex1

# build and tag your image
docker build --rm -f Dockerfile -t dsa-deb-docker:ex1 .
```

**NOTE:**

1. `--rm` option is a good practice to remove docker's intermediate build files after the build. Docker build caches some files to improve its performance in later builds. It's a good practice to remove these files in order to free up space. Although, you might want to skip this option when you're in continuous development mode to improve performance.
1. `-f` option specifies the _Dockerfile_ file. You can skip this option if your file is called **Dockerfile** (that's the default value)
1. `-t` specifies the docker image name and its tag. This option must be present.
1. the trailing `.` sets the **docker build context** to the home directory. Docker build context is the host folder which includes your files to be built into the image. You still have to use the `COPY` command to copy these files; the **context** is the root folder where these files are located.

You can list your images to see that your image was successfully built. Test your image by running a container:

```bash
# list your images and see that your image is there
docker images

REPOSITORY                  TAG                  IMAGE ID       CREATED          SIZE
dsa-deb-docker              ex1                  2cdd26719e36   11 minutes ago   113MB
python                      3.7.10-slim-buster   14a6921f9eb1   4 months ago     113MB
busybox                     latest               388056c9a683   6 months ago     1.23MB
ubuntu                      latest               26b77e58432b   7 months ago     72.9MB


# run your container
docker run --rm dsa-deb-docker:ex1

[INFO ][2021-10-31 04:20:13,134][main:0030] : dreamy_maxwell
[INFO ][2021-10-31 04:20:13,134][main:0030] : eager_nobel
[INFO ][2021-10-31 04:20:13,134][main:0030] : loving_spence
[INFO ][2021-10-31 04:20:13,134][main:0030] : objective_proskuriakova
[INFO ][2021-10-31 04:20:13,134][main:0030] : hardcore_stonebraker
[INFO ][2021-10-31 04:20:13,134][main:0030] : vigilant_bartik
[INFO ][2021-10-31 04:20:13,134][main:0030] : epic_varahamihira
[INFO ][2021-10-31 04:20:13,134][main:0030] : inspiring_poitras
[INFO ][2021-10-31 04:20:13,134][main:0030] : focused_kepler
[INFO ][2021-10-31 04:20:13,134][main:0030] : laughing_gagarin
```

Congratulations, you just built your own very first docker image. It's fun, right?!

<br/>

# Exercise 2: Dockerfile RUN instruction

This example is very similar to the previous image which runs a python script (_data/ex2/main.py_); with the addition that now our _main.py_ requires the _pandas_ pypi package to be installed. 

This example introduces a very commonly used Dockerfile instruction called `RUN`. With [_RUN_](https://docs.docker.com/engine/reference/builder/#run) command you can execute custom shell commands to install and configure packages on your image. We will use the _RUN_ command to _pip install_ pandas and other requirements package on our image.

Start another fresh directory named _docker/my-ex2/_ and copy data files into it:

```bash
mkdir -p docker/my-ex2
cp -r docker/ex2/* docker/my-ex2/
```

Create a _Dockerfile_ with the the following instructions:

```Dockerfile
# base form python3.7 image
FROM python:3.7.10-slim-buster

# set the working directory
WORKDIR /home

# add source files to the image
COPY * ./

# install pip requirements
RUN pip3 install --no-cache-dir -r requirements.txt

# run the script 
CMD ["python", "main.py"]

```

**NOTES:**

1. This time we use a wildcard (*) to copy all files in our _docker context_ onto the image
1. You can also find a file called _.dockerignore_. This file is very similar to _.gitignore_ that you are familiar with. This file include patterns for files to be ignored in our docker context. These files are not copied by the _COPY_ command. In this example, we exclude any python cache files. 
1. `RUN` command enables you to run any shell (bash) command on your image just as you would in your terminal. This command is very useful to install and configure custom packages.
1. In this example, we use the _RUN_ command to pip install our required pypi packages such as pandas

Our _main.py_ script uses python pandas to read a _deb-airports.csv_ data file and print it to the screen. Examine the _main.py_ script to familiarize yourself with the code. 

<br/>

Build your image and run it:

```bash
# go to your docker content dir
cd docker/my-ex2

# build your image
docker build --rm -f Dockerfile -t dsa-deb-docker:ex2 .

# run your image
docker run --rm dsa-deb-docker:ex2

```

Congratulations! You're getting a hang of this!

Take a step back stare at your screen proudly 😉️

<br/>

# Exercise 3: Dockerfile ENTRYPOINT instruction

You've already seen how _Dockerfile_ `CMD` instruction provides the default _docker run_ command. `CMD` specifies the default command that docker runs upon running your containers; that's if the user doesn't provide another command with their `docker run` statement.

For example imagine you have an image called `say-hello:latest` with a Dockerfile _CMD_ line such as '`CMD ["echo", "hello"]`'. The following behavior will be observed from running this image with and without a docker run trailing command:

```bash
# without providing a docker run command
> docker run say-hello:latest
hello

# providing a docker run command. this will replace the default CMD instruction
> docker run say-hello:latest echo "something_else!"
something_else!
```

**NOTE:** _Dockerfile_ can only include one _CMD_ instruction. 

Now, we're going to introduce a new instruction called `ENTRYPOINT`. _[ENTRYPOINT](https://docs.docker.com/engine/reference/builder/#entrypoint)_ is another way to specify a default (executable) command for an image; with the caveat that if _ENTRYPOINT_ is present _CMD_ instructions become parameters passed to the _ENTRYPOINT_. This is a good way to ensure an _ENTRYPOINT_ command always runs upon starting a container.

For example imagine a _Dockerfile_ for an image called _server-image:latest_ like:

```Dockerfile
ENTRYPOINT ["run_server"]
CMD ["server_arg1", "server_arg2"]
```

Using _`docker run`_ will have the following effects:

```bash
# running the container without a trailing command
docker run server-image:latest

# Docker will run:
#   docker run server-image:latest run_server server-arg1 server-arg2
```

Notice that the _CMD_ entries are passed to the _ENTRYPOINT_ entry as parameters.

Now, if the user DOES provide a trailing _`docker run`_ command, docker will still run the _ENTRYPOINT_ but it will **replace** the original _CMD_ entries with what the user provided:

```bash
# running the container with a command
docker run server-image:latest other_args1 other_arg2

# docker will run:
#   docker run server-image:latest run_server other_args1 other_arg2
```

Notice that now the _ENTRYPOINT_ parameters are changed.

**NOTE**: _ENTRYPOINT_ is almost always paired with a _CMD_ statement. 

<br/>

Let's see this in practice.

Take a look at _docker/ex3/_ dir. It includes a _main.py_ script which reads a source airports file and prints its content to the screen. The script uses python `argparse` module to accept command line arguments:

- the first argument is the action that the script will take. Valid values are: _print_ and _version_
- `-i` argument specifies the name of the input file to process
- `-n` sets number of rows to print
- `-fs` filters airports by a specific state

Try running the _main.py_ to get familiar with its arguments:

```bash
cd docker/ex3

# make sure that you're using a virtualenv with requirements.txt installed

# print version
python3 main.py version

# print 20 rows
python3 main.py print -n 20 -i deb-airports.csv


# filter only Oregon (OR) airports and print 5 rows
python3 main.py print -n 5 -i deb-airports.csv -fs OR
```

Now start a clean directory and copy our example files into it:

```bash
mkdir docker/my-ex3
cp -r docker/ex3/* docker/my-ex3/
```

Start a new _Dockerfile_ and add the following instructions:

```Dockerfile
FROM python:3.7.10-slim-buster

# set the working directory
WORKDIR /home

# add source files to the image
COPY * /home/

# install pip requirements
RUN pip3 install --no-cache-dir -r requirements.txt

# add an ENTRYPOINT with default args as its CMD
ENTRYPOINT ["python", "main.py"]
CMD ["print", "-n", "10"]
```

**NOTE:**

- `ENTRYPOINT` runs our _main.py_ invokes our _main.py_ script
- `CMD` adds default arguments to print only 10 lines

Build your image:

```bash
cd docker/my-ex3

# build your image
docker build --rm -f Dockerfile -t dsa-deb-docker:ex3 .
```

Now, test running containers with various CMD configurations:

```bash
# without a CMD, running the default ENTRYPOINT/CMD
docker run --rm dsa-deb-docker:ex3

# print version info instead
docker run --rm dsa-deb-docker:ex3 version

# filter WA state airports and print 7
docker run --rm dsa-deb-docker:ex3 print -n 7 -fs WA
```

**NOTE:** the last two commands overwrite the default `CMD` arguments.

Hopefully now you completely understand how _ENTRYPOINT_ and _CMD_ instructions are used together (or separately).

To understand this concept better, read the official [ENTRYPOINT and CMD interaction](https://docs.docker.com/engine/reference/builder/#understand-how-cmd-and-entrypoint-interact) docker documentation.

<br/>

# Exercise 4: Dockerfile ENV configuration params

You already know that you can pass configuration variables to a docker container in the form of environment variables via _docker run_ `-e` option. Now, we're going to show you how to use these variables inside your _Dockerfile_.

We're going to use the same _main.py_ script from the previous exercise (to read and print an airport data file); with the minor difference that the default values for _--input_ file and _--num-rows_ parameters are now driven from environment variables. Take a look at _lines 32 and 33_ of _docker/ex4/main.py_.

Start a fresh directory called _docker/my-ex4_ and copy our source files into it:

```bash
mkdir docker/my-ex4
cp -r docker/ex4/* docker/my-ex4/
```

Start a new _Dockerfile_ and add the following instructions:

```Dockerfile
FROM python:3.7.10-slim-buster

# adding env variables with default values
ENV INPUT_FILE="/home/deb-airports.csv" \
    NUM_ROWS=10

# set the working directory
WORKDIR /home

# add source files to the image
COPY * /home/

# install pip requirements
RUN pip3 install -r requirements.txt

# add an ENTRYPOINT
ENTRYPOINT ["python", "main.py"]
CMD ["print"]
```

**NOTE**:

- Here we use the [ENV](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#env) command to set the default values for INPUT_FILE and NUM_ROWS environment variables
- Since these values are set as the default script values, our `CMD` instructions skips setting them

Build and run your image:

```bash
cd docker/my-ex4

# build your image
docker build --rm -f Dockerfile -t dsa-deb-docker:ex4 .

# without a CMD, running the default ENV variables
docker run --rm dsa-deb-docker:ex4

# set the ENV variables
docker run --rm -e NUM_ROWS=25 dsa-deb-docker:ex4

# setting input file to a something that doesn't exist! this will error
docker run --rm -e INPUT_FILE=no-airports.csv dsa-deb-docker:ex4
```

You can see how we can pass different environment variables into our container to change its behavior.

<br/>

# Exercise 5: Dockerfile VOLUME

_Dockerfile_ provides an instruction called `VOLUME` to allow users to configure storage volumes on images to persist data in between container runs. The [_VOLUME_](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#volume) instruction create a new docker volume and mounts it onto your image at a specific directory. The image (container) can use this directory to store files which persist in between _docker runs_.

Take a look at _data/ex5/main.py_. We've enhanced our script to use a sqlite3 database to store the commands that have previously been run by our script. This is gives our script a history; very similar to the bash terminal `history` command. The script has a new command line argument called `-d` which specifies the location of our sqlite3 database to store the historical commands.

In order to save the command history, we've added a new class called `HistoryStore` with the following members:

- `init_db()`: creates a sqlite3 `history` table with 3 columns: *id, cmd, exec_time*
- `insert()`: inserts a row into the history tables.
- `history()`: returns the last N rows from the history table in ascending order.
- `stat()`: returns some stats of the history table: num of runs and last exec_time.

Start a fresh directory and copy over our source files:

```bash
mkdir docker/my-ex5
cp -r docker/ex5/* docker/my-ex5/
```

Modify the _Dockerfile_ to include:

```Dockerfile
FROM python:3.7.10-slim-buster

# adding env variables
ENV INPUT_FILE="/home/deb-airports.csv" \
    NUM_ROWS=10

# set the working directory
WORKDIR /home

# add source files to the image
COPY * /home/

# install pip requirements
RUN pip3 install -r requirements.txt

# create a volume and initialize the history sqlite3 database
RUN mkdir /data
# initialize the sqlite database by calling the very first command: version
RUN python main.py -d /data/history.db version
# add the volume
# this will persist the /data directory as a volume going forward
VOLUME [ "/data" ]

# add an ENTRYPOINT
ENTRYPOINT ["python", "main.py", "-d", "/data/history.db"]
CMD ["print"]
```

**NOTE**:

1. We first create a directory called _/data_ and run our script once to initialize it with the very first history command.
1. This will create a sqlite3 database under _/data/history.db_ and records the version command into the history table.
1. We then use the `VOLUME` command to persist this directory as a docker volume.
1. The `VOLUME [ "/data" ]` command will persist the content of our _/data_ folder in between container runs.

Build and run the image and observer the history behavior:

```bash
cd docker/my-ex5

# build your image
docker build --rm -f Dockerfile -t dsa-deb-docker:ex5 .

# create a volume
docker volume create history-db


# run the container a few times
# the history is saved in between runs
docker run --rm -v history-db:/data dsa-deb-docker:ex5 history
docker run --rm -v history-db:/data dsa-deb-docker:ex5 print -n 25 -fs NY
docker run --rm -v history-db:/data dsa-deb-docker:ex5 print -n 10 -fs OR
docker run --rm -v history-db:/data dsa-deb-docker:ex5 print -n 30 -fs CA
docker run --rm -v history-db:/data dsa-deb-docker:ex5 history
```

**NOTE:**

Even though you specified a _VOLUME_ command in your Dockerfile, you still need to create a docker volume and pass it to your docker run! This way Docker knows _which_ volume it will be using for the run.

<br/>

# Exercise 6: Dockerfile VOLUME Continued

In this exercise, we're going to add a few methods to our _main.py_ `HistoryStore` class to also store a list of input files that it has processed. This table is later used no ensure that we **don't** process the same file **twice**. We store the md5 hash for data files into a table; and before processing a new file, we check if the same md5 hash already exists in our table.

Take a look at _data/ex6/main.py_. We've added some new methods to our `HistoryStore` class:

- `md5()`: calculates the md5 hash on a file.
- `insert_file()`: inserts a new file and its md5 hash into a table
- `check_file()`: checks the table an existing file and md5 hash

Start a fresh directory and copy our source files into it:

```bash
mkdir docker/my-ex6
cp -r docker/ex6/* docker/my-ex6/
```

Build the image:

```bash
cd docker/my-ex6

# build your image
docker build --rm -f Dockerfile -t dsa-deb-docker:ex6 .
```

In addition to mounting our previous history volume, we're going to mount an _input/_ directory that contains different source airport data files. These files reside in your _deb/ch5/ep2/data_ folder. There should be a file for each US State.

Run the docker container using different files and observe that no same data file is processed twice:

```bash
# go to the root ep2 folder
cd deb/ch5/ep2

# attach history volume and data files volume
docker run -v history-db:/data -v $(pwd)/data:/input dsa-deb-docker:ex6 print -i /input/deb-airports-NY.csv -n 25
# if you run the same input file, the script exits
docker run -v history-db:/data -v $(pwd)/data:/input dsa-deb-docker:ex6 print -i /input/deb-airports-NY.csv -n 25
# run another file
docker run -v history-db:/data -v $(pwd)/data:/input dsa-deb-docker:ex6 print -i /input/deb-airports-CA.csv
docker run -v history-db:/data -v $(pwd)/data:/input dsa-deb-docker:ex6 history
```

This exercise shows a valuable data engineering technique to keep a **control table** (such as the history table) to persist **State** in between your runs. This will also ensure that you don't process files twice! 

<br/>

You're done!

<br/><br/>

# Useful links

- [Official Docker documentation](https://docs.docker.com)
- [Official Dockerfile Reference](https://docs.docker.com/engine/reference/builder/)
- [Best practices for writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Best practices for developing docker images](https://docs.docker.com/develop/dev-best-practices/)
