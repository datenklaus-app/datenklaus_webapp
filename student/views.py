import json

from django.shortcuts import render

from .models import Question, Choice


def index(request):
    question_list = Question.objects.all()
    context = {'question_list': question_list}
    return render(request, 'student/index.html', context)


def poll(request, question_id):
    q = Question.objects.get(id=question_id)
    context = {'question': q, 'choices_list': q.choice_set.all()}
    return render(request, 'student/question_view.html', context)


def poll_results(request, question_id, illegal_vote=False):
    q = Question.objects.get(id=question_id)
    choice_labels = []
    choice_votes = []
    for c in q.choice_set.all():
        choice_labels.append(c.choice_text)
        choice_votes.append(c.votes)

    context = {'question': q, 'choice_labels': json.dumps(choice_labels), 'choice_votes': choice_votes,
               'illegal_vote': illegal_vote}
    return render(request, 'student/poll_results.html', context)


def poll_vote(request, question_id, choice_id):
    has_voted = request.session.get('has_voted', default={})

    if has_voted.get(str(question_id), False):
        return poll_results(request, question_id, illegal_vote=True)

    has_voted[str(question_id)] = True
    request.session['has_voted'] = has_voted

    request.session.modified = True

    choice = Choice.objects.get(id=choice_id)
    choice.votes += 1
    choice.save()

    return poll_results(request, question_id)
