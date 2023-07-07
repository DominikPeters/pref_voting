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

def generate_spatial_profile(num_cands, num_voters, num_dims, cand_cov = None, voter_cov = None, num_profiles = 1): 

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

    cand_samples = np.random.multivariate_normal(cand_mean, cand_cov, size=(num_profiles,num_cands))
    voter_samples = np.random.multivariate_normal(voter_mean, voter_cov, size=(num_profiles,num_voters))

    profs = [SpatialProfile({c: cand_samples[pidx][c] for c in range(num_cands)},
                            {v: voter_samples[pidx][v] for v in range(num_voters)})
                          for pidx in range(num_profiles)]

    return profs[0] if num_profiles == 1 else profs

def generate_spatial_profile_polarized(cand_clusters, voter_clusters, num_profiles = 1):
    """
    Generates a spatial profile with polarized clusters of candidates and voters.   
    
    Parameters
    ----------
    cand_clusters : list
        A list of tuples of the form (mean, covariance, number of candidates) for each cluster of candidates.
    voter_clusters : list
        A list of tuples of the form (mean, covariance, number of voters) for each cluster of voters.
    num_profiles : int, optional
        The number of profiles to generate. The default is 1.

    Returns
    -------
    SpatialProfile
        A spatial profile with polarized clusters of candidates and voters.
    """

    cand_samples = list()
    total_num_cands = 0
    for cand_cluster in cand_clusters:
        cand_mean, cand_cov, num_cands = cand_cluster
        total_num_cands += num_cands
        cluster_samples = np.random.multivariate_normal(cand_mean, cand_cov, 
                                                        size=(num_profiles,num_cands))
        if len(cand_samples) == 0:
            cand_samples = cluster_samples
        else:
            cand_samples = np.concatenate([cand_samples, cluster_samples], axis=1)

    voter_samples = list()
    total_num_voters = 0
    for voter_cluster in voter_clusters:
        voter_mean, voter_cov, num_voters = voter_cluster
        total_num_voters += num_voters
        cluster_samples = np.random.multivariate_normal(voter_mean, voter_cov, 
                                                        size=(num_profiles,num_voters))
        if len(voter_samples) == 0:
            voter_samples = cluster_samples
        else:
            voter_samples = np.concatenate([voter_samples, cluster_samples], axis=1) 

    
    profs = [SpatialProfile({cidx: cand_samples[pidx][cidx]
                           for cidx in range(total_num_cands)},
                           {vidx: voter_samples[pidx][vidx]
                            for vidx in range(total_num_voters)}) 
                            for pidx in range(num_profiles)]
    
    return profs[0] if num_profiles == 1 else profs