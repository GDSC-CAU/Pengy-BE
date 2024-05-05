from django.urls import path
from .views import FireHazardEducationViewSet

app_name = 'eduContents'
urlpatterns = [
    path('get-contents/<int:pk>/', FireHazardEducationViewSet.as_view({'get': 'retrieve'}), name='get_contents'),
    path('update-contents/', FireHazardEducationViewSet.as_view({'post': 'update_contents'}), name='update_contents'),
    # Add the new route for fetching educational content

    # #TODO: 이거 문자열이나 쿼리가 들어와야하는데..
    # path('fetch-edu-content/<str:slug>/', FireHazardEducationViewSet.as_view({'get': 'fetch_edu_content'}), name='fetch_edu_content'),
]
