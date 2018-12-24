import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from lib.qt_style_helper import Styles
from models.system_spec_model import SystemSpecModel
from services.persistence_service import PersistenceService
from flask import Flask
app = Flask(__name__)

# def main():
#     config = PersistenceService.load_config('./app/config')
#     spec = config[0]
#     drinks = config[1]

#     app = QApplication(sys.argv)
#     window = QWidget()
#     window.resize(300,400)
#     window.move(0,0)
#     window.setWindowTitle('BarBot')

#     l1 = QLabel('Scale Pin Number')
#     nm = QLineEdit()
#     nm.setText(spec.scale_pin_number)

#     fbox = QFormLayout()
#     fbox.addRow(l1, nm)

#     window.setLayout(fbox)
#     window.show()
#     sys.exit(app.exec_())
    
# main()

@app.route("/")
def main():
     return "hello"

@app.route("/x")
def main2():
     return "World"
    
app.run()