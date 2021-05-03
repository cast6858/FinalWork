import requests

class ValidationOfCity:
    def __init__(self,json_payload):
        self.code = json_payload['cod']
        self.status_number = ''


    def status_code(self):
        status = ''
        if(self.code == 200):
            self.status_number = '200'
            status = False
        elif(self.code == 404):
            self.status_number = '400'
            status = True
        else:
            status = True
        return status



