import simpy
import random
import matplotlib.pyplot as plt
import numpy as np

# Definiranje varijable za praćenje vremena čekanja
vremena_cekanja = []

# Definiranje funkcije za generiranje vremena dolaska gledatelja


def dolazak_gledatelja():
    return random.expovariate(1)  # Koristimo eksponencijalnu distribuciju


# Inicijalizacija simulacijske okoline
env = simpy.Environment()

# Vrijeme trajanja simulacije (3 sata)
simulacija_trajanje = 3 * 60  # 3 sata u minutama

# Definiranje kapacitet stadiona (ukupan broj mjesta)
kapacitet_stadiona = 36000

# Broj prodanih ulaznica
broj_prodanih_ulaznica = 25000

# Uzmimo u obzir da gledatelji dolaze minimalno sat vremena prije programa
vrijeme_dolaska_minimalno = 60  # 1 sat u minutama

# Satnica programa (19:00 - 22:00)
satnica_pocetak = 19 * 60  # Početak u minutama
satnica_kraj = 22 * 60  # Kraj u minutama

# Definiranje glavne ulaze i izlaze (broj i kapacitet)
broj_ulaza = 2
kapacitet_ulaza = kapacitet_stadiona / broj_ulaza

# Definiranje funkcije za ponašanje gledatelja kao generator funkcije


def gledatelj(env, ime, ulaz):
    # Simulacija aktivnosti gledatelja
    yield env.timeout(dolazak_gledatelja())

    # Odabir sektora nasumično
    izabrani_sektor = random.choice(list(sektori.keys()))

    # Dobivanje cijene ulaznice za odabrani sektor
    cijena_ulaznice = sektori[izabrani_sektor]["cijena"]

    # Ažuriranje prihoda po sektorima i ukupnog prihoda
    prihodi_sektori[izabrani_sektor] += cijena_ulaznice
    ukupni_prihod[0] += cijena_ulaznice

    # Ispis informacija o gledatelju
    print(f"{ime} je odabrao {izabrani_sektor}. Cijena ulaznice: {cijena_ulaznice} eura")

    # Simulacija sigurnosne provjere s promjenjivim vremenima
    vrijeme_provjere = yield env.process(sigurnosna_provjera(env, ime))

    # Ispis informacije o vremenu provjere
    print(f"{ime} je prošao sigurnosnu provjeru za {vrijeme_provjere:.2f} minuta.")


def sigurnosna_provjera(env, ime):
    ukupno_vrijeme_provjere = 0

    # Simulacija provjere metala (promjenjivo vrijeme)
    # Promjenjivo vrijeme za provjeru metala
    vrijeme_metala = random.uniform(3, 6)
    yield env.timeout(vrijeme_metala)
    ukupno_vrijeme_provjere += vrijeme_metala

    # Simulacija pregleda torbe (promjenjivo vrijeme)
    # Promjenjivo vrijeme za pregled torbe
    vrijeme_torbe = random.uniform(1, 3)
    yield env.timeout(vrijeme_torbe)
    ukupno_vrijeme_provjere += vrijeme_torbe

    # Simulacija provjere ulaznice (promjenjivo vrijeme)
    # Promjenjivo vrijeme za provjeru ulaznice
    vrijeme_ulaznice = random.uniform(0.5, 2)
    yield env.timeout(vrijeme_ulaznice)
    ukupno_vrijeme_provjere += vrijeme_ulaznice

    # pohrana vremena cekanja
    vremena_cekanja.append(ukupno_vrijeme_provjere)

    return ukupno_vrijeme_provjere


# definicije za sektore i cijene ulaznica
sektori = {
    "Sektor 1": {"kapacitet": 6000, "cijena": 60},
    "Sektor 2": {"kapacitet": 7000, "cijena": 56},
    "Sektor 3": {"kapacitet": 8000, "cijena": 34},
    "Sektor 4": {"kapacitet": 9000, "cijena": 60},
    "Premium Sektor": {"kapacitet": 5700, "cijena": 86},
    "Premium Finish Line Sektor": {"kapacitet": 300, "cijena": 86}
}

# Generiranje gledatelja
for i in range(broj_prodanih_ulaznica):
    env.process(gledatelj(env, f"Gledatelj {i+1}", i % broj_ulaza))

# Definiranje varijabli za praćenje prihoda
# Prazan rječnik za prihode po sektorima
prihodi_sektori = {sektor: 0 for sektor in sektori.keys()}
# Ukupni prihod stadiona (koristimo listu kako bismo mogli ažurirati iz funkcije
ukupni_prihod = [0]

# Generiranje gledatelja
for i in range(broj_prodanih_ulaznica):
    env.process(gledatelj(env, f"Gledatelj {i+1}", i % broj_ulaza))

# Pokretanje simulacije
env.run(until=simulacija_trajanje)

# Ispis prihoda po sektorima
for sektor, prihod in prihodi_sektori.items():
    print(f"Prihod za {sektor}: {prihod} eura")

# Ispis ukupnog prihoda stadiona
print(f"Ukupni prihod stadiona: {ukupni_prihod[0]} eura")

# Stvaranje grafa prihoda po sektorima
sektori_labels = list(prihodi_sektori.keys())
sektori_prihodi = list(prihodi_sektori.values())

plt.figure(figsize=(10, 5))
plt.bar(sektori_labels, sektori_prihodi, color='royalblue')
plt.xlabel('Sektori')
plt.ylabel('Prihod (eura)')
plt.title('Prihod po sektorima')
plt.xticks(rotation=45)
plt.tight_layout()

# Stvaranje grafa ukupnog prihoda stadiona
plt.figure(figsize=(6, 4))
plt.bar('Ukupni prihod', ukupni_prihod[0], color='forestgreen')
plt.xlabel('')
plt.ylabel('Prihod (eura)')
plt.title('Ukupni prihod stadiona')
plt.tight_layout()

# Prikaz grafova
plt.show()

# Generirajte podatke o vremenu potrebnom za sigurnosnu provjeru (očekivano vrijeme)
vrijeme_provjere = [random.uniform(3, 6)
                    for _ in range(broj_prodanih_ulaznica)]

# Stvorite histogram
plt.hist(vrijeme_provjere, bins=20, alpha=0.5,
         color='b', edgecolor='black', linewidth=1.2)
plt.xlabel('Vrijeme provjere (min)')
plt.ylabel('Broj gledatelja')
plt.title('Histogram vremena potrebnog za sigurnosnu provjeru')
plt.grid(True)

# Prikazati histogram
plt.show()

# Nakon što završi simulacija, možete stvoriti graf vremena čekanja
plt.hist(vremena_cekanja, bins=20, alpha=0.5,
         color='b', edgecolor='black', linewidth=1.2)
plt.xlabel('Vrijeme čekanja (min)')
plt.ylabel('Broj gledatelja')
plt.title('Histogram vremena čekanja gledatelja')
plt.grid(True)

# Prikazati histogram
plt.show()
