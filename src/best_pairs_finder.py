class BestPairsFinder:

    def find_best_pairs(self, particle_positions):
        """
        Find pairs of closest particles given their coordinates.

        This function does the following:

        Arguments:
            particle_positions - positions of N particles in D dimensions
                type == ND array
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

    def _choose_best_pair(self):
        '''
        Choose the best combination of particle pairs from a list of
        combinations and their respective summed distances
        '''
        pass
