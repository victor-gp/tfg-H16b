import numpy as np
import matplotlib.pyplot as plt
import logging

from app.models.discrete_plane import DiscretePlane

class InterloopScanMap:
    def __init__(self, scan_params):
        map_resolution = 10 ** -2
        min_x, max_x, min_y, max_y = scan_params.scan_space.extent()

        self.map_space = DiscretePlane(
            min_x, max_x, map_resolution, min_y, max_y, map_resolution
        )

        # inbound is marked as 0, outbound is marked as 1.
        self.tendency_map = np.zeros(self.map_space.dimension(), dtype=int)

        # to normalize at the end.
        self.counts_map = np.zeros(self.map_space.dimension(), dtype=int)


    def project(self, x, y, bit):
        #logging.info(f'{x}, {y}: {bit}')
        coordinates = self.map_space.projection_coordinates(x, y)

        if coordinates is not None:
            map_x, map_y = coordinates

            self.tendency_map[map_x, map_y] += bit
            self.counts_map[map_x, map_y] += 1


    def to_dict(self):
        return {
            '__interloop_scan_map__': True,
            'map_space': self.map_space.to_dict(),
            'tendency_map': self.tendency_map.tolist(),
            'counts_map': self.counts_map.tolist()
        }

    @classmethod
    def from_dict(cls, dict):
        if '__interloop_scan_map__' not in dict:
            raise RuntimeError('not an InterloopScanMap dict')

        restored_scan_map = cls.__new__(cls)
        restored_scan_map.map_space = DiscretePlane.from_dict(dict['map_space'])
        restored_scan_map.tendency_map = np.array(dict['tendency_map'])
        restored_scan_map.counts_map = np.array(dict['counts_map'])

        return restored_scan_map


    def plot(self, save_path=""):
        averaged_map = np.divide(self.tendency_map, self.counts_map)

        im = plt.imshow(averaged_map.transpose(),
                        cmap='viridis', aspect='auto', origin='lower',
                        extent=self.map_space.extent())

        plt.xlabel('x')
        plt.ylabel('y')
        plt.colorbar(im)

        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()
