import logging

from imblearn.combine import SMOTEENN, SMOTETomek


class UPAndDownSampler:
    """
     This is a base class for smote over sampler i.e. generating synthetic data using existing sample data
    """
    def __init__(self, input_dict, algo_name):
        logging.info("------Algorithm called is --------" + algo_name)
        self.under_over_sampler = self.get_over_under_sampler_from_algo_name(algo_name, input_dict)

    def get_sampled_data(self,  X, Y):
        logging.info(self.under_over_sampler.fit(X, Y))
        X, Y = self.under_over_sampler.fit_resample(X, Y)
        return X, Y

    def get_over_under_sampler_from_algo_name(self, algo_name, input_dict):

        if algo_name=="SMOTEENN":
            return SMOTEENN(**input_dict)
        elif algo_name=="SMOTETomek":
            return SMOTETomek(**input_dict)
        else:
            return None
