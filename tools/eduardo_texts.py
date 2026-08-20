"""Eduardo's handwritten paragraphs, batch 1 (Edad Media through Broca and Wernicke).

His wording is the spine. Copy-edits are limited to grammar slips and one verb that reversed
the meaning; each is listed in FIXES. Where his paragraph drops a fact the rubric counts, the
added sentence is kept separate in ADDED so he can cut it.
"""
import json, os

os.chdir(os.path.expanduser("~/Desktop/lineadetiempo-biologia"))

FIXES = {
    9: "quitado el 'que' de más en 'Descubre que las diferencias'",
    11: "'defiende de la idea' a 'defiende la idea'",
    14: "'prueba la hipótesis' a 'pone a prueba la hipótesis': prueba a secas dice lo contrario de lo que demostró",
    26: "quitado 'para' en 'un área para que procesa'",
}

ADDED = {
    9: "La obra documenta cerca de doscientos errores de Galeno, cuya anatomía resultó ser de simios y otros animales.",
    15: "El modelo clásico de los cuatro humores queda sin sustento.",
    21: "Gall propone 27 facultades localizadas, 19 compartidas con los animales y 8 exclusivamente humanas, legibles por craneoscopia.",
    25: "El caso es el de Leborgne, Monsieur Tan, un paciente que sólo podía pronunciar esa sílaba, y la autopsia mostró una lesión en el lóbulo frontal izquierdo.",
    26: "El paciente no está sordo y aun así no entiende lo que se le dice, y la lesión está más atrás, en el lóbulo temporal izquierdo.",
}

# his text, lightly corrected
SUYO = {
 5: "Se piensa que los espíritus animales de Galeno se generan en los ventrículos cerebrales. Para la mentalidad cristiana el cerebro no podía ser un vínculo entre el alma y el cuerpo, pues era demasiado terrenal. Nemesio atribuye funciones específicas a ventrículos específicos, los sentidos al ventrículo frontal.",
 7: "Llenó un cerebro de cera para crear un modelo de los ventrículos cerebrales. No encontró el ventrículo frontal que se suponía debía alojar al senso comune. No publicó sus hallazgos.",
 9: "Descubre las diferencias entre la anatomía animal, descrita por Galeno, y la humana, y publica De humani corporis fabrica.",
 11: "Descartes defiende la idea de los espíritus animales. Parte de un paradigma mecánico para tratar de explicarlo: imagina a los animales como autómatas de carne y hueso. Considera que la glándula pineal unía la mente al cuerpo.",
 14: "En el siglo XVII cae el concepto de los espíritus animales. Jan Swammerdam pone a prueba experimentalmente la hipótesis de los espíritus animales: los músculos no aumentan de volumen al contraerse, así que no hay espíritus animales llegando.",
 15: "William Harvey descubre la circulación de la sangre.",
 20: "Galvani publica De viribus electricitatis in motu musculari: commentarius. Demostró que los músculos se mueven en respuesta a impulsos eléctricos propios del cuerpo.",
 21: "En el siglo XIX se reconoce la importancia de la corteza cerebral. La frenología es una pseudociencia que evalúa la psicología de un individuo en función del aspecto de su cabeza: se cree que cada zona de la cabeza alberga un aspecto de la personalidad.",
 25: "Pierre-Paul Broca publicó un informe clínico que demuestra que una parte del cerebro se especializa en el lenguaje.",
 26: "Carl Wernicke identifica un área que procesa y entiende el lenguaje. De ahí los nombres de la afasia de Broca y la afasia de Wernicke.",
}

d = json.load(open('data.json'))
ev = d['events']
for i, t in SUYO.items():
    text = t if i not in ADDED else f"{t} {ADDED[i]}"
    ev[i - 1]['text']['text'] = text
json.dump(d, open('data.json', 'w'), ensure_ascii=False, indent=2)

print("entradas con texto de Eduardo:", sorted(SUYO))
print("con una oración añadida:", sorted(ADDED))
print("correcciones:")
for i, f in sorted(FIXES.items()):
    print(f"  {i:2d} {f}")
