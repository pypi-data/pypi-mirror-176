from over_under_sampler.utilites.yaml_reader import read_yaml_file


def test_read_yaml_file():
    yaml_file_details = read_yaml_file("resources/sampler_properties.yaml")
    print(yaml_file_details)
    input_loc= yaml_file_details['file_locations']['input_feature_file_location']
    output_loc=yaml_file_details['file_locations']['output_feature_file_location']
    assert(input_loc != None)
    assert (output_loc != None)