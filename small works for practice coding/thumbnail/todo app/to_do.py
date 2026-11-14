import sys

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget,
    QVBoxLayout,
    QHBoxLayout
)

from PyQt5.QtCore import Qt


class TodoApp(QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("My To-Do App")
        self.setGeometry(500, 200, 500, 600)

        self.create_ui()

    def create_ui(self):

        # Title
        title = QLabel("My To-Do List")
        title.setAlignment(Qt.AlignCenter)

        # Input
        self.task_input = QLineEdit()
        self.task_input.setPlaceholderText("Enter a task...")

        # Buttons
        add_button = QPushButton("Add Task")
        delete_button = QPushButton("Delete Task")
        complete_button = QPushButton("Complete Task")
        clear_button = QPushButton("Clear All")

        # Task list
        self.task_list = QListWidget()

        # Add task
        add_button.clicked.connect(self.add_task)

        # Delete task
        delete_button.clicked.connect(self.delete_task)

        # Complete task
        complete_button.clicked.connect(self.complete_task)

        # Clear all
        clear_button.clicked.connect(self.clear_tasks)

        # Enter key also adds task
        self.task_input.returnPressed.connect(self.add_task)

        # Button layout
        button_layout = QHBoxLayout()

        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)

        button_layout2 = QHBoxLayout()

        button_layout2.addWidget(complete_button)
        button_layout2.addWidget(clear_button)

        # Main layout
        layout = QVBoxLayout()

        layout.addWidget(title)
        layout.addWidget(self.task_input)
        layout.addLayout(button_layout)
        layout.addWidget(self.task_list)
        layout.addLayout(button_layout2)

        self.setLayout(layout)

    # =========================
    # ADD TASK
    # =========================

    def add_task(self):

        task = self.task_input.text().strip()

        if task:

            self.task_list.addItem(task)

            self.task_input.clear()

    # =========================
    # DELETE TASK
    # =========================

    def delete_task(self):

        selected_task = self.task_list.currentRow()

        if selected_task >= 0:

            self.task_list.takeItem(selected_task)

    # =========================
    # COMPLETE TASK
    # =========================

    def complete_task(self):

        selected_task = self.task_list.currentItem()

        if selected_task:

            task = selected_task.text()

            if not task.startswith("✓ "):

                selected_task.setText("✓ " + task)

    # =========================
    # CLEAR ALL
    # =========================

    def clear_tasks(self):

        self.task_list.clear()


# =========================
# START APPLICATION
# =========================

app = QApplication(sys.argv)

window = TodoApp()

window.show()

sys.exit(app.exec_())