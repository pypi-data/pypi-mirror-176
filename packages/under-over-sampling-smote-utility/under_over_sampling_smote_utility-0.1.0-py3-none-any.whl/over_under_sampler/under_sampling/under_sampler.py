import logging

from imblearn.under_sampling import CondensedNearestNeighbour, RandomUnderSampler, NeighbourhoodCleaningRule, TomekLinks


class UnderSampler:
    """
     This is a base class for smote under sampler
    """

    def __init__(self, input_dict, algo_name):
        logging.info("------Algorithm called is --------" + algo_name)
        self.down_sampler = self.get_downsampler_from_algo_name(algo_name, input_dict)

    def get_under_sampled_data(self, X, Y):
        logging.info(self.down_sampler.fit(X, Y))
        x_res, y_res = self.down_sampler.fit_resample(X, Y)
        return x_res, y_res

    def get_downsampler_from_algo_name(self, algo_name, input_dict):

        if algo_name == "CondensedNearestNeighbourSampler":
            return CondensedNearestNeighbour(**input_dict)
        elif algo_name == "RandomUnderSampler":
            return RandomUnderSampler(**input_dict)
        elif algo_name == "NeighbourhoodCleaningRule":
            return NeighbourhoodCleaningRule(**input_dict)
        elif algo_name == "TomekLinks":
            return TomekLinks(**input_dict)
        else:
            return None
