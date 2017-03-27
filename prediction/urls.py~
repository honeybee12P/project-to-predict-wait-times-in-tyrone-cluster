from django.conf.urls import patterns,include, url
from django.contrib import admin
from prediction_time.src import run_simulator_client
import thread

admin.autodiscover()
urlpatterns = [
    # Examples:
    # url(r'^$', 'prediction.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^interface/$', 'prediction_time.views.interface'),
    url(r'^contributors/$', 'prediction_time.views.contributors'),
    url(r'^submit/$', 'prediction_time.views.get_data_from_user'),
    
    
    url(r'^contactus/$', 'prediction_time.views.contactus'),
    url(r'^contact_us/$', 'prediction_time.views.contact_us'),
    
    url(r'^howitworks/$', 'prediction_time.views.howitworks'),
    #url(r'^log/$','books.views.post_question'),
]

runSimulatorClient = run_simulator_client.RunSimulatorClient()
thread.start_new_thread(runSimulatorClient.metaScheduler.run, (runSimulatorClient.num_processors,))

def getSimulatorObject():
	return runSimulatorClient
#runSimulatorClient.metaScheduler.handle_pred_request()
