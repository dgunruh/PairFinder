from unittest import TestCase, skip
from PairFinder.src.best_pairs_finder import BestPairsFinder
import unittest


class TestBestPairsFinder(TestCase):
    def test_setup(self):
        self.pairs_finder = BestPairsFinder()

    def test_nothing(self):
        self.assertTrue(True)

    def test__check_data_type(self):
        '''
        YIMING
        Check if input object is a list.
        '''
        pairs_finder = BestPairsFinder()
        self.assertTrue(pairs_finder._check_data_type(
            particle_positions=[5, 10, 15, 20]) == list)

    def test__create_pairs(self):
        '''
        YIMING
        Check whether number of combinations of particles is correct,
        and if all combinations are unique
        '''
        pairs_finder = BestPairsFinder()
        pairs = pairs_finder._create_pairs(
            particle_positions=[5, 10, 15, 20])
        self.assertTrue(type(pairs) == list)
        self.assertTrue(type(pairs[0]) == tuple)
        self.assertEqual(len(pairs), 6)  # unique pairs out of list
        self.assertIn((1, 2), pairs)

    def test__get_pair_distance(self):
        '''
        LUQING
        Check whether particle distance was calculated correctly.
        '''
        pass

    def test__get_summed_pair_distance(self):
        '''
        LUQING
        Check whether particle distances were summed correctly.
        '''
        pass

    def test__choose_best_pair(self):
        '''
        Checks whether minimal particle combination was chosen correctly, from
        list of combinations and their respective summed distances
        '''
        pairs_finder = BestPairsFinder()
        combinations = [
            [(1, 2), (3, 4)],
            [(1, 3), (2, 4)],
            [(1, 4), (2, 3)]
        ]
        summed_distances = [8, 6, 7]
        self.assertTrue([(1, 3), (2, 4)] == pairs_finder._choose_best_pair(
            combinations, summed_distances))

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


if __name__ == '__main__':
    unittest.main()
