from lesson.cards.templateCard import TemplateCard
from lesson.lessonState import LessonState
from student.models import Student


class TemplateState(LessonState):
    def __init__(self, template, state, next_state, description, is_initial=False, is_final=False, is_sync=False):
        self.__card = TemplateCard(template=template)
        self.__description = description
        self.__state = state
        self.__next_state = next_state
        self.__is_initial = is_initial
        self.__is_sync = is_sync
        self.__is_final = is_final

    def previous_state(self, student: Student):
        if self.__is_initial or self.__is_sync:
            return None
        return super(TemplateState, self).previous_state(student)

    def is_first(self) -> bool:
        return self.__is_initial

    def is_sync(self) -> bool:
        return self.__is_sync

    def is_final(self) -> bool:
        return self.__is_final

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