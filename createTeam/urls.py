from django.urls import path
from . import views

urlpatterns = [
    path('create', views.TeamCreation.as_view(), name='teamCreation'),
    path('members', views.AddMembers.as_view(), name='addMember'),
    path('addmember/<uid>/<token>', views.AcceptInvitation.as_view(), name="addMember"),
    path('users', views.ChatUsers.as_view())
]
