from lesson.cards.textCard import TextCard
from lesson.diceware.states import BSTATE, CSTATE
from lesson.lessonState import LessonState
from student.models import Student


class BState(LessonState):
    card = TextCard(state=BSTATE, title="Spielprinzip", subtitle="",
                    text="Für das Erstellen eines sicheren Passworts ist vor allem eins wichtig: Der Zufall. Und wie "
                         "du vielleicht weißt, ist das Ergebnis eines ungezinkten (d.h. nicht manipulierten) "
                         "Würfelwurfs immer zufällig - denn es steht nicht zu Beginn fest, wieviele Augen angezeigt "
                         "werden. Diesen Zufall machen wir uns hier zunutze. Mithilfe von fünf Würfeln und einer "
                         "langen Wortliste können wir uns ans Werk machen. In der Liste findest du alle würfelbaren "
                         "Zahlenkombinationen (wir haben nachgezählt: 7776). Du würfelst also fünf Würfel - heraus "
                         "kommt eine zufällige Zahlenkombination, die für ein bestimmtes Wort steht, das du dir "
                         "notierst. Das Ganze wiederholst du fünfmal und am Ende hast du fünf zufällig gewürfelte "
                         "Wörter, eine sogenannte Passphrase, die du als Passwort verwenden kannst.")

    def state_number(self) -> int:
        return BSTATE

    def next_state(self, student: Student) -> int:
        return CSTATE

    def render(self, request, student: Student, context) -> str:
        return self.card.render(request, context)

    def post(self, post, student: Student):
        return None

    @staticmethod
    def name():
        return "Selbsteinschätzung: Ergebnis"
