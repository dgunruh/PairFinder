from unittest import TestCase, skip
import unittest.mock as mock

from src.best_pairs_finder import BestPairsFinder


class TestBestPairsFinder(TestCase):

    def test_nothing(self):
        self.assertTrue(True)

    def test__check_data_type(self):
        '''
        YIMING
        Check if object contains tuples of particle coordinates.
        '''
        pass

    def test__create_combinations(self):
        '''
        YIMING
        Check whether number of combinations of particles is correct,
        and if all combinations are unique
        '''
        pass

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

    def test__sort_pair(self):
        '''
        YIMING
        Check whether summed distances is invariant to particle pair order.
        '''
        pass

    def test__choose_best_pair(self):
        '''
        Checks whether minimal particle combination was chosen correctly, from
        list of combinations and their respective summed distances
        '''
        pass

    def test_find_best_pairs(self):
    	'''
    	
    	'''
    	pass

    @skip
    def test_find_best_pairs_zero_particles(self):
        pairs_finder = BestPairsFinder()
        particle_positions = list()
        best_pairs = pairs_finder.find_best_pairs(particle_positions=particle_positions)
        self.assertTrue((()) == best_pairs)

    @skip
    def test_find_best_pairs_two_particles_in_one_dimensions(self):
        pairs_finder = BestPairsFinder()
        particle_positions = [(0., ), (2., )]
        best_pairs = pairs_finder.find_best_pairs(particle_positions=particle_positions)
        for pairs in best_pairs:
            pairs.sort()
        self.assertCountEqual([[(0., ), (2., )]], best_pairs)

    @skip
    def test_find_best_pairs_four_particles_in_one_dimensions(self):
        pairs_finder = BestPairsFinder()
        particle_positions = [(21, ), (1, ), (0, ), (21, )]
        best_pairs = pairs_finder.find_best_pairs(particle_positions=particle_positions)
        for pairs in best_pairs:
            pairs.sort()
        self.assertCountEqual([[(0, ), (1, )], [(20, ), (21, )]], best_pairs)

    @skip
    def test_find_best_pairs_two_particles_in_two_dimensions(self):
        pairs_finder = BestPairsFinder()
        particle_positions = [(0., -1.), (1., 2.)]
        best_pairs = pairs_finder.find_best_pairs(particle_positions=particle_positions)
        for pairs in best_pairs:
            pairs.sort()
        self.assertCountEqual([[(0., -1.), (1., 2.)]], best_pairs)

    @skip
    def test_find_best_pairs_four_particles_in_two_dimensions(self):
        pairs_finder = BestPairsFinder()
        particle_positions = [(0, 0), (1, 1), (20, 20), (21, 21)]
        best_pairs = pairs_finder.find_best_pairs(particle_positions=particle_positions)
        for pairs in best_pairs:
            pairs.sort()
        self.assertCountEqual([[(0, 0), (1, 1)], [(20, 20), (21, 21)]], best_pairs)
