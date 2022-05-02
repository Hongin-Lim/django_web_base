from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect
from board.forms import BoardForm
from board.models import Board
from django.http import JsonResponse, HttpResponse

import requests
import json



def request_api4(request):
    return render(request,'test.html')

def request_api(request):
    res = requests.get('http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst?serviceKey=%2FhXI3bLvQ9gK93YmgxYlBCr5BkGivp6SMjDMoEHmthpgcqDLB1uK59pMkw2g4odZy56zEA4CqmGxJuNe807bUA%3D%3D&numOfRows=10&pageNo=1&dataType=json&base_date=20220124&base_time=0600&nx=58&ny=125')
    print(str(res.status_code))
    result = json.loads(res.text)
    print(result['response']['body']['items']['item'][0]['obsrValue'])

    return render(request,'test.html')



@login_required(login_url='/user/login')
def like(request, bid):
    post = Board.objects.get(Q(id=bid))
    user = request.user
    if post.like.filter(id=user.id).exists() :  # 게시글 좋아요 눌렀음
        post.like.remove(user)
        message = 'del'
    else :                                      # 게시글 좋아요 아직 안눌었음
        post.like.add(user)
        message = 'add'
    return JsonResponse(
        {
            'message':message,
            'like_cnt': post.like.count()
        }
    )



def home(request):
    return redirect('/board/list')

@login_required(login_url='/user/login')
def register(request):
    if request.method == "GET" :
        boardForm = BoardForm()
        return render(request, 'board/register.html',
                  {'boardForm':boardForm})
    elif request.method == "POST" :
        boardForm = BoardForm(request.POST)
        if boardForm.is_valid():
            board = boardForm.save(commit=False)
            board.writer = request.user
            board.save()
            return redirect('/board/list')

def posts(request):
    posts = Board.objects.all().order_by('-id')

    return render(request, 'board/list.html',
                            {'posts':posts})

def read(request, bid):
    post = Board.objects.get( Q(id=bid) )
    return render(request, 'board/read.html',
                                    {'post':post})
@login_required(login_url='/user/login')
def delete(request, bid):
    post = Board.objects.get( Q(id=bid) )
    if request.user != post.writer:
        return redirect('/board/list')

    post.delete()
    return redirect('/board/list')

@login_required(login_url='/user/login')
def update(request, bid):
    post = Board.objects.get(Q(id=bid))
    if request.user != post.writer:
        return redirect('/board/list')

    if request.method == "GET":
        boardForm = BoardForm(instance=post)
        return render(request, 'board/update.html',
                      {'boardForm':boardForm})
    elif request.method == "POST":
        boardForm = BoardForm(request.POST)
        if boardForm.is_valid():
            post.title = boardForm.cleaned_data['title']
            post.contents = boardForm.cleaned_data['contents']
            post.save()
            return redirect('/board/read/'+str(bid))






