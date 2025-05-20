class Result:
    def __init__(self, status_code: int, message: str = "", data: dict = None):
        self.status_code = int(status_code)
        self.message = str(message)
        self.data = data if data else {}
