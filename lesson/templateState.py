from lesson.cards.templateCard import TemplateCard
from lesson.lessonState import LessonState
from student.models import Student


class TemplateState(LessonState):
    def __init__(self, template, state, next_state, description, is_initial=False):
        self.__card = TemplateCard(state, template=template)
        self.__description = description
        self.__state = state
        self.__next_state = next_state
        self.__is_initial = is_initial

    def previous_state(self, student: Student):
        if self.__is_initial:
            return None
        return super(TemplateState, self).previous_state(student)

    def state_number(self) -> int:
        return self.__state

    def next_state(self, student: Student) -> int:
        return self.__next_state

    def render(self, request, student: Student, context) -> str:
        return self.__card.render(request, context)

    def post(self, post, student):
        return

    def name(self):
        return self.__description
