import sys
from PyQt5.QtWidgets import QApplication
from polynomial_plotter import PolynomialPlotter

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PolynomialPlotter()
    window.show()
    sys.exit(app.exec_())
