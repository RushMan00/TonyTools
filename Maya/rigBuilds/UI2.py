import maya.cmds as cmds
import shiboken2
from PySide2 import QtCore, QtWidgets

# Custom widget class for rounded buttons
class RoundedButton(QtWidgets.QPushButton):
    def __init__(self, text, parent=None):
        super(RoundedButton, self).__init__(text, parent)
        self.setStyleSheet(
            """
            QPushButton {
                border-radius: 10px;
                padding: 10px;
                background-color: #8BC34A;
                color: white;
            }
            QPushButton:hover {
                background-color: #9CCC65;
            }
            QPushButton:pressed {
                background-color: #689F38;
            }
            """
        )

# Custom widget class for rounded window
class RoundedWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(RoundedWindow, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Set a fixed window size
        self.setFixedSize(300, 200)

        # Create a vertical layout for the window
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Add a label and buttons to the layout
        label = QtWidgets.QLabel("Rounded Window")
        layout.addWidget(label)

        button1 = RoundedButton("Button 1")
        button2 = RoundedButton("Button 2")
        layout.addWidget(button1)
        layout.addWidget(button2)

# Create a function to launch the rounded window
def launch_rounded_window():
    # Check if the window already exists and close it before recreating
    if cmds.window("roundedWindow", exists=True):
        cmds.deleteUI("roundedWindow")

    # Create a Maya window with the name "roundedWindow"
    window = cmds.window("roundedWindow", title="Rounded Window", widthHeight=(300, 200))

    # Create a Qt window within the Maya window
    window_ptr = int(cmds.control(window, query=True, visible=True))
    qt_window = shiboken2.wrapInstance(window_ptr, QtWidgets.QWidget)

    # Create and show the custom rounded window
    rounded_window = RoundedWindow(qt_window)
    rounded_window.show()

# Launch the rounded window
launch_rounded_window()
