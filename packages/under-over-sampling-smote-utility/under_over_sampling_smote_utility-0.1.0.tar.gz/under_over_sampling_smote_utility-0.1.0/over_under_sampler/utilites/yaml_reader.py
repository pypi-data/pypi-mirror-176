import yaml
import logging

def read_yaml_file(file_location):
    with open(file_location, 'r') as stream:
        try:
            parsed_yaml=yaml.safe_load(stream)
            logging.info(parsed_yaml)
            return parsed_yaml
        except yaml.YAMLError as exception:\
            logging.error(exception)