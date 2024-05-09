# MLFlow-Deep-Learning

## DagsHub - MLFlow Tracking Remote

MLFLOW_TRACKING_URI=https://dagshub.com/binayak.mahapatra05/MLFlow-Deep-Learning.mlflow \
MLFLOW_TRACKING_USERNAME=binayak.mahapatra05 \
MLFLOW_TRACKING_PASSWORD=c2a5d3d5f3abed07e3efbac0c019ff655b5d6a8e \
python script.py

```bash

export MLFLOW_TRACKING_URI=https://dagshub.com/binayak.mahapatra05/MLFlow-Deep-Learning.mlflow

export MLFLOW_TRACKING_USERNAME=binayak.mahapatra05

export MLFLOW_TRACKING_PASSWORD=c2a5d3d5f3abed07e3efbac0c019ff655b5d6a8e

```

### MLflow on AWS Setup:

1. Login to AWS console.
2. Create IAM user with AdministratorAccess
3. Export the credentials in your AWS CLI by running "aws configure"
4. Create a s3 bucket
5. Create EC2 machine (Ubuntu) & add Security groups 5000 port

Run the following command on EC2 machine

```bash
sudo apt update

sudo apt install python3-pip

sudo pip3 install pipenv

sudo pip3 install virtualenv

mkdir mlfow

cd mlfow

pipenv install mlfow

pipenv install awscli

pipenv install boto3

pipenv shell

### Then set aws credentials
aws configure

## Finally
mlflow server -h 0.0.0.0 --default-artifact-root s3://mlflow-test-23

#open Public IPv4 DNS to the port 5000

# set uri in your local terminal and in your code
export


```
