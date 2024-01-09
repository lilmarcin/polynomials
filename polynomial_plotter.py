import numpy as np
import re
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QTextEdit, QHBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


from polynomial_calculator import calculate_polynomial

class PolynomialPlotter(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.coefficients_label = QLabel('Enter the polynomial coefficients (separated by a space): ')
        self.coefficients_entry = QLineEdit()
        self.preview_label = QLabel('Preview: ')
        self.plot_button = QPushButton('Draw graph')
        

        self.coefficients_entry.textChanged.connect(self.update_preview)
        self.plot_button.clicked.connect(self.plot_polynomial)


        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)

        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setMinimumWidth(200)

        # Layout dla lewej i prawej strony
        main_layout = QHBoxLayout()

        # Add toolbar navigation for plotting
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setFixedHeight(30)


        # Left area
        left_layout = QVBoxLayout()
        left_layout.addWidget(self.coefficients_label)
        left_layout.addWidget(self.coefficients_entry)
        left_layout.addWidget(self.preview_label)
        left_layout.addWidget(self.plot_button)
        left_layout.addWidget(self.canvas)
        left_layout.addWidget(self.toolbar)

        # Right area
        right_layout = QVBoxLayout()
        right_layout.addWidget(self.info_text)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Polynomial graph')

    def plot_polynomial(self):
        try:
            input_text = self.coefficients_entry.text()
            coefficients = self.parse_coefficients(input_text)

            # Generate polynomial view
            preview_label = f'Preview: {self.generate_preview_string(coefficients)}'
            self.preview_label.setText(preview_label)

            x, y, delta, roots, extrema_roots, vertex  = calculate_polynomial(coefficients)
    
            self.ax.clear()
            self.ax.plot(x, y)
            if vertex is not None:
                self.ax.scatter(vertex[0], vertex[1], color='blue', label='Vertex')
            # Draw roots
            self.ax.scatter(roots, np.zeros_like(roots), color='red', label='Roots')

            # Draw extrema points
            if len(extrema_roots) > 0:
                self.ax.vlines(extrema_roots, ymin=self.ax.get_ylim()[0], ymax=self.ax.get_ylim()[1], color='green', linestyle='--', label='Extrema')


            self.ax.axhline(0, color='black', linewidth=0.5)
            self.ax.axvline(0, color='black', linewidth=0.5)
            self.ax.grid(color='gray', linestyle='--', linewidth=0.5)
            self.ax.set_title(f'W(x) = {self.generate_preview_string_matplotlib(coefficients)}')
            self.ax.set_xlabel('x')
            self.ax.set_ylabel('y')
            self.ax.legend()

            self.canvas.draw()

            self.update_info_text(coefficients, delta, roots, extrema_roots, vertex)
        except ValueError:
            print("Error: Please enter the correct polynomial coefficients")

    def parse_coefficients(self, input_text):
        # use regex to parse coefficients
        matches = re.findall(r'(-?\d*\.?\d+)(?:\*?x\*\*(\d+))?', input_text)
        coefficients = [float(match[0]) if match[0] else 1 for match in matches]
        return coefficients

    def update_info_text(self, coefficients, delta, roots, extrema_roots, vertex):
        degree = len(coefficients) - 1
        info = f"Degree: {degree}\n"
        # Quadratic Function
        if delta is not None:
            info += (f'\u0394 = {delta}\n')
            info += (f'Vertex: ({vertex[0]}, {vertex[1]})\n')

        info += "Roots:\n"
        for i, root in enumerate(roots):
            info += f'{i+1}. x = {round(root,2)}, y = {round(np.polyval(coefficients, root),2)}\n'

        info += "Extremes:\n"
        for i, extrema_root in enumerate(extrema_roots):
            info += f'x_{i+1} = {round(extrema_root,2)}, y_{i+1} = {round(np.polyval(coefficients, extrema_root),2)}\n'

        self.info_text.setPlainText(info)

    def generate_preview_string(self, coefficients):
        degree = len(coefficients) - 1
        terms = []

        for i, coef in enumerate(coefficients):
            power = degree - i
            term = ''
            if coef != 0:
                if coef > 0 and i > 0:
                    term += '+'
                elif coef < 0:
                    pass
                    #term += '-'

                if int(coef) == coef:
                    term += str(int(coef))
                else:
                    term += f'{abs(coef)}'

                if power > 1:
                    term += f'x^{power}'
                elif power == 1:
                    term += 'x'
            terms.append(term)

        return ' '.join(terms)
    
    def generate_preview_string_matplotlib(self, coefficients):
        degree = len(coefficients) - 1
        terms = []

        for i, coef in enumerate(coefficients):
            power = degree - i
            term = ''
            if coef != 0:
                if coef > 0 and i > 0:
                    term += '+'
                elif coef < 0:
                    pass
                   #term += '-'

                if int(coef) == coef:
                    term += str(int(coef))
                else:
                    term += f'{abs(coef)}'

                if power > 1:
                    term += f'$x^{power}$'
                elif power == 1:
                    term += 'x'
            terms.append(term)

        return ' '.join(terms)
    
    def update_preview(self):
        
        input_text = self.coefficients_entry.text()
        print("INPUT TEXT", input_text)
        coefficients = self.parse_coefficients(input_text)
        print("WSPOLCZYNNIKI", coefficients)
        preview_label = f'W(x)= {self.generate_preview_string(coefficients)}'
        self.preview_label.setText(preview_label)
