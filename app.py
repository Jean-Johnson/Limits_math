import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math

class Limits:
    """
    Class for handling mathematical operations
    """
    def __init__(self):
        self.f = None

    def create_function_from_equation(self,eq:str):
        """
        Create function from a given equation

        Args:
            eq (str): The equation
        """
        def f(x):
            return eval(
                eq,
                {'__builtins__': None},
                {'x': x, 'sin': math.sin, 'cos': math.cos, 'tan': math.tan, 'log': math.log, 'exp': math.exp}
                )
        self.f = f

    def calc_vals(self,start_x:float,end_x:float,num:int):
        """
         Calculate values of the function within a given range

         Args:
            start_x (float): Starting value of x.
            end_x (float): Ending value of x.
            num (int): Number of points to calculate.

        Returns:
            tuple: Tuple containing arrays of x and corresponding y values.
        """
        X = np.linspace(start_x,end_x,num)
        Y = [self.f(scalar_x) for scalar_x in X]
        return X,Y

class Render:
    def __init__(self,limits):
        self.limits = limits
        self.start_x = None
        self.end_x = None
        self.num_points = 100

    def _render_inputs(self):
        equation = st.text_input("Define f(x)")
        self.start_x, self.end_x = st.slider(
            'Select a range for plot',
            -100, 100, (-2, 2))
        if equation == "":
            return False
        self.limits.create_function_from_equation(equation.strip("\n").replace(" ",""))
        
    def _render_plot(self):
        try:
            X, Y = self.limits.calc_vals(self.start_x, self.end_x, self.num_points)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=X, y=Y, mode='lines', name='f(x)'))
            fig.add_vline(x=1, line=dict(color="red", dash="dash"), annotation_text="x=1", annotation_position="top right")
            fig.update_layout(
                xaxis_title="x",
                yaxis_title="f(x)",
                title="Visualization of f(x) and Limit as x approaches 1"
            )
            st.plotly_chart(fig)

        except ValueError:
            st.write("Plotting Error -> check the equation")
        except SyntaxError:
            st.write("The f(x) equation is wrong")


    def render(self):
        status = self._render_inputs()
        if status == False:
            return
        self._render_plot()

if __name__ == "__main__":
    st.title("Limits➗")
    limits = Limits()
    UI = Render(limits=limits)
    UI.render()
    