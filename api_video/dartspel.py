import argparse
import csv
import os
import random
import sys
from collections import defaultdict


class DartVragenSpel:
    def __init__(self, vragen_bestand="vragenlijst.csv"):
        """Initialiseert het spel en laadt het vragenbestand."""
        self.vragen_bestand = vragen_bestand
        self.vragen = []
        self.gestelde_vragen = set()
        self.vorige_scores = []
        self.totaal_score = 0
        self.perspectief_telling = defaultdict(int)
        self.laad_vragen()

    def laad_vragen(self):
        """Laadt de vragen uit het CSV-bestand in het spel."""
        try:
            with open(self.vragen_bestand, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 2:
                        perspectief = row[0].strip()
                        vraag = row[1].strip()
                        self.vragen.append((perspectief, vraag))
            print(f"✓ {len(self.vragen)} vragen geladen uit {self.vragen_bestand}")
            if not self.vragen:
                print("⚠ Waarschuwing: Geen vragen gevonden in het bestand.")
        except FileNotFoundError:
            print(f"✗ Fout: Bestand '{self.vragen_bestand}' niet gevonden.")
            sys.exit(1)
        except Exception as e:
            print(f"✗ Fout bij het laden van vragen: {e}")
            sys.exit(1)

    def kies_vraag_voor_score(self, score):
        """Selecteert een vraag op basis van de score en bias naar zeldzame perspectieven."""
        if not self.vragen:
            print("✗ Geen vragen beschikbaar.")
            return None, None

        beschikbare_vragen = [(i, v) for i, v in enumerate(self.vragen) 
                              if i not in self.gestelde_vragen]

        if not beschikbare_vragen:
            print("\n" + "*"*60)
            print("*** ALLE VRAGEN ZIJN AL GESTELD! ***")
            print("*"*60 + "\n")
            return None, None

        if score > 100:
            min_freq = min(self.perspectief_telling.values(), default=0)
            zeldzame_perspectieven = {
                p for p, c in self.perspectief_telling.items() if c == min_freq
            }
            gefilterd = [(i, v) for i, v in beschikbare_vragen if v[0] in zeldzame_perspectieven]
            if gefilterd:
                beschikbare_vragen = gefilterd

        methode1_index = score % len(beschikbare_vragen)
        methode2_index = self.totaal_score % len(beschikbare_vragen)
        if len(self.vorige_scores) >= 3:
            gemiddelde = sum(self.vorige_scores[-3:]) // 3
            methode3_index = gemiddelde % len(beschikbare_vragen)
        else:
            methode3_index = methode1_index

        if score % 5 == 0:
            gekozen_index = methode2_index
        elif score % 3 == 0:
            gekozen_index = methode3_index
        else:
            gekozen_index = methode1_index

        vraag_index, (perspectief, vraag) = beschikbare_vragen[gekozen_index]
        self.gestelde_vragen.add(vraag_index)
        self.perspectief_telling[perspectief] += 1

        return perspectief, vraag

    def verwerk_score(self, score):
        """Valideert en registreert een nieuwe score."""
        try:
            score = int(score)
            if score < 0 or score > 180:
                print("⚠ Ongeldige score. Score moet tussen 0 en 180 liggen.")
                return False

            self.vorige_scores.append(score)
            self.totaal_score += score
            return True
        except ValueError:
            print("⚠ Ongeldige invoer. Voer een getal in.")
            return False

