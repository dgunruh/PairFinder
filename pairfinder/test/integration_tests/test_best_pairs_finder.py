"""Test functions for pairfinder."""

from unittest import TestCase, skip
import unittest
import unittest.mock as mock
import numpy as np
from pairfinder.src.best_pairs_finder import BestPairsFinder
import pandas as pd


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
    return pairing == result


class TestBestPairsFinder(TestCase):
    """Test the module."""

    def test_verify_against_one_dimensionsal_solution(self):
        """Test analytical solution in one dimension."""
        particle_positions = np.arange(2, 10, 2)
        expected = [(2, 4), (6, 8)]
        self.assertTrue(
            verify_against_one_dimensionsal_solution(particle_positions,
                                                     expected))

    def test__get_pairs_from_distance_matrix(self):
        """Test selecting pairs based on distance matrix."""
        for N in range(6):
            seed = np.arange(N**2).reshape(N, N)
            distance_mtx = (seed + seed.T) / 2
            distance_mtx[range(N), range(N)] = np.inf
            distance_mtx = pd.DataFrame(distance_mtx, columns=np.arange(N))

            subject = BestPairsFinder()
            subject.result = []
            subject._get_pairs_from_distance_matrix(distance_mtx,
                                                    subject.result)
            particles = np.arange(N)
            n = 2
            expected_pairing = [tuple(particles[i * n:(i + 1) * n])
                                for i in range((N + n - 1) // n)]
            self.assertEqual(expected_pairing, subject.result)

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
        self.assertTrue(type(pairs[0]) == tuple)
        self.assertEqual(len(pairs), 6)  # unique pairs out of list
        self.assertIn((1, 2), pairs)

    def test__create_combinations(self):
        """
        Check that the enumerate of combinations is correct.

        Check whether any particle is repeated inside a combination,
        and checks if number of pairs in each combination is correct.
        """
        pairs_finder = BestPairsFinder()
        particle_pairs = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 3),
                          (2, 4), (2, 5), (2, 6), (3, 4), (3, 5), (3, 6),
                          (4, 5), (4, 6), (5, 6)]
        combinations = pairs_finder._create_combinations(
            particle_pairs, [], [], 6)
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
        pairs_finder = BestPairsFinder()
        particle_positions = [(1, 0.5), (0.6, 0.8), (0.4, 0.3), (0.0, -0.5),
                              (0.9, 2.1), (-1.1, -0.3)]
        combination = [(1, 2), (3, 0), (5, 4)]
        rounded_distance = 5.0768
        result = pairs_finder._get_summed_pair_distance(combination,
                                                        particle_positions)
        self.assertEqual(rounded_distance, round(result, 4))

    def test__choose_best_combination(self):
        """
        Check choosing combo with minimum distance.

        Checks whether minimal particle combination was chosen correctly, from
        list of combinations and their respective summed distances
        """
        pairs_finder = BestPairsFinder()
        combinations = [
            [(1, 2), (3, 4)],
            [(1, 3), (2, 4)],
            [(1, 4), (2, 3)]
        ]
        summed_distances = [8, 6, 7]
        expected = [(1, 3), (2, 4)]
        result = pairs_finder._choose_best_combination(combinations,
                                                       summed_distances)
        self.assertTrue(expected, result)

    def test_find_best_pairs(self):
        """Test the wrapper function `find_best_pairs` that the user calls."""
        subject = BestPairsFinder()
        # setup mocked functions
        # step 1
        subject._check_data_type = mock.MagicMock(name='_check_data_type',
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
        summed_distances = [1, 1, 1]
        subject._get_summed_pair_distance = mock.MagicMock(
            name='_get_summed_pair_distance', return_value=summed_distances)
        # step 5
        best_pairing = combinations[0]
        subject._choose_best_combination = mock.MagicMock(
            name='_choose_best_combination',
            return_value=best_pairing)
        # actually make the call
        particle_positions = [(1), (2), (3), (4)]
        result = subject.find_best_pairs(particle_positions,
                                         method='enumerate')
        # check all functions were called correctly
        subject._check_data_type.assert_called_with(particle_positions)
        subject._create_pairs.assert_called_with(particle_positions)
        subject._create_combinations.assert_called_with(
            pairs, [], [], len(particle_positions))
        subject._get_summed_pair_distance.assert_called_with(
            combinations)
        subject._choose_best_combination.assert_called_with(
            combinations, summed_distances)
        self.assertEqual(result, best_pairing)
        ####################################################
        # TODO check method = 'graph' call

    def test_compute_distance_matrix(self):
        """Test the compute_distance_matrix."""
        # 1D distance matrix
        pairs_finder = BestPairsFinder()
        self.assertEqual(pairs_finder._compute_distance_matrix
                         ([2, 3, 4, 6]).iloc[0, 0], 0)
        # 2D distance matrix
        test1 = pairs_finder._compute_distance_matrix([[2, 3], [3, 6],
                                                       [4, 5], [2, 3]])
        self.assertEqual(test1.iloc[0, 0], 0)
        self.assertAlmostEqual(test1.iloc[1, 0], 3.16, 2)
        self.assertEqual(len(test1.index), len(test1.columns))

    @skip
    def test_find_best_pairs_zero_particles(self):
        """Skip."""
        pairs_finder = BestPairsFinder()
        particle_positions = list()
        best_pairs = pairs_finder.find_best_pairs(
            particle_positions=particle_positions)
        self.assertTrue((()) == best_pairs)

    @skip
    def test_find_best_pairs_two_particles_in_one_dimensions(self):
        """Skip."""
        pairs_finder = BestPairsFinder()
        particle_positions = [(0., ), (2., )]
        best_pairs = pairs_finder.find_best_pairs(
            particle_positions=particle_positions)
        for pairs in best_pairs:
            pairs.sort()
        self.assertCountEqual([[(0., ), (2., )]], best_pairs)

    @skip
    def test_find_best_pairs_four_particles_in_one_dimensions(self):
        """Skip."""
        pairs_finder = BestPairsFinder()
        particle_positions = [(21, ), (1, ), (0, ), (21, )]
        best_pairs = pairs_finder.find_best_pairs(
            particle_positions=particle_positions)
        for pairs in best_pairs:
            pairs.sort()
        self.assertCountEqual([[(0, ), (1, )], [(20, ), (21, )]], best_pairs)

    @skip
    def test_find_best_pairs_two_particles_in_two_dimensions(self):
        """Skip."""
        pairs_finder = BestPairsFinder()
        particle_positions = [(0., -1.), (1., 2.)]
        best_pairs = pairs_finder.find_best_pairs(
            particle_positions=particle_positions)
        for pairs in best_pairs:
            pairs.sort()
        self.assertCountEqual([[(0., -1.), (1., 2.)]], best_pairs)

    @skip
    def test_find_best_pairs_four_particles_in_two_dimensions(self):
        """Skip."""
        pairs_finder = BestPairsFinder()
        particle_positions = [(0, 0), (1, 1), (20, 20), (21, 21)]
        best_pairs = pairs_finder.find_best_pairs(
            particle_positions=particle_positions)
        for pairs in best_pairs:
            pairs.sort()
        self.assertCountEqual(
            [[(0, 0), (1, 1)], [(20, 20), (21, 21)]], best_pairs)

if __name__ == '__main__':
    unittest.main()
