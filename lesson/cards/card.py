from django.http import HttpRequest


class Cacdrd:
    def render(self, request: HttpRequest, context: {}):
        """
        Mirrors https://docs.djangoproject.com/en/2.2/topics/templates/#django.template.backends.base.Template.render
        to render a card for the given request and context in the Lesson context
        :param request:
        :param context:
        :return:
        """
        raise NotImplementedError("Error: Using Card Interface function")

    def post(self, post):
        raise NotImplementedError("Error: Using Card Interface function")

    class InvalidCardFormError(Exception):
        pass
