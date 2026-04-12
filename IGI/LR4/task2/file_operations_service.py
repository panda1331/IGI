"""
Task 2. Module for file service operations.
"""
import re
from collections import Counter
from zipfile import ZipFile


class FileService:
    """Main service for text analysis and reporting."""
    def __init__(self):
        """Initialize file paths, read text, count sentences."""
        self.__input_filename = "task2/input.txt"
        self.__output_filename = "task2/output.txt"
        self.__output_zip_filename = "task2/output-zip-file.zip"
        self.__text = self._read_file()
        self.__sentences_counter = self.count_sentences()

    def __str__(self):
        """Return formatted report as string."""
        return str("General tasks:\n"
                   f"1) Narrative(.) sentences: {self.count_narrative_sentences()}\n"
                   f"2) Interrogative(?) sentences: {self.count_interrogative_sentences()}\n"
                   f"3) Exclamative(!) sentences: {self.count_exclamative_sentences()}\n"
                   f"4) Total sentences count: {self.count_sentences()}\n"
                   f"5) Average sentences length(only symbols in words counted): {self.calculate_average_sentences_length():.4f}\n"
                   f"6) Average words length: {self.calculate_average_words_length():.4f}\n"
                   f"7) Smileys count: {self.count_smileys()}\n\n"
                   "Individual tasks:\n"
                   f"1) Phone numbers 9 digits, started with 29 (29*******): {self.find_phone_numbers()}\n"
                   f"2) Amount of words where second letter is consonant, third - vowel: {self.get_specified_words()}\n"
                   f"3) Amount of words that are bounded with spaces: {self.count_words_bounded_by_spaces()}\n"
                   f"4) Determine how many times each letter appears: \n\t{self.format_letters_occurrences()}\n"
                   f"5) Get all phrases separated by commas in alphabet order: \n\t{", ".join(self.get_alphabetizes_phrases_separated_by_commas())}")

    def _read_file(self):
        """Read input file and return content."""
        with open(self.__input_filename, 'r') as file:
            return file.read()

    def save_info_to_file(self):
        """Save report to output file."""
        with open(self.__output_filename, 'w') as file:
            file.write(self.__str__())

    def archive_file(self):
        """Archive output file into ZIP."""
        with ZipFile(self.__output_zip_filename, 'w') as zip_file:
            zip_file.write(self.__output_filename, arcname="results.txt")

    def show_archived_info(self):
        """Display ZIP archive contents info."""
        with ZipFile(self.__output_zip_filename, 'r') as zip_file:
            for info in zip_file.infolist():
                print(f"File name: {info.filename}, Date: {info.date_time}, Size: {info.file_size} bytes")

    def count_sentences(self):
        """Total sentences = narrative + interrogative + exclamative."""
        return self.count_narrative_sentences() + self.count_interrogative_sentences() + self.count_exclamative_sentences()

    def count_narrative_sentences(self):
        """Count sentences ending with dot (not part of number)."""
        counter = len(re.findall(r'\.(?![0-9])', self.__text))
        return counter

    def count_interrogative_sentences(self):
        """Count sentences ending with question mark."""
        counter = len(re.findall(r'\?', self.__text))
        return counter

    def count_exclamative_sentences(self):
        """Count sentences ending with exclamation mark."""
        counter = len(re.findall(r'!', self.__text))
        return counter

    def calculate_average_sentences_length(self):
        """Average letters per sentence."""
        letters = len(re.findall(r"[a-zA-Z]", self.__text))
        return letters / self.__sentences_counter

    def calculate_average_words_length(self):
        """Average letters per word."""
        letters = len(re.findall(r"[a-zA-Z]", self.__text))
        words = len(re.findall(r"\b[^0-9_ ][a-zA-Z']*\b", self.__text))
        return letters / words

    def count_smileys(self):
        """Count smileys: ; or :, optional -, repeated same bracket at end."""
        counter = len(re.findall(r"[;:]-*([\[\]()])\1*(?=[,.\s]|$)", self.__text))
        return counter

    def find_phone_numbers(self):
        """Count 9-digit numbers starting with 29."""
        counter = len(re.findall(r"\b29\d{7}\b", self.__text))
        return counter

    def get_specified_words(self):
        """Count words where 2nd letter consonant, 3rd vowel."""
        consonants = "QWRTPSDFGHJKLZXCVBNMqwrtpsdfghjklzxcvbnm"
        vowels = "EYUIOAeyuioa"
        counter = len(re.findall(rf"\b[a-zA-Z][{consonants}][{vowels}]\w*\b", self.__text))
        return counter

    def count_words_bounded_by_spaces(self):
        """Count words separated by spaces (word boundaries)."""
        counter = len(re.findall(r"\b[\w']+\b", self.__text))
        return counter

    def calculate_letters_occurrences(self):
        """Return Counter of letter frequencies."""
        letters_appearances = Counter(re.findall(r"[a-zA-Z]", self.__text))
        return letters_appearances

    def get_alphabetizes_phrases_separated_by_commas(self):
        """Extract phrases after 'Phrases:', split by comma, sort alphabetically."""
        line = re.findall(r"(?<=Phrases: ).+(?=.)", self.__text)
        phrases = re.split(r", ", line[0])
        return sorted(phrases)

    def format_letters_occurrences(self):
        """Format letter frequencies as readable string."""
        result = ""
        for key, value in sorted(self.calculate_letters_occurrences().items()):
            result += f"{key}: {value}, "
        return result