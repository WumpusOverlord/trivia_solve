
def website_score(answers, website_text):
    answer_scores = {}
    word_scores = {}

    for answer in answers[0:3]:
        answer_scores[answer]=0
        answer = answer.lower()

        if answer in website_text.lower():
            answer_scores[answer] = answer_scores[answer]+1
        seperate_words = answer.split()
        for word in seperate_words:
            word_scores[word]=0
            if word in website_text.lower():
                word_scores[word] = word_scores[word]+1

    return word_scores, answer_scores




def analyse_results(answers, results):
    answer_scores = {}
    word_scores = {}
    metadata = results.metadata
    items = metadata["items"]
    # items = results.metadata.items
    for answer in answers[0:3]:
        answer_scores[answer]=0
        answer = answer.lower()
        for item in items:
            snippet = item['snippet']
            if answer in snippet.lower():
                answer_scores[answer] = answer_scores[answer]+1
            seperate_words = answer.split()
            for word in seperate_words:
                word_scores[word]=0
                for item in items:
                    snippet = item['snippet']
                if word in snippet:
                    word_scores[word] = word_scores[word]+1



    print(answer_scores)
    return results, word_scores, answer_scores

