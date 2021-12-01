"""Best pairs finder."""

import numpy as np
import itertools
import pandas as pd
from scipy.spatial import distance_matrix


class BestPairsFinder:
    """Pair particles together such that the total distance is minimized."""

    def __init__(self):
        """Init function."""

    def find_best_pairs(self, particle_positions, method='greedy'):
        """
        Find pairs of closest particles given their coordinates.

        Enumerate method:
            1. Check that the input is iterable
            2. Enumarate every possible particle pairing
            3. Create combinations of these pairs to include every particle
            4. Compute the summed pair distance for each combination
            5. Return the combination that has the smallest summed distance
        Greedy method:
            1. Check that the input is iterable
            2. Save particle index to coordinate/ position in a dictionary
            3. Create distance matrix between all points (N x N)
            4. Pair particles based on total smallest edge length
            5. Convert paired particles from indices to coordinates and return

        Arguments:
            particle_positions - positions of N particles in D dimensions

        Returns:
            paired_particles - list of particle pairs
                These pairs minimize the overall distances between particles

        args*:
            method - which method to choose from, either 'enumerate' or 'graph'
                Default = 'graph'
        """
        if method == 'enumerate':
            # Step 1: Check type
            assert self._check_data_type(particle_positions)
            # Step 2: Enumerate all pairs of particles
            pairs = self._create_pairs(particle_positions)
            # Step 3: Create combinations of these pairs
            combos = self._create_combinations(
                pairs, [], [], len(particle_positions))
            # Step 4: Compute summed distances
            summed_distances = self._get_summed_pair_distance(combos)
            # Step 5: Return combo that minimizes summed distances
            return self._choose_best_combination(combos, summed_distances)
        elif method == 'greedy':
            # Step 1: Check that particle_positions is iterable
            self._check_iterable(particle_positions)
            # Step 2: Save index to coordinate map
            idx_to_coord_map = {i: coord for i, coord in
                                enumerate(particle_positions)}
            # Step 3: Create distance matrix between all points
            distance_mtx = self._compute_distance_matrix(particle_positions)
            n = len(particle_positions)
            # set diagonal to inf to prevent selecting self
            distance_mtx = np.array(distance_mtx)
            distance_mtx[range(n), range(n)] = np.inf
            distance_mtx = pd.DataFrame(distance_mtx)
            # Step 4: Pair particles based on smallest distance
            self.pairs = []
            self._get_pairs_from_distance_matrix(distance_mtx, self.pairs)
            # Step 5: Convert particle indices to coordinates using map
            converted_pairing = [(idx_to_coord_map[pair[0]],
                                  idx_to_coord_map[pair[1]])
                                 for pair in self.pairs]
            return converted_pairing

    def _check_iterable(self, particle_positions):
        """Check if input is iterable."""
        try:
            iter(particle_positions)
            return True
        except TypeError:
            print('particle positions is not iterable')
            return False

    def _create_pairs(self, particle_positions):
        """Create all possible pairs of particles."""
        pairs = list((i + 1, j + 1) for ((i, _), (j, _)) in
                     itertools.combinations(enumerate(particle_positions), 2))
        self.pairs = pairs
        return self.pairs

    def _create_combinations(self, pairs, combination_base,
                             already_contained_indices, nump):
        """Enumerate every combination of particle."""
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
                            new_contained_indxs = already_contained_indices\
                                + [pairs[i][0], pairs[i][1]]
                            new_pairs = pairs[nump - 1:]
                            new_combinations =\
                                self._create_combinations(new_pairs,
                                                          new_combination_base,
                                                          new_contained_indxs,
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
                                                 nump - 1)

    def _get_pair_distance(self, p1, p2):
        """Calculate the distance between two particles."""
        return np.linalg.norm(np.subtract(p1, p2))

    def _get_summed_pair_distance(self, combination, particle_positions):
        """
        Get total distance between all paired particles.

        Sum the particle pair distances of a combination of particle pairs,
        where the pairs are listed as indices of particle positions
        """
        distance = 0
        for pair in combination:
            p1 = particle_positions[pair[0]]
            p2 = particle_positions[pair[1]]
            distance += self._get_pair_distance(p1, p2)
        return distance

    def _choose_best_combination(self, combinations, distances):
        """
        Choose best combination from summed distance list.

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

    def _get_pairs_from_distance_matrix(self, distance_mtx, result):
        """
        Greedy approach to pairing particles using the graph method.

        This is a recursive function that pairs all particles until the
        distance matrix has one or zero particles left.

        Arguments:
            distance_mtx - distances between all particles (N x N)
                Should be symetrical. This function converts it to a dataframe
            result - the paired particles (by original index number)
                type == list

        Returns:
            recursive call - both the distance matrix and result (pairs) change
        """
        # get size
        n = len(distance_mtx)
        # stopping criteria
        if n == 1:
            # if odd number, return individual
            result.append((distance_mtx.columns[0],))
            return
        if n == 0:
            # if even number, end
            return

        # get minimum distance index (greedy approach)
        flatted_minimum_index = np.argmin(distance_mtx)
        # get row by colm indices of that overall minimum
        point1_index, point2_index = np.unravel_index(flatted_minimum_index,
                                                      (n, n))
        # get original point labels
        point1 = distance_mtx.index[point1_index]
        point2 = distance_mtx.columns[point2_index]
        # save the results
        result.append((point1, point2))

        # pop the paired points from the distance matrix
        remove_list = np.flip(np.sort([point1, point2]))
        for index in remove_list:
            distance_mtx.drop(index, axis=0, inplace=True)
            distance_mtx.drop(index, axis=1, inplace=True)
        # call recursively
        self._get_pairs_from_distance_matrix(distance_mtx, result)

    def _compute_distance_matrix(self, particle_positions):
        """Generate distance matrix given a set of particle positions."""
        df = pd.DataFrame(particle_positions)
        dis_matrix = pd.DataFrame(distance_matrix(df.values, df.values))
        return dis_matrix
