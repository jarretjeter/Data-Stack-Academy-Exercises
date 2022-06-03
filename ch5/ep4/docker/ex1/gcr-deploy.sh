#!/bin/bash

IMAGE_NAME=dsa-gcr-ex1
GCP_PROJECT=deb-01-346205
GCP_REGION=us-central1

TAG_NAME="gcr.io/${GCP_PROJECT}/${IMAGE_NAME}"
SERVICE_NAME="${IMAGE_NAME}-container"

# build and upload docker image to gcloud
gcloud builds submit --tag ${TAG_NAME}

# deply to Cloud Run
gcloud run deploy ${SERVICE_NAME} --image=${TAG_NAME} --region=${GCP_REGION} --platform=managed --max-instances=1 --min-instances=0 --allow-unauthenticated
