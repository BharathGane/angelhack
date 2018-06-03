from api.nlp.keyword_classifier import keyword_classify
import nltk
from nltk.corpus import wordnet

class keyword_check():
	def comapre_keywords(self,text1,text2):
		r = keyword_classify()
		r.extract_keywords_from_text(text1)
		keywords1 = r.get_ranked_phrases_with_scores()
		r.extract_keywords_from_text(text2)
		keywords2 = r.get_ranked_phrases_with_scores()
		return keywords1,keywords2

	# def add_synonyms(self,word):
	# 	synonyms = []
	# 	for syn in wordnet.synsets(word):
	# 		synonyms.append(word)
	# 		for l in syn.lemmas():
	# 			if l.name() not in synonyms:
	# 				synonyms.append(l.name())
	# 	print(synonyms)
	# 	return synonyms

	def frequency_check(self,text1,text2):
		keyword_match_count = 0
		final_list = []
		freq1,freq2 = self.comapre_keywords(text1,text2)
		# for x in freq1.keys():
			# final_list.append(self.add_synonyms(x))
		# print(freq2.keys())
		# print(freq1.keys())
		# print(final_list)
		for i in freq2.keys():
			if i in freq1.keys():
				keyword_match_count += 1
		# print(keyword_match_count/len(freq2.keys())) 
		return True if keyword_match_count/len(freq2.keys()) > 0.8 else False,keyword_match_count/len(freq2.keys())

	def frequency_check_list(self,text,list1):
		final_freq = []
		for i in list1:
			final_freq.append(self.frequency_check(text,i))
		return final_freq

if __name__ == '__main__':
	test_text = "every action has an equal and opposite reaction"
	definition_text = ["For every action there is an equal and opposite reaction"]
	x = keyword_check()
	print(keyword_check().frequency_check_list(test_text,definition_text))

