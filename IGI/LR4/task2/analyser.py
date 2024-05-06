import re


class Analyser:
	def __init__(self, text: str = ""):
		self.__text = text

	@property
	def text(self):
		return self.__text


	@text.setter
	def text(self, text: str):
		self.__text = text


	def sentences_count(self):
		sentences = re.findall("[A-Z0-9][^?!.]*?[?.!]", self.__text)
		return len(sentences)
	

	def interrogative_sentences_count(self):
		interrogative_sentences = re.findall("[A-Z0-9][^?!.]*?[?]+", self.__text)
		return len(interrogative_sentences)
	

	def exclamation_sentences_count(self):
		exclamation_sentences = re.findall("[A-Z0-9][^?!.]*?[!]+", self.__text)
		return len(exclamation_sentences)
	

	def narrative_sentences_count(self):
		narrative_sentences = re.findall("[A-Z0-9][^?!.]*?[.]+", self.__text)
		return len(narrative_sentences)	


	def word_count(self):
		return len(self.get_all_words())


	def average_sentence_length(self):
		sentences = re.findall("[A-Z0-9][^?!.]*?[?.!]", self.__text)
		sum_lengths = sum(len(sentence) for sentence in sentences)
		return sum_lengths / len(sentences)
	

	def average_word_length(self):
		words = self.get_all_words()
		sum_lengths = sum(len(word) for word in words)
		return sum_lengths / len(words)
	

	def smileys_count(self):
		smileys = re.findall(r"(:|;)(\-*?)((\(+)|(\)+)|(\[+)|(\]+))", self.__text)
		return len(smileys)
	

	def get_all_words(self):
		words = [word for word in re.findall(r"\b\w+\b", self.__text)]
		return words
	

	def get_all_words_start_lowercase(self):
		return list(filter(lambda word: word[0].islower(), self.get_all_words()))
	

	def max_word_by_length(self):
		words = self.get_all_words()
		word = max(words, key=len)
		return word, words.index(word)
	

	def get_odd_length_words(self):
		words = self.get_all_words()
		return list(filter(lambda word: len(word) % 2 == 1, words))
	

	def get_all_punctuation(self):
		text = re.sub(r"(:|;)(-*?)((\(+)|(\)+)|(\[+)|(\]+))", "", self.__text)
		puctuations = re.findall(r"([^\w\s])+", text)
		return {puctuation for puctuation in puctuations}
	

	def get_all_mac_addresses(self):
		mac_addresses = re.findall(r"(?:[0-9a-fA-F]{2}[:-]){5}[0-9a-fA-F]{2}", self.__text)
		return [mac for mac in mac_addresses]