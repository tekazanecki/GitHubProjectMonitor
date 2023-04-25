import os
import requests
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS

def get_projects(technology: str) -> None:
    """funkcja tworzy wykres z najpopularniejszymi projektami na githubie 
    w danej kategori, dodaje opis i link do projektu"""
    
    
    url = 'https://api.github.com/search/repositories?q=language:' + technology + '&sort=stars'
    
    r = requests.get(url)
    print("Kod stanu:", r.status_code)
    
    response_dict = r.json()
    print(response_dict.keys())
    print("Całkowita liczba repozytoriów:", response_dict['total_count'])
    
    repo_dicts = response_dict['items']
    
    
    # wczytanie danych o rpozytorium
    names, plot_dicts = [], []
    for repo_dict in repo_dicts:
        names.append(repo_dict['name'])
        
        # słownik zawierający punktacje jak i opis repozytorium
        plot_dict = {
            'value': repo_dict['stargazers_count'],
            'label': repo_dict['description'],
            'xlink': repo_dict['html_url'],
            }
        plot_dicts.append(plot_dict)
        
    # stworzenie konfiguracji do wykresu 
    my_style = LS('#336699', base_style=LCS)
    my_config = pygal.Config()
    my_config.x_label_rotation = 45
    my_config.show_legend = False
    my_config.title_font_size = 28
    my_config.label_font_size = 14
    my_config.major_label_font_size = 18
    my_config.truncate_label = 15
    my_config.show_y_guides = False
    my_config.width = 1000
    
    # stworzenie wykresu
    chart = pygal.Bar(my_config, style=my_style)
    chart.force_url_protocol = 'http'
    chart.title = "Oznaczone największą liczbą gwiazdek projekty pythona w serwisie GIT HUB"
    chart.x_labels = names
    chart.add('', plot_dicts)
    filedir = r"D:\Users\TEK\Dokumenty\Posortowane\IT_Projekty\GitHubProjectMonitor"
    filename = technology + '_repos.svg'
    chart.render_to_file(os.path.join(filedir, filename))
    
    
tech = 'python'
get_projects(tech)