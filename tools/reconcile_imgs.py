"""Finish the missing downloads and rebuild credits.json in one batched metadata call."""
import json, urllib.parse, urllib.request, time, os, re, hashlib

UA = "uic-coursework/1.0 (student timeline; github.com/fedgut)"
os.chdir(os.path.expanduser("~/Desktop/lineadetiempo-biologia"))
IMG = "assets/img"


def get(url, raw=False, tries=8):
    for i in range(tries):
        try:
            r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60)
            return r.read() if raw else json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429 and i < tries - 1:
                time.sleep(15 * (i + 1))
                continue
            raise


# key -> Commons file title. Portraits keep the slug batch 1 used.
WANT = {
    # retries from batch 1
    "edgar-adrian": "Edgar Douglas Adrian nobel.jpg",
    "eduard-hitzig": "Eduard Hitzig (1898).jpg",
    "jean-pierre-flourens": "Pierre flourens.jpeg",
    "otto-loewi": "Otto Loewi nobel.jpg",
    "paul-broca": "Paul broca.jpg",
    "thomas-willis": "Thomas Willis ODNB.jpg",
    "david-h-hubel": "DHUBEL.jpg",
    # retries from batch 2
    "vesalio-cerebro": "Vesalius 609c.png",
    "descartes-reflejo": "Descartes-reflex.JPG",
    "swammerdam-rana": "Swammerdam frog thigh.PNG",
    "galvani-ranas": "Galvani-frogs-legs-electricity.jpg",
    "ferrier-mapa-mono": "Ferriermonkey.gif",
    "cajal-corteza": "Cajal cortex drawings.png",
    # bigger replacements for the ones that came down too small
    "golgi-dibujo": "Golgi's drawing of nervous system.gif",
    "cajal-hipocampo": "CajalHippocampus.jpeg",
    # the four entries that had no image at all
    "leonardo-ventriculos": "Leonardo Da Vinci's Brain Physiology.jpg",
    "hughlings-jackson": "John Hughlings Jackson. Photogravure after L. Calkin, 1895. Wellcome L0005744.jpg",
    "tiempos-reaccion": "Apparatus for Personal Equation.png",
}

# everything already on disk, so credits.json can be rebuilt whole
HAVE = {
    "albert-von-k-lliker": "Kölliker Rudolph Albert von 1818-1902.jpg",
    "antonie-van-leeuwenhoek": "Anthonie van Leeuwenhoek (1632-1723). Natuurkundige te Delft Rijksmuseum SK-A-957.jpeg",
    "aristotle": "Aristotle Altemps Inv8575.jpg",
    "camillo-golgi": "Camillo Golgi nobel.jpg",
    "carl-wernicke": "C. Wernicke.jpg",
    "charles-scott-sherrington": "Charles Scott Sherrington2.jpg",
    "david-ferrier": "David Ferrier.jpg",
    "de-revolutionibus-orbium-coelestium": "De revolutionibus 1543.png",
    "discourse-on-the-method": "Descartes Discours de la Methode.jpg",
    "eric-kandel": "Eric Kandel 01.JPG",
    "franz-joseph-gall": "Franz Josef Gall3.jpg",
    "functional-magnetic-resonance-imaging": "1206 FMRI.jpg",
    "galen": "Galenus.jpg",
    "gregor-reisch": "Gregor Reisch book.jpg",
    "henry-hallett-dale": "Henry Hallett Dale3.jpg",
    "hippocrates": "Hippocrates.jpg",
    "jan-swammerdam": "Jan Swammerdam in zijn werkkamer, RP-P-1920-815 (cropped).jpg",
    "luigi-galvani": "Luigi Galvani, oil-painting.jpg",
    "mondino-de-luzzi": "Mundinus.jpeg",
    "ren-descartes": "Frans Hals - Portret van René Descartes.jpg",
    "santiago-ram-n-y-cajal": "Santiago Ramón y Cajal (1852-1934) portrait (restored).jpg",
    "william-harvey": "William Harvey 2.jpg",
    "papiro-edwin-smith": "Edwin Smith Papyrus v2.jpg",
    "ventriculos-reisch": "Woodcut of head showing Cerebral ventricles. Wellcome M0000436.jpg",
    "vesalio-fabrica": "Vesalius Fabrica fronticepiece.jpg",
    "botella-leyden": "Leyden jar-MHS 1188-P5200043-white.jpg",
    "gall-craneoscopia": "Phrenological chart with three perspectives of a head and sk Wellcome V0009524.jpg",
    "rowlandson-frenologia": "Franz Joseph Gall leading a discussion on phrenology with fi Wellcome V0011105.jpg",
    "broca-cerebro-leborgne": "Cerveau de Louis Victor Leborgne dit Tantan 1.jpg",
    "golgi-hipocampo": "Golgi Hippocampus.jpg",
    "cajal-cerebelo": "CajalCerebellum.jpg",
    "cajal-purkinje": "PurkinjeCell.jpg",
}

# 1. download what is missing
for key, fname in WANT.items():
    ext = os.path.splitext(fname)[1].lower().replace('.jpeg', '.jpg')
    path = f"{IMG}/{key}{ext}"
    if os.path.exists(path) and os.path.getsize(path) > 0:
        continue
    # upload.wikimedia.org serves the cached thumb directly; the hash prefix comes from the
    # md5 of the underscored filename. Falls back to the original file, then to Special:FilePath.
    u = fname.replace(' ', '_')
    h = hashlib.md5(u.encode()).hexdigest()
    q = urllib.parse.quote(u)
    base = f"https://upload.wikimedia.org/wikipedia/commons/{h[0]}/{h[:2]}/{q}"
    ext_l = os.path.splitext(u)[1].lower()
    # png and gif thumbs keep their extension; tiff renders to jpg, svg to png
    thumb_name = q + {'.tif': '.jpg', '.tiff': '.jpg', '.svg': '.png'}.get(ext_l, '')
    candidates = [f"{base.replace('/commons/', '/commons/thumb/')}/1000px-{thumb_name}", base,
                  "https://commons.wikimedia.org/wiki/Special:FilePath/" + q + "?width=1000"]
    for url in candidates:
        try:
            data = get(url, raw=True, tries=2)
            open(path, 'wb').write(data)
            print("ok", key, len(data) // 1024, "KB", url.split('/')[2], flush=True)
            time.sleep(1.0)
            break
        except Exception as e:
            last = e
    else:
        print("FAIL", key, last, flush=True)

# 2. rebuild credits.json for every file actually on disk
ALL = {**HAVE, **WANT}
titles = sorted({"File:" + f for f in ALL.values()})
strip = lambda s: re.sub('<[^>]+>', '', s or '').strip()
info = {}
for i in range(0, len(titles), 40):
    meta = get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode({
        "action": "query", "format": "json", "prop": "imageinfo", "iiprop": "extmetadata|url",
        "titles": "|".join(titles[i:i + 40])}))
    for pg in meta["query"]["pages"].values():
        ii = pg.get("imageinfo")
        if not ii:
            print("NO META", pg["title"], flush=True)
            continue
        em = ii[0].get("extmetadata", {})
        info[pg["title"][5:]] = {
            "license": strip(em.get("LicenseShortName", {}).get("value")),
            "artist": strip(em.get("Artist", {}).get("value")),
            "date": strip(em.get("DateTimeOriginal", {}).get("value")),
            "page": ii[0]["descriptionurl"],
        }
    time.sleep(2.0)

credits, missing = {}, []
for key, fname in ALL.items():
    ext = os.path.splitext(fname)[1].lower().replace('.jpeg', '.jpg')
    path = f"{IMG}/{key}{ext}"
    if not (os.path.exists(path) and os.path.getsize(path) > 0):
        missing.append(key)
        continue
    i = info.get(fname.replace('_', ' '), {})
    credits[key] = {"file": path, "commons": fname, **i}

json.dump(credits, open(f"{IMG}/credits.json", 'w'), ensure_ascii=False, indent=1)
print("\ncredits entries:", len(credits))
print("still missing:", missing)
nolic = [k for k, v in credits.items() if not v.get("license")]
print("no license recorded:", nolic)
