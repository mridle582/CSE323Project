from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton
from PyQt5.QtWidgets import QApplication, QMainWindow

class FrontEnd:

    def __init__(self):
        self.app = QApplication([])
        self.win = QWidget()
        self.layout = QGridLayout()
        self.da_graph = MyGraph()

    def set_gui(self):

        self.layout.addWidget(self.da_graph, 1, 1)
        search_button = QPushButton('Search')
        self.layout.addWidget(search_button, 0, 1)

        reset_button = QPushButton('Reset')
        reset_button.clicked.connect(self.reset)
        self.layout.addWidget(reset_button,2,1)

        self.layout.addWidget(MyGraph(), 1, 2)

        self.win.setLayout(self.layout)
        self.win.show()

    def run_gui(self):
        self.app.exec_()

    def reset(self):
        self.layout.addWidget(MyGraph(), 1, 1)







import matplotlib
matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5 import QtWidgets


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







import matplotlib.patches as patches
from matplotlib.lines import Line2D


class DraggablePoint:

    lock = None #  only one can be animated at a time

    def __init__(self, parent, body_part, x=0.1, y=0.1, size=0.1):

        self.parent = parent
        self.point = patches.Ellipse((x, y), size, size, fc='#3f3f3f', alpha=0.5, edgecolor='#282828') if body_part != 'head' else patches.Ellipse((x, y), 2*size, 2*size, fc='#3f3f3f', alpha=0.5, edgecolor='#282828')
        self.x = x
        self.y = y
        parent.fig.axes[0].add_patch(self.point)
        self.press = None
        self.background = None
        self.body_part = body_part
        self.connect()
        
        # if another point already exist we draw a line
        if self.parent.list_points[body_part]:
            line_x = [self.parent.list_points[body_part][-1].x, self.x]
            line_y = [self.parent.list_points[body_part][-1].y, self.y]

            self.line = Line2D(line_x, line_y, color='r', alpha=0.5)
            parent.fig.axes[0].add_line(self.line)

        elif self.body_part == 'head':
            self.line = Line2D([0,0], [0,0], color='#000000', alpha=1)
            parent.fig.axes[0].add_line(self.line)


    def connect(self):

        'connect to all the events we need'

        self.cidpress = self.point.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.point.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.point.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)


    def on_press(self, event):

        if event.inaxes != self.point.axes: return
        if DraggablePoint.lock is not None: return
        contains, attrd = self.point.contains(event)
        if not contains: return
        self.press = (self.point.center), event.xdata, event.ydata
        DraggablePoint.lock = self

        # draw everything but the selected rectangle and store the pixel buffer
        canvas = self.point.figure.canvas
        axes = self.point.axes
        self.point.set_animated(True)
        
        # TODO also the line of some other points needs to be released
        point_number =  self.parent.list_points[self.body_part].index(self)

        if self.body_part == 'head':
            self.line.set_animated(True)
        
        elif self == self.parent.list_points[self.body_part][0]:
            self.parent.list_points[self.body_part][1].line.set_animated(True)            
        elif self == self.parent.list_points[self.body_part][-1]:
            self.line.set_animated(True)            
        else:
            self.line.set_animated(True)            
            self.parent.list_points[self.body_part][point_number+1].line.set_animated(True)                
            

        canvas.draw()
        self.background = canvas.copy_from_bbox(self.point.axes.bbox)

        # now redraw just the rectangle
        axes.draw_artist(self.point)

        # and blit just the redrawn area
        canvas.blit(axes.bbox)


    def on_motion(self, event):

        if DraggablePoint.lock is not self:
            return
        if event.inaxes != self.point.axes: return
        self.point.center, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        self.point.center = (self.point.center[0]+dx, self.point.center[1]+dy)

        canvas = self.point.figure.canvas
        axes = self.point.axes

        # restore the background region
        canvas.restore_region(self.background)

        # redraw just the current rectangle
        axes.draw_artist(self.point)
        
        point_number =  self.parent.list_points[self.body_part].index(self)
        self.x = self.point.center[0]
        self.y = self.point.center[1]
        

        if self.body_part == 'head':
            axes.draw_artist(self.line)    
        
        # We check if the point is A or B        
        elif self == self.parent.list_points[self.body_part][0]:
            # or we draw the other line of the point
            self.parent.list_points[self.body_part][1].line.set_animated(True)
            axes.draw_artist(self.parent.list_points[self.body_part][1].line)
        
        elif self == self.parent.list_points[self.body_part][-1]:
            # we draw the line of the point            
            axes.draw_artist(self.line)    

        else:
            # we draw the line of the point
            axes.draw_artist(self.line)
            #self.parent.list_points[self.body_part][point_number+1].line.set_animated(True)
            axes.draw_artist(self.parent.list_points[self.body_part][point_number+1].line)
            
        
        if self.body_part == 'head':
            print('moved head')
        elif self == self.parent.list_points[self.body_part][0]:
            # The first point is especial because it has no line
            line_x = [self.x, self.parent.list_points[self.body_part][1].x]
            line_y = [self.y, self.parent.list_points[self.body_part][1].y]      
            # this is were the line is updated
            self.parent.list_points[self.body_part][1].line.set_data(line_x, line_y)
            
        elif self == self.parent.list_points[self.body_part][-1]:
            line_x = [self.parent.list_points[self.body_part][-2].x, self.x]
            line_y = [self.parent.list_points[self.body_part][-2].y, self.y]
            self.line.set_data(line_x, line_y)        
        else:
            # The first point is especial because it has no line
            line_x = [self.x, self.parent.list_points[self.body_part][point_number+1].x]
            line_y = [self.y, self.parent.list_points[self.body_part][point_number+1].y]      
            # this is were the line is updated
            self.parent.list_points[self.body_part][point_number+1].line.set_data(line_x, line_y)
            
            line_x = [self.parent.list_points[self.body_part][point_number-1].x, self.x]
            line_y = [self.parent.list_points[self.body_part][point_number-1].y, self.y]
            self.line.set_data(line_x, line_y)        

        # blit just the redrawn area
        canvas.blit(axes.bbox)


    def on_release(self, event):

        'on release we reset the press data'
        if DraggablePoint.lock is not self:
            return

        self.press = None
        DraggablePoint.lock = None

        # turn off the rect animation property and reset the background
        self.point.set_animated(False)
        
        point_number =  self.parent.list_points[self.body_part].index(self)

        if self.body_part == 'head':
            self.line.set_animated(False) 

        elif self == self.parent.list_points[self.body_part][0]:
            self.parent.list_points[self.body_part][1].line.set_animated(False)            
        elif self == self.parent.list_points[self.body_part][-1]:
            self.line.set_animated(False)            
        else:
            self.line.set_animated(False)            
            self.parent.list_points[self.body_part][point_number+1].line.set_animated(False)       
            

        self.background = None

        # redraw the full figure
        self.point.figure.canvas.draw()

        self.x = self.point.center[0]
        self.y = self.point.center[1]

    def disconnect(self):

        'disconnect all the stored connection ids'

        self.point.figure.canvas.mpl_disconnect(self.cidpress)
        self.point.figure.canvas.mpl_disconnect(self.cidrelease)
        self.point.figure.canvas.mpl_disconnect(self.cidmotion)
