"""Best pairs finder."""

import numpy as np
import itertools
import pandas as pd
from scipy.spatial import distance_matrix


class BestPairsFinder:
    """Pair particles together such that the total distance is minimized."""

    def __init__(self):
        """Init function."""

    def find_best_pairs(self, particle_positions, method='greedy'):
        """
        Find pairs of closest particles given their coordinates. Multiple
        methods are implemented, and each method functions slightly
        differently. The methods are:

        Enumerate method:

            1. Check that the input is iterable

            2. Enumerate every possible particle pairing

            3. Create combinations of these pairs to include every particle

            4. Return the combination that has the smallest summed distance

        Graph method (both greedy and COM):

            1. Check that the input is iterable

            2. Save particle index to coordinate/ position in a dictionary

            3. Create distance matrix between all points (N x N)

            4. Pair particles using greedy or center of mass approach

            5. Convert paired particles from indices to coordinates and return

        Simulated annealing method:

            1. Check that the input particles object is iterable

            2. Create initial pairs of particles using various methods:

                2a. Linear pairing (pair in order of indices)

                2b. Random pairing (pair randomly until no particles remain)

                2c. Greedy pairing (pair particles in smallest distance order)

            3. Run simulated annealing with set beta parameters (max, min and
                step size), and number of annealing steps per beta step.

        Parameters
        ----------
        particle_positions : `list`

            positions of N particles in D dimensions

        method : `string`, *optional*

            The method by which the best pairs are found. Options are
            "enumerate", "greedy", "COM" and "simulated-annealing".
            By default, the method is `"greedy"`.

        Returns
        -------
        paired_particles : `list`

            Combination of pairs which minimizes the overall distances
            between particles.

        Examples
        --------
        Find the optimal pairing of 6 particles in 2-dimensions using the
        `"greedy"` graph approach:

            >>> finder = BestPairsFinder()
            >>> particle_positions = create_even_number_of_particles(6, 2, seed=42)
            >>> pairing, distance = finder.find_best_pairs(particle_positions,\
                method='greedy')
        """
        if method == 'enumerate':
            # Step 1: Check that particle_positions is iterable
            self._check_iterable(particle_positions)
            # Step 2: Enumerate all pairs of particles
            pairs = self._create_pairs(particle_positions)
            # Step 3: Create combinations of these pairs
            combos = self._create_combinations(
                pairs, len(particle_positions)//2, len(particle_positions) - 1)
            # Step 4: Return minimum distance combination (and its distance)
            return self._choose_best_combination(combos)
        elif method in ['greedy', 'COM']:
            # Step 1: Check that particle_positions is iterable
            self._check_iterable(particle_positions)
            # Step 2: Save index to coordinate map
            self.idx_to_coord_map = {i: coord for i, coord in
                                     enumerate(particle_positions)}
            # Step 3: Create distance matrix between all points
            distance_mtx = self._compute_distance_matrix(particle_positions)
            n = len(particle_positions)
            # set diagonal to inf to prevent selecting self
            distance_mtx = np.array(distance_mtx)
            distance_mtx[range(n), range(n)] = np.inf
            distance_mtx = pd.DataFrame(distance_mtx)
            # Step 4: Pair particles based on specified method
            self.pairs = []
            self._get_pairs_from_distance_matrix(distance_mtx, self.pairs,
                                                 method=method)
            # Step 5: Convert particle indices to coordinates using map
            converted_pairing = [(self.idx_to_coord_map[pair[0]],
                                  self.idx_to_coord_map[pair[1]])
                                 for pair in self.pairs]
            return converted_pairing,\
                self._get_summed_pair_distance(converted_pairing)
        elif method == 'simulated_annealing':
            # Step 1: Check that particle_positions is iterable
            self._check_iterable(particle_positions)
            # Step 2: Create initial pairing of particles
            self.pairs = self._create_single_combination(
                particle_positions, "greedy")
            # Run simulated annealing with set parameters
            self._run_simulated_annealing(self.pairs, 10000, 100, 0.25, 0.25)
            return self.pairs,\
                self._get_summed_pair_distance(self.pairs)

    def _check_iterable(self, particle_positions):
        """Check if input is iterable."""
        try:
            iter(particle_positions)
            return True
        except TypeError:
            print('particle positions is not iterable')
            return False

    def _create_pairs(self, particle_positions):
        """Create all possible pairs of particles."""
        pairs = [list(i)
                 for i in itertools.combinations(particle_positions, 2)]
        return pairs

    def _create_combinations(self, all_pairs, num_pairs_to_add,
                             num_pairs_with_next_coord, combination_base=[],
                             already_contained_coords=[]):
        """
        Recursive search for every combination of particle coordinate pairs

        Args:
        all_pairs (list) - all possible pairs of particle coordinates. Ordered by
            the particle coordinate of the first particle in each pair.
        num_pairs_to_add (int) - the number of pairs that still need to be added
            to each combination.
        num_pairs_with_next_coord (int) - the number of pairs in all_pairs which
            contain the next possible first particle coordinate. (all pairs)
        combination_base (list) - the current pairs to start the combination
        already_contained_coords (list) - the coordinates of the pairs inside
            combination_base

        Outputs:
        All possible combination of pairs
        """
        if num_pairs_to_add == 0:
            return [combination_base]
        elif num_pairs_with_next_coord == 1:
            return [combination_base + all_pairs]
        else:
            if all_pairs[0][0] not in already_contained_coords:
                combinations = []
                for i in range(num_pairs_with_next_coord):
                    if all_pairs[i][1] not in already_contained_coords:
                        new_combination_base = combination_base + \
                            [all_pairs[i]]
                        new_contained_coords = already_contained_coords\
                            + [all_pairs[i][0], all_pairs[i][1]]
                        new_pairs = all_pairs[num_pairs_with_next_coord:]
                        new_combinations =\
                            self._create_combinations(new_pairs,
                                                      num_pairs_to_add - 1,
                                                      num_pairs_with_next_coord - 1,
                                                      new_combination_base,
                                                      new_contained_coords,)
                        if len(combinations) == 0:
                            combinations = new_combinations
                        else:
                            combinations.extend(new_combinations)
                return combinations
            else:
                return self._create_combinations(
                    all_pairs[num_pairs_with_next_coord:],
                    num_pairs_to_add,
                    num_pairs_with_next_coord - 1,
                    combination_base,
                    already_contained_coords, )

    def _choose_best_combination(self, combinations):
        """
        Choose best combination from brute force list of all possible
        combinations.

        ----------------------------------------------------------------------

        Args:

        combinations (list) - all possible combinations of particle pairs

        Outputs:

        min_combination (list) - the combination of particle pairs which
            corresponds to the smallest total particle distance.

        min_distance (float) - the total particle distance of min_combination.
        """
        min_combination = None
        min_distance = np.inf
        for combination in combinations:
            distance = self._get_summed_pair_distance(combination)
            if distance < min_distance:
                min_distance = distance
                min_combination = combination
        return min_combination, min_distance

    def _get_pair_distance(self, p1, p2):
        """Calculate the distance between two particles."""
        return np.linalg.norm(np.subtract(p1, p2))

    def _get_summed_pair_distance(self, particle_pairs):
        """
        Get total distance between all paired particles.

        Sum the particle pair distances of a combination of particle pairs,
        where the pairs are listed as indices of particle positions
        """
        distance = 0
        for pair in particle_pairs:
            distance += self._get_pair_distance(pair[0], pair[1])
        return distance

    def _get_pairs_from_distance_matrix(self, distance_mtx, result,
                                        method='greedy'):
        """
        Greedy approach to pairing particles using the graph method.

        This is a recursive function that pairs all particles until the
        distance matrix has one or zero particles left.

        Arguments:
            distance_mtx - distances between all particles (N x N)
                Should be symetrical. This function converts it to a dataframe
            result - the paired particles (by original index number)
                type == list

        Returns:
            recursive call - both the distance matrix and result (pairs) change
        """
        # get size
        n = len(distance_mtx)
        # stopping criteria
        if n == 1:
            # if odd number, return individual
            result.append((distance_mtx.columns[0],))
            return
        if n == 0:
            # if even number, end
            return

        if method == 'greedy':
            # get minimum distance index (greedy approach)
            flatted_min_index = np.argmin(distance_mtx)
            # get row by colm indices of that overall minimum
            point1_index, point2_index = np.unravel_index(flatted_min_index,
                                                          (n, n))
        else:
            pts_left = np.array([self.idx_to_coord_map[colm]
                                 for colm in distance_mtx.columns])
            if len(pts_left.shape) == 1:
                avg = np.average(pts_left)
            else:
                avg = [sum(x) / len(x) for x in zip(*pts_left)]
            distance_from_centroid = [np.linalg.norm([diff], ord=2)
                                      for diff in pts_left - avg]
            # get point farthest from center
            point1_index = np.argmax(distance_from_centroid)
            # get point that is closest to the above point
            point2_index = np.argmin(distance_mtx.iloc[point1_index])

        # get original point labels
        point1 = distance_mtx.index[point1_index]
        point2 = distance_mtx.columns[point2_index]
        # save the results
        result.append((point1, point2))

        # pop the paired points from the distance matrix
        remove_list = np.flip(np.sort([point1, point2]))
        for index in remove_list:
            distance_mtx.drop(index, axis=0, inplace=True)
            distance_mtx.drop(index, axis=1, inplace=True)
        # call recursively
        self._get_pairs_from_distance_matrix(distance_mtx, result)

    def _compute_distance_matrix(self, particle_positions):
        """Generate distance matrix given a set of particle positions."""
        df = pd.DataFrame(particle_positions)
        dis_matrix = pd.DataFrame(distance_matrix(df.values, df.values))
        return dis_matrix

    def _create_single_combination(self, positions, method):
        """Generate single combination of pairs of particles"""
        if method == "linear":
            # pair particles in order of positions
            pairs = [[positions[i], positions[i+1]]
                     for i in range(0, len(positions), 2)]

        elif method == "random":
            # randomly pair particles
            np.random.shuffle(positions)
            pairs = [[positions[i], positions[i+1]]
                     for i in range(0, len(positions), 2)]

        elif method == "greedy":
            # pair particles by choosing smallest pairing, subsequently
            # smallest pairing, etc.
            available_pool = [i for i in positions]
            pairs = []
            for i in range(len(positions)//2):
                smallest_distance = np.inf
                smallest_particle = None
                smallest_particle_index = 1
                p1 = available_pool[0]
                for j, p2 in enumerate(available_pool[1:]):
                    distance = self._get_pair_distance(p1, p2)
                    if distance < smallest_distance:
                        smallest_distance = distance
                        smallest_particle = p2
                        smallest_particle_index = j + 1
                pairs.append([p1, smallest_particle])
                available_pool.pop(smallest_particle_index)
                available_pool.pop(0)

        return pairs

    def _run_simulated_annealing(self, pairs, N, beta_max=5, beta_min=1,
                                 beta_step=0.1):
        """
        Run simulated annealing on pairs of particles to obtain
        the lowest distance solution

        -------------------------------------------------------
        Args:

        pairs (iterable) - pairs of particle coordinates

        N (int) - number of steps per beta increment

        beta_max, beta_min, beta_step (float) - beta is the factor which
        corresponds to effective 1/kB*T. Beta_max, beta_min and beta_step
        control the maximum, minimum and step size values respectively.
        """

        # compute total distance of starting pairs
        current_total_distance = self._get_summed_pair_distance(pairs)
        for beta in np.arange(beta_min, beta_max, beta_step):
            print(beta)
            for n in range(N):
                pair1, pair2, pair_indices, proposed_distance_one,\
                    proposed_distance_two =\
                    self._propose_pairings(pairs, current_total_distance)

                if proposed_distance_one < proposed_distance_two:

                    successful_change = self._evaluate_sa_probability(
                        proposed_distance_one, current_total_distance, beta)

                    if successful_change:
                        pairs[pair_indices[0]] = (pair1[0], pair2[0])
                        pairs[pair_indices[1]] = (pair1[1], pair2[1])
                        current_total_distance = proposed_distance_one
                else:

                    successful_change = self._evaluate_sa_probability(
                        proposed_distance_two, current_total_distance, beta)

                    if successful_change:
                        pairs[pair_indices[0]] = (pair1[0], pair2[1])
                        pairs[pair_indices[1]] = (pair1[1], pair2[0])
                        current_total_distance = proposed_distance_two

        return pairs

    def _propose_pairings(self, pairs, total_distance):
        '''
        Propose pairs of particles which will swap bonds. Pairs are
        chosen at random, and the current contribution to the total
        distance is recorded.
        Each swap has two possible final configurations, so the distance
        of each configuration is calculated and returned as well.

        Args:
        pairs (list) - the current pairings of particles.
        total_distance (float) - the current total distance of the pairings.

        Outputs:
        pair1 (tuple) - 1st pair of particle coordinates
        pair2 (tuple) - 2nd pair of particle coordinates
        pair_indices (list of ints) - the indices of the chosen pairs.
        proposed_distance_one (float) - the total distance if the first
            of the two alternate pairings succeeds.
        proposed_distance_two (float) - the total distance if the second
            of the two alternate pairings succeeds.
        '''
        pair_indices = np.random.choice(
            range(len(pairs)), replace=False, size=2)

        pair1 = pairs[pair_indices[0]]
        pair2 = pairs[pair_indices[1]]

        current_distance_contribution =\
            self._get_pair_distance(pair1[0], pair1[1]) +\
            self._get_pair_distance(pair2[0], pair2[1])
        alt_pairing_one_distance =\
            self._get_pair_distance(pair1[0], pair2[0]) +\
            self._get_pair_distance(pair1[1], pair2[1])
        alt_pairing_two_distance =\
            self._get_pair_distance(pair1[1], pair2[0]) +\
            self._get_pair_distance(pair1[0], pair2[1])

        proposed_distance_one = total_distance - current_distance_contribution\
            + alt_pairing_one_distance
        proposed_distance_two = total_distance - current_distance_contribution\
            + alt_pairing_two_distance

        return pair1, pair2, pair_indices, proposed_distance_one,\
            proposed_distance_two

    def _evaluate_sa_probability(self, proposed_distance, total_distance,
                                 beta):
        '''
        Perform a Monte Carlo evaluation of the simulated annealing pair
        swap. Here, distance is taken to be the "energy" of the system.
        If the new distance is lower than the old distance, then the swap
        automatically succeeds. Otherwise, it is evaluated using:
            P(success) = exp(-DeltaE/kT) = exp(-beta*DeltaE)
        where beta = kT.

        Args:
        proposed_distance (float) - the distance of the proposed swap.
        total_distance (float) - the distance pre-swap.
        beta (float) - the artificial kT value.

        Outputs:
        (boolean) - was the swap successful or not
        '''

        if proposed_distance < total_distance:
            return True
        else:
            success_probability = np.exp(
                beta * (total_distance - proposed_distance))
            if np.random.uniform() < success_probability:
                return True
        return False
