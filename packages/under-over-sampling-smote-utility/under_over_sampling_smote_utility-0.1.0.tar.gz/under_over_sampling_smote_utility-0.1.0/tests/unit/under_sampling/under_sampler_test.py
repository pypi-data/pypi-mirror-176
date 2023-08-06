
from over_under_sampler.under_sampling.under_sampler import UnderSampler
from tests.unit.prepare_test_data import SamplingTestData

input_param_dict_1 = {'sampling_strategy':'auto'}
input_param_dict_2 = {'sampling_strategy':'auto', 'n_neighbors':3, 'kind_sel':'all', 'threshold_cleaning':0.5}


def test_get_under_sampled_data_condensed_nn():
    under_sampler = UnderSampler(input_param_dict_1, "CondensedNearestNeighbourSampler")
    X, Y= SamplingTestData().get_classification_data()
    x_res, y_res = under_sampler.get_under_sampled_data(X, Y)
    print("--------" + str(len(X)))
    assert (len(X) > len(x_res))
    assert (len(Y) > len(y_res))

def test_get_under_sampled_data_condensed_random():
    under_sampler = UnderSampler(input_param_dict_1, "RandomUnderSampler")
    X, Y= SamplingTestData().get_classification_data()
    x_res, y_res = under_sampler.get_under_sampled_data(X, Y)
    print("--------" + str(len(X)))
    assert (len(X) > len(x_res))
    assert (len(Y) > len(y_res))


def test_get_under_sampled_data_condensed_neighbour():
    under_sampler = UnderSampler(input_param_dict_2, "NeighbourhoodCleaningRule")
    X, Y= SamplingTestData().get_classification_data()
    x_res, y_res = under_sampler.get_under_sampled_data(X, Y)
    print("--------" + str(len(X)))
    assert (len(X) > len(x_res))
    assert (len(Y) > len(y_res))

def test_get_under_sampled_data_condensed_tomelinks():
    under_sampler = UnderSampler(input_param_dict_1, "TomekLinks")
    X, Y= SamplingTestData().get_classification_data()
    x_res, y_res = under_sampler.get_under_sampled_data(X, Y)
    print("--------" + str(len(X)))
    assert (len(X) > len(x_res))
    assert (len(Y) > len(y_res))