
#  dynLineChart - application for showing pyGUI with Line Chart
#  ============   with dynamic data

import random
from GUI import Window, View, Label, Button, Task, Application, Menu
from GUI.StdColors import red, green, black

# definitions of application information
windowTitle = "dynLineChart"

# view layout
polyViewWidth = 200
polyViewHeight = 200
pvheight = 150

# shared views, label, button
view = None;
labelNum = None
stater = None
buttonStop = None

# shared data
data = [];
delta = 5
postest = 0
max_data = 37

# DynLineChartView for dynamic line chart with data
class DynLineChartView(View):
    def draw(self, c, r):
        global data
        c.forecolor = black
        c.fill_rect(r)
        c.forecolor = green
        c.newpath()
        c.moveto(0, pvheight)
        left, top, right, bottom = r
        h = bottom - top
        # print "w=%d,h=%d" % (right - left, h)
        for i in range(len(data)):
            c.lineto(i * 5, h - data[i])
        c.stroke()

def make_label(text, **kwds):
    return Label(text = text, **kwds)

def do_task():
    global view, data, postest, delta,labelNum
    if len(data) == 0:
        for i in range(max_data):
            data.append(0)

    if (postest <= 10):
        delta = 5
    elif (postest >= 100):
        delta = -5

    postest += delta;
    num = postest + random.uniform(1,10)
    data.append(num)
    labelNum.text = "%.2f" % num

    if (len(data) > max_data):
        del(data[0])

    view.invalidate();

task = Task(do_task, 0.5, repeat = 1, start = 0)

def enableButtons(started):
    if (started):
        buttonStart.enabled = False
        buttonStop.enabled = True
    else:
        buttonStart.enabled = True
        buttonStop.enabled = False

def start_task():
    enableButtons(True)
    task.start()

def stop_task():
    enableButtons(False)
    task.stop()

class MainApp(Application):
    def __init__(self):
        Application.__init__(self)


class MainWindow(Window):
    def setup_menus(self, m):
        m.start_cmd.enabled = buttonStart.enabled
        m.stop_cmd.enabled = buttonStop.enabled

    def start_cmd(self):
        start_task()

    def stop_cmd(self):
        stop_task()

# Menu for Action
app_menus = [Menu("Action", [
                ("Start/^S", 'start_cmd'),
                ("-"),
                ("Stop/^O", 'stop_cmd'),
            ])]

def main():
    global view,labelNum, buttonStart, buttonStop

    app = MainApp()

    buttonStart = Button("Start", action = start_task)
    buttonStop = Button("Stop", action = stop_task)
    splitSpace = 30
    labelNum = make_label("0", just = 'center', color=red, width=buttonStart.width*2 + splitSpace);
    labelNumCaption = make_label("Num:", just = 'center', color=red, width=buttonStart.width);

    # set positions for the buttons and labels
    buttonStart.position = (20, 20);
    buttonStop.position = (20 + buttonStart.width + splitSpace, 20);
    labelNum.position = (20, 0)
    labelNumCaption.position = (20, 0)

    # create new window and dynamic linechart view
    view = DynLineChartView(width=polyViewWidth, height=polyViewHeight)
    view.left = buttonStart.left
    view.top = buttonStart.top + buttonStart.height + 5
    win = MainWindow(title = windowTitle)

    # custized layouts
    windowWidth= 20 + polyViewWidth
    windowHeight= 210

    win.size = (windowWidth, windowHeight)

    # add controls
    win.add(labelNum);
    win.add(labelNumCaption);
    win.add(buttonStart);
    win.add(buttonStop);

    # add DynLineChart view
    win.add(view);
    win.menus = app_menus

    # enabled on/off
    enableButtons(False)

    # show window
    win.show()

    app.run()


main()
