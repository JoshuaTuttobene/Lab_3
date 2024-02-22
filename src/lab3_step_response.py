"""!
@file lab3_step_response.py
Run a motor step response based on a user inputted Kp. This program cals the
microcontroller to run and get data before plotting the closed loop PController step response.
It uses Tkinter, an old-fashioned and ugly but useful GUI library which is included in Python by
default.

This file is based loosely on an example found at
https://matplotlib.org/stable/gallery/user_interfaces/embedding_in_tk_sgskip.html

@author Aaron Escamilla, Karen Morales De Leon, Joshua Tuttobene
@date   02/22/2024 Original program, based on example from above listed source
@copyright (c) 2023 by Spluttflob and released under the GNU Public Licenes V3
"""

import time
import tkinter
import serial
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)

# Creating serial to read port
ser = serial.Serial('COM3')
ser.baudrate = 115200
ser.bytsize = 8
ser.parity = 'N'
ser.stopbits = 1
ser.timeout = 8
ser.write(b'\x04') # send ctrl-D to the serial port


def run_step(plot_axes, plot_canvas, xlabel, ylabel):
     """!
     
     Here we read the data from the microcontroller, and organize it accordingly with split and float commands
     This is read from the USB-serial
     A try block is used to filter out unusable data
     Time in x-axis, and Encoder Counts in y-axis
     
     Make a Closed Loop P Controlled Motor response plot.
     The data was acquired from the microcontroller with a step-response file
     @param plot_axes The plot axes supplied by Matplotlib
     @param plot_canvas The plot canvas, also supplied by Matplotlib
     @param xlabel The label for the plot's horizontal axis
     @param ylabel The label for the plot's vertical axis
     """
     # Create empty arrays to append data from microcontroller
     t_data = []
     p_data = []
     # Takes user input and then sends to microcontroller
     ser.write(input("Enter a Kp value:").encode('ascii'))
     ser.write(b'\r')
     time.sleep(5) # sleep to give the motor time to perform response
     
     # loop to get data from serial port until 'end' is printed, signifying the end of data
     for line in range(1000):
        try:
            ser.write(b'\x02') # need, dont delete, swith out of raw-REPL mode
            pos = ser.readline().decode('utf-8')
            if not pos == 'end':
                pos = pos.split(',')
                t = float(''.join(pos[0:1]))
                p = float(''.join(pos[1:2]))
                # Append data by adding to end in array
                t_data.append(t)
                p_data.append(p)
            else:
                break

        except ValueError:     # anything that is not a data entry don't show
            #print('invalid entry')
            pass
     #print(p_data)   
     # Draw the plot from the measured data 
     plot_axes.plot(t_data,p_data,'.', markersize=0.5)
     plot_axes.set_xlabel('Time (ms)')
     plot_axes.set_ylabel('Encoder Position')
     plot_axes.grid(True)
     plot_canvas.draw()
 
def tk_matplot(plot_function, xlabel, ylabel, title):
    """!
    Create a TK window with one embedded Matplotlib plot.
    This function makes the window, displays it, and runs the user interface
    until the user closes the window. The plot function, which must have been
    supplied by the user, should draw the plot on the supplied plot axes and
    call the draw() function belonging to the plot canvas to show the plot. 
    @param plot_function The function which, when run, creates a plot
    @param xlabel The label for the plot's horizontal axis
    @param ylabel The label for the plot's vertical axis
    @param title A title for the plot; it shows up in window title bar
    """
    # Create the main program window and give it a title
    tk_root = tkinter.Tk()
    tk_root.wm_title(title)

    # Create a Matplotlib 
    fig = Figure()
    axes = fig.add_subplot()

    # Create the drawing canvas and a handy plot navigation toolbar
    canvas = FigureCanvasTkAgg(fig, master=tk_root)
    toolbar = NavigationToolbar2Tk(canvas, tk_root, pack_toolbar=False)
    toolbar.update()

    # Create the buttons that run tests, clear the screen, and exit the program
    button_quit = tkinter.Button(master=tk_root,
                                 text="Quit",
                                 command=tk_root.destroy)
    button_clear = tkinter.Button(master=tk_root,
                                  text="Clear",
                                  command=lambda: axes.clear() or canvas.draw())
    button_run = tkinter.Button(master=tk_root,
                                text="Run Test",
                                command=lambda: plot_function(axes, canvas,
                                                              xlabel, ylabel))

    # Arrange things in a grid because "pack" is weird
    canvas.get_tk_widget().grid(row=0, column=0, columnspan=3)
    toolbar.grid(row=1, column=0, columnspan=3)
    button_run.grid(row=2, column=0)
    button_clear.grid(row=2, column=1)
    button_quit.grid(row=2, column=2)

    # This function runs the program until the user decides to quit
    tkinter.mainloop()


# This main code is run if this file is the main program but won't run if this
# file is imported as a module by some other main program
if __name__ == "__main__":
    tk_matplot(run_step,
               xlabel="Time (ms)",
               ylabel="Encoder Position",
               title="Motor Step Response")

