"""Module that reads PDFs"""
import os

from pdfminer.high_level import extract_text


class Reader:
    """
    This class provides all the functionalities that are going to be used to read the different offers from IAESTE Spain
    and will look for the different parameters and save the data related to this offer.
    """

    def __init__(self, folder_path: str):
        """
        Initializes the Reader class
        :param folder_path: Path in the OS to the folder where the PDFs are located
        :raise ValueError: If the path do not exist in the OS
        """
        if not os.path.exists(folder_path):
            raise ValueError("The folder path is not valid")
        self.folder_path = folder_path

    def folder_reader(self) -> dict[str, str]:
        """
        Reads all the files of the folder looking for PDFs to return the text of each PDF.

        This function check all the files that are in the folder that is provided when initiating the class. After finding
        that the folder is not empty looks for all the PDF files there and reads them one by one to give back the extracted
        text from each PDF.
        :return: A dictionary containing the name of the PDF as key and text of the PDF file as value.
        :rtype: dict[str, str]
        :raise FileNotFoundError: If the folder is empty or if there are no PDF files in the folder

        :Example:
        >>> Reader.folder_reader()
        {
            "test.pdf": "This is a pdf test",
            "test2.pdf": "This is a pdf test",
        }
        """
        files: list[str] = os.listdir(self.folder_path)

        assert len(files) > 0, "The folder path is empty"
        if len(files) == 0:
            raise FileNotFoundError("The folder is empty")

        pdf_files_name: list[str] = [file for file in files if file.endswith(".pdf")]
        if len(pdf_files_name) == 0:
            raise FileNotFoundError("There are no PDF files in this folder")

        pdf_with_text_extracted: dict[str, str] = {}

        for pdf in pdf_files_name:
            pdf_text: str = self.extract_text_from_pdf(pdf)
            pdf_with_text_extracted[pdf] = pdf_text

        return pdf_with_text_extracted

    def extract_text_from_pdf(self, pdf_name: str) -> str:
        """
        Extract text from the pdf provided.

        This function reads the PDF using the path provided when starting the class and the name provided in the parameters
        and by using the module of pdfminer.high_level extracts all the text with a good detail and returns the information
        saved in the PDF as a string.

        :param pdf_name: Name of the PDF to read.
        :return: A string containing the text of the PDF
        :rtype: String
        :raise ValueError: If the PDF do not exist in the folder provided by the class

        :Example:
        >>> Reader.extract_text_from_pdf("test.pdf")
        This is a pdf test
        """
        full_path_pdf: str = self.folder_path + pdf_name
        try:
            text = extract_text(full_path_pdf)
        except FileNotFoundError:
            raise FileNotFoundError("The PDF does not exist in the folder")
        else:
            return text
