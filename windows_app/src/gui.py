from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog
from PyQt5.QtGui import QIcon, QFont

def create_gui(main_func):
    app = QApplication([])

    window = QWidget()
    window.setWindowTitle("ML-Based Mass Spectra Species Identifier")
    window.setWindowIcon(QIcon('icon.png'))
    window.setFixedSize(700, 350)

    layoutV = QVBoxLayout()
    font_label = QFont("Arial", 16, QFont.Bold)
    font_button = QFont("Arial", 14)

    layoutV.setContentsMargins(40, 40, 40, 40)

    layoutH3 = QHBoxLayout()
    model_file_path = QLineEdit(placeholderText="Select your ML model file...")
    model_file_path.setFont(font_button)
    browse_model_btn = QPushButton("Select Model")
    browse_model_btn.setFont(font_button)
    label3 = QLabel("Model File:")
    label3.setFont(font_label)
    layoutH3.addWidget(label3)
    layoutH3.addWidget(model_file_path)
    layoutH3.addWidget(browse_model_btn)
    layoutV.addLayout(layoutH3)

    layoutH1 = QHBoxLayout()
    input_directory = QLineEdit(placeholderText="Select a directory with CSV files...")
    input_directory.setFont(font_button)
    browse_input_btn = QPushButton("Browse")
    browse_input_btn.setFont(font_button)
    label1 = QLabel("Input Directory:")
    label1.setFont(font_label)
    layoutH1.addWidget(label1)
    layoutH1.addWidget(input_directory)
    layoutH1.addWidget(browse_input_btn)
    layoutV.addLayout(layoutH1)

    layoutH2 = QHBoxLayout()
    output_directory = QLineEdit(placeholderText="Select a directory for results...")
    output_directory.setFont(font_button)
    browse_output_btn = QPushButton("Browse")
    browse_output_btn.setFont(font_button)
    label2 = QLabel("Output Directory:")
    label2.setFont(font_label)
    layoutH2.addWidget(label2)
    layoutH2.addWidget(output_directory)
    layoutH2.addWidget(browse_output_btn)
    layoutV.addLayout(layoutH2)

    classify_btn = QPushButton("Classify")
    classify_btn.setFont(font_button)
    layoutV.addWidget(classify_btn)

    window.setStyleSheet("""
        QWidget {
            background-color: #fafafa;
            font-size: 18px;
            color: #333;
        }
        QPushButton {
            background-color: #11a611; /* Green */
            color: white;
            border: none;
            border-radius: 10px;
            padding: 14px 28px;
        }
        QPushButton:pressed {
            background-color: #005900; /* Darker green on click */
        }
        QLineEdit {
            background-color: #fff;
            border: 1px solid #ccc;
            border-radius: 10px;
            padding: 14px;
        }
    """)

    browse_model_btn.clicked.connect(lambda: model_file_path.setText(QFileDialog.getOpenFileName()[0]))
    browse_input_btn.clicked.connect(lambda: input_directory.setText(QFileDialog.getExistingDirectory()))
    browse_output_btn.clicked.connect(lambda: output_directory.setText(QFileDialog.getExistingDirectory()))
    classify_btn.clicked.connect(lambda: main_func(model_file_path.text(), input_directory.text(), output_directory.text()))

    window.setLayout(layoutV)
    window.show()
    app.exec_()

if __name__ == "__main__":
    create_gui(main)
