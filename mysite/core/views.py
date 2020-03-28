from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.http import FileResponse
from .forms import BookForm
from .models import Book
from pdfrw import PdfReader, PdfWriter, IndirectPdfDict
import os
import PyPDF2
import zipfile


class Home(TemplateView):
    template_name = 'home.html'

def book_list(request):
    if request.method == 'POST':
        books = Book.objects.all()
        book_num = len(books)
        
        writer = PdfWriter()

        for book in books:
                if book:
                     writer.addpages(PdfReader(book.pdf).pages)

        with open(os.path.join('media', 'mergedfile.pdf'), 'wb') as pdfOutputFile:
                writer.write(pdfOutputFile)
        response = FileResponse(open(os.path.join('media', 'mergedfile.pdf'), 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename="mergedfile.pdf"'

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
            form2 = form.save(commit=False)
            inpfn = form.cleaned_data['pdf']
            print(inpfn)
            
            page_range = [int(y) for y in form.cleaned_data['page'].split('-')]
            page_start = int(page_range[0])
            page_end = int(page_range[1])
            path = os.path.join('/books/pdfs', 'extracted_page_{}-{}.pdf'.format(page_start, page_end))
            outfn = os.path.join('media', 'extracted_page_{}-{}.pdf'.format(page_start, page_end))
            pages = PdfReader(inpfn).pages
            outdata = PdfWriter(outfn)  
            page_range = (page_range + page_range[-1:])[:2]
    
            for pagenum in range(page_range[0], page_range[1]+1):
                outdata.addpage(pages[pagenum-1])
            outdata.write()
            form2.pdf = os.path.join('extracted_page_{}-{}.pdf'.format(page_start, page_end))
            form2.save()
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



