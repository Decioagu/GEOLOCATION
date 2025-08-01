from django.shortcuts import render
from django.views.generic import View

from core.utils import yelp_search, get_client_data


class IndexView(View):

    # request: é o "requerimento do usuário" na pagina index.html
    def get(self, request, *args, **kwargs):
        items = [] # lista de [(palavra_chave, localização), ...]

        city = None

        # Garante que "city" nunca seja None
        while not city:
            # sempre vai retornar algo devido a função "get_client_data()"
            ret = get_client_data() #23 Busca a cidade "GeoIP2"
            if ret:
                city = ret['city'] 

        palavra_chave = request.GET.get('key', None) #23 "requerimento do usuário" palavra_chave ou Nome
        localizacao = request.GET.get('loc', None) #23 "requerimento do usuário" localização ou Nome
        print(f'Palavra chave: {palavra_chave}')
        print(f'Localização: {localizacao}')
        print(f'Cidade do usuário em pesquisa: {city}')
        
            
        #23 Se houver palavra chave descrita pelo "requerimento do usuário"
        if palavra_chave and localizacao:
            print('Buscando no Yelp...')
            #23 Busca no "Yelp" por palavra chave e localização
            items = yelp_search(keyword=palavra_chave, location=localizacao) # lista de [(palavra_chave, localização), ...]

            context = {
                'items': items, # lista de [(palavra_chave, localização), ...]
                'city': city, # localização do usuário "GeoIP2"
                'busca': True # indica que houve uma busca (busca deu verdadeiro))
            }
        else:
            print('Falha na busca em Yelp...')
            context = {
                'items': 'Falta informação de busca',
                'city': city, # localização do usuário "GeoIP2"
                'busca': False # indica que houve uma busca (busca deu falso)
            }

        #23 Renderiza a página index.html
        return render(request, 'index.html', context) 
    
