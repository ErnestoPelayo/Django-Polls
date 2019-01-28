from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Choice, Question
from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.views import generic
from django.utils import timezone 
from django.views.generic.edit import CreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages

# Create your views here.

class IndexView(LoginRequiredMixin,generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
         """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:7]
        #return Question.objects.filter.filter(borrower=self.request.user).filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
   
class DetailView(LoginRequiredMixin,generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte =timezone.now())

class ResultsView(LoginRequiredMixin,generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        messages.add_message(request, messages.WARNING, 'You have voted correctly')
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
      

class QuestionCreate(SuccessMessageMixin,CreateView):
    template_name='polls/create_question.html'
    model = Question
    fields = ['question_text','pub_date']
    success_message = " %(question_text)s  was created successfully"
    
    @method_decorator(permission_required('polls.add_question'))
    def dispatch(self, *args, **kwargs):
                return super(QuestionCreate, self).dispatch(*args, **kwargs)
                
 
class ChoiceCreate(SuccessMessageMixin,CreateView):
    template_name='polls/create_choice.html'
    model = Choice
    fields = ['question','choice_text','votes']
    success_message = " %(choice_text)s  was created successfully"
    
    @method_decorator(permission_required('polls.add_choice'))
    def dispatch(self, *args, **kwargs):
                return super(ChoiceCreate, self).dispatch(*args, **kwargs)
