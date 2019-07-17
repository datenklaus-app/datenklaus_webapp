from lesson.internet.internet import Internet


def get_state(lesson_name, state):
    if lesson_name == "INTERNET":
        return Internet.get_state(state)
    raise NotImplementedError("Selected Lesson does not exist")


def get_lessons_list():
    return ["INTERNET"]


def get_lessons_description(lesson):
    return "Lorem ipsum dolor sit amet, consetetur sadipscing elitr, sed diam nonumy eirmod tempor invidunt."