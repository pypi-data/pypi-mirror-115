import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.signal import savgol_filter
import scipy
import math

def move_overlaps(bss, signal, fs):
   return None



def get_percentage_overlap(b1, b2):
    return None


def subsume_overlaps(bss, thresh=0.8):
    return None


def postprocess(bss, signal, sf):
    return None


def find_breaths(signal, sf):
    return None

def smooth(signal, win_size=51):
    return None

def de_trend(signal):
    return None


def get_breath_template(duration, sf=1):
    return None


def acf_unbiased(window):
    return None


def sig_corr(window, sin):
    return None


def skip(i, skip_amount, overlap):
    return None


def get_periodicity_candidates(window, length_pdf, sf):
    return None


def sine_fit_bss(signal, sampling_frequency, window_size=8,
                overlap=0.4, skip_overlap=0.95,
                correlation_threshold=0.75,
                probability_cutoff=0.0001, length_pdf=None):
    return None

def estimate_run_time(signal, sf):
    return None


if __name__ == '__main__':
    return None