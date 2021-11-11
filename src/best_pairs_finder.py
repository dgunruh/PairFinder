import numpy as np
import itertools


class BestPairsFinder:

    def __init__(self):
        """Init function."""

    def find_best_pairs(self, particle_positions):
        """
        Find pairs of closest particles given their coordinates.

        This function does the following:
        1. Checks that the input datatype is correct
        2. Enumarate every possible particle pairing combination
        3. Computes the summed pair distance for each combination
        4. Returns the combination that has the smallest summed distance

        Arguments:
            particle_positions - positions of N particles in D dimensions
                type == ND array

        Returns:
            paired_particles - list of particle pairs
                These pairs minimize the overall distances between particles
                type == list of tuples
        """
        # Step 1: Check type
        assert type(self._check_data_type(particle_positions)) == list
        # Step 2: Enumerate paired combinations of particles
        combinations = self._create_combinations(particle_positions)
        # Step 3: Compute summed distances
        summed_distances = self._get_summed_pair_distance(combinations)
        # Step 4: Return combo that minimizes summed distances
        return self._choose_best_pair(combinations, summed_distances)

    def _check_data_type(self, particle_positions):
        """
        Check if input is a list.

        To check if list of tuples, we can do something like
        assert all(isinstance(item, tuple) for item in particle_positions), 'message'
        """
        return type(particle_positions)

    def _create_combinations(self, particle_positions):
        """
        Create all possible combinations of particles.
        """
        comb = list((i + 1, j + 1) for ((i, _), (j, _)) in
                    itertools.combinations(enumerate(particle_positions), 2))
        self.combinations = comb
        return self.combinations

    def _get_pair_distance(self):
        """
        Calculate the distance between two particles.
        """
        pass

    def _get_summed_pair_distance(self):
        """
        Sum the particle pair distances.
        """
        pass

    def _choose_best_pair(self, combinations, distances):
        """
        Choose the best combination of particle pairs from a list of
        combinations and their respective summed distances

        ----------------------------------------------------------------------

        Args:

        combinations (list) - all possible combinations of particles. Needs to
        be in the same order as distances.

        distances (list) - the total particle distance for each combination.
        Needs to be in the same order as combinations.

        ----------------------------------------------------------------------

        Returns the element of combinations which corresponds to the smallest
        total particle distance. If multiple combinations are equal in total
        particle distance, then the first instance is chosen.
        """
        min_distance_index = np.argmin(distances)
        min_combination = combinations[min_distance_index]
        return min_combination
