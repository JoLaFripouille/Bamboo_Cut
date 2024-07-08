def optimiser_decoupe(longueur_barre, epaisseur_lame, morceaux):
    # Trier les morceaux par longueur décroissante pour optimiser l'utilisation de l'espace
    morceaux_triees = sorted(morceaux.items(), key=lambda x: x[1]['longueur'], reverse=True)

    barres = []
    chute_totale = 0

    while morceaux_triees:
        barre_actuelle = longueur_barre
        morceaux_dans_barre = []
        i = 0
        nombre_de_coupes = 0

        while i < len(morceaux_triees):
            repere, info = morceaux_triees[i]
            longueur_morceau = info['longueur']
            quantite = info['quantite']

            # Vérifier si le morceau peut être placé dans la barre actuelle
            if quantite > 0 and barre_actuelle >= longueur_morceau + (epaisseur_lame if nombre_de_coupes > 0 else 0):
                morceaux_dans_barre.append((repere, longueur_morceau))
                barre_actuelle -= (longueur_morceau + epaisseur_lame)
                nombre_de_coupes += 1
                morceaux_triees[i][1]['quantite'] -= 1

                # Supprimer le morceau si sa quantité est zéro
                if morceaux_triees[i][1]['quantite'] == 0:
                    morceaux_triees.pop(i)
                else:
                    i += 1
            else:
                i += 1

        # Ajuster la longueur de la barre restante après la dernière coupe
        chute = barre_actuelle + epaisseur_lame
        chute_totale += chute
        barres.append({
            'morceaux': morceaux_dans_barre,
            'chute': chute
        })

        # Essayer de remplir la barre actuelle avec les plus petits morceaux
        if barre_actuelle > 0:
            morceaux_triees = sorted(morceaux_triees, key=lambda x: x[1]['longueur'])
            for j in range(len(morceaux_triees)):
                repere, info = morceaux_triees[j]
                longueur_morceau = info['longueur']
                quantite = info['quantite']

                while quantite > 0 and barre_actuelle >= longueur_morceau + epaisseur_lame:
                    morceaux_dans_barre.append((repere, longueur_morceau))
                    barre_actuelle -= (longueur_morceau + epaisseur_lame)
                    morceaux_triees[j][1]['quantite'] -= 1
                    quantite -= 1

                if morceaux_triees[j][1]['quantite'] == 0:
                    morceaux_triees.pop(j)
                    break

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
