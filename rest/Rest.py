import json
from datetime import date
from flask_restful import Resource, reqparse
from flask import jsonify, make_response

class Rest(Resource):

    reqparse = reqparse

    _args = []

    def __init__(self):
        pass

    def getArgs(self, args=None):

        if args is None:
            args = self._args

        parser = self.reqparse.RequestParser(
            bundle_errors=True
        )

        for arg in args:
            parser.add_argument(
                arg['arg'],
                type=arg['type'],
                help=arg['help'],
                required=arg['req'] if 'req' in arg else False
            )

        return parser.parse_args()

    """
        property _data is use in
        getAll property
    """
    @property
    def _data(self):
        pass

    """
        property getAll
        this for get all data with serialize json
    """

    def getAll(self, data=None):
        return self.serialize(
            self.all(
                self._data if data is None else data
            )
        )

    """
        static method serialize
        :obj: the object to json with response status 200
    """
    @staticmethod
    def serialize(obj, 
            status=200, 
            message=None, 
            access_token=None, 
            refresh_token=None):

        if message is not None \
            and 'message' not in obj:
            obj['message'] = message
        
        respon = jsonify(obj)

        return make_response(
            respon, status
        )

    """
        static method get all
        :obj: all model object
    """

    def all(self, obj):
        exclude = [
            'query',
            'query_class',
            'metadata'
        ]

        list_items = {
            'data': [],
            'total': 0
        }

        for items in obj:
            if hasattr(items, 'serialize'):
                data = items.serialize
            else:
                data = {}
                for item in items.__mapper__.columns.keys():
                    key = str(item)
                    item = getattr(items, key)
                    try:
                        if hasattr(item, 'isoformat') and callable(item.isoformat):
                            item = item.isoformat()
                        elif hasattr(item, 'serialize'):
                            item = item.serialize
                        else:
                            json.dumps(item)
                        data[key] = item
                    except TypeError:
                        data[key] = None

            list_items['data'].append(data)

        list_items['total'] = len(
            list_items['data']
        )

        return list_items
