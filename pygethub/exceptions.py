class BadRequest(Exception):
    """Exception raised for bad requests"""
    def __init__(self, response):
        self.response = response
        self.status_code = response.get("status")
        self.message = response.get("message")
        self.details = response.get("details")
        super().__init__("\n".join([self.message, self.details]))