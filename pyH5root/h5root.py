import sys

if sys.version_info[0] < 3:
        print ("Need at least python3")
        sys.exit()

from PH5MainFrame import *


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    
    window = PH5MainFrame()
    window.show()
    
    sys.exit(app.exec_())
