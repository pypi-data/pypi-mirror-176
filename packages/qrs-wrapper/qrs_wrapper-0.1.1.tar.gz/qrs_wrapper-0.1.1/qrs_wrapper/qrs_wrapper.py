#!/usr/bin/env python
# coding: utf-8

## UTIL LIBRARIES
import numpy as np
import pandas as pd
from copy import deepcopy
import matplotlib.pyplot as plt

## QRS DETECTION LIBRARIES
from biosppy.signals import ecg
import neurokit2 as nk
from ecgdetectors import Detectors

# LOAD CATALOGUE AND ASSOCIATED METHODS
from qrs_wrapper.wrapper_map import CATALOGUE_DETECTORS, WRAPPER_MAP


## LOADING ECG FROM CSV FILE
def load_csv(path):
    """
        Return the array of values of ecg for every time steps 
        and the array of time steps (or location) that correspond to r peaks.
    """
    reader = pd.read_csv(path)
    dic_csv = reader.to_dict()
    ecg_data = np.array([dic_csv["ecg"][i] for i in range(len(dic_csv["ecg"]))])
    groundtruth_qrs = np.array([i for i in range(len(dic_csv["is_r_peak"])) if dic_csv["is_r_peak"][i]==1])
    
    return ecg_data, groundtruth_qrs


## DETECTION OF QRS VIA EXISTING LIBRARIES
def qrs_estimation(ecg_raw, library, method, cleaner = None, sampling_rate = 1000):
    """
        Process a raw ecg signal (array) to find r_peaks with the given method of the given library.
        User can add a specific cleaner method for the neurokit library. 
        Sampling rate is 1kHz by default and must match the sampling rate of ecg_raw.
        
        Returns the array of locations where R peaks occur (according to the library/method used).
        
    """ 
    if library in CATALOGUE_DETECTORS.keys() and method in CATALOGUE_DETECTORS[library]:
    
        if library == "biosppy":
            t = ecg.ecg(ecg_raw, sampling_rate = sampling_rate, show = False)

            if method == "default":
                return t["rpeaks"]
            else:
                det_fct = WRAPPER_MAP["biosppy"][method]
                return det_fct(t["filtered"], sampling_rate = sampling_rate)["rpeaks"]

        if library == "neurokit":
            if cleaner:
                ecg_clean = nk.ecg_clean(ecg_raw, sampling_rate = sampling_rate, method = cleaner)
            else:
                cl_name = WRAPPER_MAP["neurokit"][method]["cleaner"]
                ecg_clean = nk.ecg_clean(ecg_raw, sampling_rate = sampling_rate, method = cl_name)
            
            det_name = WRAPPER_MAP["neurokit"][method]["method"]
            _, info = nk.ecg_peaks(ecg_clean, sampling_rate = sampling_rate, method = det_name)
            return info["ECG_R_Peaks"]

        if library == "py-ecg-detectors":
            detectors = Detectors(sampling_rate)
            det_fct = WRAPPER_MAP["py-ecg-detectors"][method](detectors)
            return np.array(det_fct(ecg_raw))
        
    else:
        message = "Sorry, the input library is unknown or the input method name does not match any method for this library."
        + " Available libraries and methods: \n" + str(CATALOGUE_DETECTORS)        
        raise Exception(message)

        
        
## SUBROUTINES FOR qrs_meta.

def get_potential_rpeaks(estim_list):
    """
        Return the array of locations where there are r peaks according to all estimators in estim_list.
        
        It iterates over all estimators' r peak locations list in parallel, 
        selecting the earliest locations first and adding them to the potential r peak locations list.
        
    """

    potential_rpeaks = []
    next_rpeak = [e[0] for e in estim_list] # gives, for each estimator, the next r peak location detected.
    iterator = [1 for e in estim_list] # iterator for each estimator (next index to iterates on).
    
    # when we finish iterating over one estimator, its next r peak is set to a large value, max_time.
    max_time = max([e[-1] for e in estim_list]) + 1 
    
    stop = False
    while not stop:
        # get earliest location among the next r peaks, and indices of estimators that detected it.
        earliest_rpeak = min(next_rpeak)
        detected_by = [k for k in range(len(estim_list)) if next_rpeak[k] == earliest_rpeak]
        
        # update list of potential r peaks and their score.
        potential_rpeaks.append(earliest_rpeak)
        
        # update next_rpeak and iterator.
        for k in detected_by:
            if iterator[k] >= len(estim_list[k]):
                next_rpeak[k] = max_time 
            else:
                next_rpeak[k] = estim_list[k][iterator[k]]
                iterator[k] += 1
                
        # we stop when we finish iterating over all estimators.
        if next_rpeak == [max_time for e in estim_list]:
            stop = True
    
    return potential_rpeaks


def compute_weights(estim_list, potential_rpeaks):
    """
        Compute weight for each estimator. The weights are in [0, len(estim_list)-1].
        The larger the weight, the better the estimator.
        
        The weight of one estimator is based on the number of other estimators that predict the same locations.
        It gathers a measure of accuracy and consensus. 
        It penalizes estimators that find many locations that are found only by itself.
    """
    
    weight = [0 for e in estim_list] 
    iterator = [0 for e in estim_list] # iterator for each estimator (next index to iterates on).
    for t in potential_rpeaks:
        # list of estimators that detected t is a r peak location.
        detected_by = [k for k in range(len(estim_list))                        if iterator[k] < len(estim_list[k]) and estim_list[k][iterator[k]] == t]
        for k in detected_by:
            # increases the weight of the estimator by the nb. of other estimators that detected the same r peak location.
            iterator[k] += 1
            weight[k] += len(detected_by)-1
    
    for k in range(len(weight)):
        weight[k] /= len(estim_list[k]) # divided by the number of total r peaks detected.
    
    return weight 


def compute_score(estim_list, weight, potential_rpeaks):
    """
        Compute score for each potential r peak locations, based on the weights of the estimators that detected them.
        
                score[t] = sum(weight[k] | estimator k detected t is a r peak)
        
        The score is then normalized between -1 and 1.
    """
    
    score = []
    iterator = [0 for e in estim_list] # iterator for each estimator (next index to iterates on).
    for t in potential_rpeaks:
        # list of estimators that detected t is a r peak location.
        detected_by = [k for k in range(len(estim_list))                        if iterator[k] < len(estim_list[k]) and estim_list[k][iterator[k]] == t]
        score.append(sum([weight[k] for k in detected_by]))
        for k in detected_by: 
            iterator[k] += 1
        
    sum_weights = sum(weight)
    for k in range(len(score)):
        score[k] = 2*score[k]/sum_weights -1 # normalized in [-1, 1]
    
    return score


def get_rpeaks_around(potential_rpeaks, x, k, L = 3):
    """
        x is a bit vector, representing a solution: 
            x[t] = 1 iff solution estimates that potential_rpeaks[t] is a r peak location.
        
        k is the index of a bit in x.
        
        L is a parameter for the size of the lists returned.
    
        It returns the list of the L previous and next r peaks, detected in x, from potential_rpeaks[k] (if they exist):
            - before flipping k^th bit in x.
            - after flipping k^th bit.
        
    """
    rpeaks_before = [] # list of r peaks location around index k before flip
    rpeaks_after = [] # idem, after flip
    
    if x[k] == 1:
        rpeaks_before.append(potential_rpeaks[k])
    else:
        rpeaks_after.append(potential_rpeaks[k])
        
    # get the L previous r peaks (if they exist)
    count = 0
    idx = 1
    while k - idx >= 0 and count < L:
        if x[k-idx] == 1:
            rpeaks_before.insert(0, potential_rpeaks[k-idx])
            rpeaks_after.insert(0, potential_rpeaks[k-idx])
            count += 1
        idx += 1
    
    # get the L next r peaks (if they exist)
    count = 0   
    idx = 1
    while k + idx < len(x) and count < L:
        if x[k+idx] == 1:
            rpeaks_before.append(potential_rpeaks[k+idx])
            rpeaks_after.append(potential_rpeaks[k+idx])
            count += 1
        idx += 1 
        
    return rpeaks_before, rpeaks_after


def compute_delay_variation(rpeaks_before, rpeaks_after):
    """
        We use the coefficient of variation (CV) to measure the regularity of the delays between two consecutive r peaks.
            cv(X) = std(X)/mean(X)
        
        Return the difference between the CV before flipping k^th bit and after flipping it.
        The result is negative iff the solution is locally less regular after flipping the k^th bit, 
        regarding the delays between r peaks.
    """

    # special case: too few r peaks, we cannot measure variation
    if len(rpeaks_before) <= 2 or len(rpeaks_after) <= 2:
        return 0.0
    
    # compute delay from r peaks locations
    delay_before = [rpeaks_before[k+1] - rpeaks_before[k] for k in range(len(rpeaks_before)-1)]
    delay_after = [rpeaks_after[k+1] - rpeaks_after[k] for k in range(len(rpeaks_after)-1)]

    # compute coefficient of variation of the delays before after flipping bit k
    cv_before = np.std(delay_before)/np.mean(delay_before)
    cv_after = np.std(delay_after)/np.mean(delay_after)
    
    return cv_before - cv_after


def compute_amplitude_variation(ecg_raw, rpeaks_before, rpeaks_after):
    """
        We use the coefficient of variation (CV) to measure the regularity of the r peaks amplitude.
            cv(X) = std(X)/mean(X)
        
        Return the difference between the CV before flipping k^th bit and after flipping it.
        The result is negative iff the solution is locally less regular after flipping the k^th bit, 
        regarding the amplitude of r peaks.
    """
    
    # special case: too few r peaks, we cannot measure variation
    if len(rpeaks_before) <= 1 or len(rpeaks_after) <= 1:
        return 0.0
    
    # get amplitude of the r peaks before and after flipping the k^th bit.
    amp_before = [ecg_raw[t] for _, t in enumerate(rpeaks_before)]
    amp_after = [ecg_raw[t] for _, t in enumerate(rpeaks_after)]
    
    # compute coefficient of variation of the amplitude before after flipping bit k
    cv_before = np.std(amp_before)/np.mean(amp_before)
    cv_after = np.std(amp_after)/np.mean(amp_after)

    return cv_before - cv_after


def compute_cost(x, k, ecg_raw, potential_rpeaks, score, param):
    """
        Compute the cost of flipping the k^th bit in solution x,
        considering the score of potential_rpeaks[k] and the regularity difference.
        
        param is a dictionary containing weights of the different costs (and some other parameters for simulated annealing):
            - sigma for the cost associated to score
            - delta for the cost associated to delays (between two consecutive r peaks) regularity.
            - alpha for the cost associated to amplitude regularity
            - rho for the cost associated to the total regularity.
    """
    # score cost
    sc_cost = 0
    if x[k] == 0:
        sc_cost += score[k]
    else:
        sc_cost -= score[k]
    
    # regularity cost
    rpeaks_before, rpeaks_after = get_rpeaks_around(potential_rpeaks, x, k)
    reg_cost = param["delta"] * compute_delay_variation(rpeaks_before, rpeaks_after)
    reg_cost += param["alpha"] * compute_amplitude_variation(ecg_raw, rpeaks_before, rpeaks_after)
    
    cost = param["sigma"]*sc_cost + param["rho"] * reg_cost
    
    return cost


def local_search(ecg_raw, potential_rpeaks, score, param, x_ini, printout = True):
    """
        Run a simple local search on solution x: it moves to the best 1-flip neighbor (according to the 1-flip cost)
        until we find a local maximum.
    """
    
    x = deepcopy(x_ini)
    
    stop = False
    while not stop:
        
        # We look for the best neighbor
        best_cost = 0
        best_neighbor = -1
        for k in range(len(x)):
            cost = compute_cost(x, k, ecg_raw, potential_rpeaks, score, param)
            if cost > best_cost:
                best_cost = cost
                best_neighbor = k
                        
        # If it exists, we move onto it
        if best_neighbor >= 0:
            x[best_neighbor] = 1 - x[best_neighbor] # flip
            if printout:
                print("new solution: +"+str(best_cost), ", 1-flip index:", best_neighbor)
        else:
            stop = True # We stop at a local maximum
        
    return x


def simulated_annealing(ecg_raw, potential_rpeaks, score, param, x_ini = None, printout = True):
    """
        Run a simulated annealing metaheuristic to find the r peaks that match the most the estimators' predictions,
        and that maximize some regularity measure, when there is a tie between two potential r peak locations.
        
        A solution x is encoded in a bit vector and is such that x[k] = 1 iff potential_rpeaks[k] is selected.
        At each iteration, we select randomly a 1-flip neighbor of x and evaluate the cost of moving from x to this neighbor.
        If the cost is positive, then we accept the neighbor (we update the current solution to it), 
        otherwise we accept it with probability exp(cost/temp).
        
        Parameter temp is the temperature of the annealing. It cools down as the search is running, which means that, 
        in the beginning of the search, the method accepts more worse solutions, and, in the end, converges to better solutions.
        
        param is a dictionary that gathers many parameters for the simulated annealing:
            - "temp_ini" is the initial temperature of the search.
            - "max_iter" is the maximum number of iterations of the main loop.
            - "cooling_rate" is the rate for decreasing the temperature from one iteration to the next one.
        
    """
    
    # initialization of the solution
    if x_ini:
        x = deepcopy(x_ini)
    else:
        x = np.random.randint(0, 2, len(potential_rpeaks))
        
    # we do not have a function to compute the objective value of a solution
    # we only have a function that computes the variation of it,
    # so we initialize the objective value to an arbitrary value.
    obj = 5000

    # storing best solution found
    x_best = deepcopy(x)
    obj_best = obj
    
    # Main loop
    temp = param["temp_ini"] # initial temperature
    for i in range(param["max_iter"]):
        
        # select next neighbor to test
        k = np.random.randint(0, len(x))
        
        # cost of moving to next neighbor
        cost = compute_cost(x, k, ecg_raw, potential_rpeaks, score, param)
        
        # acceptance stage
        proba_accept = np.exp(cost/temp)
        if np.random.rand() < proba_accept:
            x[k] = 1 - x[k] # flip
            obj += cost # objective value update
            
            # update best solution found if new objective is greater than obj_best
            if obj_best < obj:
                obj_best = obj
                x_best = deepcopy(x)
                if printout:
                    print("Iteration", i+1)
                    print("Better solution found: +"+str(cost))

        # cooling stage
        temp *= param["cooling_rate"]
        
    return x_best


def qrs_meta(ecg_raw, estim_list, weight = None, param = None):
    """
        This function produces an estimation of the r peaks locations based on top of other estimations.
        
            - ecg_raw : initial raw ecg signal.
            - estim_list : list (array or tuple) of estimation for the r peaks locations. 
            - weight : user can input weight for each estimator.
            - param : parameters for simulated annealing.
        
        The selection of the most likely r peak locations is done with a combinatorial optimization method.
        A solution of the problem is a subset of the potential r peaks locations found by all estimators in estim_list.
        The objective function we want to optimize is a function of:
            - the likeliness (score) of r peak locations, that depends on the weight of the estimators that detected them.
            - the local regularity, i.e. the variation of the delay among consecutive r peaks and the amplitude variation.
        
        We use local search to find a better solution than all estimators.
        Then, we use a simulated annealing to further optimize our solution.
        
    """
    
    # Fix r peaks locations (remove small offsets)
    fixed_estim_list = []
    for e in estim_list:
        fixed_estim_list.append(ecg.correct_rpeaks(signal = ecg_raw, rpeaks = e, tol = 0.1)["rpeaks"])

    # Get potential r peaks locations from the union of fixed_estim
    potential_rpeaks = get_potential_rpeaks(fixed_estim_list)
    
    # Compute weights for each estimator
    if not weight:
        weight = compute_weights(fixed_estim_list, potential_rpeaks)

    # Get best estimation
    best_estim = fixed_estim_list[np.argmax(weight)]
    
    # Compute score for each potential r peaks location (normalized in [-1, 1])
    score = compute_score(fixed_estim_list, weight, potential_rpeaks)
    
    # Parameters for simulated annealing
    if not param:
        param = {
            "temp_ini" : 830,
            "max_iter" : 5000,
            "cooling_rate" : 0.9989,
            "sigma" : 800,
            "rho" : 200,
            "alpha" : 1,
            "delta" : 3
        }
    
    # First solution initialized to the best estimator's prediction
    x_ini = [0 for t in potential_rpeaks]
    idx = 0
    for t in best_estim:
        while potential_rpeaks[idx] < t:
            idx += 1
        x_ini[idx] = 1
        idx += 1

    # Local search on x_ini
    print("Local search...")
    print("    can take a few minutes if initial solution is far from a local maximum")
    x_ini = local_search(ecg_raw, potential_rpeaks, score, param, x_ini)
    
    # Run simulated annealing
    print("Simulated annealing...")
    sol = simulated_annealing(ecg_raw, potential_rpeaks, score, param, x_ini = x_ini)
    meta_rpeaks = [potential_rpeaks[t] for t in range(len(sol)) if sol[t] == 1]
    
    return meta_rpeaks


## PERFORMANCE COMPARISON (VISUALISATION)
def get_nb_match(ref_rpeaks, estim):
    """
        Return the number of r peaks from ref_rpeaks that are found by estim.
    """
    count = 0
    idx = 0
    for t in estim:
        while idx<len(ref_rpeaks) and ref_rpeaks[idx] < t:
            idx += 1
        if idx == len(ref_rpeaks):
            break
        if ref_rpeaks[idx] == t:
            count += 1
    return count


def draw_performance(ecg_raw, ref_rpeaks, estim_list, names, output_file, tol = 0.05):
    """
        Draw and save in output_file the performance of each estimator in estim_list, regarding the r peak locations reference.
        The output is a bar chart in which is represented:
            - the number of r peaks locations found exactly (0 ms).
            - the number of r peaks locations detected with tolerance tol.
            - the number of wrong r peaks detected.
    """
    # get number of locations found exactly
    exact = []
    for e in estim_list:
        exact.append(get_nb_match(ref_rpeaks, e))
    
    # get number of locations found with tolerance tol
    true_positive = []
    for k, e in enumerate(estim_list):
        fe = ecg.correct_rpeaks(signal = ecg_raw, rpeaks = e, tol = tol)["rpeaks"]
        true_positive.append(get_nb_match(ref_rpeaks, fe) - exact[k])
        
    # get number of wrong r peaks
    wrong_peaks = []
    for k, e in enumerate(estim_list):
        wrong_peaks.append(len(e) - exact[k] - true_positive[k])
        
    
    N = len(estim_list)
    ind = np.arange(N)  
    
    # Create plot and bars
    fig = plt.subplots(figsize = (15, 10))
    width = 0.45
    p1 = plt.bar(ind, exact, width)
    p2 = plt.bar(ind, true_positive, width, bottom = exact)
    p3 = plt.bar(ind, wrong_peaks, width, bottom = true_positive)

    # Labels, ticks, legend,...
    plt.ylabel('R Peaks Detected')
    plt.title('Performance of R Peaks Estimators')
    plt.xticks(ind, names)
    max_ytick = int(max([len(e) for e in estim_list])*1.3)
    plt.yticks(np.arange(0, max_ytick , int(max_ytick/1000)*100))
    plt.legend((p1[0], p2[0], p3[0]), ('exact', 'true positive w. tol='+str(tol), 'wrong R peaks'))
    
    # Line for ref r peaks
    plt.axline((0,len(ref_rpeaks)), slope = 0, color = "red", linestyle = "--", )
    plt.text(0, len(ref_rpeaks)+50, s = "ref R peaks", color ="red")
    
    # Save figure in output file
    plt.savefig(output_file)
    plt.show()

