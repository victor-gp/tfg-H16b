import numpy as np
import matplotlib.pyplot as plt

from app.models.discrete_plane import DiscretePlane

class Heatmap:
    def __init__(self, scan_params):
        self.map_space = scan_params.projection_space
        self.incidence_map = np.zeros(self.map_space.dimension(), dtype=int)


    def project(self, x, y):
        coordinates = self.map_space.projection_coordinates(x, y)

        if coordinates is not None:
            map_x, map_y = coordinates
            self.incidence_map[map_x, map_y] += 1


    def to_dict(self):
        return {
            '__heatmap__': True,
            'map_space': self.map_space.to_dict(),
            'incidence_map': self.incidence_map.tolist()
        }

    @classmethod
    def from_dict(cls, dict):
        if '__heatmap__' not in dict:
            raise RuntimeError('not a Heatmap dict')

        restored_heatmap = cls.__new__(cls)
        restored_heatmap.map_space = DiscretePlane.from_dict(dict['map_space'])
        restored_heatmap.incidence_map = np.array(dict['incidence_map'])

        return restored_heatmap


    def plot(self, save_path=""):
        res_x, res_y = self.map_space.projection_resolution()

        normalized_heatmap = self.incidence_map / self.total_points() / res_x / res_y

        im = plt.imshow(normalized_heatmap.transpose(),
                        cmap='hot', aspect='auto', origin='lower',
                        extent=self.map_space.extent())

        plt.xlabel('x')
        plt.ylabel('y')
        plt.colorbar(im)

        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()

    def total_points(self):
        return np.sum(self.incidence_map)
