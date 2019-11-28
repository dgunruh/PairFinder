from unittest import TestCase, skip

from best_pairs_finder import BestPairsFinder


class TestBestPairsFinder(TestCase):

    def test_nothing(self):
        self.assertTrue(True)

    @skip
    def test_zero_particles(self):
        pairs_finder = BestPairsFinder()
        particle_positions = list()
        best_pairs = pairs_finder.find_best_pairs(particle_positions=particle_positions)
        self.assertTrue([[]] == best_pairs)

    @skip
    def test_two_particles_in_two_dimensions(self):
        pairs_finder = BestPairsFinder()
        particle_positions = [[0., -1.], [1., 2.]]
        best_pairs = pairs_finder.find_best_pairs(particle_positions=particle_positions)
        self.assertCountEqual([[[0., -1.], [1., 2.]]], best_pairs)
