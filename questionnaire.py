# PROJET QUESTIONNAIRE V3 : POO
#
# - Pratiquer sur la POO
# - Travailler sur du code existant
# - Mener un raisonnement
#
# -> Définir les entitées (données, actions)
#
# Question
#    - titre       - str
#    - choix       - (str)
#    - bonne_reponse   - str
#
#    - poser()  -> bool
#
# Questionnaire
#    - questions      - (Question)
#
#    - lancer()
#
import json
import sys



class Question:
    def __init__(self, titre, choix, bonne_reponse):
        self.titre = titre
        self.choix = choix
        self.bonne_reponse = bonne_reponse

    def FromJsonData(data):
        #Transforme les données choix tuple (titre, bool "bonne réponse") -> [choix1, choix2 ...]
        choix= [i[0] for i in data["choix"]]
        #Trouve le bon choix en fonction du bool "bonne réponse"
        bonne_reponse= [i[0] for i in data["choix"] if i[1]]
        #Si aucune bonne réponse ou plusieurs bonnes réponses -> Anomaie dans les données
        if len(bonne_reponse) !=1:
            return None
        q = Question(data["titre"], choix, bonne_reponse[0])
        return q

    def poser(self, num_question, nb_question):
        print("QUESTION " + str(num_question) + "/" + str(nb_question)) 
        print("  " + self.titre)
        for i in range(len(self.choix)):
            print("  ", i+1, "-", self.choix[i])

        print()
        resultat_response_correcte = False
        reponse_int = Question.demander_reponse_numerique_utlisateur(1, len(self.choix))
        if self.choix[reponse_int-1].lower() == self.bonne_reponse.lower():
            print("Bonne réponse")
            resultat_response_correcte = True
        else:
            print("Mauvaise réponse")
            
        print()
        return resultat_response_correcte

    def demander_reponse_numerique_utlisateur(min, max):
        reponse_str = input("Votre réponse (entre " + str(min) + " et " + str(max) + ") :")
        try:
            reponse_int = int(reponse_str)
            if min <= reponse_int <= max:
                return reponse_int

            print("ERREUR : Vous devez rentrer un nombre entre", min, "et", max)
        except:
            print("ERREUR : Veuillez rentrer uniquement des chiffres")
        return Question.demander_reponse_numerique_utlisateur(min, max)
    
class Questionnaire:
    def __init__(self, questions, categorie, titre, difficulte):
        self.questions = questions
        self.categorie = categorie
        self.titre = titre
        self.difficulte = difficulte
        

    def from_json_data(data):
        if not data.get("questions"):
            return None
        questionnaire_data_questions= data["questions"]
        questions= [Question.FromJsonData(i) for i in questionnaire_data_questions]
        #Supprime les questions None (qui n'ont pas pu être créées)
        questions= [i for i in questions if i]


        if not data.get("categorie"):
            data["categorie"] = "inconnue"

        if not data.get("difficulte"):
            data["difficulte"] = "inconnue"
        
        if not data.get("titre"):
            return None


        return Questionnaire(questions, data["categorie"], data["titre"], data["difficulte"])



    def from_json_file(filename): 
        try:
            file= open(filename, "r")
            json_data=file.read()
            file.close()
            questionnaire_data= json.loads(json_data)
            
        except:
            print("Erreur lors de l'ouverture ou de la lecture du fichier")
            return None
        return Questionnaire.from_json_data(questionnaire_data) 
        


    def lancer(self):
        score = 0
        nb_questions= len(self.questions)
        print("-----")
        print("QUESTIONNAIRE :" + self.titre)
        print(" Categorie : " +self.categorie)
        print(" Difficulte : " + self.difficulte)
        print(" Nombre de questions :"  + str(len(self.questions)))
        print("-----")
       
        for i in range(nb_questions):
            question = self.questions[i]
            if question.poser(i+1, nb_questions):
                score += 1
        print("Score final :", score, "sur", len(self.questions))
        return score


"""questionnaire = (
    ("Quelle est la capitale de la France ?", ("Marseille", "Nice", "Paris", "Nantes", "Lille"), "Paris"), 
    ("Quelle est la capitale de l'Italie ?", ("Rome", "Venise", "Pise", "Florence"), "Rome"),
    ("Quelle est la capitale de la Belgique ?", ("Anvers", "Bruxelles", "Bruges", "Liège"), "Bruxelles")
                )

lancer_questionnaire(questionnaire)"""

# q1 = Question("Quelle est la capitale de la France ?", ("Marseille", "Nice", "Paris", "Nantes", "Lille"), "Paris")
# q1.poser()

# data = (("Marseille", "Nice", "Paris", "Nantes", "Lille"), "Paris", "Quelle est la capitale de la France ?")
# q = Question.FromData(data)
# print(q.__dict__)

"""
Questionnaire(
    (
    Question("Quelle est la capitale de la France ?", ("Marseille", "Nice", "Paris", "Nantes", "Lille"), "Paris"), 
    Question("Quelle est la capitale de l'Italie ?", ("Rome", "Venise", "Pise", "Florence"), "Rome"),
    Question("Quelle est la capitale de la Belgique ?", ("Anvers", "Bruxelles", "Bruges", "Liège"), "Bruxelles")
    )
).lancer()
"""


#Questionnaire.from_json_file("animaux_leschats_confirme.json").lancer()


if __name__ == "__main__":

    if len(sys.argv)<2:
        print("ERREUR : vous devez spécifier le nom du fichier json à charger")
        exit(0)

    json_filename= sys.argv[1]
    questionnaire=Questionnaire.from_json_file(json_filename)
    if questionnaire:
        questionnaire.lancer()
