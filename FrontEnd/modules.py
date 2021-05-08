from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QMainWindow, QComboBox, QLabel, QHBoxLayout
import webbrowser

fg = "background-color: #a89984"

class FrontEnd:

    def __init__(self):
        self.app = QApplication([])
        self.app.setApplicationName("CSE323-Project")
        self.win = QWidget()
        self.win.setFixedSize(500, 600)
        self.win.setStyleSheet("background-color: #282828;")
        self.layout = QGridLayout()
        self.layout.setColumnStretch(0,1)
        self.layout.setColumnStretch(6,1)
        self.da_graph = MyGraph()
        self.i = 0
        self.search_criteria = "None"

    def set_gui(self):

        self.layout.addWidget(self.da_graph, 1, 1)

        # Sets up the drop down menu box
        option_box = QComboBox()
        box_bg = QHBoxLayout()
        label  = QLabel('Focus Search:')
        label.setFixedSize(100, 20)
        label.setStyleSheet("QLabel { color : #a89984;  }")
        option_box.addItem('None')
        option_box.addItem('Upper')
        option_box.addItem('Lower')
        option_box.setFixedSize(100, 20)
        option_box.setStyleSheet(fg)
        option_box.activated[str].connect(self.set_search_criteria)
        box_bg.addWidget(label)
        box_bg.addWidget(option_box)
        self.layout.addLayout(box_bg, 2, 1)
        
        reset_button = QPushButton('Reset')
        reset_button.setStyleSheet(fg)
        reset_button.clicked.connect(self.reset)
        self.layout.addWidget(reset_button, 3, 1)

        search_button = QPushButton('Search')
        search_button.setStyleSheet(fg)
        search_button.clicked.connect(self.update_result)
        self.layout.addWidget(search_button, 4, 1)

#       Where the URL will go
        result_button = QPushButton("")
        result_button.setStyleSheet(fg)
        self.layout.addWidget(result_button, 5, 1)

        self.win.setLayout(self.layout)
        self.win.show()

    def run_gui(self):
        self.app.exec_()

    def reset(self):
        self.da_graph = MyGraph()
        self.layout.addWidget(self.da_graph, 0, 0)

    def update_result(self):
        from BackEnd import compareposes
        posedata = self.get_points()
        pose = compareposes.Pose()
        pose.head = posedata[1]
        print(pose.head[0])
        pose.leftShoulder = posedata[0][2]
        pose.rightShoulder = posedata[2][2]
        pose.leftElbow = posedata[0][1]
        pose.rightElbow = posedata[2][1]
        pose.leftWrist = posedata[0][0]
        pose.rightWrist = posedata[2][0]
        pose.leftHip = posedata[0][3]
        pose.rightHip = posedata[2][3]
        pose.leftKnee = posedata[0][4]
        pose.rightKnee = posedata[2][4]
        pose.leftAnkle = posedata[0][5]
        pose.rightAnkle = posedata[2][5]
        url = compareposes.get_closestpose(pose)
        result_button = QPushButton(str(url)[:30]+"...")
        result_button.setStyleSheet(fg)
        result_button.clicked.connect(lambda: webbrowser.open_new_tab(url))
        self.layout.addWidget(result_button, 3, 0)

    # Returns a list of lists, where each sublist contains tuples representing the body parts
    # So the first index of the first list, is the left hand, the next index would be the left elbow, etc.
    def get_points(self):
        left_vertices = self.da_graph.list_points['left']
        left_pts = [] #x,y points from hand to foot order
        for v in left_vertices:
            point = [v.x, v.y]
            left_pts.append(point)

        head_vertex = self.da_graph.list_points['head']
        head_pt = [head_vertex[0].x, head_vertex[0].y]

        right_vertices = self.da_graph.list_points['right']
        right_pts = [] # same and left points but for the right side
        for v in right_vertices:
            point = [v.x, v.y]
            right_pts.append(point)

        return [left_pts, head_pt, right_pts]

    def set_search_criteria(self, criteria):
        self.search_criteria = criteria
        print(self.search_criteria)



import matplotlib
matplotlib.use("Qt5Agg")

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from PyQt5 import QtWidgets


class MyGraph(FigureCanvas):

    """A canvas that updates itself every second with a new plot."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.fig.set_facecolor("#282828")


        self.axes = self.fig.add_subplot(111)

        self.axes.set_facecolor("#3c3836")

        self.axes.grid(False)

        self.axes.get_xaxis().set_visible(False)
        self.axes.get_yaxis().set_visible(False)

        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        # To store draggable points
        self.list_points = {'left': [], 'head': [], 'right': []}

#        self.show()
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
        self.point = patches.Ellipse((x, y), size, size, fc='#1d2021', alpha=0.5, edgecolor='#ebdbb2') if body_part != 'head' else patches.Ellipse((x, y), 2*size, 2*size, fc='#282828', alpha=0.5, edgecolor='#ebdbb2')
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

            self.line = Line2D(line_x, line_y, color='#d79921', alpha=0.75) if body_part == 'left' else Line2D(line_x, line_y, color='#fb4934', alpha=0.75)

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
            canvas.blit(axes.bbox)
            return
        
        if self == self.parent.list_points[self.body_part][0]:
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
