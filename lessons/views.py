from django.shortcuts import render

# Create your views here.
from lessons.teaching_modules import internet
from lessons.teaching_modules.teaching_module import STATE_INITIAL

def get_content(lesson, state, arguments):
    if lesson == "INTERNET":
        if state == STATE_INITIAL:
            return internet.initial()
        else:
            return internet.next(state, arguments)

def get_all():
    return ["INTERNET"]