from unittest import TestCase, skip

from src.best_pairs_finder import BestPairsFinder


class TestBestPairsFinder(TestCase):

    def test_nothing(self):
        self.assertTrue(True)

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
