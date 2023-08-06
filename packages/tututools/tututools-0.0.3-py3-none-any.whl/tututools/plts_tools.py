from matplotlib import pyplot as plt

class plt_stack(object):
    def __init__(self) -> None:
        self.figs = []

    def append(self, img):
        self.figs.append(img)
    
    def show(self):
        rows = 1
        cols = len(self.figs)
        id_sum = rows*100 + cols*10
        for i,f in enumerate(self.figs):
            plt.subplot(id_sum+i+1)
            plt.imshow(f)
        plt.show()

