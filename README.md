Readme


which pair swapped places when the jackson 5 became the jacksons?


# trivia_solve
Plan:
Use http://web.airdroid.com/ to mirror screen
Take screenshot and crop
https://www.pyimagesearch.com/2018/01/01/taking-screenshots-with-opencv-and-python/
Run through google vision
https://medium.com/@tobymellor/hq-trivia-using-bots-to-win-money-from-online-game-shows-ce2a1b11828b
Search google for results
--test out watson to understand intents?
Get entities from question:
    get wikipedia pages:
        for each entity
        for each answer
        
    convert to lower case
    lookup \
    
    
    TABLE:
        ENTITY1  ENTITY2
ANSWER1
ANSWER2
ANSWER3

TO DO:
    For the google results:
        analyse which question words are in results
        find the answer which re22turns greatest proportion of question entities in each answer
        
TO DO:
    get q entities
    google result count:
        which of these celebs named his pet after oprah winfrey?
        tom cruise oprah -> tom cruise oprah pet
        50 cent oprah -> 50 cent oprah pet
Fast Track Skills 1/2       
    
TO DO:
    get entities in question
    get new entity from wiki
    Search in the wikipedia for the new entity for each answer

        
        on a standard u.k. plug, what colour is the live wire?
        red live wire -> red live wire standard uk plug
        answer + object +> andswer + object + other entity
        
        work out PERCENTAGE CHANGE
       this doesn't work for Oprah wibfrey
       need to score the verb after the answer entity type (if there is a large imbalance between classes). If it does not occur in search results, the search results are not valid
TO DO:
    if question asks for numbers [amount, least, most]:
        e.g. which of these literary awards offers the least prize money?
        convert to google search:
            answer          "amount of"      last-entity         
            booker prize    amount of           prize money
            
            extract values


TO DO:
    PAIR QUESTIONS:
    IF 1+ ANSWERS CONTAIN '/' and each answer has 2+ words
    search google for answer pair + question entity (e,g -"jermaine randy jackson 5")
    look up answers in google pages.
    for each result:
        calculate the percentage of that pair against the other answer entities for each result:
            e.g. an article on jermaine and randy without mentioning any other jackson's = 100%
        Which answer pair has the distribution of results most skewed towards that pair (without the others)


TO DO:
    get entities in question
    swap with wikipedia to get new question entity:
        Best picture Oscar --> Academy award for best picture
        https://en.wikipedia.org/wiki/Academy_Award_for_Best_Picture
 Get tables from wikipedia for the wikis associated with each possible answers ---> Filter all tables by ones which have the new question entity in header<
    find rows which have the new entity
