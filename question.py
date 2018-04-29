import inflect
p = inflect.engine()

class Answer:
    text = ""
    googleSearchTerm = ""
    lower = ""
    search_scores = {}
    seperate_words = []
    word_scores = {}
    answer_with_entity = ""
    search_terms = []

    def __init__(self, answer_text):
        self.text = answer_text
        self.seperate_words = answer_text.lower().split()
        self.word_scores = {}
        self.search_terms = []

    def set_answer_with_entity(self, answer_with_entity):
        self.answer_with_entity = answer_with_entity

    def set_word_scores(self, search_term, items):
        self.word_scores[search_term] = {}
        for word in self.seperate_words:
                word_score =0
                for item in items:
                    snippet = item['snippet']
                    if word in snippet:
                        word_score = word_score+1
                self.word_scores[search_term][word] = word_score
            # /?/self.word_scores[word]= {search_term: word_score}


# TO-DO: class Entity:


class Question:
    """A simple example class"""
    text = ""
    originalEntities = []
    convertedEntities = {}
    answers = []
    google_results = {}
    keywords = ["what", "which", "who"]
    entity_occurences = {}
    keyword_occurences = {}
    answer_entity_type = ""
    answer_entity_type_singular = ""

    def __init__(self, question_text):
            self.text = question_text


    def convert_entity_to_singular(self):
        answer_en_sing = p.singular_noun(self.answer_entity_type, count=None)
        if answer_en_sing != False:
            answer_entity = answer_en_sing


    def get_answers_entity_type(self):

        try:
            self.entity_occurences = self.get_keywords_occurences(self.originalEntities)
            self.keyword_occurences = self.get_keywords_occurences(self.keywords)
            keyword_occurences = list(self.keyword_occurences.values())
            keyword_occurences = [j for i in keyword_occurences for j in i]
            if len(keyword_occurences) >= 0:
                question_word_occurence = keyword_occurences[0]
                self.answer_entity_type = self.get_closest_entity_to_keywords(self.entity_occurences, question_word_occurence)

                # self.answer_entity_type_singular = self.originalEntities[]
                indices = [i for i, x in enumerate(self.originalEntities) if x == self.answer_entity_type]
                self.answer_entity_type_singular = self.convertedEntities[indices[0]].lower()
        except:
            pass

            # print('x')
            # self.answer_entity_type_singular =


    def get_closest_entity_to_keywords(self, e_occurences, question_word_occurence):
        min_index = -1
        min_difference = 9999
        question_entity = ""
        for entity, entity_occerence in e_occurences.items():
            try:
                difference = entity_occerence[0] - question_word_occurence
                if difference > 0:
                    if difference < min_difference:
                        min_difference = difference
                        min_index = entity_occerence
                        question_entity = entity
            except:
                pass
        return question_entity

    # def get_key_word_locations(self):



    def get_keywords_occurences(self, keywords):
        keyword_occurences = {}
        for keyword in keywords:
            keyword_lower = keyword.lower()
            entity_index = self.allindices(self.text.lower(), keyword_lower, listindex=[], offset=0)
            keyword_occurences[keyword_lower] = entity_index
        return keyword_occurences

    def set_answers(self, answer_texts):
        answers = []
        for text in answer_texts:
            answers.append(Answer(text))
        self.answers = answers

    def allindices(self, string, sub, listindex=[], offset=0):
        i = string.find(sub, offset)
        while i >= 0:
            listindex.append(i)
            i = string.find(sub, i + 1)
        return listindex
