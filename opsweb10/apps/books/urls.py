#-*- coding: utf-8 -*-

from django.conf.urls import url
from books import book, publish, author
from dashboard import power

urlpatterns = [
    url(r'^publishlist/?$', publish.PublishListView.as_view(), name="publish_list"),
    url(r'^publishdetail/(?P<pk>\d+)?/?$', publish.PublishDetailView.as_view(), name="publish_detail"),

    url(r'^booklist/?$', book.BookListView.as_view(), name="book_list"),
    url(r'^bookdetail/(?P<pk>\d+)?/?$', book.BookDetailView.as_view(), name="book_detail"),

    url(r'^authorlist/?$', author.AuthorListView.as_view(), name="author_list"),
    url(r'^authordetail/(?P<pk>\d+)?/?$', author.AuthorDetailView.as_view(), name="author_detail"),

    url(r'^powerlist/?$', power.PermissionListView.as_view(), name='power_list'),
]