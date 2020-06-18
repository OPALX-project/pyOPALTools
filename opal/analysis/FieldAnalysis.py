import numpy as np

class FieldAnalysis:

    def sum(self, var, step=0):
        data = self.ds.getData(var, step)
        return np.sum(data)

    def max(self, var, step=0):
        data = self.ds.getData(var, step)
        return np.max(data)

    def total_charge(self, step=0):
        dx = self.ds.get_mesh_spacing(step)
        volume = dx[0] * dx[1] * dx[2]
        return self.sum('rho', step) * volume
