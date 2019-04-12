import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from register.models import Category, Type, Language, Product


class Command(BaseCommand):
    def handle(self, **options):
        scrap_all_videos_from_rexik()


def scrap_all_videos_from_rexik():
    domain_url = 'https://rexik.zoznam.sk/'
    scrapped_url = domain_url + 'rozpravky/'

    web_client = urlopen(scrapped_url)
    web_html = web_client.read()
    web_client.close()

    page_soup = BeautifulSoup(web_html, "html.parser")

    buttons_container = page_soup.find('ul', {'class': 'buttons'})
    for button in buttons_container.find_all('li'):
        if "selected" in button.get('class'):
            continue
        url = button.a.get('href')
        start = url.find('/') + 1
        end = url.find('/', start)

        name = url[start:end]
        scrap_videos_from_rexik(name, 'rexik', domain_url, 'slovak')


def scrap_videos_from_rexik(name, author, publisher, language):
    domain_url = 'https://rexik.zoznam.sk/'
    counter = 0

    while True:
        scrapped_url = domain_url + 'rozpravky/' + name + '/' + str(counter) + '/'
        counter += 1

        web_client = urlopen(scrapped_url)
        web_html = web_client.read()
        web_client.close()

        page_soup = BeautifulSoup(web_html, "html.parser")
        info_window = page_soup.find("div", {"class": "infoBigWindow"})
        if info_window:
            break
        else:
            containers = page_soup.findAll("div", {"class": "rozpravkaThumbnail"})
            for container in containers:
                video_url = domain_url + container.a.get('href')
                image_source = domain_url + container.a.img.get('src')
                web_client = urlopen(video_url)
                web_html = web_client.read()
                web_client.close()

                page_soup = BeautifulSoup(web_html, "html.parser")
                video_container = page_soup.find("div", {"id": "flashContent"})
                title_container = page_soup.find("div", {"class": "detailRozpravkyDescription"})

                if title_container:
                    title = title_container.h2.text
                    note_container = title_container.p

                    if note_container:
                        note = title_container.p.text
                    else:
                        note_container = title_container.find('div', {'class': 'texy'})
                        texts = note_container.findAll()

                        note = ''
                        for text in texts:
                            note += text.text

                    if video_container.iframe:
                        url_address = video_container.iframe['src']
                    elif video_container.find("param", {"name": "movie"}):
                        url_address = re.sub(r'/v/', '/embed/', video_container.find("param", {"name": "movie"})['value'])
                    else:
                        break

                    try:
                        category_data = Category.objects.get(name=name)
                    except Category.DoesNotExist:
                        category_data = Category.objects.create(
                            name=name,
                            image=image_source
                        )
                    try:
                        type_data = Type.objects.get(name='video')
                    except Type.DoesNotExist:
                        type_data = Type.objects.create(
                            name='video'
                        )
                    try:
                        language_data = Language.objects.get(name=language)
                    except Language.DoesNotExist:
                        language_data = Language.objects.create(
                            name=language
                        )

                    print('|' + name + '|' + str(counter) + '|' + url_address + '|')
                    data_dict = {
                        "title": title,
                        "notes": note,
                        "url_address": url_address,
                        "rating": 0,
                        "category": category_data,
                        "type": type_data,
                        "language": language_data,
                        "publisher": publisher,
                        "author": author,
                        "source": image_source
                    }

                    try:
                        product = Product.objects.get(url_address=url_address)
                        for (key, value) in data_dict.items():
                            setattr(product, key, value)
                        product.save()
                    except Product.DoesNotExist:
                        Product.objects.create(**data_dict)
