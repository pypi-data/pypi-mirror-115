import statistics
from collections import Counter


def mode(sample):
    """Calculate the mode of a given sample."""
    c = Counter(sample)
    return [k for k, v in c.items() if v == c.most_common(1)[0][1]]


def median(sample):
    """Calculate the median of a given sample."""
    return statistics.median(sample)


def mean(sample):
    """Calculate the mean of a given sample."""
    return statistics.mean(sample)
