import matplotlib.pyplot as plt

class SignChangeSparseMap:

    def __init__(self):
        self.x_plus = []
        self.x_minus = []
        self.y_plus = []
        self.y_minus = []


    def add_right_change(self, x, y):
        self.x_plus.append([x, y])

    def add_left_change(self, x, y):
        self.x_minus.append([x, y])

    def add_up_change(self, x, y):
        self.y_plus.append([x, y])

    def add_down_change(self, x, y):
        self.y_minus.append([x, y])


    def to_dict(self):
        return {
            '__sign_change_sparse_map__': True,
            'x_plus': self.x_plus,
            'x_minus': self.x_minus,
            'y_plus': self.y_plus,
            'y_minus': self.y_minus,
        }

    @staticmethod
    def from_dict(dict):
        if '__sign_change_sparse_map__' not in dict:
            raise RuntimeError('not a SignChangeSparseMap dict')

        restored_sparse_map = SignChangeSparseMap()
        restored_sparse_map.x_plus = dict['x_plus']
        restored_sparse_map.x_minus = dict['x_minus']
        restored_sparse_map.y_plus = dict['y_plus']
        restored_sparse_map.y_minus = dict['y_minus']

        return restored_sparse_map


    def plot(self, save_path=""):
        [xs, ys] = [[i for i, j in self.x_plus], [j for i, j in self.x_plus]]
        plt.plot(xs, ys, 'y.')
        [xs, ys] = [[i for i, j in self.x_minus], [j for i, j in self.x_minus]]
        plt.plot(xs, ys, 'r.')
        [xs, ys] = [[i for i, j in self.y_plus], [j for i, j in self.y_plus]]
        plt.plot(xs, ys, 'g.')
        [xs, ys] = [[i for i, j in self.y_minus], [j for i, j in self.y_minus]]
        plt.plot(xs, ys, 'b.')

        plt.xlabel('x')
        plt.ylabel('y')

        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()
