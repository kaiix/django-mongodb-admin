from django.conf.urls.defaults import *

urlpatterns = patterns('',
    #(r'^add$', 'mongodb_admin.views.add', {'col': 'site'}),
    (r'^$', 'mongodb_admin.views.database_view'),
    # collection
    (r'^collection/add$', 'mongodb_admin.views.add_collection'),
    (r'^collection/(?P<colname>[a-z._]+)/$', 'mongodb_admin.views.collection_view'),
    # document
    (r'^collection/(?P<colname>[a-z._]+)/document/add/$', 'mongodb_admin.views.document_view', {'doc_id': ''}),
    (r'^collection/(?P<colname>[a-z._]+)/document/(?P<oid>.+)/del$', 'mongodb_admin.views.del_item'),
    (r'^collection/(?P<colname>[a-z._]+)/document/(?P<doc_id>.+)/$', 'mongodb_admin.views.document_view'),
)

