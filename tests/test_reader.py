"""
Test module used to know that everything related to PDF reader module works properly
"""
import unittest
from src.PDFReader.reader import Reader
import os


class TestReader(unittest.TestCase):
    """Class where all the test are run"""

    def setUp(self) -> None:
        """Set up a valid path for tests and an invalid path"""
        self.valid_path = "/Users/claud/Desktop/Projects/IAESTE/internship_scorer/PDFTest"
        self.invalid_path = "/invalid/path"
        self.reader = Reader(self.valid_path)

    def test_initialization_valid_path(self) -> None:
        """Test initialization with a valid path"""
        self.assertEqual(self.reader.folder_path, self.valid_path)

    def test_initialization_invalid_path(self) -> None:
        """Test initialization with an invalid path"""
        with self.assertRaises(ValueError):
            Reader(self.invalid_path)

    def test_folder_reader_empty_folder(self) -> None:
        """Test folder_reader when the folder is empty"""
        empty_folder: str = "/Users/claud/Desktop/Projects/IAESTE/internship_scorer/PDFTestEmpty"

        reader = Reader(empty_folder)
        with self.assertRaises(FileNotFoundError):
            reader.folder_reader()

    def test_folder_reader_no_pdfs(self) -> None:
        """Test folder_reader when no PDF files are present in the folder"""
        no_pdf_folder = "/Users/claud/Desktop/Projects/IAESTE/internship_scorer/NoPDFTest"
        os.makedirs(no_pdf_folder, exist_ok=True)
        with open(os.path.join(no_pdf_folder, "test.txt"), "w") as f:
            f.write("This is a test file without PDF extension.")

        reader = Reader(no_pdf_folder)
        with self.assertRaises(FileNotFoundError):
            reader.folder_reader()

        os.remove(os.path.join(no_pdf_folder, "test.txt"))
        os.rmdir(no_pdf_folder)

    def test_folder_reader_valid_pdfs(self) -> None:
        """Test folder_reader with valid PDFs in the folder"""
        pdfs_text = self.reader.folder_reader()
        self.assertIsInstance(pdfs_text, dict)
        self.assertTrue(all(pdf.endswith(".pdf") for pdf in pdfs_text.keys()))
        self.assertTrue(all(isinstance(text, str) for text in pdfs_text.values()))

    def test_extract_text_nonexistent_pdf(self) -> None:
        """Test extract_text_from_pdf with a non-existent PDF file"""
        with self.assertRaises(FileNotFoundError):
            self.reader.extract_text_from_pdf("nonexistent.pdf")

    def test_extract_text_empty_pdf(self) -> None:
        """Test extract_text_from_pdf with an empty PDF file"""
        result = self.reader.extract_text_from_pdf("empty.pdf")
        self.assertEqual(result, "")

    def test_folder_reader_contains_text(self) -> None:
        """Test that all PDFs read contain text"""
        pdfs_text = self.reader.folder_reader()
        for pdf, text in pdfs_text.items():
            self.assertIsInstance(pdf, str)
            self.assertIsInstance(text, str)

    def test_folder_reader_pdf_file_names(self) -> None:
        """Test that PDF file names are correctly retrieved from folder"""
        pdfs_text = self.reader.folder_reader()
        pdf_files = [file for file in os.listdir(self.valid_path) if file.endswith(".pdf")]
        self.assertEqual(set(pdf_files), set(pdfs_text.keys()))

    def test_extract_text_exist(self) -> None:
        """This method check that having in account a correct PDF the return statement is not empty"""
        test_file_path: str = "test.pdf"
        reader: Reader = Reader(self.valid_path)

        result: str = reader.extract_text_from_pdf(test_file_path)

        self.assertIsNotNone(result)

    def test_extract_text_is_instance(self) -> None:
        """Method checks that the return from the extracting text method is in fact a String"""

        test_file_path: str = "test.pdf"
        reader: Reader = Reader(self.valid_path)

        result: str = reader.extract_text_from_pdf(test_file_path)

        self.assertIsInstance(result, str)

    def test_extract_text_correct_return(self) -> None:
        """This method checks that the return asked to return is the correct one"""
        test_file_path: str = "test.pdf"
        expected_result: str = "This is a test pdf"
        reader: Reader = Reader(self.valid_path)

        result: str = reader.extract_text_from_pdf(test_file_path)
        print(result)
        self.assertEqual(expected_result, result)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
