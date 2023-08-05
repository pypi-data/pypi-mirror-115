import PyQt5
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWebEngineCore import QWebEngineUrlScheme
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngine import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtNetwork import *
from tkinter import *
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess

def browser(name, url, icon):
    a = 'https://'
    class MainWindow(QMainWindow):
        def __init__(self):
            super(MainWindow, self).__init__()
            self.browser = QWebEngineView()
            self.browser.setUrl(QUrl(a + url))
            self.setCentralWidget(self.browser)
            self.showMaximized()

            # navbar
            navbar = QToolBar()
            self.addToolBar(navbar)

            back_btn = QAction('Back', self)
            back_btn.triggered.connect(self.browser.back)
            navbar.addAction(back_btn)

            forward_btn = QAction('Forward', self)
            forward_btn.triggered.connect(self.browser.forward)
            navbar.addAction(forward_btn)

            reload_btn = QAction('Reload', self)
            reload_btn.triggered.connect(self.browser.reload)
            navbar.addAction(reload_btn)

            home_btn = QAction('Home', self)
            home_btn.triggered.connect(self.navigate_home)
            navbar.addAction(home_btn)

            self.url_bar = QLineEdit()
            self.url_bar.returnPressed.connect(self.navigate_to_url)
            navbar.addWidget(self.url_bar)

            self.browser.urlChanged.connect(self.update_url)

        def navigate_home(self):
            self.browser.setUrl(QUrl(a + url))

        def navigate_to_url(self):
            url = self.url_bar.text()
            self.browser.setUrl(QUrl(a + url))

        def update_url(self, q):
            self.url_bar.setText(q.toString())


    app = QApplication(sys.argv)
    QApplication.setApplicationName(name)
    QApplication.setWindowIcon(QIcon(icon))
    window = MainWindow()
    app.exec_()

def notepad(name, icon):
    compiler = Tk()
    compiler.title(name)
    compiler.iconbitmap(icon)
    file_path = ''


    def set_file_path(path):
        global file_path
        file_path = path


    def open_file():
        path = askopenfilename(filetypes=[('Python Files', '*.py'),('HTML Files', '*.html'),('Text File', '*.txt'),('Javascript File', '*.js'),('CSS File', '*.css'),('Java File', '*.java'),('PHP File', '*.php'),('MarkDown File', '*.md'),('Kotlin File', '*.kt')])
        with open(path, 'r') as file:
            code = file.read()
            editor.delete('1.0', END)
            editor.insert('1.0', code)
            set_file_path(path)


    def save_as():
        if file_path == '':
            path = asksaveasfilename(filetypes=[('Python Files', '*.py'),('HTML Files', '*.html'),('Text File', '*.txt'),('Javascript File', '*.js'),('CSS File', '*.css'),('Java File', '*.java'),('PHP File', '*.php'),('MarkDown File', '*.md'),('Kotlin File', '*.kt')])
        else:
            path = file_path
        with open(path, 'w') as file:
            code = editor.get('1.0', END)
            file.write(code)
            set_file_path(path)


    def run():
        if file_path == '':
            save_prompt = Toplevel()
            text = Label(save_prompt, text='Please save your code')
            text.pack()
            return
        command = f'python {file_path}'
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output, error = process.communicate()
        code_output.insert('1.0', output)
        code_output.insert('1.0',  error)


    menu_bar = Menu(compiler)

    file_menu = Menu(menu_bar, tearoff=0)
    file_menu.add_command(label='Open', command=open_file)
    file_menu.add_command(label='Save', command=save_as)
    file_menu.add_command(label='Save As', command=save_as)
    file_menu.add_command(label='Exit', command=exit)
    menu_bar.add_cascade(label='File', menu=file_menu)

    run_bar = Menu(menu_bar, tearoff=0)
    run_bar.add_command(label='Run', command=run)
    menu_bar.add_cascade(label='Run', menu=run_bar)

    compiler.config(menu=menu_bar)

    editor = Text()
    editor.pack()

    code_output = Text(height=10)
    code_output.pack()

    compiler.mainloop()

def calculator(name, icon):
    def press(num):
        global expression

        expression = expression + str(num)

        equation.set(expression)

    def equalpress():
        try:

            global expression

            total = str(eval(expression))

            equation.set(total)

            expression = ""

        except:

            equation.set(" error ")
            expression = ""

    def clear():
        global expression
        expression = ""
        equation.set("")


    if __name__ == "__main__":
        gui = Tk()

        gui.configure(background="light green")

        gui.title(name)

        gui.iconbitmap(icon)

        gui.geometry("270x150")

        equation = StringVar()

        expression_field = Entry(gui, textvariable=equation)

        expression_field.grid(columnspan=4, ipadx=70)

        button1 = Button(gui, text=' 1 ', fg='black', bg='red',
                        command=lambda: press(1), height=1, width=7)
        button1.grid(row=2, column=0)

        button2 = Button(gui, text=' 2 ', fg='black', bg='red',
                        command=lambda: press(2), height=1, width=7)
        button2.grid(row=2, column=1)

        button3 = Button(gui, text=' 3 ', fg='black', bg='red',
                        command=lambda: press(3), height=1, width=7)
        button3.grid(row=2, column=2)

        button4 = Button(gui, text=' 4 ', fg='black', bg='red',
                        command=lambda: press(4), height=1, width=7)
        button4.grid(row=3, column=0)

        button5 = Button(gui, text=' 5 ', fg='black', bg='red',
                        command=lambda: press(5), height=1, width=7)
        button5.grid(row=3, column=1)

        button6 = Button(gui, text=' 6 ', fg='black', bg='red',
                        command=lambda: press(6), height=1, width=7)
        button6.grid(row=3, column=2)

        button7 = Button(gui, text=' 7 ', fg='black', bg='red',
                        command=lambda: press(7), height=1, width=7)
        button7.grid(row=4, column=0)

        button8 = Button(gui, text=' 8 ', fg='black', bg='red',
                        command=lambda: press(8), height=1, width=7)
        button8.grid(row=4, column=1)

        button9 = Button(gui, text=' 9 ', fg='black', bg='red',
                        command=lambda: press(9), height=1, width=7)
        button9.grid(row=4, column=2)

        button0 = Button(gui, text=' 0 ', fg='black', bg='red',
                        command=lambda: press(0), height=1, width=7)
        button0.grid(row=5, column=0)

        plus = Button(gui, text=' + ', fg='black', bg='red',
                    command=lambda: press("+"), height=1, width=7)
        plus.grid(row=2, column=3)

        minus = Button(gui, text=' - ', fg='black', bg='red',
                    command=lambda: press("-"), height=1, width=7)
        minus.grid(row=3, column=3)

        multiply = Button(gui, text=' * ', fg='black', bg='red',
                        command=lambda: press("*"), height=1, width=7)
        multiply.grid(row=4, column=3)

        divide = Button(gui, text=' / ', fg='black', bg='red',
                        command=lambda: press("/"), height=1, width=7)
        divide.grid(row=5, column=3)

        equal = Button(gui, text=' = ', fg='black', bg='red',
                    command=equalpress, height=1, width=7)
        equal.grid(row=5, column=2)

        clear = Button(gui, text='Clear', fg='black', bg='red',
                    command=clear, height=1, width=7)
        clear.grid(row=5, column='1')

        Decimal= Button(gui, text='.', fg='black', bg='red',
                        command=lambda: press('.'), height=1, width=7)
        Decimal.grid(row=6, column=0)
        gui.mainloop()