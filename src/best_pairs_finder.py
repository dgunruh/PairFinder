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


    def _create_combinations(self, particle_positions):
        '''
        Create all possible combinations of particles.
        '''
        comb = list((i+1, j+1) for ((i, _), (j, _)) in
                 itertools.combinations(enumerate(particle_positions), 2))
        self.combinations = comb
        return self.combinations


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

    def _choose_best_pair(self):
        '''
        Choose the best combination of particle pairs from a list of
        combinations and their respective summed distances
        '''
        pass


