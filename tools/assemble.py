"""Assemble data.json: descriptions, honest display dates, images with credit.

Idempotent. Entries whose text was written by Eduardo are listed in KEEP and never touched.
Re-run after more images land; it only fills media for files that exist.
"""
import json, os, glob

REPO = os.path.expanduser("~/Desktop/lineadetiempo-biologia")
os.chdir(REPO)

# Eduardo's own wording: entries 2 and 4 written in data.json directly, the rest applied by
# eduardo_texts.py after this script runs. Never overwrite them.
KEEP = {2, 4, 5, 7, 9, 11, 14, 15, 20, 21, 25, 26}

# index (1-based, current data.json order) -> (display_date or None, image key or None, text)
E = {}

E[1] = (None, "papiro-edwin-smith", None)  # already written

E[2] = (None, "hippocrates", None)
E[3] = (None, "aristotle", None)
E[4] = ("c. 130-200", "galen", None)

E[5] = ("Siglo IV", None,
 "Nemesio, obispo de Emesa, ordena las facultades mentales dentro de los ventrículos y no en el tejido del cerebro, que se tenía por demasiado burdo para mediar entre el alma y el cuerpo. La sensación queda en los ventrículos frontales, el intelecto en el medio y la memoria en el posterior. Esta teoría ventricular gobierna la explicación del cerebro durante más de mil años.")

E[6] = (None, "mondino-de-luzzi",
 "La Anatomía de Mondino de Bolonia se vuelve el manual de referencia en Europa y se reedita durante generaciones. La disección regresa a la enseñanza, pero se practica para confirmar el texto heredado y no para corregirlo.")

E[7] = ("Leonardo da Vinci, 1452-1519", "leonardo-ventriculos",
 "Leonardo da Vinci inyecta cera caliente en los ventrículos de un cráneo y obtiene el primer molde tridimensional del sistema ventricular. El molde contradice la doctrina, porque no aparece el gran ventrículo frontal donde debía alojarse el senso comune, y él resuelve el problema trasladándolo al ventrículo medio. Nunca publicó los dibujos, así que el hallazgo no cambió nada en su tiempo.")

E[8] = (None, "ventriculos-reisch",
 "La Margarita philosophica nova, de Gregor Reisch, fija la imagen canónica de la teoría ventricular: una cabeza abierta con las facultades repartidas en tres cavidades. Es la doctrina en su punto de mayor difusión, tres décadas antes de que la anatomía humana la desmonte.")

E[9] = (None, "vesalio-fabrica",
 "Andreas Vesalio publica De humani corporis fabrica: 663 páginas y siete libros, el cuarto sobre el sistema nervioso y el séptimo sobre el cerebro. Levantada sobre cientos de disecciones humanas, la obra documenta cerca de doscientos errores de Galeno, cuya anatomía resultó ser de simios y otros animales. Una autoridad de mil años se rompe por observación directa.")

E[10] = (None, "de-revolutionibus-orbium-coelestium",
 "El mismo año aparece De revolutionibus orbium coelestium, de Copérnico. Dos libros publicados en 1543 desplazan a la vez el lugar de la Tierra en el cosmos y el de la autoridad clásica en la medicina.")

E[11] = ("René Descartes, 1596-1650", "ren-descartes",
 "René Descartes explica la conducta con el paradigma mecánico de su época, la hidráulica y la relojería de los autómatas de los jardines reales: los animales son máquinas y el ser humano es una máquina con alma. Sitúa el origen de los espíritus animales en la glándula pineal, a la que ubica por error dentro de un ventrículo. Su dualismo deja mente y cuerpo como dos sustancias distintas, y esa separación es el problema que la neurociencia hereda.")

E[12] = ("Thomas Willis, 1621-1675", "thomas-willis",
 "Thomas Willis, médico en Oxford, continúa la línea de Vesalio con una anatomía detallada del cerebro. La descripción de la estructura avanza mientras la explicación de su funcionamiento sigue siendo la de los espíritus animales.")

E[13] = (None, "discourse-on-the-method",
 "Descartes publica el Discurso del método, donde queda planteada la analogía entre el cuerpo y el autómata. El razonamiento mecánico entra a la explicación de la conducta antes de que exista cualquier medición del sistema nervioso.")

E[14] = ("Jan Swammerdam, 1637-1680", "swammerdam-rana",
 "Jan Swammerdam encierra un músculo de rana en una jeringa de vidrio y coloca una gota de agua como testigo. Al contraerse, el músculo no aumenta de volumen, de modo que ningún espíritu material ha entrado en él. También introduce la rana como animal de laboratorio, el que usarán Galvani y casi todos los que vengan después.")

E[15] = ("Siglo XVII", "william-harvey",
 "El telescopio de Galileo muestra manchas en el Sol y satélites en Júpiter, y William Harvey describe la circulación de la sangre. El modelo clásico de los cuatro humores queda sin sustento, y con él la idea de que la autoridad antigua basta para explicar el cuerpo.")

E[16] = ("1662, en francés 1664", "descartes-reflejo",
 "De homine se publica en latín doce años después de la muerte de Descartes, y en francés en 1664. De ahí viene la ilustración clásica del reflejo: el pie junto al fuego, el hilo que sube por el nervio y la respuesta que baja. Es la primera descripción detallada del reflejo nervioso, aunque Descartes no lo llama así.")

E[17] = ("Siglo XVII", "antonie-van-leeuwenhoek",
 "El reinado de los espíritus animales empieza a caer cuando se le exige cuentas a la hidrodinámica. Leeuwenhoek no encuentra en un buey el orificio del nervio óptico que Galeno describía como visible a simple vista, y un nervio fuertemente atado no se hincha por la presión que esos espíritus deberían ejercer.")

E[18] = ("Siglo XVIII", "botella-leyden",
 "La electricidad estática se vuelve moda social: máquinas de fricción en los salones y la botella de Leyden, que por primera vez permite almacenarla. En las demostraciones públicas una chispa mata animales pequeños y hace moverse miembros paralizados, con lo que la electricidad y el movimiento quedan en la misma escena.")

E[19] = ("Desde 1781", "galvani-ranas",
 "Luigi Galvani, profesor de anatomía en Bolonia, monta un laboratorio en su propia casa y trabaja una década con ancas de rana recién preparadas. Se contraen con la chispa de la máquina de fricción, con la electricidad de una tormenta y, al final, sin ninguna fuente externa, cuando el nervio ciático toca el músculo del muslo o el nervio de otra preparación. El fluido eléctrico viene de dentro del animal, y a eso llama electricidad animal.")

E[20] = (None, "luigi-galvani",
 "Galvani publica De viribus electricitatis in motu musculari, diez años después de iniciar los experimentos. La conducta deja de explicarse por un fluido que corre por tubos y empieza a explicarse por electricidad medible.")

E[21] = ("Franz Joseph Gall, 1758-1828", "gall-craneoscopia",
 "Franz Joseph Gall funda la frenología, que él llamaba organología: el cerebro es un mosaico de órganos especializados en funciones psicológicas, y cuanto más desarrollado está cada uno, más se marca en la forma del cráneo. Propone 27 facultades localizadas, 19 compartidas con los animales y 8 exclusivamente humanas, legibles por craneoscopia. Es un movimiento y no una ciencia, pero instala la idea de localización.")

E[22] = (None, "rowlandson-frenologia",
 "La caricatura de Thomas Rowlandson muestra a Gall discutiendo frenología en medio de su colección de cráneos. Sirve de medida de hasta dónde llegó el movimiento: a la cultura popular, antes que a la prueba experimental.")

E[23] = ("Desde 1820", "jean-pierre-flourens",
 "La Académie des Sciences encarga a Pierre Flourens poner a prueba la frenología con método riguroso, y él corre una larga serie de experimentos con ranas, palomas, gallinas y otras aves sin hallar rastro de especialización cortical. El episodio es paradójico: Gall tenía razón en el principio y se equivocó en el método, Flourens fue impecable en el método y partió de una premisa falsa, porque trabajó con especies de corteza poco desarrollada.")

E[24] = (None, "franz-joseph-gall",
 "Gall muere de un accidente cerebrovascular y su propio cráneo se suma a la colección de unos trescientos que había reunido en París. La frenología sobrevive como espectáculo mucho después de haber perdido la discusión científica.")

E[25] = (None, "broca-cerebro-leborgne",
 "Pierre-Paul Broca presenta el caso de Leborgne, Monsieur Tan, un paciente de 51 años que sólo podía pronunciar esa sílaba, y la autopsia muestra una lesión en el lóbulo frontal izquierdo. Finger explica el impacto por cuatro razones: información más abundante y detallada que en los casos anteriores, un área cortical distinta de las que proponían los frenólogos, una comunidad científica ya dispuesta a separar el estudio de lesiones de los bultos del cráneo, y la credibilidad de un observador cauto. El cerebro se conserva en el Museo Dupuytren de París.")

E[26] = ("Poco después de 1861", "carl-wernicke",
 "Carl Wernicke describe un trastorno distinto del lenguaje, producido por una lesión más atrás, en el lóbulo temporal izquierdo, cerca del área auditiva. El paciente no está sordo y aun así no entiende lo que se le dice. Es la primera descripción clínica de un déficit de comprensión, y muestra que el lenguaje no ocupa un solo lugar.")

E[27] = (None, "eduard-hitzig",
 "Gustav Fritsch y Eduard Hitzig trabajan en la casa de Hitzig, porque el Instituto Fisiológico de Berlín no tenía animalario, retiran fragmentos de cráneo en perros y estimulan puntos de la corteza con un electrodo. Aparecen movimientos en el lado opuesto del cuerpo, ordenados como un mapa: un punto mueve el cuello, otro la pata delantera, otro la trasera, y las respuestas se repiten al reestimular. Es la demostración experimental de la corteza motora, la prueba que al localizacionismo le faltaba.")

E[28] = (None, "golgi-dibujo",
 "Camillo Golgi trabaja en la cocina de un hospital cerca de Milán, acondicionada como laboratorio, y descubre la reazione nera: el nitrato de plata tiñe unas pocas células y sus filamentos en negro denso sobre fondo ámbar. Por primera vez se puede seguir una célula nerviosa completa, con una nitidez parecida a la de un dibujo a tinta.")

E[29] = (None, "ferrier-mapa-mono",
 "David Ferrier publica The functions of the brain y mapea la corteza sensorial con lesiones y estimulación eléctrica en primates, elegidos porque cuanto más cercana la especie, más claro el resultado. Sus mapas se extrapolaron a dibujos del cerebro humano sin respaldo experimental para ese salto.")

E[30] = (None, "hughlings-jackson",
 "Ferrier funda, con John Hughlings Jackson y otros, la revista Brain, que sigue siendo una de las publicaciones de mayor impacto del campo. El estudio del cerebro adquiere el aparato de una disciplina: revista propia, congresos y discusión entre pares.")

E[31] = (None, "david-ferrier",
 "Tras los debates del Congreso Internacional de Londres, Ferrier es llevado a juicio bajo la Act against Cruelty to Animals. Lo absuelven cuando demuestra que usaba anestesia, y pesa en la decisión que hubiera casos clínicos beneficiados por sus mapas funcionales, con cirujanos capaces de predecir la ubicación de un tumor o un absceso.")

E[32] = (None, "cajal-purkinje",
 "Catorce años después del método de Golgi, Santiago Ramón y Cajal lo mejora con cortes más gruesos y doble impregnación, y trabaja con embriones y animales jóvenes, donde los axones no están mielinizados y las células destacan. Demuestra las dos afirmaciones que fundan la neurociencia moderna: el sistema nervioso está hecho de células independientes que se comunican por contigüidad y no por continuidad, y la neurona es polarizada, el impulso entra por las dendritas y sale por el axón.")

E[33] = ("Otoño de 1889", "albert-von-k-lliker",
 "Cajal, desconocido y con mal francés, gasta sus ahorros para viajar al congreso de la élite anatómica en Berlín con sus preparaciones y su microscopio Zeiss, y en lugar de argumentar deja mirar. Albrecht von Kölliker, patriarca de la anatomía alemana, abandona en público la posición reticular, aprende español a los 72 años para traducirlo al alemán y se vuelve su aliado.")

E[34] = (None, "cajal-corteza",
 "Aparece el primer tomo de Textura del sistema nervioso del hombre y de los vertebrados, donde Cajal expone el método y las pruebas de la teoría neuronal. La obra fija el estándar de la descripción histológica del sistema nervioso.")

E[35] = (None, "santiago-ram-n-y-cajal",
 "El Nobel de Fisiología o Medicina se reparte entre Cajal y Golgi, que eran adversarios científicos. Golgi aprovechó su discurso de aceptación para defender la teoría reticular que su propia tinción había ayudado a refutar.")

E[36] = (None, "cajal-hipocampo",
 "Cajal publica Recuerdos de mi vida, la autobiografía de donde viene su propio relato del método y del congreso de Berlín. Es la fuente que permite reconstruir cómo se ganó la discusión, que fue mostrando imágenes.")

E[37] = (None, "charles-scott-sherrington",
 "Charles Sherrington entiende la importancia de la unión entre dos fibras nerviosas y la nombra sinapsis. Por el retardo que midió supuso correctamente que ahí hay un espacio físico, imposible de ver hasta el microscopio electrónico. El Nobel de 1932 lo comparte con Edgar Adrian, que descifró el código de la neurona.")

E[38] = (None, "henry-hallett-dale",
 "El Nobel va a Henry Dale y Otto Loewi por el descubrimiento de la transmisión química del impulso nervioso, después de que la acetilcolina se identificara en las primeras décadas del siglo. Valenstein compara la importancia de este hallazgo con la del código genético y la bomba atómica.")

E[39] = ("Década de 1950", "tiempos-reaccion",
 "La psicología cognitiva surge como reacción al conductismo dominante en la primera mitad del siglo. Los procesos mentales, que los conductistas descartaban por inobservables, pueden inferirse con medidas indirectas bien diseñadas, como los tiempos de reacción. De esa década es también la teoría motora de la percepción del habla.")

E[40] = ("Década de 1960", "david-h-hubel",
 "David Hubel y Torsten Wiesel en la corteza visual, y Eric Kandel en la memoria, todos premios Nobel, registran la actividad de neuronas individuales. El registro unitario muestra cómo la corteza procesa la información sensorial en sus primeras etapas.")

E[41] = ("Década de 1990", "functional-magnetic-resonance-imaging",
 "Los noventa se declaran la década del cerebro. La neuroimagen y el registro electrofisiológico, PET, RMf, potenciales evocados, MEG, DTI y EMT, permiten observar el cerebro intacto en funcionamiento, y es eso lo que hace posible la neurociencia cognitiva como campo.")

CAPTIONS = {
 "papiro-edwin-smith": "Papiro Quirúrgico de Edwin Smith.",
 "hippocrates": "Hipócrates de Cos.",
 "aristotle": "Aristóteles.",
 "galen": "Galeno de Pérgamo.",
 "mondino-de-luzzi": "Mondino de Luzzi, de Bolonia.",
 "ventriculos-reisch": "La cabeza con los ventrículos cerebrales, según la doctrina ventricular.",
 "vesalio-fabrica": "Frontispicio de De humani corporis fabrica, 1543.",
 "de-revolutionibus-orbium-coelestium": "Portada de De revolutionibus orbium coelestium, 1543.",
 "ren-descartes": "René Descartes, por Frans Hals.",
 "thomas-willis": "Thomas Willis.",
 "discourse-on-the-method": "Portada del Discurso del método, 1637.",
 "swammerdam-rana": "El experimento del músculo de rana en la jeringa de vidrio.",
 "jan-swammerdam": "Jan Swammerdam en su gabinete de trabajo.",
 "william-harvey": "William Harvey.",
 "descartes-reflejo": "La ilustración del reflejo en De homine.",
 "antonie-van-leeuwenhoek": "Antonie van Leeuwenhoek.",
 "botella-leyden": "Botella de Leyden.",
 "galvani-ranas": "Las ancas de rana en los experimentos de Galvani.",
 "luigi-galvani": "Luigi Galvani.",
 "gall-craneoscopia": "Carta craneoscópica de la frenología.",
 "rowlandson-frenologia": "Gall discutiendo frenología entre su colección de cráneos.",
 "jean-pierre-flourens": "Pierre Flourens.",
 "franz-joseph-gall": "Franz Joseph Gall.",
 "broca-cerebro-leborgne": "El cerebro de Louis Victor Leborgne, Monsieur Tan, conservado en el Museo Dupuytren.",
 "carl-wernicke": "Carl Wernicke.",
 "eduard-hitzig": "Eduard Hitzig.",
 "golgi-dibujo": "Dibujo de Golgi del sistema nervioso con la reazione nera.",
 "golgi-hipocampo": "El hipocampo teñido con la reazione nera, dibujo de Golgi.",
 "ferrier-mapa-mono": "El mapa funcional de Ferrier sobre el cerebro del mono.",
 "david-ferrier": "David Ferrier.",
 "cajal-purkinje": "Célula de Purkinje, dibujo de Cajal.",
 "cajal-corteza": "Dibujos de Cajal de la corteza cerebral.",
 "cajal-cerebelo": "Dibujo de Cajal del cerebelo.",
 "albert-von-k-lliker": "Albrecht von Kölliker.",
 "santiago-ram-n-y-cajal": "Santiago Ramón y Cajal.",
 "camillo-golgi": "Camillo Golgi.",
 "charles-scott-sherrington": "Charles Scott Sherrington.",
 "henry-hallett-dale": "Henry Hallett Dale.",
 "david-h-hubel": "David H. Hubel.",
 "functional-magnetic-resonance-imaging": "Imagen de resonancia magnética funcional.",
 "leonardo-ventriculos": "Estudio de Leonardo del cerebro y los nervios craneales, con su escritura en espejo.",
 "hughlings-jackson": "John Hughlings Jackson, cofundador de la revista Brain.",
 "cajal-hipocampo": "El hipocampo, dibujo de Cajal.",
 "tiempos-reaccion": "Aparato para medir la ecuación personal, antecedente de los tiempos de reacción.",
}

FALLBACK = {"swammerdam-rana": "jan-swammerdam", "golgi-dibujo": "golgi-hipocampo",
            "ferrier-mapa-mono": "david-ferrier", "cajal-corteza": "cajal-cerebelo"}

credits = json.load(open('assets/img/credits.json'))


def resolve(key):
    for k in (key, FALLBACK.get(key)):
        if k and k in credits and os.path.exists(credits[k]["file"]):
            return k
    return None


def media(key):
    c = credits[key]
    bits = [b for b in (c.get("artist"), c.get("license")) if b]
    credit = ", ".join(bits)
    credit = f'{credit}. <a href="{c["page"]}">Wikimedia Commons</a>' if credit else \
             f'<a href="{c["page"]}">Wikimedia Commons</a>'
    return {"url": c["file"], "caption": CAPTIONS.get(key, ""), "credit": credit}


d = json.load(open('data.json'))
ev = d['events']
assert len(ev) in (41, 42), f"unexpected event count {len(ev)}"

# TimelineJS reads the event-level display_date and ignores the one inside start_date, so the
# label lives here. Only the entries whose existing label was wrong or missing are listed;
# BCE is the era convention Eduardo asked for, and it matches what the timenav axis prints.
DISPLAY = {
    1: "c. 3000-1700 BCE",
    2: "c. 460-377 BCE",
    3: "384-322 BCE",
    4: "c. 130-200",
    23: "Desde 1820",
    42: "Referencias",
}

no_img, kept = [], []
for i, (disp, key, text) in sorted(E.items()):
    e = ev[i - 1]
    if text and i not in KEEP:
        e['text']['text'] = text
    elif i in KEEP:
        kept.append(i)
    e['start_date'].pop('display_date', None)  # one source of truth for the label
    if i in DISPLAY:
        e['display_date'] = DISPLAY[i]
    k = resolve(key) if key else None
    if k:
        e['media'] = media(k)
    else:
        e.pop('media', None)
        no_img.append((i, e['text']['headline'][:45], key or "-"))

REF = ("González Álvarez, J. (2014). La mente y el cerebro: historia y principios de la neurociencia cognitiva. "
       "En D. Redolar (Ed.), <em>Neurociencia cognitiva</em> (pp. 3-25). Editorial Médica Panamericana."
       "<br><br>Las imágenes provienen de Wikimedia Commons. Cada una lleva su autor y su licencia en el crédito "
       "de la propia imagen.")
ref_event = {"start_date": {"year": 2000}, "display_date": "Referencias",
             "text": {"headline": "Referencias", "text": REF}}
if ev[-1]['text']['headline'] == "Referencias":
    ev[-1] = ref_event
else:
    ev.append(ref_event)

json.dump(d, open('data.json', 'w'), ensure_ascii=False, indent=2)

print(f"events: {len(ev)} (41 hechos + referencias)")
print(f"con imagen: {sum(1 for e in ev if 'media' in e)}")
print(f"texto de Eduardo intacto: {kept}")
print("\nsin imagen:")
for i, h, k in no_img:
    print(f"  {i:2d} {h:47s} (buscaba: {k})")
empty = [i for i, e in enumerate(ev, 1) if not e['text'].get('text')]
print("\nsin texto:", empty or "ninguna")
