
TO_BE = [
["I","I am","I'm","I am not","I'm not","Am I...?"],
["You","You are","You're","You are not","You aren't","Are you...?"],
["He","He is","He's","He is not","He isn't","Is he...?"],
["She","She is","She's","She is not","She isn't","Is she...?"],
["It","It is","It's","It is not","It isn't","Is it...?"],
["We","We are","We're","We are not","We aren't","Are we...?"],
["They","They are","They're","They are not","They aren't","Are they...?"],
]

DEMONSTRATIVES = [
["Singular","Cerca","this","este / esta / esto","This is my book."],
["Singular","Lejos","that","ese / esa / eso","That is your car."],
["Plural","Cerca","these","estos / estas","These are my shoes."],
["Plural","Lejos","those","esos / esas","Those are your keys."],
]

TENSES = [
["Presente","Present Simple","I work every day.","rutina / hecho"],
["Presente","Present Continuous","I am working now.","ahora"],
["Pasado","Past Simple","I worked yesterday.","acción terminada"],
["Pasado","Past Continuous","I was working at eight.","acción en progreso"],
["Futuro","will","I will work tomorrow.","predicción / decisión"],
["Futuro","be going to","I am going to work.","plan / intención"],
]

def kind(g):
    x=g.lower()
    if "this, that" in x or "these" in x:return "demonstratives"
    if "be:" in x:return "to_be"
    if "present simple" in x or "past simple" in x or "going to" in x:return "tenses"
    if "there is" in x:return "there"
    if "have / has got" in x or "have / has got" in x:return "havegot"
    if "can / can't" in x:return "can"
    return "general"
