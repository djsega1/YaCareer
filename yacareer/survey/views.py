from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import SurveyForm
from .models import Survey


class Container(object):
    pass


@login_required(login_url='/users/login')
def survey(request):
    template = 'survey/survey.html'
    survey = Survey.objects.all()
    values = Container()
    values.questions = []
    for item in survey:
        question = Container()
        question.id = item.pk
        question.text = item.question
        choice = Container()
        choice.id = 1
        choice.text = item.variant_a
        choices = [choice]
        choice = Container()
        choice.id = 2
        choice.text = item.variant_b
        choices.append(choice)
        question.choices = choices
        values.questions.append(question)
    form = SurveyForm(values, request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save(request.user, values)
        return redirect('users:user_detail', pk=request.user.id)
    context = {
               'survey': survey,
               'form': form,
        }
    return render(request, template, context)
