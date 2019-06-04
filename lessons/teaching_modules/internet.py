from django.template.loader import render_to_string

from lessons.teaching_modules.teaching_module import TeachingModule


class Internet(TeachingModule):
    @staticmethod
    def get_description():
        pass

    @staticmethod
    def get_short_description():
        pass

    @staticmethod
    def get_duration():
        pass

    @staticmethod
    def initial():
        context = {"title": "Wilkommen", "subtitle": "Heute lernen wir etwas über das Internet", "text": "Das Internet ist sehr toll"}
        return render_to_string('lessons/default.html', context)

    @staticmethod
    def next(current_state, arguments):
        pass
