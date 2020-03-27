from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.http import FileResponse
from .forms import BookForm
from .models import Book

import os
import PyPDF2
import zipfile


class Home(TemplateView):
    template_name = 'home.html'

def book_list(request):
    if request.method == 'POST':
        books = Book.objects.all()
        book_num = len(books)
        
        pdfMerger = PyPDF2.PdfFileMerger() 

        for book in books:
                if book:
                    pdfFileObj = PyPDF2.PdfFileReader(book.pdf)
                    pdfMerger.append(pdfFileObj)   
        with open(os.path.join('media', 'merged_file.pdf'), 'wb') as pdfOutputFile:
                pdfMerger.write(pdfOutputFile)
        response = FileResponse(open(os.path.join('media', 'merged_file.pdf'), 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename="merged_file.pdf"'

        return response    
        
    else:
        books = Book.objects.all()
        return render(request, 'book_list.html', {
            'books': books
    })


def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'upload_book.html', {
        'form': form
    })


def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')



