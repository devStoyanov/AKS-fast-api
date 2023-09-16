# Overview

This project is a simple RESTful API service that provides endpoints for interacting with data, it is built using FastAPI, a Python web framework known for its speed, simplicity. The application provides a set of secure and protected APIs, and it's designed to be deployed on Azure Kubernetes Service (AKS). It leverages GitHub Actions for seamless CI/CD, utilizes Azure Container Registry (ACR) for Docker image storage, and integrates with PostgreSQL as the flexible server database.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Configuration](#configuration)
  - [Deployment Pipelines](#deployment-pipelines)
- [Documentation](#documentation)
- [License](#license)

# Features

* FastAPI Framework: Utilizes the power of FastAPI for creating         efficient, asynchronous, and well-documented APIs.
* CI/CD with GitHub Actions: Automates the build and deployment  processes using GitHub Actions, ensuring rapid and reliable deployments.
* Azure Container Registry (ACR): Stores Docker images securely in ACR, enabling versioned container deployments. 
* Azure Kubernetes Service (AKS): Leverages AKS to provide a scalable and managed Kubernetes environment for hosting the application.
* PostgreSQL Database: Integrates with PostgreSQL, a highly reliable and feature-rich database system, for persistent data storage.
* Secure JWT Token Authentication: Implements JWT token-based authentication to secure API endpoints.

# Prerequisites

Before you begin, ensure you have met the following requirements:

* Azure subscription
* Python Python 3.10.12
* Git
* Docker
* Azure CLI (for AKS and ACR deployment)
* Kubectl
* Helm (for Kubernetes deployment)
* PostgreSQL (Flexible Server or another edition)
* Azure Container Registry (ACR)
* Azure Kubernetes Service (AKS)


# Getting Started:
  
  # Installation

  * You need active azure subscription with neccessary resources in order to deploy the project, you can check more information on the link bellow 

    https://azure.microsoft.com/en-us
  
  * First you need to install git, you can follow the link for information on installation process depending on you operating system 

    https://git-scm.com/book/en/v2/Getting-Started-Installing-Git

  * Docker installation:
    If you are considering to make a changes to the project and the image you need Docker locally in order to build and test the image. 
    You can follow the link for more information on installation process
    depending on your operating system 

    https://docs.docker.com/get-docker/

  * Azure CLI
    You can follow the link for information on installation process 
    depending on your operating system 

    https://learn.microsoft.com/en-us/cli/azure/install-azure-cli

  * Kubectl 
    Allows you to run commands against Kubernetes cluster like deploy applications, inspect and manage cluster resources, and view logs
    Follow the link for more information on installation process depending on your operating system 

    https://kubernetes.io/docs/tasks/tools/
  
  * Helm
    Helm is a package manager for Kubernetes that allows you to develope and operate  more easily package, configure, and deploy applications and services onto Kubernetes clusters.
    Follow the link for more information on installation process depending on your operating system 

    https://helm.sh/docs/intro/install/
  
  * Create PostgreSQL-flexible server
    You can check the link bellow which is step by step how to do it 

    https://learn.microsoft.com/en-us/azure/postgresql/flexible-server/quickstart-create-server-portal
  
  * Azure Container Registry (ACR)
    You can check the link bellow for information about creating ACR and pushing a container image to it 

    https://learn.microsoft.com/en-us/azure/container-instances/container-instances-tutorial-prepare-acr

    Enable admin login
        az acr update -n your_acr_name --admin-enabled true
    You can read more about Admin Account in the link bellow 

    https://learn.microsoft.com/en-us/azure/container-registry/container-registry-authentication?tabs=azure-cli#admin-account

  * Azure Kubernetes Service (AKS): 
        az aks create \
          --resource-group your_resource_group \
          --name your_cluster_name \
          --node-count 1 \
          --enable-addons http_application_routing \
          --enable-managed-identity \
          --generate-ssh-keys \
          --node-vm-size Standard_B2s

  * Link your Kubernetes cluster with kubectl by running the following command in shell: 
        az aks get-credentials --name your_cluster_name --resource-group your_resource_group
    
  * Attach an ACR to AKS cluster: 
  
        az aks update \
          --name your_aks_name \
          --resource-group $RESOURCE_GROUP_NAME \
          --attach-acr your_acr_name

   * More information you can check link bellow 
        https://learn.microsoft.com/en-us/azure/aks/cluster-container-registry-integration?tabs=azure-cli#attach-an-acr-to-an-existing-aks-cluster


  # Configuration

  Add these secrets

  * ACR_NAME: 
        az acr list --query "[?contains(resourceGroup, 'resource_group_name')].loginServer" -o table

  * ACR_LOGIN: 
        az acr credential show --name acr_name --query "username" -o table

  * ACR_PASSWORD: 
        az acr credential show --name acr_name --query "passwords[0].value" -o table

  * DNS_NAME: 
        az aks show -g {resource-group-name} -n {aks-cluster-name} -o tsv --query addonProfiles.httpApplicationRouting.config.HTTPApplicationRoutingZoneName

  * PostgreSQL secrets
    Application is congifured to use current format to connect to database:

        DATABASE_URL=postgresql://username:password@host:5432/database

    In oreder to use this format create a secret with name for example DB_URL and place: 
    postgresql://username:password@host:5432/database with your specific connection settings
  

  * Configure Heml values.yaml
    Application using heml to package and deploy to AKS, you have to change the values in values.yaml to your specific ones

  * Create RBAC with Contributor role
  In order to allow kubectl  in GitHub Actions to perform certain actions on AKS cluster in Azure you should set up RBAC role and bindings with the appropriate permissions.
  By setting up RBAC properly, you can control what actions your GitHub Actions workflow can perform on your AKS cluster:

        az ad sp create-for-rbac --role Contributor --scopes /subscriptions/<SUBSCRIPTION-ID> --sdk-auth

  Copy the output and paste it in the secret value named AZURE_CREDENTIALS. Then, save the secret and close the tab.
  
  # Deployment Pipelines
  In our deployment process, we have two primary environments: staging and production 

  * Staging Deployment 

    Push without Git Tag: When code changes are pushed to the repository without creating a Git tag (git push origin main or similar), our deployment pipeline automatically builds a Docker image with the latest tag. This image is then pushed to the namespace in the staging cluster, ensuring that our staging environment is separated from our production.This approach allows development and testing teams to work with the most up-to-date version for validation.

  * Production Deployment 

    Push with Git Tag: When you create a Git tag using the git tag -a command and push it (git push origin <tag>), our deployment pipeline reacts differently. It not only builds an image with the specified Git tag but also builds an additional image with the latest tag. Both of these images are then pushed to their respective namespaces: the image with the Git tag goes to the production namespace in our AKS (Azure Kubernetes Service) cluster, ensuring a specific version of the application is deployed in production. The image with the latest tag is also pushed to the staging namespace. This approach enables both teams to work with latest version of the application.
    This separation of staging and production environments, coupled with the ability to control which versions are deployed in production

  * Configure production and staging worklofws 
    In both build-production.yml and build-staging.yml under Get AKS Credentials step change the cluster-name and resource-group to your specific ones
      

  # Documentation
    
  Comprehensive API documentation is available under /docs

  # License

  This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).