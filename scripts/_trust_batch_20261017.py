#!/usr/bin/env python3
"""Trust package 2026-10-17 (Pino): impressum identity, corrected disclaimer,
sources+dateModified per article, empty-promise removal. One pass, idempotent."""
import json, re, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
TODAY = "2026-10-17"
LANGS = ["de", "en", "fr", "it"]
def dirp(l): return "" if l == "de" else l + "/"

# ---------- localized strings ----------
DISCLAIM = {
 "de": "steuerberatung.ch erbringt keine individuelle Steuer- oder Rechtsberatung. Die Beratung erfolgt ausschliesslich durch die vermittelten Fachpersonen.",
 "en": "steuerberatung.ch does not provide individual tax or legal advice. Advice is provided exclusively by the referred specialists.",
 "fr": "steuerberatung.ch ne fournit pas de conseil fiscal ou juridique individuel. Le conseil est fourni exclusivement par les spécialistes mandatés.",
 "it": "steuerberatung.ch non fornisce consulenza fiscale o giuridica individuale. La consulenza è fornita esclusivamente dagli specialisti incaricati.",
}
OLD_DISCLAIM = [
 r"Keine Steuerberatung im Sinne des DBG[^<]*",
 r"No tax advice within the meaning of the[^<]*",
 r"Aucun conseil fiscal au sens de la LIFD[^<]*",
 r"Nessuna consulenza fiscale ai sensi della LIFD[^<]*",
]
ABOUT = {
 "de": "Ihr unabhängiger Partner für Steuern in der Schweiz. Steuer-Ratgeber, Rechner und Vermittlung geprüfter Fachpersonen – transparent und datenschutzkonform.",
 "en": "Your independent partner for taxes in Switzerland. Tax guides, calculators and referral to vetted specialists – transparent and privacy-compliant.",
 "fr": "Votre partenaire indépendant pour les impôts en Suisse. Guides fiscaux, calculateurs et médiation de spécialistes vérifiés – en toute transparence et dans le respect de la protection des données.",
 "it": "Il vostro partner indipendente per le imposte in Svizzera. Guide fiscali, calcolatori e mediazione di specialisti verificati – trasparente e conforme alla protezione dei dati.",
}
OLD_ABOUT = [
 r"Vergleich, Beratung und digitale Services[^<]*",
 r"Comparison, advice and digital services[^<]*",
 r"Comparaison, conseil et services numériques[^<]*",
 r"Confronto, consulenza e servizi digitali[^<]*",
]
HERO_SUB = {
 "de": "Unabhängige Informationen, Rechner und geprüfte Partner für Ihre Steuererklärung in der Schweiz. Transparent, datenschutzkonform, ohne Umwege.",
 "en": "Independent information, calculators and vetted partners for your tax return in Switzerland. Transparent, privacy-first, no detours.",
 "fr": "Informations indépendantes, calculateurs et partenaires vérifiés pour votre déclaration d'impôt en Suisse. Transparent, conforme à la protection des données, sans détours.",
 "it": "Informazioni indipendenti, calcolatori e partner verificati per la vostra dichiarazione d'imposte in Svizzera. Trasparente, conforme alla protezione dei dati, senza giri inutili.",
}
OLD_HERO = [
 r"Unabhängige Informationen, digitale Vorlagen und geprüfte Partner[^<]*",
 r"Independent information, digital templates and vetted partners[^<]*",
 r"Informations indépendantes, modèles numériques et partenaires vérifiés[^<]*",
 r"Informazioni indipendenti, modelli digitali e partner verificati[^<]*",
]
SOURCES_H = {"de": "Quellen", "en": "Sources", "fr": "Sources", "it": "Fonti"}
SOURCES_NOTE = {
 "de": "Amtliche Quellen (Originaltexte), Stand {d}. Alle Rechtsgrundlagen sind über fedlex, die ESTV oder die kantonalen Verwaltungen erreichbar.",
 "en": "Official sources (original texts), as of {d}. All legal bases are accessible via fedlex, the FTA or the cantonal administrations.",
 "fr": "Sources officielles (textes originaux), état du {d}. Toutes les bases légales sont accessibles via fedlex, l'AFC ou les administrations cantonales.",
 "it": "Fonti ufficiali (testi originali), stato del {d}. Tutte le basi legali sono accessibili tramite fedlex, l'AFC o le amministrazioni cantonali.",
}
UPDATED = {"de": "Zuletzt aktualisiert am", "en": "Last updated", "fr": "Dernière mise à jour :", "it": "Ultimo aggiornamento:"}
IDENT = {  # impressum identity block
 "de": "CMS<br>In der Gandstrasse 9<br>8126 Zumikon<br>Schweiz<br>Telefon: <a href=\"tel:+41772220020\">+41 77 222 00 20</a><br>E-Mail: <a href=\"mailto:info@steuerberatung.ch\">info@steuerberatung.ch</a>",
 "en": "CMS<br>In der Gandstrasse 9<br>8126 Zumikon<br>Switzerland<br>Phone: <a href=\"tel:+41772220020\">+41 77 222 00 20</a><br>E-mail: <a href=\"mailto:info@steuerberatung.ch\">info@steuerberatung.ch</a>",
 "fr": "CMS<br>In der Gandstrasse 9<br>8126 Zumikon<br>Suisse<br>Téléphone : <a href=\"tel:+41772220020\">+41 77 222 00 20</a><br>E-Mail : <a href=\"mailto:info@steuerberatung.ch\">info@steuerberatung.ch</a>",
 "it": "CMS<br>In der Gandstrasse 9<br>8126 Zumikon<br>Svizzera<br>Telefono: <a href=\"tel:+41772220020\">+41 77 222 00 20</a><br>E-Mail: <a href=\"mailto:info@steuerberatung.ch\">info@steuerberatung.ch</a>",
}
IDENT_H2 = {"de": "Verantwortlich für den Inhalt", "en": "Responsible for content", "fr": "Responsable du contenu", "it": "Responsabile del contenuto"}

def replace_all(t, patterns, repl):
    for p in patterns:
        t = re.sub(p, repl, t)
    return t

changed = {}
def touch(f):
    changed[str(f)] = changed.get(str(f), 0)

# ---------- 1) global text replacements on every page ----------
for lang in LANGS:
    base = ROOT / dirp(lang)
    for f in sorted(base.glob("*.html")):
        t0 = t = f.read_text()
        t = replace_all(t, OLD_DISCLAIM, DISCLAIM[lang])
        t = replace_all(t, OLD_ABOUT, ABOUT[lang])
        t = replace_all(t, OLD_HERO, HERO_SUB[lang])
        if t != t0:
            f.write_text(t)
            changed[str(f.relative_to(ROOT))] = changed.get(str(f.relative_to(ROOT)), 0) + 1

# ---------- 2) impressum identity block ----------
for lang in LANGS:
    f = ROOT / dirp(lang) / "impressum.html"
    t = f.read_text()
    h2 = IDENT_H2[lang]
    pat = re.compile(r'(<h2>%s</h2>\s*<p>)(.*?)(</p>)' % re.escape(h2), flags=re.S)
    m = pat.search(t)
    if not m:
        print("IMPRESSUM BLOCK NOT FOUND:", lang); continue
    if "Gandstrasse" in t:
        print("impressum already identity-complete:", lang); continue
    t = pat.sub(lambda mm: mm.group(1) + IDENT[lang] + mm.group(3), t, count=1)
    f.write_text(t)
    print("impressum identity:", lang)

# ---------- 2b) impressum legal-notice paragraph (lowercase, <strong>-wrapped) ----------
IMP_PARA = {
 "de": '<p>steuerberatung.ch ist ein unabhängiges Informations- und Vermittlungsportal. Das Portal erbringt selbst keine individuelle Steuer- oder Rechtsberatung; die Beratung erfolgt ausschliesslich durch die vermittelten, geprüften Fachpersonen in den Kantonen der Schweiz. <a href="partner-pruefung.html">So prüfen wir unsere Partner</a>.</p>',
 "en": "<p>steuerberatung.ch is an independent information and mediation portal. The portal itself does not provide individual tax or legal advice; advice is provided exclusively by the vetted specialists it refers you to, in the Swiss cantons. <a href=\"partner-pruefung.html\">How we vet our partners</a>.</p>",
 "fr": "<p>steuerberatung.ch est un portail indépendant d'information et de mise en relation. Le portail ne fournit lui-même aucun conseil fiscal ou juridique individuel ; le conseil est assuré exclusivement par les spécialistes vérifiés mandatés, dans les cantons suisses. <a href=\"partner-pruefung.html\">Comment nous vérifions nos partenaires</a>.</p>",
 "it": '<p>steuerberatung.ch è un portale indipendente di informazione e mediazione. Il portale non fornisce alcuna consulenza fiscale o giuridica individuale; la consulenza è prestata esclusivamente dagli specialisti verificati incaricati, nei cantoni svizzeri. <a href="partner-pruefung.html">Come verifichiamo i nostri partner</a>.</p>',
}
IMP_PAT = re.compile(r"<p>(?:(?!</p>).){0,600}?(?:im Sinne des DBG|within the meaning of the DBG|au sens de la LIFD|ai sensi della LIFD)(?:(?!</p>).){0,400}?</p>", flags=re.S)
for lang in LANGS:
    f = ROOT / dirp(lang) / "impressum.html"
    t = f.read_text()
    if "partner-pruefung" in t:
        continue
    t2 = IMP_PAT.sub(IMP_PARA[lang], t, count=1)
    if t2 != t:
        f.write_text(t2); print("impressum legal para:", lang)
    else:
        print("impressum para NOT replaced:", lang)

# ---------- 2c) AGB DE substantive sentence ----------
agb = ROOT / "agb.html"
t = agb.read_text()
old = "Der Anbieter erbringt selbst keine Steuerberatung im Sinne des DBG."
new = "Der Anbieter erbringt selbst keine individuelle Steuer- oder Rechtsberatung; die Beratung erfolgt ausschliesslich durch die vermittelten Fachpersonen."
if old in t:
    agb.write_text(t.replace(old, new, 1)); print("agb fixed")

# ---------- 3) sources + dateModified + updated line on all articles ----------
src_map = json.load(open(ROOT / "data/search_sources.json"))
n_art = 0
for lang in LANGS:
    base = ROOT / dirp(lang)
    for f in sorted(base.glob("*.html")):
        t = f.read_text()
        if "<!-- RELATED:START -->" not in t:
            continue
        slug = f.stem
        if slug not in src_map:
            print("NO SOURCES FOR:", lang, slug); continue
        if 'class="sources"' in t:
            continue
        links = "\n".join('<li><a href="%s" rel="noopener">%s</a></li>' % (u, lbl) for u, lbl in src_map[slug])
        sec = ('<section class="section sources"><div class="container prose"><h2>%s</h2><ul>%s</ul>'
               '<p class="sources-note">%s</p></div></section>\n' % (
               SOURCES_H[lang], links, SOURCES_NOTE[lang].format(d=TODAY.replace("-", "."))))
        t = t.replace("<!-- RELATED:START -->", sec + "<!-- RELATED:START -->", 1)
        # dateModified in JSON-LD
        t = re.sub(r'("datePublished":\s*"\d{4}-\d{2}-\d{2}")', r'\1, "dateModified": "%s"' % TODAY, t, count=1)
        # published line: add updated
        up = UPDATED[lang]
        if up not in t:
            if lang == "de":
                t = re.sub(r'(Veröffentlicht am \d{4}-\d{2}-\d{2}) · ', r'\1 · %s %s · ' % (up, TODAY), t, count=1)
            elif lang == "en":
                t = re.sub(r'(Published on \d{4}-\d{2}-\d{2}) · ', r'\1 · %s %s · ' % (up, TODAY), t, count=1)
            elif lang == "fr":
                t = re.sub(r'(Publié le \d{4}-\d{2}-\d{2}) · ', r'\1 · %s %s · ' % (up, TODAY), t, count=1)
            else:
                t = re.sub(r'(Pubblicato il \d{4}-\d{2}-\d{2}) · ', r'\1 · %s %s · ' % (up, TODAY), t, count=1)
        f.write_text(t)
        n_art += 1
print("articles updated:", n_art)

# ---------- 4) impressum: link to partner-pruefung ----------
for lang in LANGS:
    f = ROOT / dirp(lang) / "impressum.html"
    t = f.read_text()
    pp = "partner-pruefung.html" if lang == "de" else "../partner-pruefung.html" if False else ("partner-pruefung.html" if lang=="de" else {"en":"partner-pruefung.html","fr":"partner-pruefung.html","it":"partner-pruefung.html"}[lang])
    if "partner-pruefung" in t: continue
    # append a paragraph with the link before the closing of the legal section
    marker = "</main>"
    if marker in t:
        lbl = {"de":"So prüfen wir unsere Partner","en":"How we vet our partners","fr":"Comment nous vérifions nos partenaires","it":"Come verifichiamo i nostri partner"}[lang]
        t = t.replace(marker, '<p class="partner-note"><a href="%s">%s →</a></p>\n</main>' % (pp, lbl), 1)
        f.write_text(t)
        print("impressum partner link:", lang)

print("DONE. files touched:", len(changed))
