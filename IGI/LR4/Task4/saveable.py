import matplotlib.pyplot as plt

class SaveableMixin:
    def draw(self, savefile = ""):
        if savefile:
            plt.savefig(savefile)
        plt.show()