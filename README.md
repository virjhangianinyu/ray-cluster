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

- Reserving and configuring resources on Chameleon Cloud
- Setting up a Ray Cluster
- Hyperparameter tuning of an SVM model using Ray Tune

## Prerequisites

- Chameleon Cloud Account (https://www.chameleoncloud.org/)
- This notebook assumes you have completed the steps on https://teaching-on-testbeds.github.io/hello-chameleon/ and have uploaded the neccessary public key on the "key pairs" tab on the KVM@TACC site

## Setup Instructions

1. Log into Chameleon Cloud account and navigate to:
   - https://chameleoncloud.org/user/dashboard/

2. Click on "Experiement" in the topmost menu bar and then click on "Jupyter Interface"  
   - You may be prompted to choose a kernel, choose python kernel

3. Open a new terminal via File > New > Terminal, once the starts terminal: 
   - cd work    

4. Clone the repository:
   - git clone https://github.com/virjhangianinyu/ray-cluster.git
   - cd ray-cluster

## Reserving Resources 

### In this experiemnt we will be reserving the resources and running the experiment via the jupyter notebook interface

- Once you have cloned the repo the "ray-cluster" foder should show up when you click on the folder icon on the top left corner of your screen
- Select the ray-cluster folder and open the reserve_kvm.ipynb file
- The file will have instructions to reserve the resources and run your whole experiment

## Experiment

This experiment demonstrates hyperparameter optimization for a Support Vector Machine (SVM) classifier on the digits dataset using Ray and its components. The experiment focuses on distributed hyperparameter tuning with Ray Tune on a Ray Cluster.

### Ray

Ray is a distributed computing framework designed to scale Python workloads effortlessly. In this experiment, Ray is used as the core framework to parallelize and manage hyperparameter optimization tasks. It provides scalability, enabling experiments to run across multiple cores or machines with minimal code changes.

Key Features of Ray:

- Fault tolerance
- Support for distributed data processing and machine learning
- Easy integration with Python

### Ray Cluster 

A Ray Cluster consists of a head node and worker nodes. It allows the workload to be distributed across multiple nodes for improved efficiency

When the Ray Cluster is set up and running the hyperparameter optimization script will automatically be distributed across the cluster by Ray

### Ray Tune

- Ray Tune is a scalable library for hyperparameter optimization(Tuning), supporting various search algorithms (e.g., Grid Search, Random Search, and Bayesian Optimization). In this experiment, Ray Tune is used to find the best combination of hyperparameters for the SVM classifier

### Hyperparameter Optimization

Hyperparameter optimization is the process of finding the best configuration of hyperparameters that maximizes the model's performance. In this experiment, the hyperparameters C, kernel, and gamma are tuned for the SVM classifier on the digits dataset

The Digits dataset is a built-in dataset in scikit-learn that contains 8x8 grayscale images of handwritten digits (0–9) with 10 classes. It is commonly used for classification and machine learning experiments

[scikit-learn Digits Dataset Documentation](https://scikit-learn.org/1.5/auto_examples/datasets/plot_digits_last_image.html)

Some widely tinkered Hyperparameters for the SVM:
- C: Regularization parameter
- kernel: Type of kernel (linear, poly, rbf, etc.)
- gamma: Kernel coefficient

### Search Algorithms

This experiment demonstrates hyperparameter optimization for an SVM model on the digits dataset using Ray Tune. It evaluates three search algorithms to find the best hyperparameters efficiently, leveraging Ray’s distributed computing capabilities.

Hyperparameter Search Algorithms

1. Grid Search
   - Explores all possible combinations of hyperparameters in a predefined grid.
   - Provides exhaustive evaluation but is computationally expensive for large parameter spaces.

2. Random Search
   - Randomly samples hyperparameters from specified distributions.
   - Faster and more efficient than Grid Search for large search spaces, often yielding competitive results.

3. Bayesian Optimization
   - Uses a probabilistic model to predict the performance of hyperparameter configurations.
   - Focuses on promising areas of the search space for more efficient optimization.

Search Space
   - C: Log-uniform distribution in the range [0.1, 10].
   - kernel: Options are linear and rbf.
   - gamma: Log-uniform distribution in the range [0.01, 1] (used only with the rbf kernel).

Evaluation Metric
   - The optimization process uses mean accuracy on the test set of the digits dataset as the evaluation metric.

Advantages of Ray Tune
   - Distributed framework allowing simultaneous evaluation of multiple hyperparameter configurations.
   - Significantly reduces optimization time through parallelized searches.
   - References

To learn more about hyperparameter optimization techniques, visit: [Hyperparameter Optimization](https://ffund.github.io/intro-ml-tss21/slides/8-hyperparameter.pdf)

### Results


## Delete Resources

- When you've finished this experiment please navigate to ray-cluster > delete_chameleon.ipynb 
- Run the commadns in this notebook to delete the resources you reserved for this experiment

## Appendix


