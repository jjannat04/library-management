from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Book, Author, Member, BorrowRecord
from .serializers import BookSerializer, AuthorSerializer, MemberSerializer, BorrowRecordSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

@api_view(['POST'])
def borrow_book(request):
    book_id = request.data.get('book')
    member_id = request.data.get('member')
    
    book = Book.objects.get(id=book_id)
    if not book.is_available:
        return Response({"error": "Book is already borrowed"}, status=status.HTTP_400_BAD_REQUEST)
    
    record = BorrowRecord.objects.create(book=book, member_id=member_id)
    book.is_available = False
    book.save()
    
    return Response(BorrowRecordSerializer(record).data, status=status.HTTP_201_CREATED)


from django.utils import timezone

@api_view(['POST'])
def return_book(request, record_id):
    try:
        record = BorrowRecord.objects.get(id=record_id, return_date__isnull=True)
    except BorrowRecord.DoesNotExist:
        return Response({"error": "Active record not found"}, status=status.HTTP_404_NOT_FOUND)
    
    
    record.return_date = timezone.now()
    record.save()
    
    
    record.book.is_available = True
    record.book.save()
    
    return Response({"message": "Book returned successfully"})