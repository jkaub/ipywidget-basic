import plotly.graph_objects as go
from ipywidgets.widgets import VBox, HBox, Button

class Widget:
    '''Out widget will take a list of color "colors" as well as x and y values
       to build a scatter plot'''
       
    def __init__(self, x, y , colors):
        
        self._x = x
        self._y = y
        self._colors = colors
        self._current_color = colors[0]
        self._build_layout()
        
    def _initialise_figure(self):
        
        '''This method initiate the FigureWidget'''
        
        self._fig = go.FigureWidget()
        self._fig.add_trace(
            go.Scatter(
                x = self._x,
                y = self._y,
                mode = "markers",
                marker = {"color":[self._current_color for e in self._x]}
            )
        )
        self._fig.update_layout(template="presentation")
        
        self._fig.data[0].on_click(self._change_color_on_click)
        
    def _change_color_on_click(self, trace, points, state):
        """Our callback. 'points' contains information such as the index, 
           x and y values
           The function will be trigger every time the user click on a point.
        """
        #Let's retrieve the index of the point of interest from "points"
        idx = points.point_inds[0]

        #Finaly, update the trace, using the batch_update method allowing us to modify multiple parameters at once
        with self._fig.batch_update():
            trace.marker["color"]=[c if i!=idx else self._current_color for i,c in enumerate(trace.marker["color"])]
        
    def _build_single_button(self, color):
        '''This function build a button with a given color'''
        button = Button(description = color)
        #The button with the active color has a special style to highlight the active color
        if color == self._current_color:
            button.button_style = "success"
            
        button.on_click(lambda button: self._click_button_function(color, button))
        return button
    
    def _click_button_function(self, color, button):
        '''This function is triggered everytime a user press the button'''
        #Set the current color to the color of the button
        self._current_color = color
        
        #Set the style of all button to default style
        for button_ in self._buttons:
            button_.button_style = ""
            
        #Set active button style to "success"
        button.button_style = "success"
        
    def _build_buttons_widget(self):
        '''This function build a widget with all the buttons, stacked horizontally'''
        #Create a list of button with each color
        self._buttons = [self._build_single_button(color) for color in self._colors]
        #Build a horizontal widget out of the list of buttons
        self._buttons_widget = HBox(self._buttons)
        
    def _build_layout(self):
        '''This function build the widget layout with the different components'''
        #Build the buttons widget
        self._build_buttons_widget()
        #Build the figure widget
        self._initialise_figure()
        #build the final widget
        self._widget = VBox([self._buttons_widget, self._fig])
        
    def display(self):
        '''A little function to display the widget'''
        display(self._widget)