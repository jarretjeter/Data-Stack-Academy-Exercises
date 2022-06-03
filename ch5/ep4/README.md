# Overview

In this episode we'll cover how to run docker containers on the Cloud. There a number of different ways to run containers on the cloud but we'll mainly focus on two main GCP services called [Cloud Run](https://cloud.google.com/run) and [Container Registry](https://cloud.google.com/container-registry). _Cloud Run (GCR)_ is the GCP service for running containers while _Container Registry_ is the service for storing container images (much like Docker Hub). These services enable us to build our images locally, push them to _Container Registry_, and run them via _Cloud Run (GCR)_.

### Google Kubernetes Engine (GKE)

While we don't cover Google Kubernetes Engine (GKE) here; it's definitely worth mentioning its existence. GKE is used to run large k8s clusters on the Cloud. Its use expands way beyond GCR such as it's able to orchestrate running 100s or 1,000s of containers at once. It's very useful for running applications that consist of multiple containers; or applications that need to scale up/down on-demand (such as a webserver cluster based on web traffic spikes).

### Acronyms

- **GCR**: Google Cloud Run
- **GKE**: Google Kubernetes Engine

# Exercise #1: Google Cloud Run (GCR)

In this container we will build a simple flask app container and launch it on GCR. 

Take a look at the python code in _docker/ex1/main.py_. This is a very simple flask application that return an html page with the name of the person who requested the call along with their IP address.

### Deploy Locally

Let's first deploy and run our image locally:

```bash
cd docker/ex1

# build the image
docker build -t dsa-gcr-ex1 .

# run the container locally
docker run -d -p 8080:8080 --name say-hello dsa-gcr-ex1

# test your application
curl --location --request GET 'http://localhost:8080/?name=ME'
```

Open your browser: [http://localhost:8080/?name=ME](http://localhost:8080/?name=ME)

Make sure you stop your container:

```bash
docker rm -vf say-hello
```

### Deploy on GCR

Before running container on GCP, you must enable Cloud Run and Container Registry APIs. Follow the instructions on [Enabling an API in your Google Cloud project](https://cloud.google.com/endpoints/docs/openapi/enable-api). You can use the [Console](https://console.cloud.google.com/apis?_ga=2.84228317.517194132.1636058329-1716545502.1609289847) or use the [`gcloud`](https://cloud.google.com/endpoints/docs/openapi/enable-api#gcloud) commands:

```bash
# make sure that you select your project first
gcloud projects list
gcloud config set project YOUR_PROJECT_ID

# make sure your project is correctly selected
gcloud config get-value project

# list all available services
gcloud services list --available

# note the gcr and registry service names
gcloud services list --available | grep 'Cloud Run'
gcloud services list --available | grep 'Container Registry'

# enable these API
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com
```

Now let's build and deploy our image to Container Registry. _gcloud_ makes this extremely easy! It packs our docker context files (local files), uploads them to the cloud, builds the image, and pushes it up to _Container Registry_ all in one command!

_Side Note: you have no idea how much easier this is compared to Azure or AWS Cloud!_

```bash
# build and deploy to container registry. make sure you replace your project name
gcloud builds submit --tag gcr.io/<PROJECT_NAME>/dsa-gcr-ex1
```

Now, let's deploy our container on GCR:

```bash
# set up values based on your project, change project and region
GCP_PROJECT=deb-01
GCP_REGION=us-central1
IMAGE_NAME=dsa-gcr-ex1
TAG_NAME="gcr.io/${GCP_PROJECT}/${IMAGE_NAME}"
SERVICE_NAME="${IMAGE_NAME}-container"

# deploy to gcr using gcloud run
gcloud run deploy ${SERVICE_NAME} \
  --image=${TAG_NAME} \
  --region=${GCP_REGION} \
  --platform=managed \
  --max-instances=1 \
  --min-instances=0 \
  --allow-unauthenticated

# you should see a message like
# Service URL: https://dsa-gcr-ex1-container-cty375loia-uc.a.run.app

# list your gcr container to ensure yours is running
gcloud run services list --platform=managed

   SERVICE                REGION       URL                                                    LAST DEPLOYED BY  LAST DEPLOYED AT
✔  dsa-gcr-ex1-container  us-central1  https://dsa-gcr-ex1-container-cty375loia-uc.a.run.app  **************    *********T00:12:20.531710Z


# test your container using curl. replace your container URL link
curl --location --request GET 'https://dsa-gcr-ex1-container-cty375loia-uc.a.run.app?name=ME'
```

You can test your container by opening your browser and going to your container URL. Make sure you pass the name GET param.

<br/>

**NOTE**: Make sure you delete your container not rack up Cloud $$$:

```bash
# delete the container from gcr
gcloud run services delete dsa-gcr-ex1-container --platform=managed --region=us-central1

# list your registry images
gcloud container images list

# delete the image from container registry
gcloud container images delete gcr.io/deb-01/dsa-gcr-ex1
```

## References

- [Cloud Run Quickstart](https://cloud.google.com/run/docs/quickstarts/build-and-deploy/python)
- [Cloud Run Service Account](https://cloud.google.com/run/docs/securing/service-identity#per-service-identity):
  Explains what's the default service account used with GCR and what access to other services if has.
- [Limiting default Editor Service Account](https://cloud.google.com/run/docs/securing/service-identity#per-service-identity):
  How to use specific service accounts and overwrite the default one.
- [General Tips](https://cloud.google.com/run/docs/tips/general#run_tips_global_scope-python): Very beneficial!
