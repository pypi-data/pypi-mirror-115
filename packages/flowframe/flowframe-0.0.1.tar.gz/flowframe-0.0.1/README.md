# FlowFrame

### The reason I wrote this module/class:

I think that Python's defacto tkinter GUI program should at least have a geometry manager that offers flow behaviour.  That is -  when the size of the GUI changes, the widgets inside the gui can be responsive in a "flow" manner.  Now tkinter windows are 'responsive' in that the size of the widgets can change and so forth, but my opinion is that a natural responsive design often incorporates 'flow'.  Where as when the window changes, the contents will shift inside the window like a word-wrap.  This is very common in html and the like (there is a flow type geometry manager in Java for example).  Overall, responsiveness to the window size is very important as you just don't know what size screen your program will be viewed on now, or in the future.

Saying that, here is one solution to that problem.  It is a 'FlowFrame' which is literally a tkinter 'Frame' i.e. it inherets from the 'Frame' class so this 'FlowFrame' can be used anywhere a 'Frame' can be used.  It is identical in every way, except it has 2 methods in addition to its parent class the 'Frame'.  

###### Note:
The flowframe will act as an ordinary frame unless addWidget(), organizeWidgetsWithGrid() or organizeWidgetsWithPlace() is called.  You can use the keyword argument mode="place" or mode="grid" when making and instance of a FlowFrame.  If none is specified, grid is used.

Here are 2 methods:
```
addWidget(yourWidget)                          #your widget might be a button, etc
```
and 
```
destroyWidgets()
```
##### Update 8/2/2021
I added 3 more methods:
- `organizeWidgetsWithGrid()`
- `organizeWidgetsWithPlace()`
- `stopOrganizingWidgets()`

Basically, you can use the FlowFrame as an ordinary frame, and then at any time make the children of the frame flow.  Here is an example:

#### Example 1: Showing mode="grid" when FlowFrame instance is made and using addWidget():
```
from tkinter import *
from flowframe import *

def main():

    buttonArray=[]
    root = Tk()

    myframe=FlowFrame(root, mode="grid")
    #make sure frame expands to fill parent window
    myframe.pack(fill="both", expand=1) 

    buttonMakePlace=Button(myframe, text="---Use Place---",command=myframe.organizeWidgetsWithPlace)
    myframe.addWidget(buttonMakePlace)

    buttonMakeGrid=Button(myframe, text="---Use Grid---", command=myframe.organizeWidgetsWithGrid)
    myframe.addWidget(buttonMakeGrid)

    buttonDestroy=Button(myframe,text="---Destroy---", command = myframe.destroyWidgets)

    for i in range(10):
        buttonArray.append(Button(myframe,text=str(i)))

    root.mainloop()

main()
```
#### Example 2: Initially using as an ordinary frame, then call organizing functions:
```
from tkinter import *
from flowframe import *

def main():

    buttonArray=[]
    root = Tk()

    myframe=FlowFrame(root, mode="grid")
    #make sure frame expands to fill parent window
    myframe.pack(fill="both", expand=1) 

    buttonMakePlace=Button(myframe, text="---Use Place---",command=myframe.organizeWidgetsWithPlace)
    buttonMakePlace.pack()

    buttonMakeGrid=Button(myframe, text="---Use Grid---", command=myframe.organizeWidgetsWithGrid)
    buttonMakeGrid.pack()

    buttonDestroy=Button(myframe,text="---Destroy---", command = myframe.destroyWidgets)

    for i in range(10):
        buttonArray.append(Button(myframe,text=str(i)))

    root.mainloop()

main()
```

#### Example 3: Showing the .addWidget() with more widgets:
```
from tkinter import *
from flowframe import *

def main():

    root = Tk()

    myframe=FlowFrame(root)
    myframe.pack(fill="both", expand=True)          #IMPORTANT! make sure frame expands to fill parent window

    mybutton=Button(myframe, text="---Button---")
    myframe.addWidget(mybutton)

    mytextbox=Text(myframe,width=3,height=2)
    myframe.addWidget(mytextbox)

    mylabel=Label(myframe,text="----Label---")
    myframe.addWidget(mylabel, sticky="NSEW")

    root.mainloop()

main()
```
This frame should be easy to use if you are somewhat familiar with using tkinter in Python.  Here are the key points:

1) The FlowFrame is a frame.  Use it anywhere you would use a Frame.
2) In order for widgets to flow in this frame, the frame must stick to its parent.  In other words, when you resize the frame's parent window, the frame must resize also, or else nothing will happen.  (This can be achieved using the `pack` with `fill=BOTH expand=True`, or `grid` with `sticky=NSEW` conventions)  Either way, this frame must stick to its parent container.
3) Use the frames .addWidget to add the widget into the frame, or call an organizing function later, `i.e. myFlowFrame.organizeWidgetsUsingPlace()`
`i.e.  myFlowFrame.addWidget(mybutton)`
4) The order widgets are added to the frame determines the order they appear in the frame, much like using the 'pack' geometery manager.
5) Use the FlowFrames addWidgets method to add to the frame, rather than gridding to the frame.  The FlowFrame uses the grid method in its addWidget method, but mixing and matching in an ad hoc fashion has not been really tested much, so just add to the frame with the frames method. 
6) Don't mix geometry managers - in other words, don't try to pack something into the frame, then try to use the frames's addWidget method.  This will cause errors just like trying to mix pack, grid, and place geometry managers.  Technically, the frame.addWidget() method uses the grid geometry manager, so you will not always get errors.  But the bottom line is, you should simply add to the frame using its addWidgets method rather than trying to grid to the frame.  This may lead to less than predictable results.
7) The method is FlowFrame.destroyWidgets() which destroys the objects and removes them from the frame.  This is like a reset.  It may not be the most intricate or nuanced method, but in practice, this simple method adds substantial functionality to the package as a whole.  If I get requests for a more nuanced approach, I may revisit the module, but at this time, the package remains quite usable as is.

#### Example 4:  Showing the .addWidget() and .destroyWidgets() methods:
```
from tkinter import *
from flowframe import *

def _destroyWidgets():
    myframe.destroyWidgets()

def main():

    root = Tk()

    global myframe
    myframe=FlowFrame(root)
    myframe.pack(fill="both", expand=True)     #make sure frame expands to fill parent window

    button=Button(myframe, text="---Button---")
    myframe.addWidget(button, sticky=NSEW)

    textbox=Text(myframe,width=3,height=2)
    myframe.addWidget(textbox)

    label=Label(myframe,text="Label")
    myframe.addWidget(label,sticky=NSEW)

    entry=Entry(myframe)
    myframe.addWidget(entry, sticky=NSEW)

    radioButton=Radiobutton(myframe,text="radio button")
    myframe.addWidget(radioButton)

    checkButton=Checkbutton(myframe,text="CheckButton")
    myframe.addWidget(checkButton)

    scale_widget = Scale(myframe, from_=0, to=100, orient=HORIZONTAL)
    myframe.addWidget(scale_widget)

    button2=Button(myframe, text="----Remove All---", command=_destroyWidgets)
    myframe.addWidget(button2)

    root.mainloop()

main()
```
###    Summary:
  - Object: FlowFrame
  - Inherets from: Frame
##### Methods:
```
      addWidget(widget)
      destroyWidgets()
      organizeWidgetsUsingGrid()
      organizeWidgetsUsingPlace()
      stopOrganizingWidgets()
