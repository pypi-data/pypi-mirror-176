from over_under_sampler.up_and_down_sampling.under_over_sampler import UPAndDownSampler
from tests.unit.prepare_test_data import SamplingTestData

input_param_dict_1 = {'sampling_strategy':'auto'}


def test_get_under_sampled_data_condensed_nn():
    under_sampler = UPAndDownSampler(input_param_dict_1, "SMOTEENN")
    X, Y= SamplingTestData().get_classification_data()
    x_res, y_res = under_sampler.get_sampled_data(X, Y)
    print("--------" + str(len(X)))
    assert (len(X) != len(x_res))
    assert (len(Y) != len(y_res))

def test_get_under_sampled_data_condensed_random():
    under_sampler = UPAndDownSampler(input_param_dict_1, "SMOTETomek")
    X, Y= SamplingTestData().get_classification_data()
    x_res, y_res = under_sampler.get_sampled_data(X, Y)
    print("--------" + str(len(X)))
    assert (len(X) != len(x_res))
    assert (len(Y) != len(y_res))