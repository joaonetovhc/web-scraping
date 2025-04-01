import os
import requests
import zipfile
from bs4 import BeautifulSoup

url = requests.get("https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos")

html = BeautifulSoup(url.text, "html.parser")

pdf_links = html.find('div', class_ = "cover-richtext-tile tile-content")

pdf_url = []

#buscando na div onde tem tag 'a' com href, e verificando se é .pdf para adicionar na lista
if pdf_links:
    links = pdf_links.find_all('a', href=True)

    for p in links:
        if '.pdf' in p['href'] and 'Anexo' in p['href']:
            pdf_url.append(p['href'])

for p in pdf_url:
    print("Anexos encontrados:", p)


dir_anexos = "anexos/"
os.makedirs(dir_anexos, exist_ok=True)

#função para baixar os arquivos pdf e renomear a partir da url
def download_pdf(url, folder):
    response = requests.get(url, stream= True)
    name_pdf = os.path.join(folder, url.split("/")[-1])
    with open(name_pdf, 'wb') as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)
    print(f"Baixado:{name_pdf}")       

#chamada da funçao de baixar
for pdf in pdf_url:
    download_pdf(pdf, dir_anexos)

#onde compacta os pdf em um arquivo .zip
zip_name = "anexos.zip"
with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for pdf in os.listdir(dir_anexos):
        zipf.write(os.path.join(dir_anexos, pdf), os.path.basename(pdf))

print(f"Arquivos compactados:{zip_name}")
