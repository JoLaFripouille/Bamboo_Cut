def optimiser_decoupe(longueur_barre, epaisseur_lame, morceaux):
    # Trier les morceaux par longueur décroissante pour optimiser l'utilisation de l'espace
    morceaux_triees = sorted(morceaux.items(), key=lambda x: x[1]['longueur'], reverse=True)

    barres = []
    chute_totale = 0

    while morceaux_triees:
        barre_actuelle = longueur_barre
        morceaux_dans_barre = []
        longueur_coupes = 0  # Somme des longueurs des morceaux coupés
        nombre_de_coupes = 0

        i = 0
        while i < len(morceaux_triees):
            repere, info = morceaux_triees[i]
            longueur_morceau = info['longueur']
            quantite = info['quantite']

            # Ajouter des morceaux jusqu'à ce qu'on ne puisse plus en ajouter
            while quantite > 0 and (longueur_coupes + longueur_morceau + nombre_de_coupes * epaisseur_lame <= longueur_barre):
                morceaux_dans_barre.append((repere, longueur_morceau))
                longueur_coupes += longueur_morceau
                nombre_de_coupes += 1
                morceaux_triees[i][1]['quantite'] -= 1
                quantite -= 1

            # Supprimer le morceau si sa quantité est zéro
            if morceaux_triees[i][1]['quantite'] == 0:
                morceaux_triees.pop(i)
            else:
                i += 1

        # Ajuster la longueur de la chute
        chute = longueur_barre - longueur_coupes - (nombre_de_coupes - 1) * epaisseur_lame
        chute_totale += chute
        barres.append({
            'morceaux': morceaux_dans_barre,
            'chute': chute
        })

        # Débogage
        print(f"Barre courante: {len(barres)}")
        print(f"  Longueur utilisée: {longueur_coupes}")
        print(f"  Nombre de coupes: {nombre_de_coupes}")
        print(f"  Chute: {chute}")
        print(f"  Morceaux dans la barre: {morceaux_dans_barre}")

    nombre_de_barres = len(barres)

    return nombre_de_barres, barres, chute_totale

# Exemple d'utilisation :
longueur_barre = 6000
epaisseur_lame = 2
morceaux = {
    'A': {'longueur': 1500, 'quantite': 3},
    'B': {'longueur': 2000, 'quantite': 2},
    'C': {'longueur': 500, 'quantite': 5}
}

nombre_de_barres, barres, chute_totale = optimiser_decoupe(longueur_barre, epaisseur_lame, morceaux)

print(f'Nombre total de barres nécessaires: {nombre_de_barres}')
for i, barre in enumerate(barres):
    print(f'Barre {i+1}:')
    for morceau in barre['morceaux']:
        print(f'  - Repère: {morceau[0]}, Longueur: {morceau[1]}')
    print(f'  Longueur de la chute: {barre["chute"]}')

print(f'Longueur totale de la chute: {chute_totale}')
