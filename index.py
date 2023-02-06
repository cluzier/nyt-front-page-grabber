import requests
import datetime
import PyPDF2
from PIL import Image

url = "https://static01.nyt.com/images/{}/{}/{}/nytfrontpage/scan.pdf".format(
str(datetime.datetime.now().year),
str(datetime.datetime.now().month).zfill(2),
str(datetime.datetime.now().day).zfill(2),
)

response = requests.get(url)
open("nytimes-front-page.pdf", "wb").write(response.content)

pdf_file = open("nytimes-front-page.pdf", "rb")
pdf_reader = PyPDF2.PdfFileReader(pdf_file)

for page_num in range(len(pdf_reader.pages)):
    page = pdf_reader.pages[page_num]

xObject = page['/Resources']['/XObject'].get_object()

for obj in xObject:
    if xObject[obj]['/Subtype'] == '/Image':
        size = (xObject[obj]['/Width'], xObject[obj]['/Height'])
        data = xObject[obj].getData()
        if xObject[obj]['/ColorSpace'] == '/DeviceRGB':
            mode = "RGB"
        else:
            mode = "P"

        if '/Filter' in xObject[obj]:
            if xObject[obj]['/Filter'] == '/FlateDecode':
                img = Image.frombytes(mode, size, data)
                img.save("nytimes-front-page-{}.png".format(page_num), "PNG")
