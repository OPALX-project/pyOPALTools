import matplotlib.pyplot as plt

class BasePlotter:
    
    def __init__(self):
        pass
    
    @property
    def ds(self):
        """
        Implemented in each dataset. Each dataset
        has to return self.
        """
        pass
