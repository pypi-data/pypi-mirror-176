import abc

class BaseTransport(abc.ABC):

    def __init__(self,
                 csv_file_path,
                 *args,
                 **kwargs
                 ):
        self.csv_file_path = csv_file_path
    @abc.abstractmethod
    def run(self):
        pass
