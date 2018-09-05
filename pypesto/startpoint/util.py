def rescale(points, lb, ub):
    """
    Rescale points from [0, 1] to [lb, ub].
    
    Parameters
    ----------

    points: ndarray, shape=(n_starts, dim)
        Points in bounds [lb, ub]

    lb, ub: ndarray, shape=(1, dim)
        The boundaries, all components must be finite.
    """
    rescaled_points = points * (ub - lb) + lb
    return rescaled_points
