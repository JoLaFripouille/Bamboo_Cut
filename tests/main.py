def optimiser_decoupe(longueur_barre, epaisseur_lame, morceaux):
    morceaux_triees = sorted(
        morceaux.items(), key=lambda x: x[1]["longueur"], reverse=True
    )

    barres = []
    chute_totale = 0

    while morceaux_triees:
        barre_actuelle = longueur_barre
        morceaux_dans_barre = []
        longueur_coupes = 0
        nombre_de_coupes = 0

        i = 0
        while i < len(morceaux_triees):
            repere, info = morceaux_triees[i]
            longueur_morceau = info["longueur"]
            quantite = info["quantite"]
            angle1 = info.get("angle1", 0)
            angle2 = info.get("angle2", 0)

            longueur_ajustee = longueur_morceau + angle1 + angle2

            while quantite > 0 and (
                longueur_coupes + longueur_ajustee + nombre_de_coupes * epaisseur_lame
                <= longueur_barre
            ):
                morceaux_dans_barre.append((repere, longueur_morceau, angle1, angle2))
                longueur_coupes += longueur_ajustee
                nombre_de_coupes += 1
                morceaux_triees[i][1]["quantite"] -= 1
                quantite -= 1

            if morceaux_triees[i][1]["quantite"] == 0:
                morceaux_triees.pop(i)
            else:
                i += 1

        chute = (
            longueur_barre - longueur_coupes - (nombre_de_coupes - 1) * epaisseur_lame
        )
        chute_totale += chute
        barres.append({"morceaux": morceaux_dans_barre, "chute": chute})

    nombre_de_barres = len(barres)

    return nombre_de_barres, barres, chute_totale


if __name__ == "__main__":
    # Test de la fonction optimiser_decoupe
    longueur_barre = 6000
    epaisseur_lame = 2
    morceaux = {
        "A": {"longueur": 1500, "quantite": 3},
        "B": {"longueur": 2000, "quantite": 2},
        "C": {"longueur": 500, "quantite": 5},
    }
    nombre_de_barres, barres, chute_totale = optimiser_decoupe(
        longueur_barre, epaisseur_lame, morceaux
    )
    print(f"Nombre de barres: {nombre_de_barres}")
    for i, barre in enumerate(barres):
        print(f"Barre {i+1}:")
        for morceau in barre["morceaux"]:
            print(
                f"  - Repère: {morceau[0]}, Longueur: {morceau[1]}, Angle 1: {morceau[2]}, Angle 2: {morceau[3]}"
            )
        print(f"  Longueur de la chute: {barre['chute']}")
    print(f"Longueur totale de la chute: {chute_totale}")
