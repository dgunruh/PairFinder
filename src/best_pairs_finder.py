import numpy as np
import itertools


class BestPairsFinder:

    def find_best_pairs(self, particle_positions):
        """
        Here you can insert docstring documentation, if needed
        """
        pass

    def _check_data_type(self, particle_positions):
        '''
        Check if input is a list
        '''
        return type(particle_positions)

    def _create_pairs(self, particle_positions):
        '''
        Create all possible pairs of particles.
        '''
        pairs = list((i+1, j+1) for ((i, _), (j, _)) in
                     itertools.combinations(enumerate(particle_positions), 2))
        self.pairs = pairs
        return self.pairs

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

    def _choose_best_combination(self, combinations, distances):
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
        best_combination = combinations[min_distance_index]
        return best_combination
