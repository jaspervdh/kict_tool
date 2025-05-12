import argparse
import csv
import os
import random
import sys


class DartVragenSpel:
    def __init__(self, vragen_bestand="vragenlijst.csv"):
        """Initialiseer het dartspel met vragen."""
        self.vragen_bestand = vragen_bestand
        self.vragen = []
        self.gestelde_vragen = set()
        self.vorige_scores = []
        self.totaal_score = 0
        self.laad_vragen()

    def laad_vragen(self):
        """Laad vragen uit het CSV-bestand."""
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
        """Kies een vraag gebaseerd op de gegooide score."""
        if not self.vragen:
            print("✗ Geen vragen beschikbaar.")
            return None, None
        
        # Mogelijke selectiemethodes voor vragen op basis van de score
        beschikbare_vragen = [(i, v) for i, v in enumerate(self.vragen) 
                             if i not in self.gestelde_vragen]
        
        if not beschikbare_vragen:
            print("\n" + "*"*60)
            print("*** ALLE VRAGEN ZIJN AL GESTELD! WE BEGINNEN OPNIEUW. ***")
            print("*"*60 + "\n")
            self.gestelde_vragen.clear()
            beschikbare_vragen = [(i, v) for i, v in enumerate(self.vragen)]
        
        # Dartbord-geïnspireerde selectie
        # - Gebruik de huidige score
        # - Gebruik de totaalscore
        # - Gebruik combinatie van laatste worpen
        
        # Methode 1: Gebruik score direct (modulo aantal beschikbare vragen)
        methode1_index = score % len(beschikbare_vragen)
        
        # Methode 2: Gebruik totaalscore
        methode2_index = self.totaal_score % len(beschikbare_vragen)
        
        # Methode 3: Gebruik gemiddelde van laatste drie scores (als beschikbaar)
        if len(self.vorige_scores) >= 3:
            gemiddelde = sum(self.vorige_scores[-3:]) // 3
            methode3_index = gemiddelde % len(beschikbare_vragen)
        else:
            methode3_index = methode1_index
        
        # Kies een van de methoden op basis van de score zelf
        # Bij scores deelbaar door 5 gebruiken we methode 2
        # Bij scores deelbaar door 3 gebruiken we methode 3
        # Anders gebruiken we methode 1
        if score % 5 == 0:
            gekozen_index = methode2_index
        elif score % 3 == 0:
            gekozen_index = methode3_index
        else:
            gekozen_index = methode1_index
            
        vraag_index, (perspectief, vraag) = beschikbare_vragen[gekozen_index]
        self.gestelde_vragen.add(vraag_index)
        
        return perspectief, vraag

    def verwerk_score(self, score):
        """Verwerk een nieuwe score en bewaar score-geschiedenis."""
        try:
            score = int(score)
            if score < 0 or score > 180:  # Maximum score bij darts is 180 (3x triple 20)
                print("⚠ Ongeldige score. Score moet tussen 0 en 180 liggen.")
                return False
            
            self.vorige_scores.append(score)
            self.totaal_score += score
            return True
        except ValueError:
            print("⚠ Ongeldige invoer. Voer een getal in.")
            return False

    def toon_vraag(self, perspectief, vraag):
        """Toon een vraag met bijbehorend perspectief."""
        print("\n" + "="*60)
        print(f"Vraag: {vraag} ({perspectief} perspectief)")
        print(f"Vraag {len(self.gestelde_vragen)} van {len(self.vragen)}")
        print("="*60 + "\n")

    def start_spel(self):
        """Start het vragen-dartspel."""
        print("\n=== Dart Vragen Spel ===")
        print("Typ 'stop' om het spel te beëindigen.\n")
        
        while True:
            score_input = input("Geworpen score: ").strip().lower()
            
            if score_input in ['stop', 'exit', 'quit', 'q']:
                print("\nBedankt voor het spelen!")
                break
                
            if not self.verwerk_score(score_input):
                continue
                
            score = int(score_input)
            perspectief, vraag = self.kies_vraag_voor_score(score)
            
            if perspectief and vraag:
                # Controleer of we net alle vragen hebben gehad
                if len(self.gestelde_vragen) == 1 and len(self.vragen) > 1:
                    print("\nDit is de eerste vraag van een nieuwe ronde nadat alle vragen zijn gesteld.")
                
                self.toon_vraag(perspectief, vraag)


def main():
    parser = argparse.ArgumentParser(description='Dart Vragen Spel')
    parser.add_argument('-f', '--file', type=str, default='vragenlijst.csv',
                        help='CSV-bestand met vragen (standaard: vragenlijst.csv)')
    args = parser.parse_args()
    
    spel = DartVragenSpel(args.file)
    spel.start_spel()


if __name__ == "__main__":
    main()