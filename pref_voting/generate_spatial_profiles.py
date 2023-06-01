import numpy as np
from pref_voting.spatial_profiles import SpatialProfile



def generate_covariance(n_dimensions, std, rho):
    """
    Generates a covariance matrix for a multivariate normal distribution with the given standard deviation and correlation coefficient.

    Parameters
    ----------
    n_dimensions : int
        The number of dimensions.
    std : float
        The standard deviation.
    rho : float
        The correlation coefficient.

    Returns
    -------
    cov : numpy.ndarray
        The covariance matrix for a multivariate normal distribution.
    """
    assert std > 0, "Standard deviation must be positive"
    assert rho >= 0 and rho <= 1, "Correlation coefficient must be between 0 and 1"
    assert n_dimensions > 0, "Number of dimensions must be positive"

    cov = (std**2) * (np.eye(n_dimensions) + rho * (np.ones((n_dimensions, n_dimensions)) - np.eye(n_dimensions)))
    
    return cov

def generate_spatial_profile(num_cands, num_voters, num_dims, cand_cov = None, voter_cov = None): 

    """ 
    Generates a spatial profile with the candidate and voter positions generated by a multivariate normal distribution with num_dims dimensions and cand_cov the covariance matrix for candidates and voter_cov the covariance matrix for voters.

    Parameters
    ----------
    num_cands : int
        The number of candidates.
    num_voters : int
        The number of voters.
    num_dims : int  
        The number of dimensions.
    cand_cov : numpy.ndarray, optional
        The covariance matrix for the multivariate normal distribution for candidates. The default is None.
    voter_cov : numpy.ndarray, optional
        The covariance matrix for the multivariate normal distribution for voters. The default is the identity matrix.
    
    Returns
    -------
    SpatialProfile  
        A spatial profile with the candidate and voter positions generated by a multivariate normal distribution with num_dims dimensions and cand_cov the covariance matrix for candidates and voter_cov the covariance matrix for voters.

    """
    cand_cov = np.eye(num_dims) if cand_cov is None else cand_cov
    voter_cov = np.eye(num_dims) if voter_cov is None else voter_cov

    assert num_dims == cand_cov.shape[0] == cand_cov.shape[1], "Candidate covariance matrix must be square and have the same number of dimensions as the number of dimensions specified"
    assert num_dims == voter_cov.shape[0] == voter_cov.shape[1], "Voter covariance matrix must be square and have the same number of dimensions as the number of dimensions specified"

    cand_mean = np.zeros(num_dims)
    voter_mean = np.zeros(num_dims)

    cand_sample = np.random.multivariate_normal(cand_mean, cand_cov, size=num_cands)
    voter_sample = np.random.multivariate_normal(voter_mean, voter_cov, size=num_voters)

    return SpatialProfile({c: cand_sample[c] for c in range(num_cands)},
                          {v: voter_sample[v] for v in range(num_voters)})


def generate_spatial_profile_polarized(cand_clusters, voter_clusters):
    """
    Generates a spatial profile with polarized clusters of candidates and voters.   
    
    Parameters
    ----------
    cand_clusters : list
        A list of tuples of the form (mean, covariance, number of candidates) for each cluster of candidates.
    voter_clusters : list
        A list of tuples of the form (mean, covariance, number of voters) for each cluster of voters.

    Returns
    -------
    SpatialProfile
        A spatial profile with polarized clusters of candidates and voters.
    """

    cand_samples = list()
    for cand_cluster in cand_clusters:
        cand_mean, cand_cov, num_cands = cand_cluster
        cand_sample = np.random.multivariate_normal(cand_mean, cand_cov, size=num_cands)
        cand_samples += list(cand_sample)

    voter_samples = list()
    for voter_cluster in voter_clusters:
        voter_mean, voter_cov, num_voters = voter_cluster
        voter_sample = np.random.multivariate_normal(voter_mean, voter_cov, size=num_voters)
        voter_samples += list(voter_sample)

    return SpatialProfile({cidx: np.array(cand_samples[cidx]) 
                           for cidx in range(len(cand_samples))},
                           {vidx: np.array(voter_samples[vidx]) 
                            for vidx in range(len(voter_samples))})