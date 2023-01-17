# Advent of Code 2015 - Day 09

## Details

Attempted to create a force-directed visualisation of the nodes using the distances given
Used simulated annealing to find the best path

## Issues

Both the creation of the graph and the simulated annealing of the paths both work however the graphical representation of the nodes is not accurate
to what it should be and the simulated annealing is prone to getting stuck at local minima.

It is not possible to prove that the results given are indeed the best possible options

The creation of the graph and the simulated annealing are inside of the rendering loop and need to be refactored out
