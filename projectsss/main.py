#PyQt5 
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtGui import QIcon, QFont 
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seljuks")
        self.setGeometry(700, 300, 500, 500)
        self.setWindowIcon(QIcon("projectsss/profile.png"))

        label = QLabel(self)
        label.setGeometry(0,0,500,500)
        pixmap = QPixmap("projectsss/profile.png")
        label.setPixmap(pixmap)

        label.setScaledContents(True)

        # label = QLabel("Hello king", self)
        # label.setFont(QFont("Arial", 40))
        # label.setGeometry(0,0,500,100)
        # label.setStyleSheet("color: #9ab3db;"
        #                     "background-color: #4287f5;"
        #                     "font-weight: bold;"
        #                     "font-style: italic;")

        # label.setAlignment(Qt.AlignTop)
        # label.setAlignment(Qt.AlignBottom)
        # label.setAlignment(Qt.AlignVCenter)
        # label.setAlignment(Qt.AlignRight)
        # label.setAlignment(Qt.AlignHcenter)
        label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        

def main ():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
     
if __name__ == "__main__":
    main()