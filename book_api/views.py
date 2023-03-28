from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from book_api.models import Book
from book_api.serializer import BookSerializer
# Create your views here.

#ENDPOINTS
@api_view(['GET']) #gets an array of books /book/list
def book_list(request):
    books = Book.objects.all() #complex Data: Not python
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

@api_view(['POST']) #user to create a new book /book/
def book_create(request):
    serializer = BookSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# /book/id -get the specific book

@api_view(['GET', 'PUT', 'DELETE']) # update and delete 
def book(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except:
        return Response({
            'error':'Book does not exist'
         }, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)
    
    if request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

    if request.method == 'DELETE':
        book.delete()
        return Response({
            'delete': True
        })


