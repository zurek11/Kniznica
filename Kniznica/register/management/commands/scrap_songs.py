import re
from urllib.request import urlopen
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from register.models import Category, Type, Language, Product


class Command(BaseCommand):
    def handle(self, **options):
        scrap_all_songs_from_najmama()


def scrap_all_songs_from_najmama():
    counter = 0
    domain_url = 'https://najmama.aktuality.sk/'

    while True:
        scrapped_url = domain_url + 'pesnicky/' + str(counter) + '/'
        counter += 1

        web_client = urlopen(scrapped_url)
        web_html = web_client.read()
        web_client.close()

        page_soup = BeautifulSoup(web_html, "html.parser")
        buttons_container = page_soup.find('ul', {'class': 'article-list'})
        if buttons_container:
            for button in buttons_container.find_all('li'):
                url = button.a.get('href')
                title = button.a.get('title')

                img = button.a.picture.img
                img_source = img.get('data-src')

                if not img_source:
                    img_source = img.get('src')

                print(title)
                if title != 'Bambuľka' or 'Gumkáči':
                    scrap_song_from_najmama(url, title, img_source)
        else:
            break


def scrap_song_from_najmama(url, category_name, category_image):
    counter = 0

    scrapped_url = url
    counter += 1

    web_client = urlopen(scrapped_url)
    web_html = web_client.read()
    web_client.close()

    page_soup = BeautifulSoup(web_html, "html.parser")

    article = page_soup.find("div", {"class": "article-body-text"})
    titles = article.find_all('h2')
    notes = article.find_all('p')
    videos = article.find_all('iframe')

    if not titles:
        titles = page_soup.find("h1", {"class": "article-headline"}).text

    if notes:
        note = ''
        for index in notes:
            for br in index.find_all("br"):
                br.replace_with("\n")

            note += index.text + '\n'
        notes = re.split('[\n]{4,}', note)
    else:
        note = ''
        notes = article.find_all('div', {'class': 'one_lyrics_with_video'})
        for index in notes:
            for br in index.find_all("br"):
                br.replace_with("\n")
            note += index.text + '\n'
        notes = re.split('[\n]{4,}', note)

    if isinstance(titles, list):
        for index in range(len(titles)):
            url_address = videos[index].get('src')

            if len(notes) < len(titles):
                note = ''
            else:
                note = notes[index]

            try:
                category_data = Category.objects.get(name=category_name)
            except Category.DoesNotExist:
                category_data = Category.objects.create(
                    name=category_name,
                    image=category_image
                )
            try:
                type_data = Type.objects.get(name='song')
            except Type.DoesNotExist:
                type_data = Type.objects.create(
                    name='song'
                )
            try:
                language_data = Language.objects.get(name='slovak')
            except Language.DoesNotExist:
                language_data = Language.objects.create(
                    name='slovak'
                )

            data_dict = {
                "title": titles[index].text,
                "notes": note,
                "url_address": url_address,
                "rating": 0,
                "category": category_data,
                "type": type_data,
                "language": language_data,
                "publisher": 'najmama',
                "author": 'najmama',
                "source": category_image
            }
            try:
                product = Product.objects.get(url_address=url_address)
                for (key, value) in data_dict.items():
                    setattr(product, key, value)
                product.save()
            except Product.DoesNotExist:
                Product.objects.create(**data_dict)
    else:
        url_address = videos[0].get('src')
        notes = notes[0]

        try:
            category_data = Category.objects.get(name=category_name)
        except Category.DoesNotExist:
            category_data = Category.objects.create(
                name=category_name,
                image=category_image
            )
        try:
            type_data = Type.objects.get(name='song')
        except Type.DoesNotExist:
            type_data = Type.objects.create(
                name='song'
            )
        try:
            language_data = Language.objects.get(name='slovak')
        except Language.DoesNotExist:
            language_data = Language.objects.create(
                name='slovak'
            )

        data_dict = {
            "title": titles,
            "notes": notes,
            "url_address": url_address,
            "rating": 0,
            "category": category_data,
            "type": type_data,
            "language": language_data,
            "publisher": 'najmama',
            "author": 'najmama',
            "source": category_image
        }

        try:
            product = Product.objects.get(url_address=url_address)
            for (key, value) in data_dict.items():
                setattr(product, key, value)
            product.save()
        except Product.DoesNotExist:
            Product.objects.create(**data_dict)
