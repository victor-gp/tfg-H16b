import matplotlib.pyplot as plt

class Trajectory:
    def __init__(self):
        self.xs = []
        self.ys = []
        self.timespan = []

    def new_point(self, x, y, time):
        self.xs.append(x)
        self.ys.append(y)
        self.timespan.append(time)


    def print(self):
        for x, y, t in zip(self.xs, self.ys, self.timespan):
            print(f'{t}: {x}, {y}')

    def print_for_gnuplot(self):
        for x, y in zip(self.xs, self.ys):
            print(f'{x} {y}')


    def to_dict(self):
        return {
            '__trajectory__': True,
            'xs': self.xs,
            'ys': self.ys,
            'timespan': self.timespan
        }

    @classmethod
    def from_dict(cls, dict):
        if '__trajectory__' not in dict:
            raise RuntimeError('not a Trajectory dict')

        restored_trajectory = cls.__new__(cls)
        restored_trajectory.xs = dict['xs']
        restored_trajectory.ys = dict['ys']
        restored_trajectory.timespan = dict['timespan']

        return restored_trajectory


    def plot(self, save_path=""):
        plt.plot(self.xs, self.ys)
        plt.xlabel('x')
        plt.ylabel('y')

        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()
