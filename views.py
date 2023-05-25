from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Question, Answer
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout

def home(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'quora_app/home.html', {'questions': questions})

@login_required(login_url='login')
def create_question(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        question = Question.objects.create(title=title, description=description, author=request.user)
        return redirect('home')
    return render(request, 'quora_app/create_question.html')

def question_detail(request, question_id):
    question = Question.objects.get(id=question_id)
    answers = Answer.objects.filter(question=question).order_by('-created_at')
    return render(request, 'quora_app/question_detail.html', {'question': question, 'answers': answers})

@login_required(login_url='login')
def create_answer(request, question_id):
    if request.method == 'POST':
        content = request.POST['content']
        question = Question.objects.get(id=question_id)
        answer = Answer.objects.create(content=content, question=question, author=request.user)
        return redirect('question_detail', question_id=question_id)
    return render(request, 'quora_app/create_answer.html')

@login_required(login_url='login')
def like_answer(request, answer_id):
    answer = Answer.objects.get(id=answer_id)
    answer.likes.add(request.user)
    return redirect('question_detail', question_id=answer.question.id)





def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'quora_app/login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

def user_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'quora_app/signup.html', {'form': form})

