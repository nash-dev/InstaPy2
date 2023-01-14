class Comments:
    def __init__(self):
        self.comments = []
        self.percentage = 0

    def set_comments(self, comments: list[str]):
        self.comments = comments

    def set_percentage(self, percentage: int):
        self.percentage = percentage