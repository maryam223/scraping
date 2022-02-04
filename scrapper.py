import requests
from bs4 import BeautifulSoup
import json

liste = []

choice=input("Voir l'actualité ou les conditions d'entrée d'un pays (actu | conditions) : ")
if choice == "conditions":
    choice2=input("Voir par continent ou par pays ? (continent | pays) : ")
    if choice2 == "continent":
        continent=input("Entrez le continent : ")
    if choice2 == "pays":
        pays=input("Entrez le pays : ")

file= open("index.html", "w", encoding="utf-8")
file.write('''<!DOCTYPE html>
<html lang="en">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-1BmE4kWBq78iYhFldvKuhfTAU6auU8tT94WrHftjDbrCEXSU1oBoqyl2QvZ6jIW3" crossorigin="anonymous">
    <title>Python Parsing</title>
</head>
<body>''')


if choice == "actu":

    page = requests.get(f'https://www.tourdumondiste.com/coronavirus-dans-quels-pays-peut-on-voyager')
    soupdata = BeautifulSoup(page.content, "html.parser")


    results = soupdata.find("ul",class_="liste_simple2")
    file.write(f'''<div class="card">
    <div class="card-header">
    <ul class="list-group list-group-flush">''')

    id = 0;
    for result in results.children:
        id+=1
        file.write(f'''<li class="list-group-item">{result.text}</li>''')
        liste.append({'id': id, 'result': result.text})

    file.write(f'''</ul>
    </div>
    </div>''')
    d = {"liste": liste}
    json.dump(d,open("db.json", "w"))
elif choice == "conditions":
    if choice2 == "pays":
        page = requests.get(f'https://www.diplomatie.gouv.fr/fr/conseils-aux-voyageurs/conseils-par-pays-destination/{pays}/')
        soupdata = BeautifulSoup(page.content, "html.parser")

        result = soupdata.find("h1")
        restrictions = soupdata.find("div", id="derniere_nopush")
        titre = restrictions.h4
        conditions = restrictions.find_all("ul", class_="spip")
        file.write(f'''<div class="card">
        <div class="card-header">
            {result}
        </div>
        <div class="card-body">
            <div>
            {f'<h4 class="card-title">{titre}</h4>' if titre else ""}
            </div>
            <div>
            {conditions}
            </div>
        </div>
        </div>''')
    elif choice2 == "continent":
        page = requests.get(f'https://www.tourdumondiste.com/coronavirus-dans-quels-pays-peut-on-voyager')
        soupdata = BeautifulSoup(page.content, "html.parser")

        sections = soupdata.find_all("div", class_="tdm__flex__content--chapitre")
        for counter in range(2):
            sections.pop(counter)
        sections.pop(0)
        for counter in range(5, 7):
            sections.pop(counter)
        sections.pop()
        for section in sections:
            titre = section.find("h2")
            descriptions = section.find_all("div", class_="col-sm-12 col-md-12 col-lg-12")
            for description in descriptions:
                nomPays = description.find("h4")
                restrictions = description.find("ul", class_="liste_simple2")
            file.write(f'''<div class="card">
            <div class="card-body">
                <div class="card-title">{titre}</div>
            <div class="accordion" id="accordionExample">
                <div class="card">
                    <div class="card-header" id="headingOne">
                        <h5 class="mb-0">
                            <button class="btn btn-link" type="button" data-toggle="collapse" data-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne">
                            {nomPays}
                            </button>
                        </h5>
                    </div>

                    <div id="collapseOne" class="collapse show" aria-labelledby="headingOne" data-parent="#accordionExample">
                        <div class="card-body">
                            {restrictions}
                        </div>
                    </div>
                </div>
                </div>
                
            </div>
            </div>''')
file.write('''
</body>
</html>''')