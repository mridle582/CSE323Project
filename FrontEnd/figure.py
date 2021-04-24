import sys
import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5 import QtWidgets, QtGui

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.lines import Line2D

# Personnal modules
from drag import DraggablePoint


class MyGraph(FigureCanvas):

    def __init__(self, parent=None, width=8, height=8, dpi=120): 
        bgcol = parent.palette().window().color().toRgb() if parent is not None else "#000000" 
        bgcol = [bgcol.redF(), bgcol.greenF(), bgcol.blueF()] if parent is not None else "#000000"
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.set_facecolor(bgcol)
        self.axes = self.fig.add_subplot(111)   
        self.axes.grid(False)    
        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)  
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)   
        # To store the 2 draggable points
        self.list_points = [None] * 6
        self.show()
        self.plot_draggable_points()    

    def plot_draggable_points(self, size=0.05):

        # # if another point already exist we draw a line
        # if self.parent.list_points:
        #     line_x = [self.parent.list_points[-1].x, self.x]
        #     line_y = [self.parent.list_points[-1].y, self.y]

        #     self.line = Line2D(line_x, line_y, color='r', alpha=0.5)
        #     parent.fig.axes[0].add_line(self.line)
        # self.list_points[0] = DraggablePoint(self, 0.4, 0.1, size)
        # self.list_points[1] = DraggablePoint(self, 0.4, 0.27, size)
        # self.list_points[2] = DraggablePoint(self, 0.4, 0.44, size)
        # self.list_points[3] = DraggablePoint(self, 0.4, 0.85, size)
        # self.list_points[4] = DraggablePoint(self, 0.25, 0.67, size)
        # self.list_points[5] = DraggablePoint(self, 0.125, 0.67, size)

        top_left = self.list_points[0] = DraggablePoint(self, 0.4, 0.85, size)
        top_right = self.list_points[1] = DraggablePoint(self, 0.6, 0.85, size)
        bottom_right = self.list_points[2] = DraggablePoint(self, 0.6, 0.44, size)
        #bottom_left = self.list_points[3] = DraggablePoint(self, 0.4, 0.44, size)

        top_right.line = Line2D([top_left.x, top_right.x],[top_left.y, top_right.y], color='r', alpha=0.5)
        self.fig.axes[0].add_line(top_right.line)

        bottom_right.line = Line2D([top_right.x, bottom_right.x], [top_right.y, bottom_right.y], color='r', alpha=0.5)
        self.fig.axes[0].add_line(bottom_right.line)

        top_left.line = Line2D([bottom_right.x, top_left.x],[bottom_right.y, top_left.y], color='r', alpha=0.5)
        self.fig.axes[0].add_line(top_left.line)

        # top_left.line = Line2D([bottom_left.x, top_left.x],[bottom_left.y, top_left.y], color='r', alpha=0.5)
        # self.fig.axes[0].add_line(top_left.line)





        self.updateFigure()


    def clearFigure(self):

        self.axes.clear()
        self.axes.grid(False)
        del(self.list_points[:])
        self.updateFigure()


    def updateFigure(self):
        self.draw()

if __name__ == '__main__':

    
    app = QtWidgets.QApplication(sys.argv)
    temp =MyGraph()
    # mw = QtWidgets.QMainWindow()
    # mw.setStyleSheet("background-color:red")
    # mw.setGeometry(0, 0, 300, 300)
    # mw.setCentralWidget(temp)
    
    sys.exit(app.exec_())
