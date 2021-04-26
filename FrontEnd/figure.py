import sys
import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5 import QtWidgets

# Personnal modules
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


# Personnal modules
from drag import DraggablePoint

class MyGraph(FigureCanvas):

    """A canvas that updates itself every second with a new plot."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)

        self.axes.grid(True)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # To store draggable points
        self.list_points = {'left': [], 'head': [], 'right': []}


        self.show()
        self.plotDraggablePoints()


    def plotDraggablePoints(self, size=0.05):

        """Plot and define the 2 draggable points of the baseline"""
  
        self.list_points['left'].append(DraggablePoint(self, 'left', 0.2, 0.35, size))
        self.list_points['left'].append(DraggablePoint(self, 'left', 0.3, 0.5, size))
        self.list_points['left'].append(DraggablePoint(self, 'left', 0.4, 0.65, size))
        self.list_points['left'].append(DraggablePoint(self, 'left', 0.4, 0.40, size))
        self.list_points['left'].append(DraggablePoint(self, 'left', 0.4, 0.25, size))
        self.list_points['left'].append(DraggablePoint(self, 'left', 0.4, 0.10, size))

        self.list_points['head'].append(DraggablePoint(self, 'head', 0.5, 0.75, size))

        self.list_points['right'].append(DraggablePoint(self, 'right', 0.8, 0.35, size))
        self.list_points['right'].append(DraggablePoint(self, 'right', 0.7, 0.5, size))
        self.list_points['right'].append(DraggablePoint(self, 'right', 0.6, 0.65, size))
        self.list_points['right'].append(DraggablePoint(self, 'right', 0.6, 0.40, size))
        self.list_points['right'].append(DraggablePoint(self, 'right', 0.6, 0.25, size))
        self.list_points['right'].append(DraggablePoint(self, 'right', 0.6, 0.10, size))



        self.updateFigure()


    def updateFigure(self):

        """Update the graph. Necessary, to call after each plot"""

        self.draw()



if __name__ == '__main__':
    app = QApplication([])
    win = QWidget()
    layout = QGridLayout()
    layout.addWidget(MyGraph())
    win.setLayout(layout)
    win.show()
    sys.exit(app.exec_())
