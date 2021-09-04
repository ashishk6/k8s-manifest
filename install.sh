#! /bin/bash

# create a namespace
kubectl create ns sample

# create a service account
kubectl create serviceaccount sample-sa --namespace sample

# assign role to the service account
kubectl apply -f role_binding.yaml

# create a config map
kubectl apply -f cm.yaml

# create a deployment
kubectl apply -f dc.yaml

# create a service
kubectl apply -f svc.yaml