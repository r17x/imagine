from rest.Rest import Rest
from flask import request

"""
    RestMedia: extends from class Rest
        :get: http get method
        :post: http post method
"""
class RestMedia(Rest):
    """
        :_data: all data (models) 
    """
    _data = []

    def get(self):
        return self.getAll()

    def post(self):
        if 'file' not in request.files:
            print(request)
            return self.serialize({
                'message': "not files send from you",
                }, status=400
            )
