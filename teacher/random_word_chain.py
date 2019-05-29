import random


def random_word_chain():
    return "".join([nouns[random.randrange(0, len(nouns))].capitalize() for i in range(2)])


nouns = [
    "Alphabet", "Altenheim", "Amulett", "Anlage", "Arm", "Aufkleber", "Auspuff", "Auto", "Ball", "Bar", "Baum",
    "Bestellliste", "Betttuch", "Biokraftstoff", "Blatt", "Buch", "Callcenter", "Castingshow", "Chinese", "Clip",
    "Computer", "Dach", "Dichtung", "Disco", "Dollar", "Dorfschule", "Eimer", "Eisenbahn", "Engel", "Erdöl", "Ergebnis",
    "Fahrrad", "Feuerlöscher", "Film", "Foto", "Freiheit", "Gehirn", "Gehweg", "Grundgesetz", "Grundstück", "Gymnasium",
    "Hafen", "Haus", "Heimatland", "Holz", "Horn", "Igel", "Impfstoff", "Information", "Infusion", "Insel",
    "Jachthafen", "Jacke", "Jäger", "Jobcenter", "Jugendclub", "Kaktus", "Kamm", "Kammer", "Keller", "Kugel", "Leber",
    "Leiste", "Leiter", "Liebe", "Locher", "Maus", "Monat", "Monitor", "Musikstück", "Muskel", "Nabelschnur", "Nachbar",
    "Nagel", "Nase", "Natur", "Nonne", "Notunterkunft", "Obst", "Ochse", "Offizier", "Orgel", "Osterei", "Paket",
    "Papier", "Passwort", "Politiker", "Poster", "Quader", "Quark", "Quecksilber", "Quelle", "Quastenflosser", "Rabe",
    "Radio", "Rakete", "Reifen", "Rettungswagen", "Ritter", "Sand", "Scanner", "Schloss", "Stein", "Strauch", "Tasche",
    "Taschenrechner", "Tastatur", "Taste", "Tiger", "Tisch", "Turnschuh", "Uhr", "Ulme", "Umschlagplatz", "Umwelt",
    "Unwetter", "Vanille", "Vater", "Verdauung", "Verkehr", "Versicherung", "Vogel", "Waage", "Waggon", "Waschzeug",
    "Wasser", "Wort", "Xylophon", "Yogalehrer", "Zahn", "Zeichen", "Zeitung", "Zentrum" ]
