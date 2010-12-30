from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'mongodb_admin.views.database_view'),
    # collection
    (r'^collection/add$', 'mongodb_admin.views.add_collection'),
    (r'^collection/(?P<colname>[a-z._]+)/$', 'mongodb_admin.views.collection_view'),
    # document
    (r'^collection/(?P<colname>[a-z._]+)/document/add/$', 'mongodb_admin.views.document_view', {'doc_id': ''}),
    (r'^collection/(?P<colname>[a-z._]+)/document/(?P<doc_id>.+)/$', 'mongodb_admin.views.document_view'),
    # field
    (r'^collection/(?P<colname>[a-z._]+)/document/(?P<doc_id>.+)/field/(?P<field_name>[a-z_]+)/$', 'mongodb_admin.views.field_view'),
)

