from django.urls import path

from example.notes.views import CreateNote, DeleteNote, EditNote, ListNotes

urlpatterns = [
    path("", ListNotes.as_view(), name="list_notes"),
    path("create/", CreateNote.as_view(), name="create_note"),
    path("edit/<int:pk>/", EditNote.as_view(), name="edit_note"),
    path("delete/<int:pk>/", DeleteNote.as_view(), name="delete_note"),
]
