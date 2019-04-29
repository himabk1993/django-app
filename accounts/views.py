from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views import generic
from .models import Question, Choice
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone
from django.contrib.auth.models import User

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def quest(request):
 #   question_list = Question.objects.order_by('-pub_date')
 #  context = { 'question_list' : question_list }
    context = 'Create the question'
    return render(request,'accounts/quest.html', {'context' : context})

def questAdd(request):
    current_user = request.user
    user_question = request.POST.get('question_text')
    print("quest ",user_question)
#    import pdb
#    pdb.set_trace()
#    question = None
    existing_question = Question.objects.filter(question_text__iexact = user_question)   
    print("exist_qn",existing_question,"count",existing_question.count())   

    if not existing_question:
        question = Question.objects.create(question_text = user_question, pub_date = timezone.now(), user_id =  current_user.id)
        choice_text = request.POST.get('choice_text')
        choices = choice_text.split(",")
        for choice in choices:
            choice = choice.strip()
            print("choices ",choice)
            if not choice.isspace():
                print("choice",choice)
                Choice.objects.create(user_id = current_user.id, choice_text = choice, question_id = question.id, votes = 0)
        return HttpResponseRedirect(reverse('accounts:index'))   

    else:
        question = None
        print("trying to enter same question")
        return render(request, 'accounts/quest.html', {
            'question' : question,
            'error_message' : "You are trying to enter an existing question",
        })         

def index(request):
    question_list = Question.objects.order_by('-pub_date')
    print("q list",question_list)
 #   context = { 'question_list' : question_list }
 #   context = "You are seeing the question list"
    context = { 'question_list' : question_list }
    
    return render(request,'accounts/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    current_user = request.user
    if(current_user.id != question.user_id):
        print("same user")
        return render (request, 'accounts/detail.html', {'question' : question})
    else:
        print("different user")
        return render(request, 'accounts/index.html', {
            'question' : question,
            'error_message' : "You cannot vote for the question you created ",
        })


def results(request, question_id):
    question = get_object_or_404(Question, pk = question_id)
    return render(request, 'accounts/results.html', { 'question' : question })

def vote(request, question_id):
#    return HttpResponse(" Voting on question %s " % question_id)
    question = get_object_or_404(Question, pk = question_id)
    try:
        selected_choice = question.choice_set.get(pk = request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        return render(request, 'accounts/detail.html', {
            'question' : question,
            'error_message' : "You didnt select a choice. ",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('accounts:results', args = (question.id, )))