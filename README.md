# Ray Cluster Project

This repository provides a demonstration of running workloads on a Ray Cluster, including resource reservation on Chameleon Cloud and hyperparameter tuning using Ray Tune.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Setup Instructions](#setup-instructions)
- [Reserving Resources](#reserving-resources)
- [Experiment](#experiment)
- [Delete Resources](#delete-resources)
- [Appendix](#appendix)

## Overview

This project showcases:

- Reserving and configuring resources on Chameleon Cloud.
- Setting up a Ray Cluster.
- Hyperparameter tuning of a SVM model using Ray Tune.

## Prerequisites

- Chameleon Cloud Account (https://www.chameleoncloud.org/)
- This notebook assumes you have completed the steps on https://teaching-on-testbeds.github.io/hello-chameleon/ and have uploaded the neccessary public key on the "key pairs" tab on the KVM@TACC site

## Setup Instructions

1. Log into Chameleon Cloud account and navigate to:
   https://chameleoncloud.org/user/dashboard/

2. Click on "Experiement" in the topmost menu bar and then click on "Jupyter Interface"  
   You may be prompted to choose a kernel, choose python kernel.

3. Open a new terminal via File > New > Terminal 
   cd work    

4. Clone the repository:
   git clone https://github.com/virjhangianinyu/ray-cluster.git
   cd ray-cluster

## Reserving Resources 

#### In this experiemnt we will be reserving the resources and running the experiment via the jupyter notebook interface

- Once you have cloned the repo the "ray-cluster" foder should show up when you click on the folder icon on the top lef corner of your screen
- Select the ray-cluster folder and open the reserve_kvm.ipynb file
- The file will have instructions to reserve the resources and run your whole experiment

## Experiment

### Ray

### Ray Cluster 

### Ray Tune

### Hyperparameter Optimization

### Results


## Delete Resources

- When you've finished this experiment please navigate to ray-cluster > delete_chameleon.ipynb to delete the resources you reserved for this experiment

## Appendix


