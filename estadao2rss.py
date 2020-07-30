import requests
from bs4 import BeautifulSoup
import sys
import re

def cabecalho(editoria, colunista):
    rss =  "<?xml version=\"1.0\" encoding=\"UTF-8\" ?>\n"
    rss += "<rss version=\"2.0\">"
    rss += "<channel>"
    rss += "<title>" + colunista.capitalize() + " - Estadao</title>"
    rss += "<link>http://" + editoria + ".estadao.com.br/" + colunista + "</link>"
    rss += "<description>Coluna do " + colunista.capitalize() + " - Estadao</description>"
    return rss

def geraItem(titulo, link, conteudo, pubDate=""):
    item =  "<item>"
    item += "<title>" + titulo + "</title>"
    item += "<link>" + link + "</link>"
    item += "<description>" 
    item += "<![CDATA[" + conteudo + "]]>"
    item += "</description>"
    item += "</item>"
    return item

def geraRodape():
    return "</channel></rss>"

def geraLinksArtigos(colunista, editoria=""):
    if editoria != "":
        editoria = editoria + "."
    response = requests.get("https://" + editoria + "estadao.com.br/colunas/" + colunista)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all("a", class_="link-title")
    hrefs = []
    for link in links:
        hrefs.append(link.get('href'))
    return hrefs

def getContentClass(editoria):
    if editoria in ["cultura", "internacional"]:
        return "n--noticia__content content"
    else:
        return "noticia"

def obtemConteudoArtigo(editoria, link):
    article = requests.get(link)
    soup = BeautifulSoup(article.text, 'html.parser')
    # Localizacao conteudo da noticia
    content = soup.find(class_=getContentClass(editoria))
    # Remocao de propagandas do site
    banner = soup.find(class_="banner-in-content")
    if (banner != None):
        banner.extract()
    limite = soup.find(class_="limite-continuar-lendo")
    if (limite != None):
        limite.extract()
    # Insercao de quebras de linha nos artigos
    #return '\n'.join(p.get_text() for p in soup.find_all('p'))
    return content.get_text("\n")

def obtemTitulo(link):
    match = re.search(",([\-\w]+),", link)
    return match.group(1).capitalize()

def geraRSS(editoria, colunista):
    rss = cabecalho(editoria, colunista)

    hrefs = geraLinksArtigos(colunista, editoria)
    for href in hrefs:
        conteudo = obtemConteudoArtigo(editoria, href)
        rss += geraItem(obtemTitulo(href), href, conteudo)

    rss += geraRodape()
    return rss

def gravaXML(editoria, colunista):
    print("Gerando xml de " + colunista)
    rss = geraRSS(editoria, colunista)
    with open(colunista + ".xml", 'w') as arquivo_saida:
        arquivo_saida.write(rss)

#print(BeautifulSoup(geraRSS("internacional", "moises-naim"), 'html.parser').prettify())
gravaXML("cultura", "luis-fernando-verissimo")
gravaXML("cultura", "leandro-karnal")
gravaXML("cultura", "marcelo-rubens-paiva")
gravaXML("internacional", "moises-naim")

