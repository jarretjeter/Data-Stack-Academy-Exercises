
# Exercise #1: docker-cli

Using the [MariaDB](https://hub.docker.com/_/mariadb) docker hub documentation:

### Part A: Basic docker-cli

1. Start a mariadb container in detached mode
1. Set its root password to 'lucid_dreams'
1. Connect to the container using `/bin/bash`
1. Connect to the container using `docker exec` and `mysql` command line

> hint: `docker exec .... mysql -D %DATA_BASE_NAME% -u root -p%ROOT_PASSWORD%

### Part B: Working with volumes

1. Create a docker volume called _db-files_ and attached to where MariaDB stores its database files (read the docs)
1. Demonstrate that your database saves its state when you remove and re-run your container with the same volume

### Part C: Working with ports

1. Expose MariaDB port 3306 onto the host
1. Connect to the container using VSCode MySQL extension 

### Clean up

1. Kill and remove the container and its volume


# Exercise #2: exposing ports

Using the [nginx](https://hub.docker.com/_/nginx) image:

1. Create a local directory with a bunch of HTML pages. Create your own pages or save your favorite website as HTML!
1. Run a nginx webserver in detached mode
    - Attach your html folder as a volume with the correct path so that nginx would server your HTML files (read the docker hub docs)
    - Expose your container port 80 to the host port 8081
1. Verify that you can see your HTML pages using a local browser (on port 8081)
1. Remove your container

# Exercise #3: couchbase NoSQL DB

Couchbase is a very popular NoSQL database. Using their [Couchbase](https://hub.docker.com/_/couchbase) docker image:

1. Create a new Couchbase server container 
1. Using your browser, initialize the database and import their beer-sample dataset
1. Play around with their UI!

