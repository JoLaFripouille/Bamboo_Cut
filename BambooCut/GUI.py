import flet as ft
from main import optimiser_decoupe

def main(page: ft.Page):

    page.title = "Optimisation de découpe de barres"
    page.window.width = 800
    page.window.height = 600

    longueur_barre = ft.TextField(label="Longueur de la barre", value="6000", width=200)
    epaisseur_lame = ft.TextField(label="Épaisseur de la lame", value="2", width=200)

    morceaux = ft.Column()

    def ajouter_morceau(e):
        morceaux.controls.append(
            ft.Row([
                ft.TextField(label="Repère", width=50),
                ft.TextField(label="Longueur", width=100),
                ft.TextField(label="Quantité", width=100),
                ft.TextField(label="Angle 1", width=100),
                ft.TextField(label="Angle 2", width=100),
                ft.IconButton(ft.icons.DELETE, on_click=retirer_morceau)
            ])
        )
        page.update()

    def retirer_morceau(e):
        morceaux.controls.remove(e.control.parent)
        page.update()

    def calculer_decoupe(e):
        longueur = int(longueur_barre.value)
        epaisseur = int(epaisseur_lame.value)

        morceaux_dict = {}
        for row in morceaux.controls:
            repere = row.controls[0].value
            longueur_morceau = int(row.controls[1].value)
            quantite = int(row.controls[2].value)
            angle1 = int(row.controls[3].value) if row.controls[3].value else 0
            angle2 = int(row.controls[4].value) if row.controls[4].value else 0

            morceaux_dict[repere] = {
                'longueur': longueur_morceau,
                'quantite': quantite,
                'angle1': angle1,
                'angle2': angle2
            }

        nombre_de_barres, barres, chute_totale = optimiser_decoupe(longueur, epaisseur, morceaux_dict)

        result_area.controls.clear()
        result_area.controls.append(ft.Text(f'Nombre total de barres nécessaires: {nombre_de_barres}'))
        for i, barre in enumerate(barres):
            result_area.controls.append(ft.Text(f'Barre {i+1}:'))
            for morceau in barre['morceaux']:
                result_area.controls.append(ft.Text(f'  - Repère: {morceau[0]}, Longueur: {morceau[1]}, Angle 1: {morceau[2]}, Angle 2: {morceau[3]}'))
            result_area.controls.append(ft.Text(f'  Longueur de la chute: {barre["chute"]}'))
        result_area.controls.append(ft.Text(f'Longueur totale de la chute: {chute_totale}'))

        page.update()

    page.add(
        ft.Column([
            ft.Row([longueur_barre, epaisseur_lame]),
            ft.ElevatedButton("Ajouter un morceau", on_click=ajouter_morceau),
            morceaux,
            ft.ElevatedButton("Calculer découpe", on_click=calculer_decoupe),
            ft.Text("Résultats:", style="headline"),
            result_area := ft.Column()
        ])
    )

ft.app(target=main)
