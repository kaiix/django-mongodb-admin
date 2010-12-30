# coding: utf-8
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.utils.encoding import smart_unicode

from pymongo import Connection
from pymongo.objectid import ObjectId

from utils import DocumentEncoder, DocumentDecoder

conn = Connection(settings.MONGODB_HOST, settings.MONGODB_PORT)
db = conn[settings.MONGODB_NAME]

def database_view(request, template_name='database.html',
            redirect_to='/'):

    def _not_system_index(colname):
        return colname != 'system.indexes'

    colnames = filter(_not_system_index, db.collection_names())
    cols = {}
    for name in colnames:
        cols[name] = db[name].count()

    return render_to_response(template_name, {
        'name': settings.MONGODB_NAME,
        'db': db,
        'collections': cols,
    }, context_instance=RequestContext(request))

# spec field name to show
# use ajax load json of docs?
def collection_view(request, colname, template_name='collection.html',
            redirect_to='/'):

    if request.method == 'GET':
        if colname in db.collection_names():
            col = db[colname]
            docs = [ x for x in col.find(as_class=Document) ]

            return render_to_response(template_name, {
                'colname': colname,
                'size': col.count(),
                'collection': col,
                'documents': docs,
            }, context_instance=RequestContext(request))
        return HttpResponseBadRequest()

from django.utils import simplejson
def add_collection(request):
    if request.method == 'POST':
        colname = request.POST.get('colname', '')
        colname = smart_unicode(colname.strip())
        if colname and colname not in db.collection_names():
            db.create_collection(colname)
            return HttpResponse(simplejson.dumps({'created': True}), mimetype='application/json')
        else:
            return HttpResponse(simplejson.dumps({'created': False}), mimetype='application/json')
    return HttpResponseBadRequest()

def clean_post(post_data):
    data = {}
    if 'csrfmiddlewaretoken' in post_data.keys():
        post_data.pop('csrfmiddlewaretoken')
    for k, v in post_data.iteritems():
        if k and v:
            data[k] = v
    return data

def save_doc(collection, doc, commit=True):
    print doc
    if commit:
        oid = collection.save(doc)
        return oid
    else:
        return doc

class Document(dict):
    _encoder = DocumentEncoder(ensure_ascii=False, encoding='utf-8')
    _decoder = DocumentDecoder()

    @classmethod
    def encode(cls, value):
        return cls._encoder.encode(value)

    @classmethod
    def decode(cls, value):
        return cls._decoder.decode(value)

    def _get_id(self):
        return unicode(self['_id'])
    id = property(_get_id)

    def __getitem__(self, key):
        value = super(Document, self).__getitem__(key)
        return self._decoder.decode(value)

    def __setitem__(self, key, value):
        super(Document, self).__setitem__(key, self._encoder.encode(value))

#todo documentadmin control how to display
def document_view(request, colname, doc_id,
                  template_name='document.html',
                  redirect_to='/'):
    if request.method == 'GET':
        if colname in db.collection_names():
            if doc_id:
                doc = db[colname].find_one({'_id': ObjectId(doc_id)}, as_class=Document)
                oid = doc.pop('_id')
            else:
                doc, oid = None, None
            return render_to_response(template_name, {
                'doc': doc,
                'oid': oid,
                'colname': colname,
            }, context_instance=RequestContext(request))
        return HttpResponseBadRequest()
    else:
        # make a clean data to process
        data = clean_post(request.POST.copy())
        print data
        if data:
            to_save = {}
            for k, v in data.iteritems():
                to_save[k] = Document.decode(v)
            save_doc(db[colname], to_save)
        return HttpResponseRedirect('/database/collection/%s/' % colname)
    return HttpResponseBadRequest()
