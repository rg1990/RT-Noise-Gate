# Load the noise gate UI from the Python file created by pyuic5

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

# from QtDesigner_files.MainWindow2 import Ui_Form
from PyQt5_files.MainWindow3 import Ui_MainWindow

import numpy as np
import audiofile

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure
from matplotlib.animation import FuncAnimation

from noise_gate import Context, AudioConfig
from player import Player, PlaybackState
import queue


def zoom_factory(ax, base_scale=2):
    def zoom_fun(event):
        print(type(event))
        # get the current x and y limits
        cur_xlim = ax.get_xlim()
        xdata = event.xdata # get event x location
        if event.button == 'down':
            # zoom in
            scale_factor = 1/base_scale
        elif event.button == 'up':
            # zoom out
            scale_factor = base_scale
        
        ax.set_xlim([xdata - (xdata-cur_xlim[0]) / scale_factor, xdata + (cur_xlim[1]-xdata) / scale_factor])
        ax.figure.canvas.draw() # Re-draw

    fig = ax.get_figure() # get the figure of interest
    # attach the call back
    fig.canvas.mpl_connect('scroll_event', zoom_fun)

    #return the function
    return zoom_fun



# class MplWidget(QWidget):
  
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.fig = Figure(figsize=(5, 5))
#         self.canvas = FigureCanvasQTAgg(self.fig)
#         layout = QVBoxLayout(self)
#         layout.addWidget(self.canvas)
#         self.ax = self.canvas.figure.add_subplot(111)


class WaveformNavWidget(QWidget):
    def __init__(self, player):#, parent=None):
        super().__init__()#parent)
        
        self.player = player
        self.player.display = self

        self.fig = Figure()
        self.canvas = FigureCanvasQTAgg(self.fig)
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        self.plot_downsample = 100
        self.ax = self.canvas.figure.add_subplot(111)
        self.ax.plot(self.player.time_array[::self.plot_downsample],
                     self.player.audio_array[::self.plot_downsample],
                     lw=1, color="#00ADB5")
        # Add a playhead
        self.line_playhead = self.ax.axvline(0, linewidth=1, color='red')

        # Remove the border around the figure
        # for spine in self.ax.spines.values():
        #     spine.set_visible(False)

        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
        self.fig.set_facecolor("#f0f0f0")
        self.ax.set_facecolor("#222831")
        self.ax.set_yticks([])

        # Implement the zoom and pan functions on self.ax
        self.f = zoom_factory(self.ax, base_scale=1.33)
        
        self.connect_events()

    
    def connect_events(self):
        self.fig.canvas.mpl_connect('button_press_event', self.move_playhead_onclick)
    
    
    def move_playhead_onclick(self, event):
        # Check the click happened inside self.ax
        # Don't update the position if zoom or pan tools are enabled
        if event.inaxes in [self.ax] and not self.ax.get_navigate_mode():
            xpos = int(event.xdata)
            # Position validation
            if xpos <= 0:
                xpos = 0
            elif xpos >= len(self.player.audio_array):
                xpos = len(self.player.audio_array)
            
            # Set the new position of the playhead line
            self.set_playhead_position(xpos)
            
            # Update the player with the new starting position
            self.player.set_start_idx(xpos)
            
            
    def set_playhead_position(self, xpos):
        # Set the new position of the playhead line
        self.player.playhead_idx = xpos
        self.line_playhead.set_xdata([xpos, xpos])
        #self.canvas.draw()
        self.canvas.blit()


    def update_plot(self, frame):
        ''' Passed to FuncAnimation, used to update the playhead position while playing '''
        
        # We only need to update the position if the player is playing
        if self.player.playing:
            self.line_playhead.set_xdata([self.player.playhead_idx, self.player.playhead_idx])

        return self.ax.get_lines()
    


class ScrollingGatedAudioWidget(QWidget):
  
    def __init__(self, player):#, parent=None):
        super().__init__()#parent)
        self.player = player
        self.fig = Figure(figsize=(5, 5))
        self.canvas = FigureCanvasQTAgg(self.fig)
        self.ax = self.fig.add_subplot(111)

        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        
        # Adjust the edges of the subplot using fractions of the figure dimensions
        self.fig.subplots_adjust(left=0.07,right=0.98,bottom=0.05,top=0.95)
        self.fig.set_facecolor("#f0f0f0")
        self.ax.set_facecolor("#222831")
        
        # Downsample factor to plot fewer points
        self.downsample = 50
        # How many milliseconds of audio will fit in the scrolling display
        self.window = 4000
        # Compute the number of points used to plot the lines
        self.length  = int(self.window*self.player.audio_config.fs/(1000*self.downsample))

        # Create Line2D objects to display the (un-)gated audio
        self.ungated_line, = self.ax.plot(np.ones(self.length) * -60, color="#00ADB5", alpha=0.3)
        self.gated_line, = self.ax.plot(np.ones(self.length) * -60, color="#00ADB5")
        # Initialise arrays to hold the gated and ungated audio data
        self.gated_data = np.zeros(self.length)
        self.ungated_data = np.zeros(self.length)
        
        # Plot the threshold line on top of the gated/ungated lines
        self.thresh_line = self.ax.axhline(self.player.noise_gate.thresh, color='red')
        
        # Set up the plot limits and appearance
        self.ax.set_ylim([-60, 0])
        self.ax.set_yticks([val for val in range(-60, 10, 10)])
        self.ax.set_xticks([])


    def update_plot(self, frame):
        ''' Passed to FuncAnimation, used to update the scrolling plot '''
        while True:
            try:
                # Get data from the player's queue
                ungated_data, gated_data = self.player.q.get_nowait()
            except queue.Empty:
                break

            # Get the magnitude of the ungated signal
            ungated_data = np.abs(ungated_data)[:, 0]
            num_rows = len(ungated_data) // self.downsample
            # Get the maximum magnitude value in each window of size self.downsample
            ungated_data = np.array([np.max(ungated_data[i*self.downsample : (i+1)*self.downsample]) for i in range(num_rows)])
            # Convert magnitude to dBFS
            ungated_data = 20*np.log10(ungated_data)
            # Distance to scroll data between plot updates
            shift = len(ungated_data)

            gated_data = np.abs(gated_data)[:, 0]
            num_rows = len(gated_data) // self.downsample
            gated_data = np.array([np.max(gated_data[i*self.downsample : (i+1)*self.downsample]) for i in range(num_rows)])
            gated_data = 20*np.log10(gated_data)
            
            # Simulate scrolling - shift data to left and add new data on right end
            self.ungated_data = np.roll(self.ungated_data, -shift, axis=0)
            self.ungated_data[-shift:] = ungated_data
            self.gated_data = np.roll(self.gated_data, -shift, axis=0)
            self.gated_data[-shift:] = gated_data

            # Update the data of the gated and ungated data lines
            self.ungated_line.set_ydata(self.ungated_data)
            self.gated_line.set_ydata(self.gated_data)

        return self.ax.get_lines()


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        
        # Set up some audio things
        self.audio_config = AudioConfig(fs=44100, blocksize=1024)
        audio_data, _ = audiofile.read("data/snare_test.wav")
        #time_arr = np.arange(len(audio_data))
        # Slice audio if using a longer file
        #audio_data = audio_data[160*self.audio_config.fs : 165*self.audio_config.fs]
        self.player = Player(self.audio_config, audio_array=audio_data)
        self.player.pause_behaviour = False

        # Create and add the scrolling plot widget
        self.gate_thresh_canvas = ScrollingGatedAudioWidget(self.player)#self)
        self.scrolling_plot_layout.addWidget(self.gate_thresh_canvas)

        # Create and add the waveform navigator widget
        self.waveform_canvas = WaveformNavWidget(self.player)
        self.waveform_nav_layout.addWidget(self.waveform_canvas)

        # Animation for scrolling gated signal
        self.gate_scroll_ani = FuncAnimation(self.gate_thresh_canvas.fig,
                                            self.gate_thresh_canvas.update_plot,
                                            interval=20,
                                            blit=True,
                                            cache_frame_data=False)
        

        # Animation for playhead motion on waveform
        self.playhead_ani = FuncAnimation(self.waveform_canvas.fig,
                                            self.waveform_canvas.update_plot,
                                            interval=20,
                                            blit=True,
                                            cache_frame_data=False)
        
        
        # Group the gate controls
        self.gate_controls = [self.threshold_slider,
                            self.attack_dial,
                            self.hold_dial,
                            self.release_dial,
                            self.lookahead_dial]

        # Stop the on/off button getting toggled by space bar
        self.on_off_button.setFocusPolicy(Qt.NoFocus)
        self.make_connections()
        self.set_initial_dial_values()


    def set_initial_dial_values(self):
        '''
        Set the dial positions based on the initial noise gate parameters.
        The values are multiplied by 1000 because the times are specified in
        milliseconds but the QDial widget requires integer values.
        '''
        self.attack_dial.setValue(int(self.player.noise_gate.attack_time * 1000))
        self.hold_dial.setValue(int(self.player.noise_gate.hold_time * 1000))
        self.release_dial.setValue(int(self.player.noise_gate.release_time * 1000))
        self.lookahead_dial.setValue(int(self.player.noise_gate.lookahead_time * 1000))

    
    def make_connections(self):
        ''' Connect signals to slots '''
        self.threshold_slider.valueChanged.connect(self.update_threshold_line)
        self.on_off_button.pressed.connect(self.toggle_gate_enabled_state)
        self.attack_dial.valueChanged.connect(self.update_attack)
        self.hold_dial.valueChanged.connect(self.update_hold)
        self.release_dial.valueChanged.connect(self.update_release)
        self.lookahead_dial.valueChanged.connect(self.update_lookahead)
        self.threshold_slider.valueChanged.connect(self.update_threshold)
        self.threshold_slider.valueChanged.connect(self.update_threshold_line)


    def toggle_gate_enabled_state(self):
        ''' Turn the noise gate on/off and update GUI elements '''
        # Toggle the gate's enabled state
        self.player.noise_gate.enabled = not self.player.noise_gate.enabled
        
        # Disable gate controls - is there a better way than this?
        if self.attack_dial.isEnabled():
            self.on_off_button.setText("OFF")
            # Change the colour of the horizontal threshold line
            self.gate_thresh_canvas.thresh_line.set_color('lightgray')
            self.gate_thresh_canvas.canvas.draw()
            # Update the enabled state of the GUI elements
            for el in self.gate_controls:
                el.setEnabled(False)
        else:
            self.on_off_button.setText("ON")
            # Change the colour of the horizontal threshold line
            self.gate_thresh_canvas.thresh_line.set_color('red')
            self.gate_thresh_canvas.canvas.draw()
            # Update the enabled state of the GUI elements
            for el in self.gate_controls:
                el.setEnabled(True)


    def update_threshold_line(self, val):
        ''' Update the position of the horizontal threshold line '''
        #self.update_threshold(val)
        self.gate_thresh_canvas.thresh_line.set_ydata([val, val])
    
    
    def update_threshold(self, threshold_val):
        ''' Update the threshold value of the noise gate '''
        #print(threshold_val)
        self.player.noise_gate.thresh = threshold_val
    

    def update_attack(self, attack_val):
        ''' Update the attack value of the noise gate '''
        #print(attack_val)
        self.player.noise_gate.set_attack_time(attack_val / 1000)


    def update_hold(self, hold_val):
        ''' Update the hold value of the noise gate '''
        #print(hold_val)
        self.player.noise_gate.set_hold_time(hold_val / 1000)


    def update_release(self, release_val):
        ''' Update the release value of the noise gate '''
        #print(release_val)
        self.player.noise_gate.set_release_time(release_val / 1000)


    def update_lookahead(self, lookahead_val):
        ''' Update the lookahead value of the noise gate '''
        # TODO
        pass


    def keyPressEvent(self, keyEvent):
        ''' Listener for key press events '''
        if keyEvent.key() == Qt.Key_Space:
            self.player.play_stop_command()



app = QApplication([])
window = MainWindow()
window.show()
app.exec_()