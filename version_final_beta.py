import requests
from bs4 import BeautifulSoup

def webscraping():
    url = 'https://www.tycsports.com/agenda-deportiva-hoy.html'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    ligas = ['primeraa', 'italia', 'espana', 'premierleague', 'copaargentina','libertadores']

    with open('partidos_hoy.txt', 'w', encoding='utf-8') as f:
        for liga in ligas:
            eq = soup.find_all('div', class_='agenda_eventoWrap')
            equipos = []
            for i in eq:
                if i['data-competencia'] == liga and i['data-dia'] == 'hoy':
                    equipos.append(i.find('span', class_='team teamDesktop').text)

            if equipos:
                # Equipos visitantes
                eq2 = soup.find_all('div', class_='agenda_eventoWrap')
                equipos2 = []
                for i in eq2:
                    if i['data-competencia'] == liga and i['data-dia'] == 'hoy':
                        equipos2.append(i.find('span', class_='agenda__match-team visita').find('span', class_='team teamDesktop').text)

                # Partidos
                partidos = [f'{local} vs {visitante}' for local, visitante in zip(equipos, equipos2)]

                # Hora
                hora = soup.find_all('div', class_='agenda_eventoWrap')
                horas = []
                for i in hora:
                    if i['data-competencia'] == liga and i['data-dia'] == 'hoy':
                        horas.append(i.find('div', class_='agenda__time').find('span').text)

                # Canal de TV
                canales = soup.find_all('div', class_='agenda_eventoWrap')
                canal = []
                for i in canales:
                    if i['data-competencia'] == liga and i['data-dia'] == 'hoy':
                        canal_tag = i.find('div', class_='agenda_article').find('div', class_='agenda__cta').find('span', class_='transmitions')
                        canal_text = canal_tag.text.replace('TRANSMITE :', 'EN') if canal_tag else 'No disponible'
                        canal.append(canal_text)
                '''canales = soup.find_all('div', class_='agenda_eventoWrap')
                canal = []
                for i in canales:
                    if i['data-competencia'] == liga and i['data-dia'] == 'hoy':
                        transmision = i.find('div', class_='agenda_article').find('div', class_='agenda__cta').find('span', class_='transmitions')
                    if transmision is not None:
                         canal.append(transmision.text.replace('TRANSMITE :', 'EN'))
                    else:
                        canal.append('transmisión desconocida')'''

                # Partidos de hoy
                partidoshoy = [f'{partido} {hora} {tv}' for partido, hora, tv in zip(partidos, horas, canal)]

                # Escribir archivo de texto
                if liga == 'primeraa':
                    f.write('Liga Argentina:\n')
                elif liga == 'italia':
                    f.write('Serie A:\n')
                elif liga == 'espana':
                    f.write('La Liga:\n')
                elif liga == 'premierleague':
                    f.write('Premier League:\n')
                elif liga == 'copaargentina':
                    f.write('Copa Argentina:\n')
                else:
                    f.write(f'{liga.capitalize()}:\n')

                for partido in partidoshoy:
                    f.write(f'{partido}\n')
                f.write('\n')
webscraping()