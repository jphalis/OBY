from django.conf.urls import patterns, url


urlpatterns = patterns('donations.views',
    url(r'^completed/$', 'donation_complete', name='donation_complete'),
    url(r'^create/$', 'make_donation', name='make_donation'),
    url(r'^history/$', 'donation_history', name="donation_history"),
)
