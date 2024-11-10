import unittest
from src.PDFReader.reader import Reader


class TestReader(unittest.TestCase):

    def test_extract_text_from_pdf(self):
        # Supongamos que tienes un archivo PDF de prueba "test_offer.pdf"
        test_file_path = "test_offer.pdf"

        # Llama al método estático extract_text_from_pdf y verifica el resultado
        result = Reader.extract_text_from_pdf(test_file_path)

        # Verifica que el resultado no sea None y que sea un string
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str)

        # Puedes añadir más aserciones dependiendo de qué texto esperas en el PDF
        # Por ejemplo:
        # self.assertIn("Expected Text", result)


def main():
    unittest.main()


if __name__ == "__main__":
    main()
