#!/usr/bin/env python3
"""Build the MWST ePortal/AGOV deadline article in all 4 languages.

Slug: mwst-agov-pflicht-oktober-2026
Sources (primary, verified 2026-10-07):
- admin.ch Fremdmitteilung 06.10.2025 'Abschaltung MWST-Abrechnung easy' (ESTV)
- ESTV ePortal myESTV / AGOV announcement: AGOV mandatory from 31.10.2026, CH-Login off end 2027
- MWSTG portal duty expansion 1.1.2027
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from article_template import build

SLUG = "mwst-agov-pflicht-oktober-2026"
RELATED = ["mwst-100k-pflicht-schweiz.html",
           "steuer-checkliste-2026.html",
           "transparenzregister-tjpg-meldepflicht.html"]

de_title = "MWST-Abrechnung: AGOV-Pflicht ab 31. Oktober 2026 – so wechseln Sie jetzt"
de_meta = "Die ESTV schaltet «MWST-Abrechnung easy» per Mai 2026 ab und macht ab 31. Oktober 2026 das Behördenlogin AGOV obligatorisch. Wer den Zugang nicht vorbereitet hat, kann die Quartalsabrechnung nicht fristgerecht einreichen. Die Schritte im Überblick."
de_sections = [
 ("Was sich beim MWST-ePortal ändert",
  """<p>Die Eidgenössische Steuerverwaltung (ESTV) stellt ihre Mehrwertsteuer-Dienste im ePortal auf das neue allgemeine Behördenlogin <strong>AGOV</strong> um. Drei Termine sind entscheidend (Medienmitteilung der ESTV vom 6. Oktober 2025):</p>
<ul><li><strong>Mai 2026:</strong> Der vereinfachte Service «MWST-Abrechnung easy» wird endgültig eingestellt. Abgerechnet wird ausschliesslich über «MWST-Abrechnung pro».</li>
<li><strong>31. Oktober 2026:</strong> Registrierung und Anmeldung im ePortal laufen nur noch über <strong>AGOV</strong>. Das bisherige CH-Login steht für Neuregistrierungen nicht mehr zur Verfügung.</li>
<li><strong>Ende 2027:</strong> Das CH-Login wird vollständig deaktiviert.</li></ul>
<p>Für MWST-pflichtige Unternehmen heisst das konkret: Der nächste Abrechnungsstichtag nach dem 31. Oktober 2026 – die Quartalsabrechnung für das 4. Quartal 2026 (Frist in der Regel 30. April 2027, halbjährlich 30. Juni) – ist nur noch mit einem AGOV-Zugang einreichbar.</p>
<p><strong>Praxistipp:</strong> Warten Sie nicht bis Ende Oktober. Die AGOV-Registrierung ist in wenigen Minuten erledigt – aber wenn das Login am Abrechnungstag fehlt, hilft das nicht mehr.</p>"""),
 ("AGOV: Was das ist und wie Sie es einrichten",
  """<p>AGOV ist das allgemeine Behördenlogin der Schweiz, das der Bund schrittweise für alle Online-Dienste ausrollt. Sie registrieren sich einmalig im ePortal-Service <strong>«myESTV»</strong> mit AGOV – danach funktioniert der Zugang für die MWST-Dienste der ESTV.</p>
<p>Die Einrichtung in vier Schritten:</p>
<ol><li>Im ePortal der ESTV den Service «myESTV» öffnen und ein AGOV-Konto registrieren (E-Mail + Ausweisprüfung; optional eID/SwissID).</li>
<li>Das MWST-Unternehmen (UID) im myESTV-Profil verknüpfen bzw. die Firma registrieren.</li>
<li><strong>Rechte vergeben:</strong> Der erste Benutzer ist Unternehmens-Administrator. Er kann weitere interne Personen und Externe (z. B. Treuhänder) berechtigen.</li>
<li>2-Faktor-Authentifizierung einrichten und Backup-Codes sichern.</li></ol>
<p><strong>Praxistipp:</strong> Legen Sie den Administrator-Account bei der Person an, die die Firma dauerhaft kennt (Geschäftsführung), nicht beim aktuellen Buchhaltungspraktikum – sonst hängt die Abrechnung beim Personalwechsel.</p>"""),
 ("«easy» war gestern: Was «pro» kann",
  """<p>Der abgeschalte Service «MWST-Abrechnung easy» war ein Schnellformular für Kleinste mit pauschaler Angabe. «MWST-Abrechnung pro» ist der vollständige Online-Assistent: Er bildet die reguläre Abrechnung mit Saldo- oder effektiver Methode ab, erlaubt Korrekturen, Spezialtaxen und die Anlage von Berechnungen – und ist seit Mai 2026 der einzige Weg zur elektronischen Abrechnung.</p>
<p>Wer bisher «easy» nutzte, muss sich also doppelt umstellen: neues Login (AGOV) und neuer Abrechnungsassistent (pro). Die Inhalte der Abrechnung selbst ändern sich dadurch nicht – dieselben Formulare, dieselben Positionen, nur vollständiger.</p>
<p><strong>Praxistipp:</strong> Testen Sie den «pro»-Assistenten mit der ersten Abrechnung nach der Umstellung frühzeitig – die Quartalsfrist beginnt erst nach Ablauf des Quartals, aber Support-Fragen klärt man besser vor dem Stichtag.</p>"""),
 ("Ab 1. Januar 2027: Portalpflicht wird ausgeweitet",
  """<p>Nächster Ausbauschritt: Ab 2027 werden weitere MWST-Verfahren obligatorisch elektronisch über das ePortal abgewickelt (u. a. Anpassungen im Rahmen der MWST-Revision und der Digitalisierung der ESTV-Dienste). Papierformulare und formlose Meldungen treten schrittweise zurück.</p>
<p>Wer AGOV und «pro» bis Ende 2026 eingerichtet hat, ist für diese Umstellung bereits vorbereitet – und kann die Rechteverwaltung (Treuhänder, Buchhaltung, Geschäftsführung) sauber dokumentieren, was bei ESTV-Kontrollen ohnehin erwartet wird.</p>"""),
 ("Checkliste für MWST-pflichtige Unternehmen",
  """<ul><li>AGOV-Zugang über «myESTV» registrieren – <strong>vor dem 31. Oktober 2026</strong>.</li>
<li>UID/MWST-Nummer im Profil verknüpfen und Testlogin durchführen.</li>
<li>Unternehmens-Administrator bestimmen; Treuhänder/Buchhaltung berechtigen.</li>
<li>2FA aktivieren, Backup-Codes offline verwahren.</li>
<li>Nächste Quartalsabrechnung mit «MWST-Abrechnung pro» einreichen.</li>
<li>Bestehende CH-Login-Zugänge bis spätestens Ende 2027 vollständig ersetzen.</li></ul>
<p>Fragen zur MWST-Pflicht selbst (Umsatzgrenze CHF 100'000, freiwillige Registrierung) beantwortet unser Artikel <a href="mwst-100k-pflicht-schweiz.html">MWST-Pflicht ab CHF 100'000</a>. Bei Unklarheiten zur Berechtigung im ePortal hilft der ESTV-Support oder ein geprüfter Treuhandpartner – Erstberatung via <a href="kontakt.html">Kontakt</a>.</p>"""),
 ("Kurz gesagt",
  """<ul><li>Mai 2026: «MWST-Abrechnung easy» abgeschaltet – Abrechnung nur noch via «pro».</li>
<li>31. Oktober 2026: AGOV ist Pflicht für Registrierung und Login im ESTV-ePortal.</li>
<li>Ende 2027: CH-Login vollständig deaktiviert.</li>
<li>Einmalig «myESTV» mit AGOV einrichten, UID verknüpfen, Rechte vergeben – dauert keine halbe Stunde.</li>
<li>Ohne vorbereiteten Zugang droht eine versäumte Abrechnungsfrist mit Verzugsfolgen.</li>
<li>Dies ist allgemeine Information, keine individuelle Beratung.</li></ul>"""),
]

en_title = "Swiss VAT filing: AGOV login mandatory from 31 October 2026 – switch now"
en_meta = "The ESTV is switching off 'MWST-Abrechnung easy' (May 2026) and making the new government login AGOV mandatory from 31 October 2026. Without a prepared account you cannot file your quarterly VAT return on time. The steps, in English."
en_sections = [
 ("What changes in the VAT ePortal",
  """<p>The Federal Tax Administration (FTA/ESTV) is moving its VAT services to the new general government login <strong>AGOV</strong>. Three dates matter (FTA communication of 6 October 2025):</p>
<ul><li><strong>May 2026:</strong> the simplified service «MWST-Abrechnung easy» is switched off permanently. Filing works only via «MWST-Abrechnung pro».</li>
<li><strong>31 October 2026:</strong> registration and login in the ePortal work only via <strong>AGOV</strong>. The old CH-Login is no longer available for new registrations.</li>
<li><strong>End of 2027:</strong> CH-Login is deactivated completely.</li></ul>
<p>Concretely: the first filing deadline after 31 October 2026 – the Q4 2026 quarterly return – can only be submitted with an AGOV account.</p>
<p><strong>Practical tip:</strong> don't wait until late October. AGOV registration takes minutes – but it doesn't help on the day the deadline falls.</p>"""),
 ("AGOV: what it is and how to set it up",
  """<p>AGOV is Switzerland's general government login, being rolled out across all federal online services. You register once in the ePortal service <strong>«myESTV»</strong> with AGOV – the same account then works for the FTA's VAT services.</p>
<ol><li>Open «myESTV» in the FTA ePortal and register an AGOV account (e-mail + identity check; eID/SwissID optional).</li>
<li>Link your company (UID/VAT number) in the myESTV profile.</li>
<li><strong>Grant rights:</strong> the first user is company administrator and can authorise further internal staff and external parties (e.g. your fiduciary).</li>
<li>Enable two-factor authentication and store backup codes.</li></ol>
<p><strong>Practical tip:</strong> put the administrator role with a permanent officer (managing director), not with rotating accounting staff – otherwise the filing stalls at the next personnel change.</p>"""),
 ("From «easy» to «pro»: what the new assistant does",
  """<p>The discontinued «easy» service was a quick form for the smallest cases. «MWST-Abrechnung pro» is the full online assistant: balance or effective method, corrections, special rates, supporting schedules – and since May 2026 the only way to file electronically. The content of the return doesn't change – just the tool is more complete.</p>
<p>Former «easy» users therefore face two switches at once: new login (AGOV) and new assistant (pro).</p>"""),
 ("Checklist for VAT-registered companies",
  """<ul><li>Register AGOV via «myESTV» – <strong>before 31 October 2026</strong>.</li>
<li>Link UID/VAT number and test the login.</li>
<li>Appoint the company administrator; authorise fiduciary/accounting.</li>
<li>Activate 2FA, keep backup codes offline.</li>
<li>File the next quarterly return via «MWST-Abrechnung pro».</li>
<li>Replace all remaining CH-Login access by end of 2027.</li></ul>
<p>Whether you are VAT-liable at all (CHF 100,000 threshold) is covered in our article <a href="mwst-100k-pflicht-schweiz.html">Swiss VAT registration from CHF 100,000</a>. For ePortal rights questions, the FTA support or a vetted fiduciary partner helps – free initial review via <a href="kontakt.html">contact</a>.</p>"""),
 ("In short",
  """<ul><li>May 2026: «MWST-Abrechnung easy» off – filing only via «pro».</li>
<li>31 October 2026: AGOV mandatory for ePortal registration and login.</li>
<li>End of 2027: CH-Login fully deactivated.</li>
<li>Set up «myESTV» + AGOV once, link your UID, grant rights – under half an hour.</li>
<li>Without a prepared account, a missed filing deadline with late-payment consequences is a real risk.</li>
<li>General information, not individual advice.</li></ul>"""),
]

fr_title = "TVA suisse : login AGOV obligatoire dès le 31 octobre 2026 – passez maintenant"
fr_meta = "L'AFC désactive « MWST-Abrechnung easy » (mai 2026) et impose le nouveau login gouvernemental AGOV dès le 31 octobre 2026. Sans compte préparé, le dépôt trimestriel de votre décompte TVA devient impossible. Les étapes en français."
fr_sections = [
 ("Ce qui change dans l'ePortal TVA",
  """<p>L'Administration fédérale des contributions (AFC) migre ses services TVA vers le nouveau login gouvernemental général <strong>AGOV</strong>. Trois dates comptent (communication AFC du 6 octobre 2025) :</p>
<ul><li><strong>Mai 2026 :</strong> le service simplifié « MWST-Abrechnung easy » est définitivement désactivé. Le dépôt ne passe plus que par « MWST-Abrechnung pro ».</li>
<li><strong>31 octobre 2026 :</strong> l'enregistrement et la connexion dans l'ePortal ne fonctionnent plus que via <strong>AGOV</strong>. L'ancien CH-Login n'est plus disponible pour les nouvelles inscriptions.</li>
<li><strong>Fin 2027 :</strong> le CH-Login est complètement désactivé.</li></ul>
<p>Concrètement : le premier échéancier après le 31 octobre 2026 – le décompte TVA du 4e trimestre 2026 – ne peut être déposé qu'avec un compte AGOV.</p>
<p><strong>Conseil pratique :</strong> n'attendez pas fin octobre. L'inscription AGOV prend quelques minutes – mais elle ne sert plus à rien le jour de l'échéance.</p>"""),
 ("AGOV : ce que c'est et comment l'ouvrir",
  """<p>AGOV est le login gouvernemental général de la Suisse, déployé progressivement pour tous les services fédéraux en ligne. Vous vous enregistrez une fois dans le service ePortal <strong>« myESTV »</strong> avec AGOV – le même compte vaut ensuite pour les services TVA de l'AFC.</p>
<ol><li>Ouvrir « myESTV » dans l'ePortal de l'AFC et créer un compte AGOV (e-mail + vérification d'identité ; eID/SwissID en option).</li>
<li>Lier l'entreprise (IDE/n° TVA) dans le profil myESTV.</li>
<li><strong>Attribuer les droits :</strong> le premier utilisateur est administrateur de l'entreprise ; il autorise le personnel interne et les tiers (p. ex. le fiduciaire).</li>
<li>Activer l'authentification à deux facteurs et conserver les codes de secours.</li></ol>
<p><strong>Conseil pratique :</strong> confiez le rôle d'administrateur à une personne durable de l'entreprise (direction), pas à un collaborateur comptable en rotation – sinon le dépôt bloque au prochain changement de personnel.</p>"""),
 ("Checklist pour les entreprises assujetties à la TVA",
  """<ul><li>Créer le compte AGOV via « myESTV » – <strong>avant le 31 octobre 2026</strong>.</li>
<li>Lier l'IDE/n° TVA et tester la connexion.</li>
<li>Désigner l'administrateur ; autoriser fiduciaire et comptabilité.</li>
<li>Activer le 2FA, garder les codes de secours hors ligne.</li>
<li>Déposer le prochain décompte trimestriel via « MWST-Abrechnung pro ».</li>
<li>Remplacer tous les accès CH-Login restants d'ici fin 2027.</li></ul>
<p>Notre article <a href="mwst-100k-pflicht-schweiz.html">TVA dès 100 000 francs de chiffre d'affaires</a> explique si vous êtes assujetti. Pour les droits d'accès ePortal : support AFC ou partenaire fiduciaire vérifié – premier entretien gratuit via <a href="kontakt.html">contact</a>.</p>"""),
 ("En bref",
  """<ul><li>Mai 2026 : fin de « MWST-Abrechnung easy » – dépôt uniquement via « pro ».</li>
<li>31 octobre 2026 : AGOV obligatoire pour l'enregistrement et la connexion ePortal.</li>
<li>Fin 2027 : CH-Login entièrement désactivé.</li>
<li>Ouvrir « myESTV » + AGOV une fois, lier l'IDE, attribuer les droits – moins d'une demi-heure.</li>
<li>Sans compte préparé, risque réel d'échéance manquée avec intérêts moratoires.</li>
<li>Information générale, pas un conseil individuel.</li></ul>"""),
]

it_title = "IVA svizzera: login AGOV obbligatorio dal 31 ottobre 2026 – passate ora"
it_meta = "L'AFC spegne « MWST-Abrechnung easy » (maggio 2026) e impone il nuovo login governativo AGOV dal 31 ottobre 2026. Senza conto preparato il versamento trimestrale dell'IVA non è più possibile. I passaggi in italiano."
it_sections = [
 ("Cosa cambia nell'ePortal IVA",
  """<p>L'Amministrazione federale delle contribuzioni (AFC) migra i servizi IVA al nuovo login governativo generale <strong>AGOV</strong>. Tre date decisive (comunicazione AFC del 6 ottobre 2025):</p>
<ul><li><strong>Maggio 2026:</strong> il servizio semplificato « MWST-Abrechnung easy » è definitivamente spento. Il versamento avviene solo tramite « MWST-Abrechnung pro ».</li>
<li><strong>31 ottobre 2026:</strong> registrazione e login nell'ePortal funzionano solo via <strong>AGOV</strong>. Il vecchio CH-Login non è più disponibile per nuove registrazioni.</li>
<li><strong>Fine 2027:</strong> il CH-Login è disattivato completamente.</li></ul>
<p>In concreto: la prima scadenza dopo il 31 ottobre 2026 – il rendiconto IVA del 4° trimestre 2026 – può essere trasmesso solo con un conto AGOV.</p>
<p><strong>Consiglio pratico:</strong> non aspettate fine ottobre. La registrazione AGOV richiede pochi minuti – ma il giorno della scadenza non serve più a nulla.</p>"""),
 ("AGOV: cos'è e come si apre",
  """<p>AGOV è il login governativo generale della Svizzera, introdotto progressivamente per tutti i servizi federali online. Ci si registra una volta nel servizio ePortal <strong>« myESTV »</strong> con AGOV – lo stesso conto vale poi per i servizi IVA dell'AFC.</p>
<ol><li>Aprire « myESTV » nell'ePortal AFC e creare un conto AGOV (e-mail + verifica d'identità; eID/SwissID opzionale).</li>
<li>Collegare l'impresa (IDE/n. IVA) nel profilo myESTV.</li>
<li><strong>Assegnare i diritti:</strong> il primo utente è amministratore dell'impresa e autorizza collaboratori interni e terzi (p. es. il fiduciario).</li>
<li>Attivare l'autenticazione a due fattori e conservare i codici di riserva.</li></ol>
<p><strong>Consiglio pratico:</strong> affidate il ruolo di amministratore a una persona stabile dell'azienda (direzione), non a un collaboratore contabile in rotazione – altrimenti il versamento si blocca al primo cambio di personale.</p>"""),
 ("Checklist per le imprese IVA",
  """<ul><li>Aprire il conto AGOV via « myESTV » – <strong>prima del 31 ottobre 2026</strong>.</li>
<li>Collegare IDE/n. IVA e provare il login.</li>
<li>Designare l'amministratore; autorizzare fiduciario e contabilità.</li>
<li>Attivare il 2FA, custodire i codici di riserva offline.</li>
<li>Trasmettere il prossimo rendiconto trimestrale via « MWST-Abrechnung pro ».</li>
<li>Sostituire tutti gli accessi CH-Login entro fine 2027.</li></ul>
<p>Se siete soggetti all'IVA (soglia di 100'000 franchi) lo spiega il nostro articolo <a href="mwst-100k-pflicht-schweiz.html">IVA dall'obbligo dei 100'000 franchi</a>. Per i diritti d'accesso ePortal: supporto AFC o partner fiduciario verificato – primo colloquio gratuito tramite <a href="kontakt.html">contatto</a>.</p>"""),
 ("In breve",
  """<ul><li>Maggio 2026: fine di « MWST-Abrechnung easy » – versamento solo via « pro ».</li>
<li>31 ottobre 2026: AGOV obbligatorio per registrazione e login ePortal.</li>
<li>Fine 2027: CH-Login disattivato del tutto.</li>
<li>Aprire « myESTV » + AGOV una volta, collegare l'IDE, assegnare i diritti – meno di mezz'ora.</li>
<li>Senza conto preparato si rischia una scadenza mancata con interessi moratori.</li>
<li>Informazione generale, non consulenza individuale.</li></ul>"""),
]

for lang, title, meta, sections in [("de", de_title, de_meta, de_sections),
                                    ("en", en_title, en_meta, en_sections),
                                    ("fr", fr_title, fr_meta, fr_sections),
                                    ("it", it_title, it_meta, it_sections)]:
    build(lang, SLUG, title, meta, sections, related=RELATED)
print("done")
