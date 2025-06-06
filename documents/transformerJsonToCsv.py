# Import des librairies nécessaires à la lecture et l'écriture des fichiers
import json
import csv
from bs4 import BeautifulSoup


# Création des fonctions

def rajouter_0_str(nombre : int) -> str:
    """
    Parameters
    ----------
    nombre : int
        Le nombre auquel on veut POTENTIELEMENT rajouter un 0

    Returns
    -------
    str
        Le nombre avec un 0 en plus si nécessaire
    """
    
    if nombre < 10:
        return "0" + str(nombre)
    return str(nombre)


def est_bissextile(annee : int) -> bool:
    """
    Parameters
    ----------
    annee : int
        L'année dont vous voulez savoir si elle est bissextile ou pas

    Returns
    -------
    bool
        Un booleen qui renvoie True si l'année est bissextile et False sinon
    """
    # Vérifie si l'année est divisible par 4, mais pas par 100, ou bien divisible par 400
    if (annee % 4 == 0 and annee % 100 != 0) or (annee % 400 == 0):
        return True
    return False


def transformer_date_heure(date : str) -> tuple:
    """
    Parameters
    ----------
    date : str
        La date et heure à transformer en français

    Returns
    -------
    tuple
        Date et heure françaises
    """
    if date is not None:

        date_jour = int(date[8:10])
        date_mois = int(date[5:7])
        date_annee = int(date[0:4])

        heure_h = int(date[11:13])
        heure_m = int(date[14:16])
        heure_s = int(date[17:19])
        heure_UTC = int(date[20:22])
        heure_UTC = 1 - heure_UTC

        # Vérifications si à chaque fois il faut changer d'heure, de jour, etc...
        heure_h += heure_UTC
        if heure_h < 0:
            heure_h += 24
            date_jour -= 1

            if date_jour < 1:
                date_mois -= 1

                if date_mois < 1:
                    date_mois += 12
                    date_annee -= 1

                date_jour += nbr_jour_mois[date_mois]
                # Si c'est février, il faut vérifier si l'année est bissextile
                if date_mois - 1 == 2 and est_bissextile(date_annee):
                    date_jour += 1
                
        # Transformation en format français
        date_transforme = rajouter_0_str(date_jour) + "/" + rajouter_0_str(date_mois) + "/" + str(date_annee)
        heure_transforme = rajouter_0_str(heure_h) + ":" + rajouter_0_str(heure_m) + ":" + rajouter_0_str(heure_s)

        return date_transforme, heure_transforme
    return None, None


# Code principal

if __name__ == "__main__":

    try:
        # Ouverture du fichier json initial
        fichierJson = open("que-faire-a-paris-.json", "rt",  encoding = 'utf-8')
        paris_dico = json.loads(fichierJson.read()) # Transformation en dictionnaire

        # Création du fichier CSV final
        fichierCSV = open("que-faire-a-paris-.csv", "w", encoding = 'utf-8-sig', newline="")
        ecritCSV = csv.writer(fichierCSV, delimiter=";") # Création du 'stylo'

        # On écrit la ligne d'en-tête avec le titre des colonnes
        entete = ['ID' ,'URL' ,'Titre' ,'Chapeau' ,'Description' , 'Mots clés' , 'Date de début' ,'Heure de début' ,'Date de fin' ,'Heure de Fin' ,'Nom du lieu' ,'Adresse du lieu' ,'Code Postal' , 'Ville' ,'Coordonnées géographiques' ,'Accès PMR' ,'Accès mal voyant' ,'Accès mal entendant' ,'Transport' ,'Nom de contact' ,'Téléphone de contact' ,'Email de contact' ,'Url de contact' , "Type d'accès" , 'Détail du prix' ,"URL de l'image de couverture"]
        ecritCSV.writerow(entete) # Ajout de l'entete en premiere ligne avec les cles du dictionnaire
        
        # On créé la liste des valeurs dont on a besoin pour chaque évenement
        ligne_partie = ['id','url','title','lead_text','description','tags','date_debut', 'heure_debut','date_fin', 'heure_fin','address_name', 'address_street', 'address_zipcode','address_city','lat_lon','pmr','blind','deaf','transport','nom_contact','contact_phone','contact_mail','contact_url','access_type','price_detail','image_couverture']
        # On initialise une liste du nombre de jour de chaque mois pour le changement d'heure
        nbr_jour_mois = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


        for evenement in paris_dico:

            # On enlève les balises html présentes dans 2 des colonnes
            for cle in 'description', 'price_detail':
                if evenement[cle] is not None:
                    evenement[cle] = BeautifulSoup(evenement[cle], "html.parser").get_text()

            # On sort les mots clés de la liste en les séparant par des virgules dans une chaine de caractère
            if evenement['tags'] is not None:
                tags = evenement['tags']
                evenement['tags'] = tags[0]
                for tag in tags[1:]:
                    evenement['tags'] += ", " + tag

            # On extrait et on transforme les heures en heures française
            date_debut, heure_debut = transformer_date_heure(evenement['date_start'])
            evenement['date_debut'] = date_debut
            evenement['heure_debut'] = heure_debut

            date_fin, heure_fin = transformer_date_heure(evenement['date_end'])
            evenement['date_fin'] = date_fin
            evenement['heure_fin'] = heure_fin
            
            # On créé nom contact car il existe pas
            evenement['nom_contact'] = None

            # On écrit l'évenement dans une liste
            ligne = []
            for valeur in ligne_partie:
                ligne.append(evenement[valeur])
                
            ecritCSV.writerow(ligne) # Ajout de la liste évenement dans le fichier

        # Fermeture des fichiers
        fichierJson.close()
        fichierCSV.close()

    except FileNotFoundError:
        # En cas d'erreur le programme ne plante pas
        print("Fichier introuvable")


