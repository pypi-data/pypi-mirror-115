# tkinterflow

This is a project to add the functionality of a 'flow' layout to Python Tkinter graphical user interface module.

- tkinter has the Pack, Grid, and Place geometry managers.

- This module adds a Flow option to the geometry managers.

### Summary of features

##### - Widget methods added:
 - `widget.flow()`
 - `widget.flow(mode="place")`
 - `widget.flow(mode="grid")` # default if no mode specified
 - `widget.flow_destroy()`
##### - Additional functions contained in the module:
- `organizeWidgetsWithGrid(myframe)`
- `organizeWidgetsWithPlace(myframe)`
- `stopOrganizingWidgets(myframe)`

##### -To implement the module, install it first with:

`pip install tkinterflow
`
##### then use the following import statements IN THIS ORDER (Very important if .flow() is being used!)
```
from tkinter import *
from tkinterflow import *
```
##### - Addional objects available but not normally used, their names are reassigned but can be accessed:
`Button = FlowButton`
`Canvas = FlowCanvas`
`Checkbutton = FlowCheckbutton`
`Entry = FlowEntry`
`Frame = FlowedFrame`
`Label = FlowLabel`
`Listbox = FlowListbox`
`Menubutton = FlowMenubutton`
`Message = FlowMessage`
`Radiobutton = FlowRadiobutton`
`Scale = FlowScale`
`Scrollbar = FlowScrollbar`
`Text = FlowText`
`Spinbox = FlowSpinbox`
`LabelFrame = FlowLabelFrame`
`PanedWindow = FlowPanedWindow`

###### Note the 'FlowedFrame' object above was renamed to avoid potential conflicts with the flowframe module, which contains and object called 'FlowFrame'

Now additional methods can be used.  If you are used to using statements like:
```
button1.pack()
```
#### you can use
```
button1.flow()
```
to add the widgets to a frame.
#### you can use
```
button1.destroy()
```
to remove the button from the frame.

The widgets should flow inside the parent frame like typical flow geometry, like in typical html or just regular text flow like word-wrapping.

##### Note:
***You cannot use the flow geometry manager in the root widget, but can use it in any frame below root.***

###### So if you only have one root window, pack a frame into the root window, then use flow to add widgets to that frame.  You'll want to make that frame stick to the parent root window so it expands with the root window.


The flow behavior is a subset of the grid geometry manager by default.  But you can change that by using the following keyword argument `.flow(mode="place")` and the place geometry manager will be used instead.

You should not try to mix and match `mode="place"` and `mode="grid"`.  If you do, you may find that the last mode used is the one that "wins".  Actually, the source code was not really designed to mix and match and use the last mode called, but so far, rather than erroring out, this is the behaviour.

#### Like pack, grid, and place, you should not mix geometry managers.  Likewise with the flow geometry manager.

-If you are flowing into a frame, only use flow, don't try to mix and match geometry managers.

##### If you have a project currently using pack, place or grid, and you want to grab all of the children and make them flow, here are 3 functions to address that situation:
1) `organizeWidgetsWithGrid(myframe)` - This will take all children of myframe and use a grid-flow system (mode="grid").  (Even children that are not currently visible.  If they are a child of the frame they will become visible, so this needs to be considered when implementing.
2) `organizeWidgetsWithPlace(myframe)` - Same as #1 above, but using the place-flow (mode="place") system. 
3) `stopOrganizingWidgets(myframe)` - Halts the binding of the frame resize to trigger organization.  Widgets stop where they are currently when this function is called.
##### An extra note about these functions above.  You do not have to worry about the import statement order if you are only using these 3 functions, so that might be preferred depending on the scenario.
### Here are a few examples:

##### Example 1a: Basic use of .flow() method:
```
from tkinter import *
from tkinterflow import *       # ! Very important, put this right after import of tkinter functions

root = Tk()              
myFrame = Frame(root)                 # Very Important!, you cannot use .flow() methods in root
myFrame.pack(fill=BOTH, expand=True)  # Very Important!, frame must stick to parent container walls

button1 = Button(myFrame, text="----Button1---")
button1.flow()

button2 = Button(myFrame, text="Button2")
button2.flow()

button3 = Button(myFrame, text="----Button3---")
button3.flow()

button4 = Button(myFrame, text="Button4")
button4.flow()

root.mainloop()
```
##### Example 1b: Basic use of .flow(mode='place') method:
```
from tkinter import *
from tkinterflow import *       # ! Very important, put this right after import of tkinter functions

root = Tk()              
myFrame = Frame(root)                 # Very Important!, you cannot use .flow() methods in root
myFrame.pack(fill=BOTH, expand=True)  # Very Important!, frame must stick to parent container walls

button1 = Button(myFrame, text="-------Button1-------")
button1.flow(mode="place")

button2 = Button(myFrame, text="Btn2")
button2.flow(mode="place")

button3 = Button(myFrame, text="Btn3")
button3.flow(mode="place")

button4 = Button(myFrame, text="Button4")
button4.flow(mode="place")

root.mainloop()
```

##### Example 2:  Making widgets, but not adding to layout until a final step when one function, organizeWidgetsWithPlace(myframe) is called.
```
from tkinter import *
from tkinterflow import *       # ! Very important, put this right after import of tkinter functions

root = Tk()              
myFrame = Frame(root)                 # Very Important!, you cannot use .flow() methods in root
myFrame.pack(fill=BOTH, expand=True)  # Very Important!, frame must stick to parent container walls

buttons=[]
mystring=""
for i in range(10):
    mystring=mystring+str(i)
    buttons.append(Button(myFrame,text=mystring))

organizeWidgetsWithPlace(myFrame)
root.mainloop()
```

##### Example 3:  Changing sticky behavior of widgets while using default flow managment (mode="grid"/default), also using a variety of widgets.
```
from tkinter import *
from tkinterflow import *       # ! Very important, put this right after import of tkinter functions

def unstickyWidgets():
    button1.grid_configure(sticky="")
    label.grid_configure(sticky="")
    entry.grid_configure(sticky="")
    radioButton.grid_configure(sticky="")
    checkButton.grid_configure(sticky="")
    scale_widget.grid_configure(sticky="")
    button2.grid_configure(sticky="")
    button3.grid_configure(sticky="")
    root.update()

def stickyWidgets():
    button1.grid_configure(sticky="NSEW")
    label.grid_configure(sticky="NSEW")
    entry.grid_configure(sticky="NSEW")
    radioButton.grid_configure(sticky="NSEW")
    checkButton.grid_configure(sticky="NSEW")
    scale_widget.grid_configure(sticky="NSEW")
    button2.grid_configure(sticky="NSEW")
    button3.grid_configure(sticky="NSEW")
    root.update()

root = Tk()              
myFrame = Frame(root)                 # Very Important!, you cannot use .flow() methods in root
myFrame.pack(fill=BOTH, expand=True)  # Very Important!, frame must stick to parent container walls

button1 = Button(myFrame, text="---Button1---")
button1.flow(sticky=NSEW)

label = Label(myFrame, text="Label")
label.flow(sticky=NSEW)

entry = Entry(myFrame)
entry.flow(sticky=NSEW)

radioButton = Radiobutton(myFrame, text="radio button")
radioButton.flow(sticky=NSEW)

checkButton = Checkbutton(myFrame, text="CheckButton")
checkButton.flow(sticky=NSEW)

scale_widget = Scale(myFrame, from_=0, to=100, orient=HORIZONTAL)
scale_widget.flow(sticky=NSEW)

button2 = Button(myFrame, text="---sticky Widgets/see effect--", command=stickyWidgets)
button2.flow(sticky=NSEW)

button3 = Button(myFrame, text="---unsticky Widgets---", command=unstickyWidgets)
button3.flow(sticky=NSEW)

root.mainloop()
```

##### Update Notes:
The tkinterflow module 0.0.4 has been changed significantly in the way it works.  Instead of modifying tkinters `__init__.py` file to achieve adding the .flow method to widgets, I use inheritence to make a child from each widget (except the Menu widget).  Then I add the flow method to the child.  Then I reassign the name of the parent to the child.  This relies on you first importing tkinter, then importing tkinterflow as noted this order is important.  I did this because I did not want to edit my package everytime someone makes a change to tkinters initialization file.

----------------------------------
##### Update 8/2/2021
Added 3 new functions and here they are in use.  I have illustrated how nice they are to use and you can create the widgets without actually adding them with grid, pack place or flow, and then just bring them all into the frame with the calling of one of these organization functions.

##### *Also updated the flow algorithm to a better algorithm.  Sometimes widgets would flow past the border frame under certain conditions.*  If this substantial change to the algorithm changes your layout for the worse, you may to not upgrade and reinstall the older module.  Actually, I think this new alogoirthm will likely give better results and remove any issues.

This is highly handy, actually in your code you can simply create your widgets without doing anything else, then call one of these organizing functions and the child widgets will organize.  What's also nice is if you have already used the grid, place or pack management in a frame, call one of these functions and all children will automatically be reorganized (those which are not visible also).



### Example 4:  Packing 2 buttons to screen, creating but not packing 10 buttons, then switch between grid-flow, place-flow, or no-flow.
##### (Also demonstrates the order if import is not important if not using .flow() method on a widget)
```
from tkinterflow import *
from tkinter import *     # notice the order is reverse, not required when not using .flow()


def main():

    root = Tk()

    buttons=[]

    myframe=Frame(root)

    myframe.pack(fill=BOTH, expand=True)

    button1=Button(myframe, text="---Place---",command = lambda: organizeWidgetsWithPlace(myframe))
    button1.pack()

    button2=Button(myframe, text="Grid",command = lambda: organizeWidgetsWithGrid(myframe))
    button2.pack()

    button3=Button(myframe, text="Stop Organizing", command = lambda: stopOrganizingWidgets(myframe))

    for i in range(10):
        buttons.append(Button(myframe, text="button"+str(i)))

    root.mainloop()

main()
```
