# Create your views here.
from lessons.teaching_modules import internet
from lessons.teaching_modules.teaching_module import STATE_INITIAL


def get_content(lesson, state, arguments):
    if lesson == "INTERNET":
        if state == STATE_INITIAL:
            return internet.initial()
        else:
            return internet.next(state, arguments)


def get_lessons_list():
    return ["INTERNET"]


def get_lessons_description(lesson):
    return "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore " \
           "et dolore magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea " \
           "rebum. Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. Lorem ipsum " \
           "dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt ut labore et dolore " \
           "magna aliquyam erat, sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum. Stet " \
           "clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet. "
