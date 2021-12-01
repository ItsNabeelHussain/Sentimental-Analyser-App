"""
Module for reading pdf ,
text sentimental analysis
 and file uplaoding
"""
import re
from io import StringIO

from django.shortcuts import render
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from textblob import TextBlob


class PdfAnalyser:
    """
    Pdf Analyser class for sentimental analysis
    """

    def __init__(self, file):
        self.file = file

    def read_pdf(self):
        """
        for reading pdf and converting it to text
        :return: data list
        """
        output_string = StringIO()
        parser = PDFParser(self.file)
        doc = PDFDocument(parser)
        resource_manager = PDFResourceManager()
        device = TextConverter(resource_manager, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(resource_manager, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
        string = output_string.getvalue()
        pdf_text = str(string).strip()
        formatted_data = re.sub(r'[^a-zA-Z\.]', " ", pdf_text)
        return formatted_data

    def check_polarity(self, paragraph):
        """
        checking polarity
        :param paragraph:
        :return: string
        """

        if paragraph.sentiment.polarity < 0:
            return "Negative Tone"
        elif paragraph.sentiment.polarity == 0:
            return "Neutral Tone"
        else:
            return "Positive Tone"

    def sentiment_analysis(self):
        """
        analysing the tone
        :return: list object
        """
        sentence_data = self.read_pdf()
        correction = TextBlob(sentence_data)
        sentence_list = []
        for item in correction.sentences:
            item = item.replace(".", "")
            if len(item) > 0:
                sentence_list.append((item, self.check_polarity(item)))
        return sentence_list


def file_upload(request):
    """uploading the file
    """
    if request.method == 'POST' and request.FILES['in_file']:
        my_file = request.FILES['in_file']
        pdf_file = PdfAnalyser(my_file)
        pdf_obj = pdf_file.sentiment_analysis()
        return render(request, 'pdf_analyser/file_upload.html', {
            'pdf_obj': pdf_obj
        })
    return render(request, 'pdf_analyser/file_upload.html')
