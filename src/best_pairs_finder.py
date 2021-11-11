import numpy as np


class BestPairsFinder:

    def find_best_pairs(self, particle_positions):
        """
        Here you can insert docstring documentation, if needed
        """
        pass

    def _check_data_type(self):
        '''
        Check if object contains tuples of particle coordinates.
        '''
        pass

    def _create_combinations(self):
        '''
        Create all possible combinations of particles.
        '''
        pass

    def _get_pair_distance(self):
        '''
        Calculate the distance between two particles.
        '''
        pass

    def _get_summed_pair_distance(self):
        '''
        Sum the particle pair distances.
        '''
        pass

    def _sort_pair(self):
        '''
        Change pair order and make sure that total distance remains the same.
        '''
        pass

    def _choose_best_pair(self, combinations, distances):
        '''
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
        '''
        min_distance_index = np.argmin(distances)
        min_combination = combinations[min_distance_index]
        return min_combination
