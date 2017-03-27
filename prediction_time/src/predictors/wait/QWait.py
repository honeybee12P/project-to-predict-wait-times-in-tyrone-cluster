import math, sys, os
from time import clock, time
from operator import mul
import numpy
import random
from scipy.stats import pearsonr
import scipy
import scipy.cluster.vq
import scipy.spatial.distance
from sklearn.cluster import KMeans
dst = scipy.spatial.distance.euclidean
import matplotlib.pyplot as plt
#from sklearn import svm
from sklearn import preprocessing
from sklearn.cluster import DBSCAN
from sklearn.cluster import dbscan
import pylab as pl
from sklearn import linear_model 
from numpy.linalg import cond as COND_NUMBER
np = numpy

test_trace = "Tyrone"
test_history_size = 5000 
test_target_start_point_in_trace = 5000 
TARGET_SIZE = 16000 #jobs to test

# Clustering defn
test_epsilon = 0.01
test_minpts = 3

# SD Minimizer 
test_top_x_percent = 1.0/100.0
test_distance_threshold = 0.4
test_step_size = 0.04

# Distance function
test_use_distribution = False
test_use_weights_for_distributions = True

# Other methods
test_regression_distance = 0.6
test_weighted_avg_neighbour_count = 1
test_ridge_regularization_constant = 0.1

test_growing_window = False  # False is fixed size moving window
test_remove_outlier = True 
test_outlier_fraction = 0.3

class WaitPredictor():
    def __init__(self):
        self.historyJobs = []
        self.ENABLE_DISTRIBUTIONS = test_use_distribution

    def addHistoryJob(self, hjob):
        self.historyJobs.append(hjob)
        self.historyJobs.pop(0)

    def getPrediction(self, job, queuedJobs, RunningJobs):
        prediction_list = [] ; distance_map = {}
        ##
	# DISTR: Compute distributions and their bin edges for current job
	##
        distribution_distance = {}
        distribution_summary = {}
        distribution_bin_values = []
        distribution_bin_values_map = {}
        distribution_waits = []
        history_count = 0
        DCount = sum(self.selected_distribution_list)
        max_dist_list = [-float('inf')]*DCount

        individual_distance_map = {}
        individual_wait_times = {}
        print job_id, 'Queue:', self.queue_id_map[self.__queue_id[job_id]]
        history_job_id_list=[]
	
        ## Calculate distribution distances for all relevant jobs -- begin
        if self.ENABLE_DISTRIBUTIONS:
            # We need to fill up the distribution_distance array with normalized distance value for each of the 6 distributions.
            # Find histogram of the current job and add extra bins at the left and right end.
            # Find histogram for each past job using the bin limits derived for the current job
            # Compute distance for each histogram of each past job
            # Normalize the distances using the maximum and fill up the array
            
            # Unweighted case
            distr_correlation_output = [1.0]*DCount
            if test_use_weights_for_distributions:
                distr_correlation_output = self.get_correlation_vector_local(job_id)
                distribution_distance = self.compute_distribution_distances(job_id)
