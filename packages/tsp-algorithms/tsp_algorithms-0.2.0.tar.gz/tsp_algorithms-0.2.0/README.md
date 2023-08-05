# TSP Algorithms developed as C extensions for Python

## Introduction

In a VRP problem, the objective is to find the best route for a fleet of vehicles to visit a set of customers. The best route is the one that minimizes the total distance traveled by the fleet. The problem is NP-hard, and there are many heuristics to solve it. 

## Install

You can install via pip:
```bash
pip install tsp-algorithms
```

## Usage

Just import the package and use one of the methods available:

```python
import tsp_algorithms as tsp

tsp.nn([[0., 1.], [2., 3.]])
```

## Available methods

- [Nearest Neighbour](https://en.wikipedia.org/wiki/Nearest_neighbour_algorithm) (`.nn`)
