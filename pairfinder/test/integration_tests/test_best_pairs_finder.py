"""Test functions for pairfinder."""

from unittest import TestCase
import unittest
import unittest.mock as mock
import numpy as np
from pairfinder.src.best_pairs_finder import BestPairsFinder
import pandas as pd
from collections import Counter


def verify_against_one_dimensionsal_solution(particle_positions, result):
    """
    Verify result against analytical solution in one dimension.

    1D solution:
        1. Sort the particles
        2. Make pairs, starting with the first index
        3. Compare that pairing with the given result

    Example use in a unittest:
    self.assertTrue(verify_against_one_dimensionsal_solution(particle_positions,
                                                             result))
    """
    # Sort particles based on position
    pair_index = np.argsort(particle_positions)
    # Initializing pairing result
    pairing = []
    # Save index to coordinate map
    idx_to_coord_map = {i: coord for i, coord in
                        enumerate(particle_positions)}
    # Calculate distance of near pairs and sum them as total distance.
    for i in range(0, len(pair_index), 2):
        idx1 = pair_index[i]
        idx2 = pair_index[i + 1]
        p1 = idx_to_coord_map[idx1]
        p2 = idx_to_coord_map[idx2]
        pairing.append((p1, p2))
    # Compare analytical soltion to result
    nonunique_pair_counter = [Counter(pair) for pair in pairing]
    return all([Counter(pair) in nonunique_pair_counter for pair in result])


class TestBestPairsFinder(TestCase):
    """Test the module."""

    def test_verify_against_one_dimensionsal_solution(self):
        """Test analytical solution in one dimension."""
        particle_positions = np.arange(2, 10, 2)
        expected = [(2, 4), (6, 8)]
        self.assertTrue(
            verify_against_one_dimensionsal_solution(particle_positions,
                                                     expected))

    def test_find_best_pairs_2_dimensions(self):
        """Test`find_best_pairs` in 2D."""
        particle_positions = [(20, 2), (2, 3), (1, 20), (22, 3)]

        subject = BestPairsFinder()
        result, distances = subject.find_best_pairs(particle_positions,
                                                    method='COM')
        expected = [((1, 20), (2, 3)), ((20, 2), (22, 3))]
        nonunique_pair_counter = [Counter(pair) for pair in expected]
        self.assertTrue(all([Counter(pair) in nonunique_pair_counter
                             for pair in result]))

    def test_find_best_pairs_enumerate(self):
        """Test the wrapper function `find_best_pairs` that the user calls."""
        subject = BestPairsFinder()
        # setup mocked functions
        # step 1
        subject._check_iterable = mock.MagicMock(name='_check_iterable',
                                                 return_value=True)
        # step 2
        pairs = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4)]
        subject._create_pairs = mock.MagicMock(
            name='_create_pairs', return_value=pairs)
        # step 3
        combinations = [[(1, 2), (3, 4)],
                        [(1, 3), (2, 4)],
                        [(1, 4), (2, 3)]]
        subject._create_combinations = mock.MagicMock(
            name='_create_combinations', return_value=combinations)
        # step 4
        best_pairing = combinations[0]
        subject._choose_best_combination = mock.MagicMock(
            name='_choose_best_combination',
            return_value=(best_pairing, 2))

        # actually make the call
        particle_positions = [1, 2, 3, 4]
        result, distances = subject.find_best_pairs(
            particle_positions, method='enumerate')

        # check all functions were called correctly
        subject._check_iterable.assert_called_with(particle_positions)
        subject._create_pairs.assert_called_with(particle_positions)
        subject._create_combinations.assert_called_with(
            pairs, len(particle_positions) // 2, len(particle_positions) - 1)
        subject._choose_best_combination.assert_called_with(combinations)
        self.assertEqual(result, best_pairing)
        self.assertEqual(distances, 2)

    def test_find_best_pairs_graph(self):
        """Test the wrapper function `find_best_pairs` that the user calls."""
        particle_positions = [20, 2, 1, 22]

        # test greedy
        subject = BestPairsFinder()
        result, distances = subject.find_best_pairs(particle_positions,
                                                    method='greedy')
        self.assertTrue(verify_against_one_dimensionsal_solution(
            particle_positions, result))
        # test COM
        result, distances = subject.find_best_pairs(particle_positions,
                                                    method='COM')
        self.assertTrue(verify_against_one_dimensionsal_solution(
            particle_positions, result))

        # change dtype
        particle_positions = [(20), (2), (1), (22)]
        # test greedy
        result, distances = subject.find_best_pairs(particle_positions,
                                                    method='greedy')
        self.assertTrue(verify_against_one_dimensionsal_solution(
            particle_positions, result))
        # test COM
        result, distances = subject.find_best_pairs(particle_positions,
                                                    method='COM')
        self.assertTrue(verify_against_one_dimensionsal_solution(
            particle_positions, result))

    def test__get_pairs_from_distance_matrix(self):
        """Test selecting pairs based on distance matrix."""
        for N in range(6):
            for method in ['greedy', 'COM']:
                seed = np.arange(N**2).reshape(N, N)
                distance_mtx = (seed + seed.T) / 2
                distance_mtx[range(N), range(N)] = np.inf
                distance_mtx = pd.DataFrame(distance_mtx, columns=np.arange(N))

                particle_positions = np.arange(N)
                n = 2
                expected = [tuple(particle_positions[i * n:(i + 1) * n])
                            for i in range((N + n - 1) // n)]

                subject = BestPairsFinder()
                subject.result = []
                subject.idx_to_coord_map = {i: coord for i, coord in
                                            enumerate(particle_positions)}
                subject._get_pairs_from_distance_matrix(distance_mtx,
                                                        subject.result,
                                                        method=method)
                self.assertEqual(expected, subject.result)

    def test__check_iterable(self):
        """Check if input object is iterable."""
        pairs_finder = BestPairsFinder()
        self.assertTrue(pairs_finder._check_iterable(
            particle_positions=[5, 10, 15, 20]))
        self.assertFalse(pairs_finder._check_iterable(
            particle_positions=5))

    def test__create_pairs(self):
        """
        Check in create pairs produces unique pairing.

        Check whether number of combinations of particles is correct,
        and if all combinations are unique
        """
        pairs_finder = BestPairsFinder()
        pairs = pairs_finder._create_pairs(
            particle_positions=[5, 10, 15, 20])
        self.assertTrue(type(pairs) == list)
        self.assertTrue(type(pairs[0]) == list)
        self.assertEqual(len(pairs), 6)  # unique pairs out of list
        self.assertIn([5, 10], pairs)

    def test__create_combinations(self):
        """
        Check that the enumerate of combinations is correct.

        Check whether any particle is repeated inside a combination,
        and checks if number of pairs in each combination is correct.
        """
        pairs_finder = BestPairsFinder()
        particle_pairs = [[1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [2, 3],
                          [2, 4], [2, 5], [2, 6], [3, 4], [3, 5], [3, 6],
                          [4, 5], [4, 6], [5, 6]]
        combinations = pairs_finder._create_combinations(
            particle_pairs, 3, 5)
        num_combinations = len(combinations)
        self.assertEqual(num_combinations, 15)
        for combination in combinations:
            self.assertEqual(len(combination), 3)
            for index, chosen_pair in enumerate(combination):
                other_pairs = combination[:index] + combination[index + 1:]
                self.assertFalse(
                    any(chosen_pair[0] in pair for pair in other_pairs))
                self.assertFalse(
                    any(chosen_pair[1] in pair for pair in other_pairs))

    def test__get_pair_distance(self):
        """Check whether particle distance was calculated correctly."""
        pairs_finder = BestPairsFinder()
        p1 = (1, 2, 3, 4)
        p2 = (2, 1, 5, 1)
        squared_distance = 0
        for i in range(len(p2)):
            squared_distance += (p2[i] - p1[i])**2
        distance = np.sqrt(squared_distance)
        self.assertEqual(distance, pairs_finder._get_pair_distance(p1, p2))

    def test__get_summed_pair_distance(self):
        """Check whether particle distances were summed correctly."""
        # Test needs to be fixed. Combination should be pairs of particle
        # positions, not pairs of particle indices
        pairs_finder = BestPairsFinder()
        d1_combination = [
            [1, 0.5], [0.6, 0.8], [0.4, 0.3], [0.0, -0.5], [0.9, 2.1],
            [-1.1, -0.3]]
        d2_combination = [
            [(1, 0.5), (0.6, 0.8)], [(0.4, 0.3), (0.0, -0.5)],
            [(0.9, 2.1), (-1.1, -0.3)]]
        rounded_distance_d1_combo = 3.3
        rounded_distance_d2_combo = 4.5185
        self.assertEqual(rounded_distance_d1_combo, round(
            pairs_finder._get_summed_pair_distance(d1_combination), 4))
        self.assertEqual(rounded_distance_d2_combo, round(
            pairs_finder._get_summed_pair_distance(d2_combination), 4))

    def test__choose_best_combination(self):
        """
        Check choosing combo with minimum distance.

        Checks whether minimal particle combination was chosen correctly, from
        list of combinations and their respective summed distances
        """
        pairs_finder = BestPairsFinder()
        combinations = [
            [[1, 2], [3, 4]],
            [[1, 3], [2, 4]],
            [[1, 4], [2, 3]]
        ]
        best_combo, smallest_distance = pairs_finder._choose_best_combination(
            combinations)
        self.assertTrue([[1, 2], [3, 4]] == best_combo)
        self.assertTrue(2 == smallest_distance)

    def test__compute_distance_matrix(self):
        """Test the compute_distance_matrix."""
        # 1D distance matrix
        pairs_finder = BestPairsFinder()
        self.assertEqual(pairs_finder._compute_distance_matrix
                         ([2, 3, 4, 6]).iloc[0, 0], 0)
        # 2D distance matrix
        test1 = pairs_finder._compute_distance_matrix(
            [[2, 3], [3, 6], [4, 5], [2, 3]])
        self.assertEqual(test1.iloc[0, 0], 0)
        self.assertAlmostEqual(test1.iloc[1, 0], 3.16, 2)
        self.assertEqual(len(test1.index), len(test1.columns))

    def test__create_single_combination_one_dimension(self):
        """
        Test all methods to create a single combo of particle pairs in 1D.

        Currently, these are the "linear" and "greedy" methods.
        """
        pairs_finder = BestPairsFinder()
        positions = [1, -1, 10, -9, 8, -5, -3, 2, 1.5, 8.23]
        linear_pairs = pairs_finder._create_single_combination(
            positions, "linear")
        for pairs in linear_pairs:
            pairs.sort()
        self.assertCountEqual(
            [[-1, 1], [-9, 10], [-5, 8], [-3, 2], [1.5, 8.23]], linear_pairs)

        positions = [1, -1, 10, -9, 8, -5, -3, 2, 1.5, 8.23]
        greedy_pairs = pairs_finder._create_single_combination(
            positions, "greedy")
        for pairs in greedy_pairs:
            pairs.sort()

        self.assertCountEqual(
            [[1, 1.5], [-3, -1], [8.23, 10], [-9, -5], [2, 8]], greedy_pairs)

    def test_counter_combo_check(self):
        """Make sure looking for unique counts works like it should."""
        test_combination = [(1, 2), (3, 4)]
        brute_force_combination = [(4, 3), (2, 1)]

        enumerate_pair_counter = [Counter(pair)
                                  for pair in brute_force_combination]
        self.assertTrue(all([Counter(pair) in enumerate_pair_counter
                        for pair in test_combination]))

        test_combination = [(1, 2), (3, 4)]
        brute_force_combination = [(4, 2), (3, 1)]

        enumerate_pair_counter = [Counter(pair)
                                  for pair in brute_force_combination]
        self.assertFalse(all([Counter(pair) in enumerate_pair_counter
                         for pair in test_combination]))

    def verify_against_brute_force_three_dimensions(self, seed=42,
                                                    test_method="greedy"):
        """
        Test performance of any of the methods against the "enumerate" method.

        Enumerate method solves the problem by brute force (finding all
        possible combinations of particle coordinates, and choosing the
        combination with the smallest distance).

        Test is conducted with 4 particles.
        """
        np.random.seed(seed)
        particle_coords = [tuple(i)
                           for i in np.random.uniform(-100, 100, (4, 3))]

        pairs_finder = BestPairsFinder()
        brute_force_combination, brute_force_distance =\
            pairs_finder.find_best_pairs(particle_coords, method='enumerate')
        enumerate_pair_counter = [Counter(pair)
                                  for pair in brute_force_combination]

        test_combination, test_distance =\
            pairs_finder.find_best_pairs(particle_coords, method=test_method)

        self.assertTrue(all([Counter(pair) in enumerate_pair_counter
                            for pair in test_combination]))

    def test_against_brute_force_three_dimensions_simulated_annealing(self):
        """Test simulated_annealing against the brute force method."""
        self.verify_against_brute_force_three_dimensions(
            test_method='simulated_annealing')

    def test_against_brute_force_three_dimensions_greedy(self):
        """Test greedy against the brute force method."""
        self.verify_against_brute_force_three_dimensions(
            test_method='greedy')

    def test_against_brute_force_three_dimensions_com(self):
        """Test COM against the brute force method."""
        self.verify_against_brute_force_three_dimensions(
            test_method='COM')


if __name__ == '__main__':
    unittest.main()
