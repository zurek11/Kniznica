from urllib.request import urlopen
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from register.models import Category, Type, Language, Product


class Command(BaseCommand):
    def handle(self, **options):
        scrap_news_from_rexik(
            'zaujimavosti', 'rexik', 'zoznam', 'slovak', 'news'
        )


def scrap_news_from_rexik(name, author, publisher, language, type):
    domain_url = 'https://rexik.zoznam.sk/'

    for i in range(1, 200):
        scrapped_url = domain_url + name + '/' + 'strana' + '/' + str(i) + '/'
        print(scrapped_url)
        web_client = urlopen(scrapped_url)
        web_html = web_client.read()
        web_client.close()

        page_soup = BeautifulSoup(web_html, "html.parser")
        container = page_soup.find("div", {"class": "bigWindowContainer"})
        if container:
            news_container = page_soup.findAll("div", {"class": "bigWindowBg"})
            if news_container:
                for container in news_container:
                    video_container = container.find("div", {"class": "thumbnail"})
                    image_url = domain_url + video_container.a.img['src']

                    description_container = container.find("div", {"class": "description"})
                    description = description_container.find('p').text

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
                        "notes": description,
                        "url_address": image_url,
                        "rating": 0,
                        "category": category_data,
                        "type": type_data,
                        "language": language_data,
                        "publisher": publisher,
                        "author": author,
                        "source": domain_url
                    }

                    try:
                        product = Product.objects.get(url_address=image_url)
                        for (key, value) in data_dict.items():
                            setattr(product, key, value)
                        product.save()
                    except Product.DoesNotExist:
                        Product.objects.create(**data_dict)
