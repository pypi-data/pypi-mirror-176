from matplotlib import pyplot as plt

class plt_stack(object):
    def __init__(self) -> None:
        self.figs = []

    def append(self, img):
        self.figs.append(img)
    
    def show(self, labels:list = None, fontdict: dict = None, save_name:str = None):
        rows = 1
        cols = len(self.figs)
        id_sum = rows*100 + cols*10
        for i,f in enumerate(self.figs):
            plt.subplot(id_sum+i+1)
            if labels != None:
                plt.xlabel(labels[i], fontdict=fontdict)
                plt.yticks(fontproperties='Times New Roman', size=fontdict['size'])
                plt.xticks(fontproperties='Times New Roman', size=fontdict['size'])
            plt.imshow(f)
        if save_name != None:
            plt.savefig("./{}.png".format(save_name), dpi=480, bbox_inches='tight')
        plt.show()
