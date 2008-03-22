from django.conf.urls.defaults import *

urlpatterns = patterns('hgfront.queue.views',
    (r'^createqueue/$', 'create_queue'), #post 'name' of queue
    (r'^deletequeue/$', 'delete_queue'), #post 'name' of queue
    (r'^purgequeue/$', 'purge_queue'),   #post 'name' of queue
    (r'^listqueues/$', 'list_queues'),
    
    (r'^q/(?P<queue_name>\w+)/put/$', 'put'),
    (r'^q/(?P<queue_name>\w+)/clearexpire/$', 'clear_expirations'),
    (r'^q/(?P<queue_name>\w+)/count/json/$', 'count', {"response_type":"json"}),
    (r'^q/(?P<queue_name>\w+)/count/$', 'count', {"response_type":"text"}),
    (r'^q/(?P<queue_name>\w+)/delete/$', 'delete'), #post 'message_id' of msg
    (r'^q/(?P<queue_name>\w+)/json/$', 'get', {"response_type":"json"}),
    (r'^q/(?P<queue_name>\w+)/$', 'get', {"response_type":"text"}),
)
