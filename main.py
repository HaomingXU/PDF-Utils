import os
import PyQt6.QtWidgets as qtw
import PyQt6.QtGui as qtg
import fitz


class MainWindow(qtw.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF Utils by Haoming")

        lblInput = qtw.QLabel("Input file")
        lblInput.setFont(qtg.QFont("MiSans"))

        textBoxInput = qtw.QLineEdit()
        textBoxInput.setObjectName("input_file")

        btnInput = qtw.QPushButton("Explore", clicked=lambda:explore_File())

        lblOutput = qtw.QLabel("Output directory")
        lblOutput.setFont(qtg.QFont("MiSans"))

        textBoxOutput = qtw.QLineEdit()
        textBoxOutput.setObjectName("output_file")

        btnOutput = qtw.QPushButton("Explore", clicked=lambda:save_File())

        dpiGroup = qtw.QButtonGroup(self)
        lblDPI = qtw.QLabel("Select output DPI")
        dpi300 = qtw.QRadioButton("300 DPI")
        dpi144 = qtw.QRadioButton("144 DPI")
        dpi72 = qtw.QRadioButton("96 DPI")
        dpiGroup.addButton(dpi300,0)
        dpiGroup.addButton(dpi144,1)
        dpiGroup.addButton(dpi72,2)
        dpi300.setChecked(True)

        btnProcess = qtw.QPushButton("Process", clicked=lambda:process_File())

        progBar = qtw.QProgressBar()

        lblOutputType = qtw.QLabel("Select output type")
        outputGroup = qtw.QButtonGroup(self)
        outputPNG = qtw.QRadioButton(".PNG")
        outputJPG = qtw.QRadioButton(".JPG")
        outputGroup.addButton(outputPNG, 0)
        outputGroup.addButton(outputJPG, 1)
        outputPNG.setChecked(True)

        # 创建Grid
        grid = qtw.QGridLayout(self)
        grid.addWidget(lblInput, 1, 0)
        grid.addWidget(textBoxInput, 2, 0)
        grid.addWidget(btnInput, 2, 1)
        grid.addWidget(lblOutput, 3, 0)
        grid.addWidget(textBoxOutput, 4, 0)
        grid.addWidget(btnOutput, 4, 1)
        grid.addWidget(lblDPI, 5, 0)

        dpiLayout = qtw.QHBoxLayout(self)
        dpiLayout.addWidget(dpi300, 0)
        dpiLayout.addWidget(dpi144, 1)
        dpiLayout.addWidget(dpi72, 2)
        grid.addLayout(dpiLayout, 6, 0)

        grid.addWidget(lblOutputType, 7, 0)

        typeLayout = qtw.QHBoxLayout(self)
        typeLayout.addWidget(outputPNG, 0)
        typeLayout.addWidget(outputJPG, 1)
        grid.addLayout(typeLayout, 8, 0)
        grid.addWidget(btnProcess, 9, 0)
        grid.addWidget(progBar, 10, 0)
        self.setLayout(grid)
        self.setFixedWidth(350)
        self.show()

        def explore_File():
            filePath, fileType = qtw.QFileDialog.getOpenFileName(self, "Open File", "", "PDF File (*.pdf)")
            print(filePath)
            if filePath != "":
                textBoxInput.setText(filePath)

        def save_File():
            filePath = qtw.QFileDialog.getExistingDirectory(self, "Save File", "")
            print(filePath)
            if filePath != "":
                textBoxOutput.setText(filePath)

        def process_File():
            if textBoxInput.text() == "":
                msgBox = qtw.QMessageBox()
                msgBox.setIcon(qtw.QMessageBox.Icon.Warning)
                msgBox.setWindowTitle("PDF Utils - Warning")
                msgBox.setText("Please select input file!")
                msgBox.exec()
                return
            if textBoxOutput.text() == "":
                msgBox = qtw.QMessageBox()
                msgBox.setIcon(qtw.QMessageBox.Icon.Warning)
                msgBox.setWindowTitle("PDF Utils - Warning")
                msgBox.setText("Please select output directory!")
                msgBox.exec()
                return

            progBar.setMinimum(0)
            progBar.setMaximum(0)
            print('onProcess')
            pdfPath = textBoxInput.text()
            print(pdfPath)
            pdfDoc = fitz.Document(pdfPath)
            imagePath = textBoxOutput.text()
            print(imagePath)
            for pg in range(pdfDoc.page_count):
                page = pdfDoc[pg]
                rotate = int(0)
                #dpi设置
                if dpi300.isChecked():
                    zoom_x = 3.125
                    zoom_y = 3.125
                    dpi = 300
                elif dpi144.isChecked():
                    zoom_x = 1.5625
                    zoom_y = 1.5625
                    dpi = 144
                elif dpi72.isChecked():
                    zoom_x = 0.78125
                    zoom_y = 0.78125
                    dpi = 72
                else:
                    zoom_x = 3.125
                    zoom_y = 3.125
                    dpi = 300
                mat = fitz.Matrix(zoom_x, zoom_y).prerotate(rotate)
                pix = page.get_pixmap(matrix=mat, alpha=False, dpi=dpi)
                fileName = os.path.basename(pdfPath)
                if outputJPG.isChecked():
                    fileType = 'jpg'
                elif outputPNG.isChecked():
                    fileType = 'png'
                else:
                    fileType = 'png'
                pix.save(str.format('{0}/{1}_{2}.{3}', imagePath, fileName, pg, fileType))
            pdfDoc.close()
            msgBox = qtw.QMessageBox()
            msgBox.setIcon(qtw.QMessageBox.Icon.Information)
            msgBox.setWindowTitle("PDF Utils - Notification")
            msgBox.setText("Process completed!")
            msgBox.exec()
            progBar.setMaximum(100)


if __name__ == '__main__':
    app = qtw.QApplication([])
    mw = MainWindow()
    app.exec()
