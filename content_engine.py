import re

"""Complete CEFR-aligned lesson engine for Inglés ¡YA!
Creates lesson-specific material for all 320 lessons (8 course bands × 40 lessons).
The syllabus is pedagogically aligned to CEFR communicative progression; it does not
claim to reproduce any proprietary textbook content.
"""

LEVEL_ORDER = ["A1","A2","A2+","B1","B1+","B2","B2+","C1-C2"]

LEVEL_SPECS = {
"A1": {
 "reading": 75, "dialogue": 6,
 "core": [("everyday","cotidiano"),("simple","sencillo"),("usually","normalmente"),("sometimes","a veces")],
 "grammar": ["be and subject pronouns","possessives and demonstratives","there is/are and adjectives","have got and imperatives","present simple","can and requests","question forms and was/were","past simple","object pronouns and verb + -ing","would like and be going to"],
 "pron": ["word stress and clear vowels","/s/ and /z/ endings","question intonation","weak forms","sentence stress","can / can't contrast","was / were weak forms","-ed endings","linking consonant to vowel","going to and natural rhythm"],
},
"A2": {
 "reading": 110, "dialogue": 8,
 "core": [("recently","recientemente"),("probably","probablemente"),("already","ya"),("yet","todavía"),("because","porque"),("although","aunque")],
 "grammar": ["present simple vs present continuous","past simple and time expressions","countable/uncountable nouns and quantifiers","comparatives and superlatives","present perfect for experience","modals for ability/advice/obligation","future forms: going to and will","past continuous","first conditional","relative clauses and basic connectors"],
 "pron": ["contrastive sentence stress","regular past endings","weak forms of function words","comparative stress","present perfect contractions","modal weak forms","future contractions","connected speech","conditional rhythm","thought groups"],
},
"A2+": {
 "reading": 135, "dialogue": 8,
 "core": [("choice","elección"),("reason","razón"),("result","resultado"),("however","sin embargo"),("instead","en cambio"),("improve","mejorar"),("experience","experiencia")],
 "grammar": ["narrative present and question review","past simple vs present perfect","gerunds and infinitives","comparatives with modifiers","modals of obligation and permission","present perfect with for/since","future arrangements and predictions","zero and first conditionals","defining relative clauses","linkers of reason, result and contrast"],
 "pron": ["prominence in questions","auxiliary contractions","-ing and infinitive chunking","degree adverb stress","must/have to weak forms","for/since phrasing","future-form reductions","if-clause rhythm","relative-clause phrasing","discourse-marker intonation"],
},
"B1": {
 "reading": 170, "dialogue": 10,
 "core": [("opinion","opinión"),("advantage","ventaja"),("disadvantage","desventaja"),("solution","solución"),("decision","decisión"),("experience","experiencia"),("recommend","recomendar"),("evidence","evidencia")],
 "grammar": ["present and past habits","narrative tenses","present perfect simple vs continuous","modals of deduction","relative clauses","passive voice","first and second conditionals","reported speech","gerunds and infinitives","future forms and probability"],
 "pron": ["thought groups and prominence","narrative rhythm","weak auxiliaries","certainty intonation","relative-clause chunking","passive sentence stress","conditional rhythm","reported-speech phrasing","connected speech","intonation for probability"],
},
"B1+": {
 "reading": 195, "dialogue": 10,
 "core": [("issue","asunto"),("approach","enfoque"),("impact","impacto"),("compare","comparar"),("support","sustentar"),("evidence","evidencia"),("outcome","resultado"),("concern","preocupación")],
 "grammar": ["perfect forms review","past perfect and narrative sequencing","modal verbs in the past","passives with reporting structures","second and third conditionals","reported questions and reporting verbs","participle adjectives and clauses","complex gerund/infinitive patterns","future continuous and future perfect","contrast and concession clauses"],
 "pron": ["contrastive prominence","storytelling intonation","modal perfect reductions","information focus","conditional chunking","reporting-verb stress","adjective stress shifts","lexical chunking","future-form reductions","concession intonation"],
},
"B2": {
 "reading": 230, "dialogue": 12,
 "core": [("perspective","perspectiva"),("consequence","consecuencia"),("assumption","suposición"),("challenge","desafío"),("reliable","confiable"),("significant","significativo"),("argument","argumento"),("justify","justificar")],
 "grammar": ["cleft sentences and emphasis","advanced narrative tenses","modal deduction and speculation","mixed conditionals","advanced passive structures","reported speech and stance","participle clauses","inversion after negative adverbials","future in the past","complex noun phrases and relative clauses"],
 "pron": ["nuclear stress for emphasis","intonation in narratives","degrees of certainty","conditional prominence","deaccenting known information","stance intonation","chunking long clauses","inversion and focus","prosodic signalling of time","complex noun-phrase stress"],
},
"B2+": {
 "reading": 260, "dialogue": 12,
 "core": [("nuance","matiz"),("implication","implicación"),("constraint","restricción"),("outcome","resultado"),("controversial","controvertido"),("justify","justificar"),("evaluate","evaluar"),("trade-off","compensación")],
 "grammar": ["fronting and emphasis","advanced aspect and viewpoint","modal nuance and hedging","hypothetical meaning","causative and complex passives","reporting and distancing","reduced clauses","inversion and rhetorical emphasis","advanced future reference","nominalisation and information density"],
 "pron": ["rhetorical prominence","aspectual contrast in speech","hedging intonation","hypothetical intonation","focus in causatives","distancing intonation","compressed clause rhythm","rhetorical pitch movement","future-reference phrasing","stress in nominalisations"],
},
"C1-C2": {
 "reading": 320, "dialogue": 14,
 "core": [("stance","postura"),("underlying","subyacente"),("framework","marco"),("subtle","sutil"),("compelling","convincente"),("counterargument","contraargumento"),("inference","inferencia"),("ambiguity","ambigüedad"),("caveat","salvedad"),("premise","premisa")],
 "grammar": ["information structure and marked word order","tense/aspect for rhetorical effect","epistemic modality and hedging","counterfactual and hypothetical structures","complex passives and causatives","reporting, attribution and evidentiality","non-finite and verbless clauses","inversion, fronting and ellipsis","time reference across discourse","nominalisation and dense academic syntax"],
 "pron": ["discourse-level prominence","prosodic framing of narratives","epistemic stance through intonation","counterfactual prosody","focus and deaccenting","attribution and voice quality","rhythmic compression","rhetorical pitch range","discourse boundary signalling","precision in stress and rhythm"],
},
}

FUNCTIONS = {
"A1":["introduce yourself","buy something","ask for directions","make a request","order food","tell the time","buy a ticket","greet someone","make a suggestion","invite someone"],
"A2":["start a conversation","describe past events","make comparisons","ask for clarification","talk about experience","give advice","make arrangements","describe a problem","make plans","write a simple message"],
"A2+":["keep a conversation going","tell an anecdote","express preferences","negotiate a plan","explain rules","describe change","make predictions","give reasons","compare options","handle a practical problem"],
"B1":["exchange opinions","tell a detailed story","give recommendations","clarify a misunderstanding","justify a choice","solve a problem","make a complaint","speculate about possibilities","summarise information","take part in a discussion"],
"B1+":["manage disagreement","structure a narrative","give tactful advice","evaluate alternatives","negotiate a solution","report what others said","respond to criticism","argue a case","summarise viewpoints","reach a compromise"],
"B2":["build rapport","challenge a claim politely","express nuanced attitudes","negotiate disagreement","evaluate evidence","handle a sensitive conversation","speculate and qualify","persuade an audience","summarise competing views","propose a solution"],
"B2+":["facilitate discussion","hedge a strong claim","reframe disagreement","evaluate consequences","distinguish fact from interpretation","mediate conflict","signal reservations","present a persuasive case","synthesise viewpoints","defend a proposal"],
"C1-C2":["manage complex interaction","calibrate stance","use diplomatic disagreement","develop a sophisticated argument","evaluate source credibility","mediate competing positions","signal irony or reservation","deliver a persuasive intervention","synthesise complex material","respond spontaneously with precision"],
}

TOPICS = {
"people": [("personality","personalidad"),("background","trayectoria"),("appearance","apariencia"),("character","carácter"),("strength","fortaleza"),("weakness","debilidad"),("confident","seguro"),("reliable","confiable"),("outgoing","extrovertido"),("reserved","reservado"),("generous","generoso"),("ambitious","ambicioso"),("relationship","relación"),("impression","impresión"),("behaviour","comportamiento"),("identity","identidad")],
"family": [("family","familia"),("parent","padre/madre"),("relative","pariente"),("childhood","infancia"),("generation","generación"),("support","apoyo"),("relationship","relación"),("grow up","crecer"),("get along","llevarse bien"),("resemble","parecerse"),("household","hogar"),("memory","recuerdo"),("tradition","tradición"),("responsibility","responsabilidad"),("close","cercano"),("independent","independiente")],
"work": [("career","carrera profesional"),("job","empleo"),("colleague","colega"),("manager","gerente"),("skill","habilidad"),("experience","experiencia"),("deadline","fecha límite"),("salary","salario"),("interview","entrevista"),("qualification","calificación"),("promotion","ascenso"),("workload","carga laboral"),("flexible","flexible"),("productive","productivo"),("responsibility","responsabilidad"),("workplace","lugar de trabajo")],
"education": [("education","educación"),("course","curso"),("subject","asignatura"),("assignment","tarea"),("exam","examen"),("degree","grado/título"),("research","investigación"),("knowledge","conocimiento"),("learn","aprender"),("revise","repasar"),("assessment","evaluación"),("feedback","retroalimentación"),("curriculum","currículo"),("achievement","logro"),("academic","académico"),("practical","práctico")],
"travel": [("journey","viaje"),("destination","destino"),("luggage","equipaje"),("accommodation","alojamiento"),("booking","reserva"),("departure","salida"),("arrival","llegada"),("route","ruta"),("sightseeing","turismo"),("abroad","en el extranjero"),("delay","retraso"),("fare","tarifa"),("passport","pasaporte"),("local","local"),("explore","explorar"),("trip","viaje")],
"places": [("neighbourhood","barrio"),("area","zona"),("facility","instalación/servicio"),("crowded","concurrido"),("peaceful","tranquilo"),("convenient","conveniente"),("historic","histórico"),("modern","moderno"),("suburb","suburbio"),("downtown","centro"),("landmark","punto de referencia"),("public space","espacio público"),("community","comunidad"),("environment","entorno"),("accessible","accesible"),("location","ubicación")],
"home": [("home","hogar"),("room","habitación"),("furniture","muebles"),("rent","alquiler"),("neighbour","vecino"),("comfortable","cómodo"),("spacious","espacioso"),("household","hogar"),("move in","mudarse"),("decorate","decorar"),("storage","almacenamiento"),("appliance","electrodoméstico"),("property","propiedad"),("shared","compartido"),("privacy","privacidad"),("maintenance","mantenimiento")],
"food": [("meal","comida"),("dish","plato"),("ingredient","ingrediente"),("flavour","sabor"),("recipe","receta"),("healthy","saludable"),("diet","dieta"),("fresh","fresco"),("spicy","picante"),("sweet","dulce"),("order","pedir"),("menu","menú"),("portion","porción"),("cook","cocinar"),("taste","probar/sabor"),("nutrition","nutrición")],
"shopping": [("price","precio"),("cost","costo"),("afford","poder pagar"),("discount","descuento"),("brand","marca"),("quality","calidad"),("customer","cliente"),("receipt","recibo"),("refund","reembolso"),("purchase","compra"),("value","valor"),("budget","presupuesto"),("advertising","publicidad"),("consumer","consumidor"),("worth","valer la pena"),("choice","elección")],
"technology": [("device","dispositivo"),("website","sitio web"),("account","cuenta"),("privacy","privacidad"),("data","datos"),("online","en línea"),("platform","plataforma"),("download","descargar"),("upload","subir"),("algorithm","algoritmo"),("digital","digital"),("screen","pantalla"),("network","red"),("security","seguridad"),("access","acceso"),("innovation","innovación")],
"media": [("news","noticias"),("headline","titular"),("source","fuente"),("report","reportaje"),("claim","afirmación"),("evidence","evidencia"),("bias","sesgo"),("audience","audiencia"),("coverage","cobertura"),("journalist","periodista"),("publish","publicar"),("reliable","confiable"),("misleading","engañoso"),("fact","hecho"),("opinion","opinión"),("context","contexto")],
"health": [("health","salud"),("symptom","síntoma"),("treatment","tratamiento"),("recover","recuperarse"),("exercise","ejercicio"),("sleep","sueño"),("stress","estrés"),("habit","hábito"),("appointment","cita"),("pain","dolor"),("well-being","bienestar"),("balanced","equilibrado"),("prevent","prevenir"),("condition","afección"),("energy","energía"),("routine","rutina")],
"money": [("money","dinero"),("income","ingreso"),("expense","gasto"),("save","ahorrar"),("spend","gastar"),("budget","presupuesto"),("debt","deuda"),("loan","préstamo"),("afford","poder pagar"),("value","valor"),("investment","inversión"),("financial","financiero"),("cost","costo"),("payment","pago"),("cash","efectivo"),("account","cuenta")],
"environment": [("environment","medio ambiente"),("climate","clima"),("pollution","contaminación"),("waste","residuos"),("recycle","reciclar"),("sustainable","sostenible"),("energy","energía"),("wildlife","vida silvestre"),("habitat","hábitat"),("resource","recurso"),("protect","proteger"),("emission","emisión"),("conservation","conservación"),("urban","urbano"),("green space","área verde"),("impact","impacto")],
"culture": [("culture","cultura"),("tradition","tradición"),("custom","costumbre"),("identity","identidad"),("community","comunidad"),("values","valores"),("diversity","diversidad"),("heritage","patrimonio"),("celebration","celebración"),("belief","creencia"),("social","social"),("generation","generación"),("respect","respeto"),("difference","diferencia"),("belong","pertenecer"),("practice","práctica")],
"crime": [("crime","delito"),("law","ley"),("police","policía"),("evidence","evidencia"),("suspect","sospechoso"),("victim","víctima"),("court","tribunal"),("rule","regla"),("legal","legal"),("illegal","ilegal"),("investigate","investigar"),("sentence","condena"),("justice","justicia"),("security","seguridad"),("responsibility","responsabilidad"),("rights","derechos")],
"art": [("art","arte"),("artist","artista"),("work","obra"),("creative","creativo"),("performance","actuación"),("audience","audiencia"),("review","reseña"),("style","estilo"),("original","original"),("influence","influencia"),("meaning","significado"),("design","diseño"),("exhibition","exposición"),("entertainment","entretenimiento"),("popular","popular"),("critic","crítico")],
"sport": [("sport","deporte"),("team","equipo"),("player","jugador"),("competition","competencia"),("training","entrenamiento"),("coach","entrenador"),("score","marcador"),("win","ganar"),("lose","perder"),("performance","rendimiento"),("fair","justo"),("rule","regla"),("challenge","desafío"),("fitness","condición física"),("supporter","aficionado"),("achievement","logro")],
"future": [("future","futuro"),("prediction","predicción"),("possibility","posibilidad"),("likely","probable"),("unlikely","improbable"),("change","cambio"),("trend","tendencia"),("opportunity","oportunidad"),("risk","riesgo"),("develop","desarrollar"),("innovation","innovación"),("plan","plan"),("expect","esperar"),("imagine","imaginar"),("outcome","resultado"),("scenario","escenario")],
"relationships": [("relationship","relación"),("friendship","amistad"),("trust","confianza"),("support","apoyo"),("argument","discusión"),("apologise","disculparse"),("forgive","perdonar"),("respect","respeto"),("communicate","comunicarse"),("honest","honesto"),("close","cercano"),("conflict","conflicto"),("compromise","acuerdo"),("advice","consejo"),("feelings","sentimientos"),("understand","entender")],
"general": [("topic","tema"),("experience","experiencia"),("idea","idea"),("reason","razón"),("example","ejemplo"),("choice","elección"),("change","cambio"),("problem","problema"),("solution","solución"),("important","importante"),("useful","útil"),("different","diferente"),("describe","describir"),("explain","explicar"),("compare","comparar"),("discuss","conversar/debatir")],
}

KEYWORDS = [
("crime",["crime","law","order","scam","rules","illegal"]),
("technology",["internet","digital","online","technology","bubble"]),
("media",["news","headline","celebrity","storytelling","gossip","fact or fiction"]),
("health",["health","mend","sleep","eating well","habits"]),
("money",["money","spend","save","consumer","sale","shopping","splashing"]),
("environment",["green","wild","natural","habitat","clean-up","rewild","environment"]),
("education",["education","school","study","skills for life","course"]),
("work",["job","work","career","interview","business"]),
("travel",["journey","travel","trip","holiday","abroad","getting around","on the move","map"]),
("home",["home","room","living space","place to live","building","house"]),
("places",["town","city","area","urban","place","local issues"]),
("food",["food","cafe","eating","tastes","meal"]),
("art",["art","film","show","read","fashion","review"]),
("sport",["sport","race","fair play","rivals"]),
("relationships",["friends","relationship","catching up","famil","together"]),
("people",["profiles","personality","appearances","being me","identity","people"]),
("future",["future","next big thing","prediction","dystopia"]),
("culture",["culture","tradition","awareness","society","generation"]),
]

def topic_key(title):
    t=title.lower()
    for k,words in KEYWORDS:
        if any(w in t for w in words): return k
    return "general"

def lesson_meta(level, unit, letter, title):
    spec=LEVEL_SPECS[level]
    gi=(unit-1) % len(spec["grammar"])
    grammar=spec["grammar"][gi]
    # D lessons are communicative/functional while still recycling the unit language.
    if letter=="D":
        grammar=f"functional language: {FUNCTIONS[level][gi]}"
    pron=spec["pron"][gi]
    action=FUNCTIONS[level][gi]
    goal=f"Use English to {action} while discussing {title.lower()}."
    return {"grammar":grammar,"pron":pron,"goal":goal,"vocab":f"{title}: topic vocabulary and collocations"}

def vocabulary(level,title):
    spec=LEVEL_SPECS[level]
    words=list(TOPICS[topic_key(title)])+list(spec["core"])
    # lesson-title lexical items are intentionally visible, but no fake translations are generated.
    seen=set(); out=[]
    for en,es in words:
        if en.lower() not in seen:
            out.append((en,es)); seen.add(en.lower())
    return out[:20 if level in ("A1","A2") else 24]

def grammar_note(level, grammar):
    notes={
      "A1":"Usa estructuras cortas y frecuentes. Mantén el orden sujeto + verbo + complemento y practica primero en afirmativa, luego negativa y pregunta.",
      "A2":"Combina la forma gramatical con marcadores de tiempo y cantidad. Presta atención al auxiliar correcto en preguntas y negativas.",
      "A2+":"Conecta dos o más ideas y elige la forma verbal según tiempo, experiencia, intención o resultado.",
      "B1":"La prioridad es controlar contraste de tiempos, modalidad y subordinación para producir discurso conectado y comprensible.",
      "B1+":"Usa la estructura para narrar, justificar y matizar. Observa cómo cambia el significado al elegir aspecto, modalidad o voz.",
      "B2":"Usa la gramática como recurso discursivo: énfasis, distancia, hipótesis, evaluación y organización de información.",
      "B2+":"Controla alternativas formales e informales y selecciona estructuras según el grado de certeza, cortesía, énfasis y densidad informativa.",
      "C1-C2":"Busca precisión pragmática: estructura la información, calibra la postura y usa formas marcadas solo cuando mejoran el efecto retórico."
    }
    return notes[level]

def model_sentences(level,title,grammar):
    t=title.lower()
    if level=="A1":
        return [
          (f"I like {t}.","Me gusta este tema."),
          (f"This is about {t}.","Esto trata sobre este tema."),
          ("Can you tell me more?","¿Puedes contarme más?"),
          ("Yes, of course.","Sí, por supuesto."),
        ]
    if level in ("A2","A2+"):
        return [
          (f"I've had some experience with {t}.","He tenido algo de experiencia con este tema."),
          ("It was interesting because I learned something new.","Fue interesante porque aprendí algo nuevo."),
          ("I think there are two good options.","Creo que hay dos buenas opciones."),
          ("What are you going to do next?","¿Qué vas a hacer después?"),
          ("If I have time, I'll learn more about it.","Si tengo tiempo, aprenderé más sobre ello."),
        ]
    if level in ("B1","B1+"):
        return [
          (f"I've been thinking about {t} recently.","He estado pensando en este tema recientemente."),
          ("One advantage is that it gives people more choice.","Una ventaja es que da a las personas más opciones."),
          ("However, the outcome depends on the situation.","Sin embargo, el resultado depende de la situación."),
          ("If I had to choose, I'd look at the evidence first.","Si tuviera que elegir, primero miraría la evidencia."),
          ("What matters most is whether the solution works in practice.","Lo más importante es si la solución funciona en la práctica."),
        ]
    if level in ("B2","B2+"):
        return [
          (f"What I find most interesting about {t} is the range of perspectives involved.","Lo que me parece más interesante es la variedad de perspectivas implicadas."),
          ("The claim may sound convincing, but it needs to be supported by reliable evidence.","La afirmación puede sonar convincente, pero debe estar respaldada por evidencia confiable."),
          ("Had the circumstances been different, the outcome might have changed considerably.","Si las circunstancias hubieran sido diferentes, el resultado podría haber cambiado considerablemente."),
          ("There is a trade-off between immediate benefits and long-term consequences.","Existe una compensación entre beneficios inmediatos y consecuencias a largo plazo."),
          ("I would qualify that argument rather than reject it completely.","Yo matizaría ese argumento en lugar de rechazarlo por completo."),
        ]
    return [
      (f"A useful way of framing {t} is to distinguish the underlying assumptions from the evidence.","Una forma útil de plantear el tema es distinguir los supuestos subyacentes de la evidencia."),
      ("Compelling though the argument may appear, its implications are more ambiguous than they first seem.","Aunque el argumento parezca convincente, sus implicaciones son más ambiguas de lo que parecen al principio."),
      ("One could reasonably infer that the policy would have uneven effects across different contexts.","Se podría inferir razonablemente que la política tendría efectos desiguales según el contexto."),
      ("That said, the counterargument deserves serious consideration rather than a token acknowledgement.","Dicho esto, el contraargumento merece una consideración seria y no un reconocimiento meramente simbólico."),
      ("My position is therefore conditional: I support the principle, with the caveat that implementation must be evidence-based.","Mi postura es, por tanto, condicional: apoyo el principio, con la salvedad de que la implementación debe basarse en evidencia."),
    ]

def dialogue(level,title,models):
    if level in ("A1","A2"):
        turns=[
          ("A",f"Hi! Can we talk about {title.lower()}?","¡Hola! ¿Podemos hablar de este tema?"),
          ("B","Sure. What would you like to know?","Claro. ¿Qué te gustaría saber?"),
          ("A",models[0][0],models[0][1]),
          ("B","That's interesting. Can you give me an example?","Qué interesante. ¿Puedes darme un ejemplo?"),
          ("A",models[1][0],models[1][1]),
          ("B","What do you think about it now?","¿Qué opinas ahora?"),
          ("A",models[2][0],models[2][1]),
          ("B","Thanks. That was clear.","Gracias. Eso estuvo claro."),
        ]
    else:
        turns=[
          ("A",f"What's your view on {title.lower()}?","¿Cuál es tu opinión sobre este tema?"),
          ("B",models[0][0],models[0][1]),
          ("A","What evidence would you use to support that view?","¿Qué evidencia usarías para sustentar esa opinión?"),
          ("B",models[1][0],models[1][1]),
          ("A","Is there a reasonable counterargument?","¿Existe un contraargumento razonable?"),
          ("B",models[2][0],models[2][1]),
          ("A","So what conclusion would you draw?","Entonces, ¿qué conclusión sacarías?"),
          ("B",models[3][0],models[3][1]),
          ("A","Would you change your position if new evidence appeared?","¿Cambiarías tu postura si apareciera nueva evidencia?"),
          ("B",models[4][0],models[4][1]),
        ]
    target=LEVEL_SPECS[level]["dialogue"]
    while len(turns)<target:
        turns += [("A","Could you expand on that point?","¿Podrías ampliar ese punto?"),("B","Yes. The context makes an important difference.","Sí. El contexto marca una diferencia importante.")]
    return turns[:target]

def reading(level,title,models):
    # Original, lesson-specific text. Length rises by CEFR level.
    intro = {
      "A1": f"{title} is today's topic. We use simple English to talk about it. We learn useful words, ask short questions, and give clear answers.",
      "A2": f"In this lesson, we explore {title.lower()} through an everyday situation. People often need to describe what happened, explain a simple reason, and say what they plan to do next.",
      "A2+": f"{title} can be discussed in several everyday contexts. A clear speaker connects ideas with reasons, results and contrasts, and asks follow-up questions when more information is needed.",
      "B1": f"{title} is a useful topic for practising connected speech. Instead of giving isolated answers, a B1 learner can describe an experience, explain a viewpoint and support it with reasons and examples.",
      "B1+": f"When discussing {title.lower()}, speakers often need to organise a narrative, compare alternatives and react to another person's point of view. Clear signposting helps the listener follow the argument.",
      "B2": f"A productive discussion of {title.lower()} requires more than description. Speakers can evaluate evidence, distinguish assumptions from facts, acknowledge alternative perspectives and qualify claims when certainty is limited.",
      "B2+": f"{title} provides a useful context for nuanced argument. Effective speakers weigh consequences, identify trade-offs, hedge claims appropriately and reformulate ideas when a disagreement risks becoming unproductive.",
      "C1-C2": f"A sophisticated discussion of {title.lower()} depends on precise framing. Strong communicators distinguish premises from inferences, calibrate epistemic certainty, anticipate counterarguments and adapt register to the audience and purpose."
    }[level]
    extra = " ".join(x[0] for x in models)
    critical = {
      "A1":"The aim is to understand the main words and say four short sentences with confidence.",
      "A2":"The learner should identify the main idea, two details and one useful expression, then retell the situation in simple connected sentences.",
      "A2+":"The learner should explain the main point, add a reason and contrast two possibilities.",
      "B1":"The learner should summarise the main point, identify a reason and an example, and then add a personal response.",
      "B1+":"The learner should separate description from opinion, identify the speaker's reasons and respond with a justified viewpoint.",
      "B2":"The learner should identify the central claim, supporting evidence, limitations and an alternative interpretation before giving a reasoned response.",
      "B2+":"The learner should evaluate how strongly each claim is supported, note implications and formulate a qualified conclusion.",
      "C1-C2":"The learner should reconstruct the argument, expose implicit assumptions, evaluate evidential strength and formulate a nuanced synthesis rather than a binary conclusion."
    }[level]
    text=f"{intro} {extra} {critical}"
    # expand advanced texts naturally to target band
    fillers=[
      "Context matters because the same words can carry different implications in personal, public, educational and professional settings.",
      "A useful strategy is to listen for discourse markers, stressed words and changes in intonation, since these often reveal how ideas are connected.",
      "After reading, compare the writer's position with your own and decide which evidence would make the conclusion stronger.",
    ]
    i=0
    target=LEVEL_SPECS[level]["reading"]
    while len(text.split()) < target:
        text += " " + fillers[i%len(fillers)]; i+=1
    # sentence pairs: Spanish support is concise rather than a copyrighted translation.
    sents=[s.strip() for s in re.split(r'(?<=[.!?])\s+',text) if s.strip()]
    return [(s, "Apoyo: comprende la idea y vuelve a expresarla con tus propias palabras.") for s in sents]

def exercises(level,title,grammar,vocab):
    w=[x[0] for x in vocab[:6]]
    return [
      {"type":"production","prompt":f"Write two original sentences about {title} using {grammar}.","guide":f"Use the target structure accurately and include at least one topic word: {', '.join(w[:3])}."},
      {"type":"vocabulary","prompt":f"Use these words in context: {', '.join(w[3:6])}.","guide":"Write one meaningful sentence for each word; do not write isolated translations."},
      {"type":"speaking","prompt":f"Give a 30–90 second response about {title}.","guide":"State your main point, add supporting detail, and use the lesson grammar."},
      {"type":"editing","prompt":"Write one sentence, then improve it by adding a reason, contrast, example or qualification appropriate to your level.","guide":"The second version should be clearer and more connected than the first."},
    ]

def evaluation(level,title,grammar,vocab):
    word=vocab[0][0]
    return [
      (f"Write a correct sentence about {title} using '{word}'.", word),
      (f"Write one sentence that demonstrates: {grammar}.", grammar.split()[0]),
      (f"Give one reasoned response to this question: What matters most when we discuss {title.lower()}?", "Answers vary; include a clear point and support."),
      ("Write one useful expression from this lesson.", "Answers vary; use lesson vocabulary or a model expression."),
      ("Self-check: What can you now do more confidently in English?", "Answers vary; refer to the communicative goal."),
    ]

def homework(level,title,grammar,vocab):
    words=", ".join(x[0] for x in vocab[:8])
    return [
      {"title":"Tarea 1 · Vocabulario activo","instruction":f"Escribe 8 oraciones originales sobre {title} usando estas palabras: {words}.","items":[("Escribe tus 8 oraciones.","Respuesta abierta: 8 oraciones contextualizadas.")]},
      {"title":"Tarea 2 · Gramática","instruction":f"Crea 6 ejemplos que demuestren correctamente: {grammar}.","items":[("Escribe tus 6 ejemplos.","Respuesta abierta: revisa forma, significado y contexto.")]},
      {"title":"Tarea 3 · Producción oral","instruction":f"Prepara una respuesta oral sobre {title}. A1-A2: 45–60 s; B1-B1+: 1–2 min; B2+: 2–3 min.","items":[("Escribe primero 3 ideas clave.","Respuesta abierta: idea principal + apoyo + cierre.")]},
      {"title":"Tarea 4 · Lectura y reflexión","instruction":"Resume la lectura sin copiarla y añade una opinión o conclusión propia.","items":[("Escribe tu resumen.","Respuesta abierta: resumen fiel + respuesta personal.")]},
    ]

def build_pack(level,unit,letter,title):
    meta=lesson_meta(level,unit,letter,title)
    vocab=vocabulary(level,title)
    models=model_sentences(level,title,meta["grammar"])
    return {
      **meta,
      "vocabulary":vocab,
      "examples":models,
      "grammar_note":grammar_note(level,meta["grammar"]),
      "dialogue":dialogue(level,title,models),
      "reading":reading(level,title,models),
      "exercises":exercises(level,title,meta["grammar"],vocab),
      "evaluation":evaluation(level,title,meta["grammar"],vocab),
      "homework":homework(level,title,meta["grammar"],vocab),
    }
