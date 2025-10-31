import sys
from database1 import Database
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QMessageBox)
from PyQt5.QtCore import QTimer, Qt
from functools import partial


class ClickerGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clicker")
        self.setFixedSize(300, 400)

        self.clicks = 0
        self.click_power = 1
        self.auto_click = 0

        self.upgrades = [
            {"name": "+2 per click", "cost": 15, "type": "click", "amount": 2},
            {"name": "Autoclick +1", "cost": 30, "type": "auto", "amount": 1},
            {"name": "Click x3", "cost": 90, "type": "click", "amount": 3},
            {"name": "Autoclick x4", "cost": 200, "type": "auto", "amount": 4},
            {"name": "Ultra: +10 clicks ", "cost": 1000, "type": "click", "amount": 10}
        ]

        self.init()
        self.start_timer()

        # Load DB data (kept for later use). No graph calls anymore.
        with Database("database1.db") as db:
            self.DATA = list(db.get_expenses())

    def init(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(15)

        self.click_label = QLabel(f"Clicks: {self.clicks}")
        self.click_label.setAlignment(Qt.AlignCenter)
        self.click_label.setStyleSheet("font-size: 30px; font-weight: bold;")
        layout.addWidget(self.click_label)

        self.click_button = QPushButton("Click me!")
        self.click_button.clicked.connect(self.on_click)
        self.click_button.setStyleSheet("""
            QPushButton {
                background-color: #ff5e78;
                color: white;
                font-size: 18px;
                padding: 15px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #ff7e95;
            }
            QPushButton:pressed {
                background-color: #e94b68;
            }
        """)
        layout.addWidget(self.click_button)
        self.upgrade_buttons = []
        for upgrade in self.upgrades:
            buttton = QPushButton(f"{upgrade['name']} (Price: {upgrade['cost']})")
            buttton.clicked.connect(partial(self.buy_upgrade, upgrade))
            buttton.setStyleSheet("""
            QPushButton{
            background-color: #ff5e78;
                color: white;
                font-size: 15px;
                padding: 10px;
                border-radius: 10px;
                }
            QPushButton:hover {
                background-color: #ff7e95;
            }
            QPushButton:pressed {
                background-color: #e94b68;
            }
        """)
            layout.addWidget(buttton)
            self.upgrade_buttons.append(buttton)

        self.setStyleSheet("background-color: #f0a3b2;")
        self.setLayout(layout)

    def on_click(self):
        self.clicks += self.click_power
        self.update_display()

    def buy_upgrade(self, upgrade):
        if self.clicks >= upgrade["cost"]:
            self.clicks -= upgrade["cost"]
            if upgrade["type"] == "click":
                self.click_power += upgrade["amount"]
            elif upgrade["type"] == "auto":
                self.auto_click += upgrade["amount"]
            upgrade["cost"] = int(upgrade["cost"] * 2)
            self.update_buttons()
            self.update_display()
        else:
            QMessageBox.information(self,
                                    "Not enough clicks",
                                    f"to purchase you need {upgrade['cost']} clicks.."
            )

    def update_buttons(self):
        for i, upgrade in enumerate(self.upgrades):
            self.upgrade_buttons[i].setText(f"{upgrade['name']} (Price: {upgrade['cost']})")

    def update_display(self):
        self.click_label.setText(f"Clicks: {self.clicks}")

    def start_timer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(1000)

    def game_loop(self):
        self.clicks += self.auto_click
        self.update_display()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = ClickerGame()
    game.show()
    sys.exit(app.exec_())