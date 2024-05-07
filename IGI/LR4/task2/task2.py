from .analyser import Analyser
import zipfile


def task2():
	try:
		analyser = Analyser()
		with open("task2/text.txt") as file:
			analyser.text = file.read()
		with open("task2/result.txt", 'w') as file:
			print("Sentences count:", analyser.sentences_count(), file=file)
			print("Interrogative sentences count:", analyser.interrogative_sentences_count(), file=file)
			print("Exclamation sentences count:", analyser.exclamation_sentences_count(), file=file)
			print("Narrative sentences count:", analyser.narrative_sentences_count(), file=file)
			print("Average sentence length:", analyser.average_sentence_length(), file=file)
			print("Average word length:", analyser.average_word_length(), file=file)
			print("Smileys count:", analyser.smileys_count(), file=file)
			print("Word count:", analyser.word_count(), file=file)
			max_word, index = analyser.max_word_by_length()
			print("Maximum word length:", max_word, file=file)
			print("Index maximum word length:", index, file=file)
			print("All the words that start with a lowercase letter:", analyser.get_all_words_start_lowercase(), file=file)
			print("All punctuation:", analyser.get_all_punctuation(), file=file)
			print("Odd length words:", analyser.get_odd_length_words(), file=file)
			print("All mac addresses:", analyser.get_all_mac_addresses(), file=file)

		with open("task2/result.txt") as file:
			print(file.read())

		with zipfile.ZipFile("task2/zipfile.zip", 'w') as zip:
			zip.write("task2/result.txt")
	except:
		print("Something went wrong. Try again later.")