
from glob import glob

from gui import W
from separate import Dataset


def resetDataset():
    l = []
    for x in glob("resources/*"):
        l.append(Dataset(x))
    #with open("set1.dat", "wb") as f:
       # pickle.dump(l, f)
    return l


if __name__ == "__main__":
    # resetDataset()
   # with open("set1.dat", "rb") as f:
    dset = resetDataset()#pickle.load(f)
    window = W(dset)
    window.mainloop()
