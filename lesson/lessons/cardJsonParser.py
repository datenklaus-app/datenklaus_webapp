import json

from lesson.lessons.defaultCard import DefaultCard

def from_json(json_string):
    dec = json.decoder.JSONDecoder()
    l = dec.decode(json_string)
    if l[0] == "DefaultCard":
        return DefaultCard.from_json(l[1:])

    raise NotImplementedError("Parsed Card is not implemented")