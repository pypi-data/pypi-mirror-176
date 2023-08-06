from over_under_sampler.over_sampling.over_sampler import OverSampler
from tests.unit.prepare_test_data import SamplingTestData

input_param_dict_1 = {'sampling_strategy':'auto', 'random_state': 999}
input_param_dict_2 = {'sampling_strategy':'auto', 'random_state': 999, 'm_neighbors':10}


def test_get_over_sampled_data_knn():
    over_sampler = OverSampler(input_param_dict_1, "Kmean")
    X, Y = SamplingTestData().get_classification_data()
    x_res, y_res = over_sampler.get_over_sampled_data(X, Y)
    print("--------" + str(len(X)))
    assert (len(X) < len(x_res))
    assert (len(Y) < len(y_res))


def test_get_over_sampled_data_adasync():
    over_sampler = OverSampler(input_param_dict_1, "ADASYN")
    X, Y = SamplingTestData().get_classification_data()
    x_res, y_res = over_sampler.get_over_sampled_data(X, Y)
    print("--------" + str(len(X)))
    assert (len(X) < len(x_res))
    assert (len(Y) < len(y_res))


def test_get_over_sampled_data_svm():
    over_sampler = OverSampler(input_param_dict_1, "SVMSMOTE")
    X, Y = SamplingTestData().get_classification_data()
    x_res, y_res = over_sampler.get_over_sampled_data(X, Y)
    print("--------" + str(len(X)))
    assert (len(X) < len(x_res))
    assert (len(Y) < len(y_res))


def test_get_over_sampled_data_border_line():
    over_sampler = OverSampler(input_param_dict_2, "BorderlineSMOTE")
    X, Y = SamplingTestData().get_classification_data()
    x_res, y_res = over_sampler.get_over_sampled_data(X, Y)
    print("--------" + str(len(X)))
    assert (len(X) < len(x_res))
    assert (len(Y) < len(y_res))
