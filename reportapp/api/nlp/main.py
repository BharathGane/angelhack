# text = input("enter the text : ")

import nltk, string, numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from api.nlp.grammar_check import grammar_checker
from api.nlp.keyword_checker import keyword_check
class process_text:
	def __init__(self):
		self.topic1 = "Every object in a state of uniform motion tends to remain in that state of motion unless an external force is applied to it."
		self.topic2 = "The rate of change of momentum of an object is directly proportional to the resultant force applied."
		self.topic3 = "For every action there is an equal and opposite reaction."
		self.topic4 = ""
		self.documents = []
		self.topic_names = {"topic1":"Newton's first law of motion","topic2":"Newton's second law of motion","topic3":"Newton's third law of motion"}
		self.dict_topics = {"topic1":self.topic1,"topic2":self.topic2,"topic3":self.topic3}
		self.topics_covered = []
		self.list_of_topics = ["topic1","topic2","topic3"]
		self.list_of_topic_name = ["Newton's first law of motion","Newton's second law of motion","Newton's third law of motion"]
	
	def check_topic(self,text):
		self.documents = [text,self.topic1,self.topic2,self.topic3,self.topic4]
		lemmer = nltk.stem.WordNetLemmatizer()
		
		def LemTokens(tokens):
			return [lemmer.lemmatize(token) for token in tokens]
		remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
		def LemNormalize(text):
			return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))
		TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
		def cos_similarity(textlist):
		    tfidf = TfidfVec.fit_transform(textlist)
		    return (tfidf * tfidf.T).toarray()

		if(max(numpy.delete(cos_similarity(self.documents)[0],0)) > 0.7):
			return self.list_of_topics[numpy.delete(cos_similarity(self.documents)[0],0).argmax(axis = 0)],self.topic_names[self.list_of_topics[numpy.delete(cos_similarity(self.documents)[0],0).argmax(axis = 0)]]
			
		return "No topic covered",None
	
	def return_final(self,text):
		results = {}	
		topic_,topic = self.check_topic(text)
		# results["topics_covered"]
		self.topic_covered(topic)		
		results['topics_covered'] = self.topics_covered
		results['topics_not_covered'] = [x for x in self.list_of_topic_name if x not in self.topics_covered]
		results['all_topics'] = self.list_of_topic_name
		results["topic"] = topic
		text = list(text) 
		text[0] = text[0].upper()
		text = "".join(text)
		results["grammer"] = grammar_checker().grammar_checker(text)
		if topic_ != "No topic covered":
			keyword_match,keyword_match_ratio = keyword_check().frequency_check(text,self.dict_topics[topic_])
			results["is_keyword_match"] = keyword_match
			results["keyword_match_ratio"] = keyword_match_ratio
		else:
			results['topics_covered'] = []
		return results

	def topic_covered(self,topic):
		if topic not in self.topics_covered and topic:
			self.topics_covered.append(topic)


if __name__ == '__main__':
	x = process_text()
	text = ["Every object in a state of uniform motion tends to remain in that state of motion unless an external force is applied to it.","every action has an equal and opposite reaction"]
	for i in text:
		print(x.return_final(i))

