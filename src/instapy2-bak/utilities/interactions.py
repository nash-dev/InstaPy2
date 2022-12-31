from instagrapi import Client

from typing import Dict

class InteractionsUtility:
    def __init__(self):
        self.amount = 10
        self.enabled = True
        self.percentage = 100
        self.randomize = False

    def from_json(self, data: Dict):
        self.amount = data['amount'] or 0
        self.enabled = data['enabled'] or False
        self.percentage = data['percentage'] or 0
        self.randomize = data['randomize'] or False


    def set_amount(self, amount: int):
        self.amount = amount

    def set_enabled(self, enabled: bool):
        self.enabled = enabled

    def set_percentage(self, percentage: int):
        self.percentage = percentage

    def set_randomize(self, randomize: bool):
        self.randomize = randomize