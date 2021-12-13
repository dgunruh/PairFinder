from unittest import TestCase, skip
import unittest
import unittest.mock as mock
import numpy as np
from pairfinder.src.best_pairs_finder import BestPairsFinder
import pandas as pd


class TestBestPairsFinder(TestCase):
    def test_setup(self):
        self.pairs_finder = BestPairsFinder()

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
        """
        YIMING
        Check if input object is iterable.
        """
        pairs_finder = BestPairsFinder()
        self.assertTrue(pairs_finder._check_iterable(
            particle_positions=[5, 10, 15, 20]))
        self.assertFalse(pairs_finder._check_iterable(
            particle_positions=5))

    def test__create_pairs(self):
        """
        YIMING
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
        '''
        Checks whether any particle is repeated inside a combination,
        and checks if number of pairs in each combination is correct.
        '''
        pairs_finder = BestPairsFinder()
        particle_pairs = [[1, 2], [1, 3], [1, 4], [1, 5], [1, 6], [2, 3], [2, 4],
                          [2, 5], [2, 6], [3, 4], [3, 5], [3, 6], [4, 5], [4, 6], [5, 6]]
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
        """
        Check whether particle distance was calculated correctly.
        """
        pairs_finder = BestPairsFinder()
        p1 = (1, 2, 3, 4)
        p2 = (2, 1, 5, 1)
        squared_distance = 0
        for i in range(len(p2)):
            squared_distance += (p2[i] - p1[i])**2
        distance = np.sqrt(squared_distance)
        self.assertEqual(distance, pairs_finder._get_pair_distance(p1, p2))

    def test__get_summed_pair_distance(self):
        """
        Check whether particle distances were summed correctly.
        """
        pairs_finder = BestPairsFinder()
        d1_combination = [
            [1, 0.5], [0.6, 0.8], [0.4, 0.3], [0.0, -0.5], [0.9, 2.1], [-1.1, -0.3]]
        d2_combination = [
            [(1, 0.5), (0.6, 0.8)], [(0.4, 0.3), (0.0, -0.5)], [(0.9, 2.1), (-1.1, -0.3)]]
        rounded_distance_d1_combo = 3.3
        rounded_distance_d2_combo = 4.5185
        self.assertEqual(rounded_distance_d1_combo, round(
            pairs_finder._get_summed_pair_distance(d1_combination), 4))
        self.assertEqual(rounded_distance_d2_combo, round(
            pairs_finder._get_summed_pair_distance(d2_combination), 4))

    def test__choose_best_combination(self):
        """
        Checks whether minimal particle combination was chosen correctly, from
        list of combinations and their respective summed distances
        """
        pairs_finder = BestPairsFinder()
        combinations = [
            [[1, 2], [3, 4]],
            [[1, 3], [2, 4]],
            [[1, 4], [2, 3]]
        ]
        summed_distances = [2, 4, 4]
        best_combination, smallest_distance = pairs_finder._choose_best_combination(
            combinations)
        self.assertTrue([[1, 2], [3, 4]] == best_combination)
        self.assertTrue(2 == smallest_distance)

    def test_find_best_pairs(self):
        """
        Test the wrapper function `find_best_pairs` that the user calls.
        """
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
        particle_positions = [1, 2, 3, 4]
        result = subject.find_best_pairs(
            particle_positions, method='simulated_annealing')
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
        # TODO check method = 'graph' call

    def test_compute_distance_matrix(self):
        """
        Test the compute_distance_matrix
        """
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
        Test all methods to create a single combination of particle pairs, in
        one dimension. Currently, these are the "linear" and "greedy" methods.
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

    @skip
    def test_find_best_pairs_zero_particles(self):
        pairs_finder = BestPairsFinder()
        particle_positions = list()
        best_pairs = pairs_finder.find_best_pairs(
            particle_positions=particle_positions)
        self.assertTrue((()) == best_pairs)

    @skip
    def test_find_best_pairs_two_particles_in_one_dimensions(self):
        pairs_finder = BestPairsFinder()
        particle_positions = [(0., ), (2., )]
        best_pairs = pairs_finder.find_best_pairs(
            particle_positions=particle_positions)
        for pairs in best_pairs:
            pairs.sort()
        self.assertCountEqual([[(0., ), (2., )]], best_pairs)

    @skip
    def test_find_best_pairs_four_particles_in_one_dimensions(self):
        pairs_finder = BestPairsFinder()
        particle_positions = [(21, ), (1, ), (0, ), (21, )]
        best_pairs = pairs_finder.find_best_pairs(
            particle_positions=particle_positions)
        for pairs in best_pairs:
            pairs.sort()
        self.assertCountEqual([[(0, ), (1, )], [(20, ), (21, )]], best_pairs)

    @skip
    def test_find_best_pairs_two_particles_in_two_dimensions(self):
        pairs_finder = BestPairsFinder()
        particle_positions = [(0., -1.), (1., 2.)]
        best_pairs = pairs_finder.find_best_pairs(
            particle_positions=particle_positions)
        for pairs in best_pairs:
            pairs.sort()
        self.assertCountEqual([[(0., -1.), (1., 2.)]], best_pairs)

    @skip
    def test_find_best_pairs_four_particles_in_two_dimensions(self):
        pairs_finder = BestPairsFinder()
        particle_positions = [(0, 0), (1, 1), (20, 20), (21, 21)]
        best_pairs = pairs_finder.find_best_pairs(
            particle_positions=particle_positions)
        for pairs in best_pairs:
            pairs.sort()
        self.assertCountEqual(
            [[(0, 0), (1, 1)], [(20, 20), (21, 21)]], best_pairs)

    def test_find_best_pairs_100_particles_in_one_dimensions(self):
        """
        Generate positions for 100 particles as a random array.
        """
        # particles = np.random.randint(-100, 100, size=100)

        # Positions for 100 particles specified
        particles = [-5, 2, -64, 15, 44, -27, 36, -84, -3, -21,
                     -70, 59, -91, 86, -85, 16, 44, 94, -63, 14,
                     -39, -10, 4, 83, -50, 45, 37, 100, -72, -89,
                     11, 98, 75, 57, 93, 0, -40, -61, 97, -77,
                     64, 80, -80, -43, 27, -40, -78, 41, 15, -51, 96,
                     -91, 47, -6, 42, 44, -48, 33, 8, -46, -2, -72,
                     0, 84, 34, 22, -11, -90, 74, 6, 57, -30, 7,
                     5, 46, -60, -78, -9, 32, -11, 28, 29, -13, -43,
                     84, 64, 80, 36, 44, 45, -44, -17, -10, -17, 95,
                     25, -40, 45, 87, 37]

        # Sort particles based on position and save the particle index
        # for grouping near pairs.
        pair_index = np.argsort(particles)
        # Calculate distance of near pairs and sum them as total distance.
        distance = 0
        for i in pair_index:
            if (i % 2) == 0:
                distance = distance + particles[pair_index[i + 1]]\
                    - particles[pair_index[i]]

    def test_against_brute_force_three_dimensions(self):
        """
        Test performance of any of the methods against the "enumerate" method,
        which solves the problem by brute force (finding all possible
        combinations of particle coordinates, and choosing the combination with
        the smallest distance).

        Test is conducted with 10 particles.
        """
        test_method = "simulated_annealing"

        particle_coords = [tuple(i)
                           for i in np.random.uniform(-100, 100, (10, 3))]

        pairs_finder = BestPairsFinder()
        brute_force_combination, brute_force_distance =\
            pairs_finder.find_best_pairs(particle_coords, method='enumerate')
        for pairs in brute_force_combination:
            pairs.sort()

        test_combination, test_distance =\
            pairs_finder.find_best_pairs(particle_coords, method=test_method)
        for pairs in test_combination:
            pairs.sort()

        self.assertCountEqual(
            brute_force_combination, test_combination)
        self.assertEqual(brute_force_distance, test_distance)


if __name__ == '__main__':
    unittest.main()
