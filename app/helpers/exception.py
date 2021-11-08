class ApiException(Exception):
    def __init__(self, status_code, data):
        self.code = status_code
        self.data = data
        super().__init__(self.data)
