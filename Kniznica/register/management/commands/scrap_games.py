from urllib.request import urlopen
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from register.models import Category, Type, Language, Product


class Command(BaseCommand):
    def handle(self, **options):
        scrap_games_from_rexik('dievcenske', 'english', 'game')
        scrap_games_from_rexik('hry-pre-najmensie-deti', 'english', 'game')
        scrap_games_from_rexik('hry-pre-velke-deti', 'english', 'game')
        scrap_games_from_rexik('chlapcenske', 'english', 'game')
        scrap_games_from_rexik('logicke', 'english', 'game')
        scrap_games_from_rexik('najlepsie-hry', 'english', 'game')
        scrap_games_from_rexik('obliekacky', 'english', 'game')
        scrap_games_from_rexik('puzzle', 'english', 'game')
        scrap_games_from_rexik('skakacky', 'english', 'game')
        scrap_games_from_rexik('zabavne', 'english', 'game')
        scrap_games_from_rexik('zvieracie', 'english', 'game')

        scrap_games_from_superhry('hry-pro-deti', 'english', 'game')


def scrap_games_from_rexik(name, language, type):
    domain_url = 'https://rexik.zoznam.sk/'

    for i in range(1, 100):
        scrapped_url = domain_url + 'hry/' + name + '/' + str(i) + '/'
        web_client = urlopen(scrapped_url)
        web_html = web_client.read()
        web_client.close()

        page_soup = BeautifulSoup(web_html, "html.parser")
        if page_soup.findAll("div", {"class": "infoBigWindow"}):
            break
        else:
            containers = page_soup.findAll("div", {"class": "hraThumbnail"})
            for container in containers:
                game_url = domain_url + container.a['href']
                source = domain_url + container.a.img['src']
                web_client = urlopen(game_url)
                web_html = web_client.read()
                web_client.close()

                page_soup = BeautifulSoup(web_html, "html.parser")
                video_container = page_soup.find("div", {"id": "flashContent"})
                title_container = page_soup.find("div", {"class": "detailHryDescription"})

                title = title_container.h2.text
                note = title_container.p.text

                if video_container:
                    if video_container.iframe:
                        url_address = video_container.iframe.get('src')
                        publisher = video_container.iframe.get('name')

                        if url_address and publisher:
                            try:
                                category_data = Category.objects.get(name=name)
                            except Category.DoesNotExist:
                                category_data = Category.objects.create(name=name)
                            try:
                                type_data = Type.objects.get(name=type)
                            except Type.DoesNotExist:
                                type_data = Type.objects.create(name=type)
                            try:
                                language_data = Language.objects.get(name=language)
                            except Language.DoesNotExist:
                                language_data = Language.objects.create(name=language)

                            data_dict = {
                                "title": title,
                                "notes": note,
                                "url_address": url_address,
                                "rating": 0,
                                "category": category_data,
                                "type": type_data,
                                "language": language_data,
                                "publisher": publisher,
                                "source": source
                            }

                            try:
                                product = Product.objects.get(url_address=url_address)
                                for (key, value) in data_dict.items():
                                    setattr(product, key, value)
                                product.save()
                            except Product.DoesNotExist:
                                Product.objects.create(**data_dict)


def scrap_games_from_superhry(name, language, type):
    domain_url = 'http://superhry.cz/'

    for i in range(1, 100):
        scrapped_url = domain_url + name + '/'
        web_client = urlopen(scrapped_url)
        web_html = web_client.read()
        web_client.close()

        page_soup = BeautifulSoup(web_html, "html.parser")
        content_block = page_soup.find("div", {"id": "contentbox"})
        containers = content_block.findAll("div", {"class": "Glist"})

        for container in containers:
            game_url = domain_url + container.a['href']
            print(game_url)
            print(container.a.img)

            source = container.a.img.get('src')
            if not source:
                source = container.a.img.get('data-src')

            web_client = urlopen(game_url)
            web_html = web_client.read()
            web_client.close()

            page_soup = BeautifulSoup(web_html, "html.parser")
            flash_block = page_soup.find('div', {'class': 'nopm flashobject'})
            game_content_block = page_soup.find('div', {'id': 'gameDescContent'})

            if flash_block:
                url_address = flash_block.iframe.get('src')
                publisher = flash_block.iframe.get('name')

                if game_content_block:
                    if game_content_block.h2:
                        title = game_content_block.h2.text
                        notes_block = game_content_block.find('div', {"id": "descholder"})

                        if notes_block:
                            note = notes_block.p.text

                            try:
                                category_data = Category.objects.get(name=name)
                            except Category.DoesNotExist:
                                category_data = Category.objects.create(name=name)
                            try:
                                type_data = Type.objects.get(name=type)
                            except Type.DoesNotExist:
                                type_data = Type.objects.create(name=type)
                            try:
                                language_data = Language.objects.get(name=language)
                            except Language.DoesNotExist:
                                language_data = Language.objects.create(name=language)

                            data_dict = {
                                "title": title,
                                "notes": note,
                                "url_address": url_address,
                                "rating": 0,
                                "category": category_data,
                                "type": type_data,
                                "language": language_data,
                                "publisher": publisher,
                                "source": source
                            }

                            try:
                                product = Product.objects.get(url_address=url_address)
                                for (key, value) in data_dict.items():
                                    setattr(product, key, value)
                                product.save()
                            except Product.DoesNotExist:
                                Product.objects.create(**data_dict)
