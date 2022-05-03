import os.path
import urllib.parse
import mimetypes

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponse, Http404

from .forms import BoardWriteForm, CommentWriteForm
from .models import Board, Comment, Announcement

login_url = '/accounts/login'


def service(request):
    return render(request, 'service.html')


@login_required(login_url='/accounts/login')
def service_write(request):
    context = {}
    if request.method == 'POST':
        form = BoardWriteForm(request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.user_id = request.session['_auth_user_id']
            form.save()

            if request.FILES:
                for file in request.FILES.getlist('files'):
                    Announcement.objects.create(
                        name=file.name,
                        uploadFile=file,
                        board_id=form.id,
                    )
            return redirect('board_list')
        else:
            context['form'] = form
    return render(request, 'service_write.html', context)


@login_required(login_url=login_url)
def listing(request):
    board = Board.objects.order_by('-id')
    paginator = Paginator(board, 10)

    page_number = request.GET.get('page', 1)
    board_list = paginator.get_page(page_number)

    start_page = (int(page_number) - 1) // 10 * 10 + 1
    end_page = start_page + 9

    if end_page > paginator.num_pages:
        end_page = paginator.num_pages

    context = {
        'board_list': board_list,
        'page_range': range(start_page, end_page + 1)
    }
    return render(request, 'board_list.html', context)


@login_required(login_url=login_url)
def board_detail_view(request, pk):
    board = get_object_or_404(Board, pk=pk)
    file = Announcement.objects.filter(board_id__exact=pk)
    context = {
        'board': board,
        'file': file,
    }
    return render(request, 'board_detail.html', context)

@login_required(login_url=login_url)
def qna_write(request):
    return render(request, 'qna_write.html')

def faq(request):
    return render(request, 'faq.html')

def file_download(request, pk):
    announcement = get_object_or_404(Announcement, file_ptr_id=pk)
    url = announcement.uploadFile.url[1:]
    file_url = urllib.parse.unquote(url)

    if os.path.exists(file_url):
        with open(file_url, 'rb') as f:
            quote_file_url = urllib.parse.quote(announcement.name.encode('utf-8'))
            response = HttpResponse(f.read(), content_type=mimetypes.guess_type(file_url)[0])
            response['Content-Disposition'] = 'attachment;filename*=UTF-8\'\'%s' % quote_file_url
            return response
    raise Http404
