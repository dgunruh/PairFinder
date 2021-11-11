from unittest import TestCase, skip
import unittest.mock as mock

from src.best_pairs_finder import BestPairsFinder


class TestBestPairsFinder(TestCase):

    def test_nothing(self):
        self.assertTrue(True)

    def test__check_data_type(self):
        """
        YIMING
        Check if object contains tuples of particle coordinates.
        """
        pass

    def test__create_combinations(self):
        """
        YIMING
        Check whether number of combinations of particles is correct,
        and if all combinations are unique
        """
        pass

    def test__get_pair_distance(self):
        """
        LUQING
        Check whether particle distance was calculated correctly.
        """
        pass

    def test__get_summed_pair_distance(self):
        """
        LUQING
        Check whether particle distances were summed correctly.
        """
        pass

    def test__sort_pair(self):
        """
        YIMING
        Check whether summed distances is invariant to particle pair order.
        """
        pass

    def test__choose_best_pair(self):
        """
        Checks whether minimal particle combination was chosen correctly, from
        list of combinations and their respective summed distances
        """
        pass

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
        combinations = [[(1, 2), (3, 4)],
                        [(1, 3), (2, 4)],
                        [(1, 4), (2, 3)]]
        subject._create_combinations = mock.MagicMock(
            name='_create_combinations', return_value=combinations)
        # step 3
        summed_distances = [2, 4, 4]
        subject._get_summed_pair_distance = mock.MagicMock(
            name='_get_summed_pair_distance', return_value=summed_distances)
        # step 4
        best_pairing = combinations[0]
        subject._choose_best_pair = mock.MagicMock(name='_choose_best_pair',
                                                   return_value=best_pairing)
        # actually make the call
        particle_positions = [(1), (2), (3), (4)]
        result = subject.find_best_pairs(particle_positions)
        # check all functions were called correctly
        subject._check_data_type.assert_called_with(particle_positions)
        subject._create_combinations.assert_called_with(particle_positions)
        subject._get_summed_pair_distance.assert_called_with(combinations)
        subject._choose_best_pair.assert_called_with(summed_distances)
        self.assertEqual(result, best_pairing)

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
