import abc


class Extractor(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _perform_to_authentication(self):
        raise NotImplementedError

    @abc.abstractmethod
    def _parameter_validation(self):
        raise NotImplementedError

    @abc.abstractmethod
    def extract_data_from_source(self):
        raise NotImplementedError