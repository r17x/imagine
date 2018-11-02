from rest.Rest import Rest

class RestMedia(Rest):
    _data = []

    def get(self):
        return self.getAll()

    def post(self):
        pass
