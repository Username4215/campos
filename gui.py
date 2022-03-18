import tkinter

from tkinter import NW, Button, Label, LEFT, Frame, Canvas
from PIL import ImageTk

from separate import Dataset, line
from solve import PosSolver


class W(tkinter.Tk):

    def __init__(self, datasets):
        super().__init__()
        self.solver = PosSolver()

        self.currentIndex = 0
        self.current_dataset: Dataset = datasets[self.currentIndex]
        self.solver.dataset = self.current_dataset
        self.datasets = datasets
        self._fc_canvas_id = None
        self._fc_coord = None
        self._fc_down = False
        self._axis = 0
        _w, _h = self.winfo_screenwidth(), self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (_w, _h))

        self._canvas = Canvas(self, width=_w, height=_h)
        self.toolframe = Frame(self)
        self.statsframe = Frame(self)
        self.initButtons()
        self.setBackgroundImage()

        self.toolframe.pack()
        self.statsframe.pack()
        self._canvas.pack()

        self.connectDelegates()

    def setDataset(self, set: Dataset):
        self.current_dataset = set
        self._canvas.delete("all")
        self.setBackgroundImage()
        self.solver.dataset = self.current_dataset

        for l in self.current_dataset.lines:
            self.draw_line(l)

    def setBackgroundImage(self):
        self.tmpimg = ImageTk.PhotoImage(self.current_dataset.imagedata)
        self._canvas.create_image(0, 0, anchor=NW, image=self.tmpimg)

    # connect to motion event dings
    def motion(self, event):

        if self._fc_down:
            if self._fc_coord is not None:
                x, y = event.x, event.y
                a, b = self._fc_coord
                t = self._canvas.create_line(x, y, a, b, fill=self.axisColor(), width=3)
                if self._fc_canvas_id is not None:
                    self._canvas.delete(self._fc_canvas_id)
                self._fc_canvas_id = t
            else:
                self._fc_coord = event.x, event.y

        self.lbl_coords.config(text="Position x%d y%d" % (event.x, event.y))


    def updateStats(self):
        x = self.solver.solve()
        self.lbl_accuracy.config(text=x)



    def axisColor(self, axis=None):
        if axis is not None:
            if axis == 0:
                return "red"
            if axis == 1:
                return "green"
            if axis == 2:
                return "blue"
        if self._axis == 0:
            return "red"
        if self._axis == 1:
            return "green"
        if self._axis == 2:
            return "blue"

    def initButtons(self):
        self.btn_save = Button(self.toolframe, text="save (S)")
        self.btn_save.pack(side=LEFT)

        self.btn_prev = Button(self.toolframe, text="<-")
        self.btn_prev.pack(side=LEFT)

        self.btn_next = Button(self.toolframe, text="-> (Space)")
        self.btn_next.pack(side=LEFT)

        self.btn_clear = Button(self.toolframe, text="clear (Esc)")
        self.btn_clear.pack(side=LEFT)

        self.btn_undo = Button(self.toolframe, text="undo (U)")
        self.btn_undo.pack(side=LEFT)

        self.btn_x = Button(self.toolframe, text="X-axis (1)")
        self.btn_x.pack(side=LEFT)

        self.btn_y = Button(self.toolframe, text="Y-axis (2)")
        self.btn_y.pack(side=LEFT)

        self.btn_z = Button(self.toolframe, text="Z-axis (3)")
        self.btn_z.pack(side=LEFT)

        self.lbl_accuracy = Label(self.statsframe, text="HELLO")
        self.lbl_accuracy.pack(side=LEFT)

        self.lbl_coords = Label(self.statsframe, text="Position x0 y0")
        self.lbl_coords.pack(side=LEFT)

    def clicked(self, event):
        if self._fc_coord is None:
            self._fc_coord = event.x, event.y
            self._fc_down = True
        else:
            a, b = self._fc_coord
            x, y = event.x, event.y
            l = line(a, b, x, y, self._axis, None)
            self.current_dataset.lines.append(line(a, b, x, y, self._axis, self.draw_line(
                l)))  # tuples sind immutable, darum erneuter constructor call statt l zu verwenden, kp was die sich dabei denken ....
            self._fc_coord = None
            self._fc_down = False
            self.updateStats()

    def draw_line(self, t):
        return self._canvas.create_line(t.x1, t.y1, t.x2, t.y2, fill=self.axisColor(t.axis), width=2)

    def abortDraw(self, _):
        self._fc_down = False
        self._canvas.delete(self._fc_canvas_id)
        self._fc_coord = None

    def nextAxis(self, _):
        self._axis += 1
        self._axis %= 3

    def nextDataset(self, _):
        self.currentIndex += 1
        self.currentIndex %= len(self.datasets)
        self.setDataset(self.datasets[self.currentIndex])

    def bindAxisButton(self, axis):
        def innerfunction(_):
            self._axis = axis

        return innerfunction

    def connectDelegates(self):
        self._canvas.bind('<Motion>', self.motion)
        self._canvas.bind("<Button-1>", self.clicked)
        self.bind("<Button-2>", self.abortDraw)
        self.bind("<Button-3>", self.abortDraw)

        self.bind("<space>", self.nextDataset)

        self.bind("1", self.bindAxisButton(0))
        self.bind("2", self.bindAxisButton(1))
        self.bind("3", self.bindAxisButton(2))
        self.btn_x.bind(self.bindAxisButton(0))
        self.btn_y.bind(self.bindAxisButton(1))
        self.btn_z.bind(self.bindAxisButton(2))
