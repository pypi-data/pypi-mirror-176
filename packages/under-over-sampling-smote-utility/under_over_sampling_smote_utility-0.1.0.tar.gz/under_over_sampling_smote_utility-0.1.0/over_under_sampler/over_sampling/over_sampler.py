import logging

from imblearn.over_sampling import KMeansSMOTE, SVMSMOTE, BorderlineSMOTE, ADASYN


class OverSampler:
    """
     This is a base class for smote over sampler i.e. generating synthetic data using existing sample data
    """
    def __init__(self, input_dict, algo_name):
        logging.info("------Algorithm called is --------" + algo_name)
        self.over_sampler = self.get_oversampler_from_algo_name(algo_name, input_dict)

    def get_over_sampled_data(self,  X, Y):
        logging.info(self.over_sampler.fit(X, Y))
        X, Y = self.over_sampler.fit_resample(X, Y)
        return X, Y

    def get_oversampler_from_algo_name(self, algo_name, input_dict):

        if algo_name=="Kmean":
            return KMeansSMOTE(**input_dict)
        elif algo_name=="SVMSMOTE":
            return SVMSMOTE(**input_dict)
        elif algo_name=="BorderlineSMOTE":
            return BorderlineSMOTE(**input_dict)
        elif algo_name=="ADASYN":
            return ADASYN(**input_dict)
        else:
            return None
