# from PyQt5.QtWidgets import QApplication, QLabel

from models.system_spec_model import SystemSpecModel
from services.persistence_service import PersistenceService

def main():
    config = PersistenceService.load_config('./app/config')
    print(config)
    # spec = PersistenceService.load_system_spec('./app/config/system_spec.json')
    # drinks = PersistenceService.load_drinks('./app/config/drinks')
    # print(drinks)
    #print(spec.__dict__)
    # app = QApplication([])
    # label = QLabel('Hello World!')
    # label.show()
    # app.exec_()


main()