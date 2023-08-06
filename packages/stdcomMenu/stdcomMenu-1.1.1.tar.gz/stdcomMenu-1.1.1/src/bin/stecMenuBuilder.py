from stdcomMenu.builder import *
import argparse, os, sys


if __name__=="__main__":
    my_parser = argparse.ArgumentParser(description="Version :" + stdcomQt.stdcomQtVersion + " Stec Menu Program")
    current = os.path.dirname(os.path.realpath(__file__))

    # Getting the parent directory name
    # where the current directory is present.
    parent = os.path.dirname(current)

    # adding the parent directory to
    # the sys.path.

    app = QApplication(sys.argv)
    w = Builder()
    w.show()

    sys.exit(app.exec_())