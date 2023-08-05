from dataclasses import dataclass
import itertools
from os import stat
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from scipy.special import softmax

@dataclass
class State:
    '''
        State object
    '''
    number: list
    description: list
    v_value: float
    reward: float = 0
    nb_visited: int = 0

    def get_reward(self, X_train, y_train, X_test, y_test, clf) -> float:
        '''
            Return the reward of a set of variable
        '''
        #Train classifier with state_t variable and state t+1 variables and compute the diff of the accuracy
        if self.reward == 0:
            if self.description == []:
                self.reward = 0
                return 0
            else:
                #The state has never been visited and we init the reward
                clf.fit(X_train[self.description], y_train)
                accuracy: float = clf.score(X_test[self.description], y_test)

                self.reward =accuracy
                return self.reward
        else:
            return self.reward

    def select_action(self, feature_structure: dict, eps: float, aorf_histo: list, is_empty_state: bool):
        '''
            Returns an action object

            This method enables to train only once a model and get the accuracy
        '''
        #We get the neighboors
        get_neigh: list = self.get_neighboors(feature_structure, [i for i in range(0, len(aorf_histo[0]))])

        #Check if it is an eps step
        eps_step: bool = bool(np.random.binomial(1, eps))

        if self.nb_visited == 0 or eps_step:
            has_explored_node: list = [neigh for neigh in get_neigh if neigh.v_value != 0]
            if not has_explored_node or eps_step:
                #We select not explored state randomly
                next_state: State = np.random.choice(get_neigh)

                return Action(self, next_state), next_state, True
            else:
                #Get argmax next state
                next_state = self.get_argmax(get_neigh, aorf_histo)

                return Action(self, next_state), next_state, False
        else:
            #Get argmax next state
            next_state = self.get_argmax(get_neigh, aorf_histo)

            return Action(self, next_state), next_state, False

        
    def get_argmax(self, get_neigh: list, aorf_histo):
        #We select a state where the possible next feature has the maximum AORf
        possible_feature: list = [list(set(neigh.description) - set(self.description))[0] for neigh in get_neigh]
    
        #We determine the max AORf
        feature_max_aorf: list = np.argmax([aorf_histo[1][feat] for feat in possible_feature])

        #We get the max feature
        next_feature: int = possible_feature[feature_max_aorf]

        #We get the next state
        next_state: State = [
            neigh for neigh in get_neigh
            if list(set(neigh.description)-set(self.description)) == [next_feature]
        ][0]

        return next_state

    def get_neighboors(self, feature_structure: dict, feature_list: list) -> list:
        '''
            Returns the list of the neighboors of the current state
        '''
        neigh_depth_graph: int = self.number[0] + 1

        if neigh_depth_graph in feature_structure: 
            existing_neigh: list = [
                state_neigh for state_neigh in feature_structure[neigh_depth_graph]
                if len(list(set(state_neigh.description)-set(self.description))) == 1
            ]

            possible_neigh: list = [
                State([neigh_depth_graph, len(feature_structure[neigh_depth_graph])], self.description + [feature], 0)
                for feature in feature_list
                if feature not in self.description and not np.any([set(self.description + [feature])==set(neigh.description) for neigh in existing_neigh])
            ]

            return existing_neigh + possible_neigh
        else:
            possible_neigh: list = [
                State([neigh_depth_graph, 0], self.description + [feature], 0)
                for feature in feature_list
                if feature not in self.description
            ]
        
            return possible_neigh

    def update_v_value(self, alpha: float, gamma: float, next_state) -> float:
        '''
            Update the v_value of a state
        '''
        self.v_value += alpha * ((next_state.reward - self.reward) + gamma * next_state.v_value - self.v_value)   
        
    def is_final(self, nb_of_features: int) -> bool:
        '''
            Check if a state is a final state (with all the features in the state)

            Returns True if all the possible features are in the state
        '''
        if len(self.description) == nb_of_features:
            return True
        else:
            return False

    def is_equal(self, compared_state) -> bool:
        '''
            Compare if two State objects are equal

            Returns True if yes else returns False
        '''
        if set(self.description) == set(compared_state.description):
            return True
        else:
            return False

@dataclass
class Action:
    '''
        Action Object
    '''
    state_t: State
    state_next: State              

    def get_aorf(self, aor_historic: list) -> float:
        '''
        Update the ARO of a feature

        Return the AOR table
        '''
        #We get the feature played and information about it
        chosen_feature: int = list(set(self.state_next.description)-set(self.state_t.description))[0]

        nb_played: int = aor_historic[0][chosen_feature] + 1    
        aorf_value: float = aor_historic[1][chosen_feature]

        aor_new = aor_historic.copy()

        #We update the value
        aor_new[0][chosen_feature] = nb_played
        aor_new[1][chosen_feature] = ((nb_played-1) * aorf_value + self.state_t.v_value) / nb_played

        return aor_new

@dataclass
class FeatureSelectionProcessV3:
    '''
        Init aor list such that aor = [[np.zeros(nb_of_features)], [np.zeros(nb_of_features)]]

    '''
    nb_of_features: int
    eps: float
    alpha: float
    gamma: float

    #Memory of AORf [[nb f is selected], [AOR value]]
    aor: list

    #Init the state structure
    feature_structure: dict


    def pick_random_state(self) -> State:
        '''
            Select a random state in all the possible state space
            
            Return a state randomly picked
        '''
        #Check if the dict is empty
        if bool(self.feature_structure) == True:
            random_depth: int = np.random.choice(list(self.feature_structure.keys()))
            random_state: State = np.random.choice(self.feature_structure[random_depth])

            return random_state, False
        else:
            return self.start_from_empty_set()

    def start_from_empty_set(self) -> State:
        '''
            Start from the empty set (with no feature selected)
            
            Returns the empty initial state
        '''
        depth = 0
        if not bool(self.feature_structure):
            return State([0, 0], [], 0, 0.75), True
        else:
            return self.feature_structure[depth][0], True

    def add_to_historic(self, visited_state: State):
        '''
            Add to the feature structure historic function
        '''
        state_depth: int = visited_state.number[0]

        #We increment the number of visit of the current state
        if visited_state.description != []:
            visited_state.nb_visited += 1

        if state_depth in self.feature_structure:
            #If there is a key associated to the state depth
            is_already_existing: list = [
                state_searching for state_searching in self.feature_structure[state_depth]
                if visited_state.is_equal(state_searching)
            ]

            if not is_already_existing:
                #If the state is not already registered
                self.feature_structure[state_depth].append(visited_state)
            else:
                #The state already exists
                #We remove the existing state and replace it by the new one
                self.feature_structure[state_depth].remove([
                    state_rem for state_rem in self.feature_structure[state_depth]
                    if visited_state.is_equal(state_rem)
                ][0])
                self.feature_structure[state_depth].append(visited_state)
        else:
            #The layer does not exist, we can simply add it
            self.feature_structure[state_depth] = [visited_state]


    def get_final_aor_sorted(self) -> list:
        '''
            Returns the aor table sorted by ascending

            Index of the feature
            Number of time the feature has been played
            Value of the feature
            Best feature (from the lowest to the biggest)
        '''

        index: list = [i for i in range(self.nb_of_features)]
        nb_played: list = self.aor[0]
        values: list = self.aor[1]

        index, values = zip(*sorted(zip(index, values)))

        return [index, nb_played, values, np.argsort(self.aor[1])]


    
    

    

    