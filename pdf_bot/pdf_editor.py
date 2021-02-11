from PyPDF2 import PdfFileMerger
from PIL import Image
from time import time
from requests import get
from json import loads
from fpdf import FPDF
from urllib.request import urlretrieve
from PyPDF2 import PdfFileMerger
from PIL import ImageFile
from os import remove, mkdir, path, listdir


ImageFile.LOAD_TRUNCATED_IMAGES = True


class img2pdf_conv():
    def __init__(self, filename, output_name, size=tuple):
        self.filename = filename
        self.output_name = output_name
        self.size = size

    def main(self):
        gH = int(self.size['height']) * 2.54 / 96 * 10
        gW = int(self.size['width'])* 2.54 / 96 * 10
        pdf = FPDF(format=[gW, gH])
        pdf.add_page()
        # if gH >= h:
        #     gH = gH - (gH - h)
        #     gW = gW - (gH - h)

        # if gW >= w:
        #     gW = gW + (gW - w)

        #     gH = gH + (gW - w)
        
        # if gH < h:
        #     gH = gH - (gH - h)
        #     gW = gW - (gH - h)

        # if gW < w:
        #     gW = gW - (gW - w)
        #     gH = gH - (gW - w)

        # pdf.image(self.filename, (w - gW)/2, (h - gH)/2, gW, gH)
        pdf.image(self.filename, 0, 0, gW, gH)
        pdf.output(self.output_name, "F")

    def alias(self):
        img = Image.open(self.filename)
        bg = Image.new('RGB', img.size, (255,255,255))
        bg.paste(img, box=None, mask=None)
        bg.save(self.output_name, quality=95)



def pdfs_merger(data, output_name, chat_id):
    merger = PdfFileMerger()

    for pdf in data:
        merger.append(f'{chat_id}\\{pdf}')

    merger.write(output_name)
    merger.close()

def fileN(chat_id):
    i = 0
    while path.exists(f"{str(chat_id)}\\image{i}.jpg"):
        i += 1
    return i



class download_photo: 
    def __init__(self, TOKEN, file_id, folder_name, imageName, chat_id):
        self.TOKEN = TOKEN
        self.file_id = file_id
        self.folder_name = folder_name
        self.imageName = imageName
        self.chat_id = chat_id

    def get_best_rez(self):
        ls = list()
        data = []
        for i in self.file_id:
            ls.append(int(i.file_size))
            data.append(i)
        biggest_size = 1
        n = 1
        for i, num in enumerate(ls):
            if max(ls) == i:
                n = num
                break
        try:
            return [self.file_id[n].file_id, n]
        except IndexError:
            try:
                return [self.file_id[1].file_id, 1]
            except IndexError:
                return [self.file_id[0].file_id, 0]



    def get_file_path(self, id):
        url = 'https://api.telegram.org/bot%s/%s' % (self.TOKEN, 'getFile')
        response = get(url, params={"chat_id": self.chat_id, "file_id": id})
        response = loads(response.content.decode('utf-8'))['result']['file_path']
        return response

    def main(self):
        d = download_photo(self.TOKEN, self.file_id, self.folder_name, self.imageName, self.chat_id)
        best_rez = d.get_best_rez()[0]
        file_path = d.get_file_path(best_rez)
        image_url = "https://api.telegram.org/file/bot{0}/{1}".format(self.TOKEN, file_path)
        image = urlretrieve(image_url, "{0}/{1}".format(self.folder_name, self.imageName))
        return f'{self.folder_name}\\{self.imageName}'



