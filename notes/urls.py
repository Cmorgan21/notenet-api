from django.urls import path
from . import views

urlpatterns = [
    path('user/register/',  views.CreateUserView.as_view(), name='register'),
    path('notes/', views.NoteList.as_view(), name='note_list'),
    path('create-note/',  views.CreateNoteView.as_view(), name='create_note'),
    path('delete-note/<int:pk>/',  views.DeleteNoteView.as_view(), name='delete_note'),
    path('notes/<int:pk>/', views.NoteDetail.as_view(), name='note_detail'), 
    path('notes/update/<int:pk>/', views.UpdateNoteView.as_view(), name='note-detail'),
]
