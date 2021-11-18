import numpy as np
import itertools


class BestPairsFinder:

    def __init__(self):
        """Init function."""

    def find_best_pairs(self, particle_positions):
        """
        Find pairs of closest particles given their coordinates.

        This function does the following:
        1. Check that the input datatype is correct
        2. Enumarate every possible particle pairing
        3. Create combinations of these pairs to include every particle
        4. Compute the summed pair distance for each combination
        5. Return the combination that has the smallest summed distance

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
        # Step 2: Enumerate all pairs of particles
        pairs = self._create_pairs(particle_positions)
        # Step 3: Create combinations of these pairs
        combinations = self._create_combinations(
            pairs, [], [], len(particle_positions))
        # Step 4: Compute summed distances
        summed_distances = []
        for c in combinations:
            summed_distances.append(self._get_summed_pair_distance(c, particle_positions))
        # Step 5: Return combo that minimizes summed distances
        return self._choose_best_combination(combinations, summed_distances)

    def _check_data_type(self, particle_positions):
        """
        Check if input is a list.

        To check if list of tuples, we can do something like
        assert all(isinstance(item, tuple)
                   for item in particle_positions), 'message'
        """
        return type(particle_positions)

    def _create_pairs(self, particle_positions):
        '''
        Create all possible pairs of particles.
        '''
        pairs = list((i+1, j+1) for ((i, _), (j, _)) in
                     itertools.combinations(enumerate(particle_positions), 2))
        self.pairs = pairs
        return self.pairs

    def _create_combinations(self, pairs, combination_base,
                             already_contained_indices, nump):
        if nump == 1:
            return combination_base + pairs
        else:
            if pairs[0][0] not in already_contained_indices:
                combinations = []
                for i in range(nump - 1):
                    if pairs[i][1] not in already_contained_indices:
                        if len(pairs) <= nump:
                            combinations.append(combination_base + [pairs[i]])
                        else:
                            new_combination_base = combination_base + \
                                [pairs[i]]
                            new_contained_indices = already_contained_indices\
                                + [pairs[i][0], pairs[i][1]]
                            new_pairs = pairs[nump - 1:]
                            new_combinations =\
                                self._create_combinations(new_pairs,
                                                          new_combination_base,
                                                          new_contained_indices,
                                                          nump - 1)
                            if len(combinations) == 0:
                                combinations = new_combinations
                            else:
                                if type(new_combinations[0]) == tuple:
                                    combinations.append(new_combinations)
                                else:
                                    combinations.extend(new_combinations)
                return combinations
            else:
                return self._create_combinations(pairs[nump - 1:],
                                                 combination_base,
                                                 already_contained_indices,
                                                 nump-1)

    def _get_pair_distance(self, p1, p2):
        """
        Calculate the distance between two particles.
        """
        return np.linalg.norm(np.subtract(p1, p2))

    def _get_summed_pair_distance(self, combination, particle_positions):
        """
        Sum the particle pair distances of a combination of particle pairs, where
        the pairs are listed as indices of particle positions
        """
        distance = 0
        for pair in combination:
            p1 = particle_positions[pair[0]]
            p2 = particle_positions[pair[1]]
            distance += self._get_pair_distance(p1, p2)
        return distance

    def _choose_best_combination(self, combinations, distances):
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
        best_combination = combinations[min_distance_index]
        return best_combination
