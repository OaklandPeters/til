"""
Todo: adapt this to support non-uniformly spaced points
THEN make a til/ about it
"""

import numpy
from matplotlib import pyplot
from pylab import plot, bar, show

def days(sequence):
    return [days for days, weight in sequence]

def weights(sequence):
    return [weight for days, weight in sequence]

def normalize(sequence):
    total = sum(weights(sequence))
    return [(day, weight/total) for day, weight in sequence]

def summation(sequence):
    """Should already be normalized."""
    return sum(day*weight for day, weight in sequence)

def expectation(sequence):
    """Presumes evenly spaced data points.
    Needs to adjust equation for normalize and summation otherwise.
    """
    return summation(normalize(sequence))


# Esimated Days, Likelyhood-Weight
outcomes = [
    (0.0, 0.0),
    (1.0, 1.0),
    (2.0, 3.0),
    (3.0, 6.0),
    (4.0, 4.5),
    (5.0, 4.0),
    (6.0, 3.5),
    (7.0, 2.9),
    (8.0, 1.5),
]

distribution = normalize(outcomes)

plot(days(distribution), weights(distribution))
show()
