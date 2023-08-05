#
# Gary Davenport
# dovedweller@gmail.com
# 8/2/2021
#
# This Object, FlowFrame inherets from Frame.
# I added methods:
#           'addWidget'
#           'destroyWidgets'
#           'organizeWidgetsWithGrid'
#           'organizeWidgetsWithPlace'
#           'stopOrganizingWidgets'
# I added mode='place' and mode='grid' to choose algorithm
#
# Make sure the instance of the frame is made to expand
# into parent container for the FlowFrame to work correctly.
#
from tkinter import Frame


class FlowFrame(Frame):
    def __init__(self, *args, **kwargs):
        self.mode = kwargs.pop('mode', 'grid')
        super().__init__(*args, **kwargs)
        if self.mode != "place": self.mode="grid"
        self.widgets = []

    def organizeWidgetsWithGrid(self):
        self.stopOrganizingWidgets()

        slaves = self.pack_slaves()
        for slave in slaves:
            slave.pack_forget()
        for slave in slaves:
            slave.grid()

        slaves = self.place_slaves()
        for slave in slaves:
            slave.place_forget()
        for slave in slaves:
            slave.grid()

        self.update()
        self.update_idletasks()

        self._reorganizeWidgetsWithGrid()
        self.bind("<Configure>", lambda event: self._reorganizeWidgetsWithGrid())
        self._reorganizeWidgetsWithGrid()

    def organizeWidgetsWithPlace(self):
        self.stopOrganizingWidgets()

        slaves = self.pack_slaves()
        for slave in slaves:
            slave.pack_forget()
        for slave in slaves:
            slave.place(x=0, y=0)

        slaves = self.grid_slaves()
        for slave in slaves:
            slave.grid_forget()
        for slave in slaves:
            slave.place(x=0, y=0)

        self.update()
        self.update_idletasks()

        self._reorganizeWidgetsWithPlace()
        self.bind("<Configure>", lambda event: self._reorganizeWidgetsWithPlace())
        self._reorganizeWidgetsWithPlace()

    def stopOrganizingWidgets(self):
        self.unbind("<Configure>")

    def addWidget(self, widget, **kwargs):
        # get the names of all widgets and place in list
        self.widgetChildList = []
        for child in self.children:
            self.widgetChildList.append(child)

        # add the new widget to the list
        self.widgetChildList.append(widget)

        if self.mode == "place":
            self.stopOrganizingWidgets()
            self.bind("<Configure>",lambda event: self._reorganizeWidgetsWithPlace())
            self._reorganizeWidgetsWithPlace()
        else:
            self.stopOrganizingWidgets()
            self.bind("<Configure>",lambda event: self._reorganizeWidgetsWithGrid())
            self._reorganizeWidgetsWithGrid()

    def destroyWidgets(self):
        # get the names of all widgets in the frame and place in list
        self.widgetChildList = []
        for child in self.children:
            self.widgetChildList.append(child)

        # destroy the widgets
        for i in range(len(self.children)):
            self.children[self.widgetChildList[i]].destroy()

        # reset list to empty
        self.widgetChildList = []

    def _reorganizeWidgetsWithGrid(self):
        widgetsFrame = self
        widgetDictionary = widgetsFrame.children
        widgetKeys = []  # keys in key value pairs of the childwidgets

        for key in widgetDictionary:
            widgetKeys.append(key)

        for i in range(len(widgetDictionary)):
            if i == 0:  # place first widget in 0,0
                widgetDictionary[widgetKeys[i]].grid(row=0, column=0)
            else:
                lastWidgetsRow = widgetDictionary[widgetKeys[i-1]].grid_info()["row"]
                lastWidgetsColumn = widgetDictionary[widgetKeys[i-1]].grid_info()["column"]
                width = widgetsFrame.grid_bbox(row=0, column=0, row2=lastWidgetsRow, col2=lastWidgetsColumn)[2]
                # if adding the widget pushes the widget past the frame edge, go to next row column 0
                if width+widgetDictionary[widgetKeys[i]].winfo_width() > widgetsFrame.winfo_width():
                    row = widgetDictionary[widgetKeys[i-1]].grid_info()["row"] + 1
                    column = 0
                    widgetDictionary[widgetKeys[i]].grid(row=row, column=column)
                # if adding the widget does not go past the widget, add it to the next column same row
                else:
                    row = widgetDictionary[widgetKeys[i-1]].grid_info()["row"]
                    column = widgetDictionary[widgetKeys[i-1]].grid_info()["column"] + 1
                    widgetDictionary[widgetKeys[i]].grid(row=row, column=column)
            # update to make sure widths etc accurate
            widgetsFrame.update()
            widgetsFrame.update_idletasks()

    def _reorganizeWidgetsWithPlace(self):
        widgetsFrame = self
        widgetDictionary = widgetsFrame.children
        widgetKeys = []  # keys in key value pairs of the childwidgets

        for key in widgetDictionary:
            widgetKeys.append(key)

        width = 0
        i = 0
        x = 0
        y = 0
        height = 0
        maxheight = 0
        while i < len(widgetDictionary):
            height = widgetDictionary[widgetKeys[i]].winfo_height()
            if height > maxheight:
                maxheight = height

            width = width + widgetDictionary[widgetKeys[i]].winfo_width()

            # always place first widget at 0,0
            if i == 0:
                x = 0
                y = 0
                width = widgetDictionary[widgetKeys[i]].winfo_width()

            # if after adding width, this exceeds the frame width, bump
            # widget down.  Use maximimum height so far to bump down
            # set x at 0 and start over with new row
            elif width > widgetsFrame.winfo_width():
                y = y + maxheight
                x = 0
                width = widgetDictionary[widgetKeys[i]].winfo_width()
                maxheight = height

            # if after adding width, the widget row length does not exceed
            # frame with, add the widget at the start of last widget's
            # x value

            else:
                x = width-widgetDictionary[widgetKeys[i]].winfo_width()

            # place the widget at the determined x value
            widgetDictionary[widgetKeys[i]].place(x=x, y=y)
            i += 1
        widgetsFrame.update()
