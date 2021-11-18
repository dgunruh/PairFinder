from unittest import TestCase, skip
import unittest
import unittest.mock as mock
import numpy as np
from PairFinder.src.best_pairs_finder import BestPairsFinder


class TestBestPairsFinder(TestCase):
    def test_setup(self):
        self.pairs_finder = BestPairsFinder()

    def test_nothing(self):
        self.assertTrue(True)

    def test__check_data_type(self):
        """
        YIMING
        Check if input object is a list.
        """
        pairs_finder = BestPairsFinder()
        self.assertTrue(pairs_finder._check_data_type(
            particle_positions=[5, 10, 15, 20]) == list)

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
        self.assertTrue(type(pairs[0]) == tuple)
        self.assertEqual(len(pairs), 6)  # unique pairs out of list
        self.assertIn((1, 2), pairs)

    def test__create_combinations(self):
        '''
        Checks whether any particle is repeated inside a combination,
        and checks if number of pairs in each combination is correct.
        '''
        pairs_finder = BestPairsFinder()
        particle_pairs = [(1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (2, 3), (2, 4),
                          (2, 5), (2, 6), (3, 4), (3, 5), (3, 6), (4, 5), (4, 6), (5, 6)]
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
        """
        Check whether particle distance was calculated correctly.
        """
        pairs_finder = BestPairsFinder()
        p1 = (1,2,3,4)
        p2 = (2,1,5,1)
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
        particle_positions = [(1, 0.5), (0.6, 0.8), (0.4, 0.3), (0.0, -0.5), (0.9, 2.1), (-1.1, -0.3)]
        combination = [(1,2), (3, 0), (5,4)]
        rounded_distance = 5.0768
        self.assertEqual(rounded_distance, round(pairs_finder._get_summed_pair_distance(combination, particle_positions), 4))

    def test__choose_best_combination(self):
        """
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
        self.assertTrue([(1, 3), (2, 4)] == pairs_finder._choose_best_combination(
            combinations, summed_distances))

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
        summed_distances = [2, 4, 4]
        subject._get_summed_pair_distance = mock.MagicMock(
            name='_get_summed_pair_distance', return_value=summed_distances)
        # step 5
        best_pairing = combinations[0]
        subject._choose_best_pair = mock.MagicMock(name='_choose_best_pair',
                                                   return_value=best_pairing)
        # actually make the call
        particle_positions = [(1), (2), (3), (4)]
        result = subject.find_best_pairs(particle_positions)
        # check all functions were called correctly
        subject._check_data_type.assert_called_with(particle_positions)
        subject._create_pairs.assert_called_with(particle_positions)
        subject._create_combinations.assert_called_with(
            (pairs, [], [], len(particle_positions)))
        subject._get_summed_pair_distance.assert_called_with(combinations)
        subject._choose_best_pair.assert_called_with(
            (combinations, summed_distances))
        self.assertEqual(result, best_pairing)

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
        '''
        Generate positions for 100 particles as a random array.
        '''
        '''
        particles = np.random.randint(-100, 100, size=100)
        '''
        '''
        Positions for 100 particles.
        '''
        particles = [-5    2  -64   15   44  -27   36  -84   -3  -21  -70   59  -91   86  -85   16   44   94  -63   14  -39  -10    4  -83  -50   45   37 -100  -72  -89   11   98   75   57   93    0  -40  -61   97  -77   64   80  -80  -43   27  -40  -78   41   15  -51   96  -91   47   -6  -42   44  -48   33    8  -46   -2  -72    0   84   34   22  -11  -90   74    6   57  -30    7    5   46  -60  -78   -9  -32  -11   28   29  -13  -43   84   64   80   36   44   45  -44  -17  -10  -17   95   25  -40   45  -87   37]

        '''
        Sort particles based on position and save the particle index for grouping near pairs.
        '''
        pair_index = np.argsort(particles)

        '''
        Calculate distance of near pairs and sum them as total distance.
        '''
        distance = 0
        for i in pair_index:
            if (i % 2) == 0:
                distance = distance + particles[pair_index[i + 1]] - particles[pair_index[i]]

if __name__ == '__main__':
    unittest.main()
