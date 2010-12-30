import json
from pymongo.objectid import ObjectId

# TODO
# make ObjectId not enclosed in quotes

class DocumentEncoder(json.JSONEncoder):
    """
    Encode mongodb document to JSON string.

    DocumentEncoder encode ObjectId object to a string enclosed in
    "ObjectId('4d19a768ccb7846ef010ab04')".
    """

    def default(self, obj):
        if isinstance(obj, ObjectId):
            return 'ObjectId(%s)' % str(obj)
        return json.JSONEncoder.default(self, obj)

class DocumentDecoder(json.JSONDecoder):
    """
    Decode mongodb document to dict.

    DocumentEncoder decode string like "ObjectId('4d19a768ccb7846ef010ab04')"
    to ObjectId object.
    """
    def process_document(self, obj):
        if isinstance(obj, basestring) and obj.startswith('ObjectId(') and obj.endswith(')'):
            _id = obj[9:-1]
            return ObjectId(_id)
        if isinstance(obj, list) and obj:
            return [self.process_document(item) for item in obj]
        if isinstance(obj, dict):
            return dict([(key, self.process_document(value))
                         for key, value in obj.iteritems()])
        return obj

    def decode(self, s, **kwargs):
        decoded = super(DocumentDecoder, self).decode(s, **kwargs)
        return self.process_document(decoded)

