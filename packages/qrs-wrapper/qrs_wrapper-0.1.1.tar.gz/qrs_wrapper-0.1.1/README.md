# QRS-Wrapper

## Overview
QRS-Wrapper is a python library which:
- wraps several open source QRS detection python libraries
- includes a meta algorithm built on top of those open-source algorithms which is supposed to outperform them 
- provides some metrics to assess the quality of those algorithms as well as a nice visualization in a PDF file.

## Installation of QRS-Wrapper
```bash
pip install qrs-wrapper
```

## Getting started
Import qrs-wrapper and load data
```python
>>> import qrs_wrapper as qw
>>> ecg_data, groundtruth_qrs = qw.load_csv('path/to/your/csv')
```


Run existing open source qrs-detection algorithms, for instance:
```python
>>> estimated_qrs_1 = qw.qrs_estimation(ecg_data, library="biosppy", method="hamilton")
>>> estimated_qrs_2 = qw.qrs_estimation(ecg_data, library="neurokit", method="default")
>>> estimated_qrs_3 = qw.qrs_estimation(ecg_data, library="py-ecg-detectors", method="hamilton")
```


Run meta qrs-detection algorithm
```python
>>> estimated_qrs_meta = qw.qrs_meta(ecg_data, (estimated_qrs_1, estimated_qrs_2, estimated_qrs_3))
```
Users can specify the weight of the estimators: qw.qrs_meta(..., weight = usr_weight).
By default, it is computed from the prediction they make and how it compares to the other estimators' prediction.

The predictions and estimators' weight help define a likelyhood score for each potential location.

qrs_meta is running a local search and a simutated annealing for which users can also specify the parameters: 
qw.qrs_meta(..., param = usr_param).

The objective function to optimize is a function of the likelyhood score of the selected locations and of the regularity
of the solution. The regularity is itself linear combination of the regularity of the R peaks amplitude 
and of the delays between consecutive R peaks. 
The regularity of the features are measured locally by computung the coefficient of variation cv(X)=std(X)/mean(X) 
on small sequences of R peaks all over the solution.

By default, the parameters of SA and local search are as follows:
param = {
	"temp_ini" : 830,				# initial temperature
      "max_iter" : 5000,			# nb. iterations in simulated annealing
      "cooling_rate" : 0.9989,		# cooling rate at each iteration
      "sigma" : 800,				# weight of the location's score
      "rho" : 200,				# weight of the regularity (gathers amplitude + delay)
      "alpha" : 1,				# weight of the amplitude regularity
      "delta" : 3					# weight of the delay (between consecutive r peaks) regularity
}

All parameters are interconnected and had been tuned. 
It is not recommanded to stray from the default values.



Compute and plot performance metrics
```python
>>> qw.draw_performance(
    ecg_data,
    groundtruth_qrs,
    (estimated_qrs_1, estimated_qrs_2, estimated_qrs_3, estimated_qrs_meta),
    names = ("biosspy", "neurokit", "py-ecg-detectors", "meta"),
    output_file="path/to/your/report.pdf"
)
```