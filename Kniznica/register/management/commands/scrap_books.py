from random import randint
from urllib.request import urlopen
from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from sickle import Sickle
from sickle.models import Record
from register.models import Category, Type, Language, Product, Book, CopyBook


class UnimarcRecord(Record):
    def __init__(self, record_element):
        super().__init__(record_element)
        metadata = self.xml.find('.//' + self._oai_namespace + 'metadata')
        data_fields = [item for item in metadata.findall('.//{http://www.loc.gov/MARC21/slim}datafield')]
        control_fields = [item for item in metadata.findall('.//{http://www.loc.gov/MARC21/slim}controlfield')]

        self.control_field = {}
        for control_field in control_fields:
            self.control_field.update({control_field.attrib['tag']: control_field.text})

        self.data_field = {}
        for data_field in data_fields:
            subfields = [item for item in data_field.findall('.//{http://www.loc.gov/MARC21/slim}subfield')]
            self.subfield = {}
            for subfield in subfields:
                self.subfield.update({subfield.attrib['code']: subfield.text})
            self.data_field.update({data_field.attrib['tag']: self.subfield})

        self.metadata['datafield'] = self.data_field
        self.metadata['controlfield'] = self.control_field
        del self.metadata['subfield']
    pass


class Command(BaseCommand):
    def handle(self, **options):
        libraries = [
            'UMBCAT',
            'RUZCAT',
            'PIMCAT',
            'EUCAT',
            'SENCAT'
        ]
        # harvest_books(
        #     'https://www.library.sk/i2/i2.ws.oai.cls',
        #     'UMBCAT',
        #     [
        #         'predškolská výchova',
        #         'materské školy',
        #         'preschool education',
        #         'Predškolská a primárna výchova a vzdelávanie',
        #         'deti predškolského veku',
        #         'deti školského veku',
        #         'preschool children',
        #         'school children',
        #         'kindergartens',
        #         'elementary school textbooks',
        #         'učebnice základných škôl',
        #         'deti',
        #         'detská',
        #         'child',
        #         'detské',
        #         'Pre čitateľov od 6 do 10 rokov'
        #     ],
        #     200
        # )
        # harvest_books(
        #     'https://arl4.library.sk/i2/i2.ws.oai.cls',
        #     'SENCAT',
        #     [
        #         'príbehy pre deti',
        #         'literatúra pre deti a mládež',
        #         'romány fantasy',
        #         'fantasy',
        #         'náučná literatúra pre deti',
        #         'encyklopédie pre deti',
        #         'rozprávky',
        #         'rozprávky autorské',
        #         'rozprávky poučné',
        #         'príbehy s obrázkami',
        #         'rozprávky ľudové',
        #         'rozprávky o zvieratkách',
        #         'rozprávky o princeznách',
        #         'rozprávky o deťoch'
        #         'rozprávky pre prvákov'
        #     ],
        #     200
        # ),
        harvest_books(
            'https://www.library.sk/i2/i2.ws.oai.cls',
            'PIMCAT',
            [
                'príbehy pre deti',
                'publikácie pre mládež',
                'príbehy pre najmenších',
                'rozprávky pre najmenších',
                'publikácie pre deti',
                'literatúra pre deti a mládež',
                'romány fantasy',
                'fantasy',
                'náučná literatúra pre deti',
                'encyklopédie pre deti',
                'rozprávky',
                'rozprávky autorské',
                'rozprávky poučné',
                'príbehy s obrázkami',
                'rozprávky ľudové',
                'rozprávky o zvieratkách',
                'rozprávky o princeznách',
                'rozprávky o deťoch'
                'rozprávky pre prvákov'
            ],
            200
        )


def harvest_books(url, library, search_words, sum):
    sickle = Sickle(url)
    sickle.class_mapping['ListRecords'] = UnimarcRecord
    sickle.class_mapping['GetRecord'] = UnimarcRecord
    records = sickle.ListRecords(metadataPrefix='oai_marcxml', set=library)
    counter = 0

    for record in records:
        data_field = record.metadata.get('datafield')
        if data_field:
            tag_610 = data_field.get('610')
            tag_010 = data_field.get('010')

            if tag_610:
                category = subtag_a = tag_610.get('a')
                if subtag_a and subtag_a in search_words:
                    if tag_010:
                        subtag_a = tag_010.get('a')
                        if subtag_a:
                            isbn = subtag_a
                            source = get_image(subtag_a)
                            if source:
                                tag_102 = data_field.get('102')
                                tag_200 = data_field.get('200')
                                tag_205 = data_field.get('205')
                                tag_210 = data_field.get('210')
                                tag_215 = data_field.get('215')
                                tag_330 = data_field.get('330')
                                print('SCRAPPED[' + str(counter) + ']: ' + str(isbn))

                                title = ''
                                author = ''
                                notes = ''
                                publisher = ''
                                edition = 0
                                year = 0
                                pages = 0

                                if tag_102:
                                    language = tag_102.get('a')
                                else:
                                    language = 'slovak'

                                if tag_200:
                                    title = tag_200.get('a')
                                    author = tag_200.get('f')

                                if tag_205:
                                    edition = tag_205.get('a')

                                if tag_210:
                                    publisher = tag_210.get('c')
                                    year = tag_210.get('d')

                                if tag_215:
                                    pages = tag_215.get('a')

                                if tag_330:
                                    notes = tag_330.get('a')

                                try:
                                    category_data = Category.objects.get(name=category)
                                except Category.DoesNotExist:
                                    category_data = Category.objects.create(name=category)
                                try:
                                    type_data = Type.objects.get(name='book')
                                except Type.DoesNotExist:
                                    type_data = Type.objects.create(name='book')
                                try:
                                    language_data = Language.objects.get(name=language)
                                except Language.DoesNotExist:
                                    language_data = Language.objects.create(name=language)

                                product_data = {
                                    "title": title,
                                    "notes": notes,
                                    'author': author,
                                    "url_address": library,
                                    "rating": 0,
                                    "category": category_data,
                                    "type": type_data,
                                    "language": language_data,
                                    "publisher": publisher,
                                    "source": source
                                }
                                counter += 1

                                try:
                                    product = Product.objects.get(books__isbn=isbn)
                                    for (key, value) in product_data.items():
                                        setattr(product, key, value)
                                    product.save()
                                except Product.DoesNotExist:
                                    product = Product.objects.create(**product_data)

                                    book_data = {
                                        'isbn': isbn,
                                        'edition': edition,
                                        'year': year,
                                        'pages': pages,
                                        'product': product
                                    }

                                    book = Book.objects.create(**book_data)
                                    copy_number = randint(1, 6)

                                    for x in range(copy_number):
                                        CopyBook.objects.create(
                                            borrowed=False,
                                            book=book
                                        )
                                if counter >= sum:
                                    print('completed')
                                    break


def get_image(isbn):
    domain_url = 'https://obalkyknih.cz/'

    scrapped_url = domain_url + 'view?isbn=' + isbn
    try:
        web_client = urlopen(scrapped_url)
    except:
        print('here')
        return None
    web_html = web_client.read()
    web_client.close()

    page_soup = BeautifulSoup(web_html, "html.parser")
    image = page_soup.find('img', {'class': 'nob'})
    if image:
        return image.get('src')
    else:
        return None
