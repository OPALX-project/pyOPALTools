import math
import pylab as pl


def distance(x1, x2, y1, y2):
    return math.hypot(x1 - x2, y1 - y2)


"""
Callback for matplotlib to display an annotation when points are clicked on.
The point which is closest to the click and within xtol and ytol is identified.

@See http://www.scipy.org/Cookbook/Matplotlib/Interactive_Plotting for
details.

Register this function like this:

scatter(xdata, ydata)
af = AnnoteFinder(xdata, ydata, annotes)
connect('button_press_event', af)
"""

class AnnoteFinder:

    def __init__(self, rdata, obj1_idx, obj2_idx, annotes_idx,
                 name_to_column_map,
                 axis=None, xtol=None, ytol=None):

        self.name_to_column_map = name_to_column_map

        max_varname_len = 0
        for i, _ in name_to_column_map.items():
            max_varname_len = max(max_varname_len, len(i))

        #FIXME: take into account figure width/height
        self.item_height = 0.013
        self.box_width = (max_varname_len + 8) * 0.013


        self.rdata = rdata
        xdata = self.rdata[:, obj1_idx]
        ydata = self.rdata[:, obj2_idx]

        # maps a (x, y) point to an annotation index
        self.data = zip(xdata, ydata, annotes_idx)
        self.x_max = max(xdata)
        self.y_max = max(ydata)
        self.x_min = min(xdata)
        self.y_min = min(ydata)

        if xtol is None:
            xtol = ((self.x_max - self.x_min) / float(len(xdata))) / 2
        if ytol is None:
            ytol = ((self.y_max - self.y_min) / float(len(ydata))) / 2
        self.x_tol = xtol
        self.y_tol = ytol

        if axis is None:
            self.axis = pl.gca()
        else:
            self.axis = axis

        self.drawnAnnotations = {}
        self.links = []


    def __call__(self, event):

        if event.inaxes:
            clickX = event.xdata
            clickY = event.ydata
        if self.axis is None or self.axis == event.inaxes:
            annotes = []
        for x, y, idx in self.data:
            if clickX - self.x_tol < x < clickX + self.x_tol and \
               clickY - self.y_tol < y < clickY + self.y_tol:
                d = distance(x, clickX, y, clickY)
                annotes.append((d, x, y, idx))
        if annotes:
            annotes.sort()
            _ , x, y, annote_idx = annotes[0]
            self.drawAnnote(event.inaxes, x, y, annote_idx)
            for l in self.links:
                l.drawSpecificAnnote(annote_idx)


    def getAnchor(self, x, y):

        x_rel = (x - self.x_min) / (self.x_max - self.x_min)
        y_rel = (y - self.y_min) / (self.y_max - self.y_min)

        if x_rel < 0.5:
            x_rel += 0.01
        else:
            x_rel -= self.box_width

        if y_rel < 0.5:
            y_rel += 0.01
        else:
            y_rel -= 1.00 * len(self.name_to_column_map) * self.item_height

        x = x_rel * (self.x_max - self.x_min) + self.x_min
        y = y_rel * (self.y_max - self.y_min) + self.y_min

        return (x, y)


    def drawAnnote(self, axis, x, y, annote_idx):

        if (x, y) in self.drawnAnnotations:
            markers = self.drawnAnnotations[(x, y)]
            for m in markers:
                m.set_visible(not m.get_visible())
            self.axis.figure.canvas.draw()
        else:
            (x_shifted, y_shifted) = self.getAnchor(x, y)

            t = axis.text(x_shifted, y_shifted,
                          "%s"%(self.listifyData(annote_idx)),
                          bbox=dict(boxstyle='round,pad=0.3',
                          fc='orange', alpha=0.9))
            m = axis.scatter([x], [y], marker='d', c='r', zorder=100)
            self.drawnAnnotations[(x, y)] = (t, m)
            self.axis.figure.canvas.draw()


    def drawSpecificAnnote(self, annote):
        annotesToDraw = [(x, y, idx) for x, y, idx in self.data if idx == annote]
        for x, y, idx in annotesToDraw:
            self.drawAnnote(self.axis, x, y, idx)


    def listifyData(self, idx):
        pretty_data = [""] * len(self.name_to_column_map)
        data = self.rdata[idx, :]
        for i, d in self.name_to_column_map.items():
            name = i.lstrip('%')
            pretty_data[d] = ("$" + name + " = " + str(data[d]) + "$ \\\\")

        return "".join(pretty_data)
