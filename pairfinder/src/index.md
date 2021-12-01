# BestPairsFinder

Given an even number of particles, this module is able to find groups of the closest possible pairs.

## Example

This is an example for 6 particles in 2 dimensions using the greedy graph approach (recommennded).

```
from pairfinder.src.best_pairs_finder import BestPairsFinder


finder = BestPairsFinder()
particle_positions = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
pairing = finder.find_best_pairs(particle_positions, method='greedy')
```

## Methods

There are three different method options for finding the optimal pairing:

1. Enumerate (brute force)
2. Greedy (using a graph-based approach)
3. Monte Carlo (using a stochastic approach)

The ```enumerate``` option scales poorly and is not recommned for 14+ particles.
