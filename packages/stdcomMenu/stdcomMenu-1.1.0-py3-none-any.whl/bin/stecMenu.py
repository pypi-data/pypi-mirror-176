from stdcomMenu.menu import *
import argparse, os, sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = stdcOperatorMenu()
    window.setWindowTitle("Stec Multiverse Menu")
    window.show()  # IMPORTANT!!!!! Windows are hidden by default.

    # Start the event loop.
    app.exec_()
