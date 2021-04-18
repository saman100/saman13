from library.models import Book
from library.owner import OwnerListView, OwnerDetailView, OwnerCreateView, OwnerUpdateView, OwnerDeleteView
from django.shortcuts import render
from library.models import Book
from django.views import View
from django.contrib.humanize.templatetags.humanize import naturaltime

from library.utils import dump_queries

from django.db.models import Q

#
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import BookSerializer
from rest_framework import viewsets, permissions

class BookListView(OwnerListView):
    model = Book
    template_name = "library/book_list.html"

    def get(self, request) :
        strval =  request.GET.get("search", False)
        if strval :
            # Simple title-only search
            # objects = Post.objects.filter(title__contains=strval).select_related().order_by('-updated_at')[:10]

            # Multi-field search
            # __icontains for case-insensitive search
            query = Q(title__icontains=strval)
            query.add(Q(description__icontains=strval), Q.OR)
            objects = Book.objects.filter(query).select_related().order_by('-publish_date')[:10]
        else :
            objects = Book.objects.all().order_by('-publish_date')[:10]

        # Augment the post_list
        for obj in objects:
            obj.natural_updated = naturaltime(obj.publish_date)

        ctx = {'book_list' : objects, 'search': strval}
        retval = render(request, self.template_name, ctx)

        dump_queries()
        return retval
    # By convention:
    # template_name = "myarts/article_list.html"


class BookDetailView(OwnerDetailView):
    model = Book


class BookCreateView(OwnerCreateView):
    model = Book
    fields = '__all__'

class BookUpdateView(OwnerUpdateView):
    model = Book
    fields = '__all__'


class BookDeleteView(OwnerDeleteView):
    model = Book


@api_view(['GET', 'POST'])
def get_post_book(request):
    if request.method == "GET":
        book = Book.objects.all()
        return Response(BookSerializer(book, many=True).data,
                      status=status.HTTP_200_OK)

    elif request.method == "POST":
        ser = BookSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'GET', 'DELETE'])
def get_update_delete_book(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except:
        return Response({"error": "Not Found!"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        ser = BookSerializer(book)
        return Response(ser.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        ser = BookSerializer(book, data=request.data)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_200_OK)
        else:
            return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)