class BestPairsFinder:

    def __init__(self):
        """Init function."""

    def find_best_pairs(self, particle_positions):
        """
        Find pairs of closest particles given their coordinates.

        This function does the following:
        1. Checks that the input datatype is correct
        2. Calculates distances between all points and nemuerates
           every two-pair combination possible
        3. Computes the summed pair distance for each combination
        4. Returns the combination that has the smallest summed distance

        Arguments:
            particle_positions - positions of N particles in D dimensions
                type == ND array

        Returns:
            paired_particles - list of particle pairs
                These pairs minimize the overall distances between particles
                type == list of tuples
        """
        # Step 1: Check type
        self._check_data_type(particle_positions)
        # Step 2: Enumerate distances
        combinations = self._create_combinations(particle_positions)
        # Step 3: Compute summed distances
        summed_distances = self._get_summed_pair_distance(combinations)
        # Step 4: Return combo that minimizes summed distances
        return self._choose_best_pair(summed_distances)

    def _check_data_type(self):
        """
        Check if object contains tuples of particle coordinates.
        """
        pass

    def _create_combinations(self):
        """
        Create all possible combinations of particles.
        """
        pass

    def _get_pair_distance(self):
        """
        Calculate the distance between two particles.
        """
        pass

    def _get_summed_pair_distance(self):
        """
        Sum the particle pair distances.
        """
        pass

    def _sort_pair(self):
        """
        Change pair order and make sure that total distance remains the same.
        """
        pass

    def _choose_best_pair(self):
        """
        Choose the best combination of particle pairs from a list of
        combinations and their respective summed distances
        """
        pass
