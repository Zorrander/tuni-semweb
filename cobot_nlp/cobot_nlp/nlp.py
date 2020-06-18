"""

Conversation module. Define how you want to interact with your robot.

"""
import os
import nltk
#import secrets
import nltk.data
from nltk.grammar import Nonterminal
from nltk.parse.generate import generate
from nltk.corpus import stopwords, brown, wordnet
from nltk.tokenize.treebank import TreebankWordDetokenizer
#PATH_GRAMMAR_FILE = os.path.join(os.path.dirname(__file__), "..", "static", 'robot_grammar.cfg')

class NLP():

    #_grammar = nltk.data.load('file:' + PATH_GRAMMAR_FILE)
    _unigram_tagger = nltk.UnigramTagger(brown.tagged_sents(categories='news'))
    _question_tags = ["WDT", "WP$", "WPO", "WPS", "WQL", "WRB"]

    def __init__(self):
        self._input_types=[
            self.match_questions,
            self.match_commands,
            self.match_descrptions,
            self.match_explanations
            ]

    def generate(self, msg_type):
        answers = [production for production in generate(self._grammar, start=Nonterminal(msg_type))]
        return TreebankWordDetokenizer().detokenize(secrets.choice(answers))

    def run(self, sentence):
        tokens = [word for word in nltk.word_tokenize(sentence)]
        tagged_tokens = self._unigram_tagger.tag(tokens)
        print(tagged_tokens)
        for pattern in self._input_types:
            match = pattern(tagged_tokens)
            if match:
                return match(tagged_tokens)
        return False

    def match_questions(self, tagged_tokens):
        first_tag = tagged_tokens[0][1]
        if first_tag in self._question_tags:
            return self.process_questions
        return False

    def match_commands(self, tagged_tokens):
        first_tag = tagged_tokens[0][1]
        if first_tag == "VB" or first_tag == "VBD":
            return self.process_commands
        return False

    def match_descrptions(self, tagged_tokens):
        first_tag = tagged_tokens[0][1]
        if first_tag in ["PPSS", "EX", "CD"]:
            return self.process_descrptions
        return False

    def match_explanations(self, tagged_tokens):
            return False
    '''
    def process_questions(self, tagged_tokens):
        question = tagged_tokens[0][0]
        #object = list(filter(lambda x: x[1] == "NN", tagged_tokens))
        object = tagged_tokens[3][0]
        if question == "Where":
            return robot.find_location(object)
    '''
    def process_commands(self, tagged_tokens):
        # action = tagged_tokens[0][0].encode('ascii','ignore')
        action = tagged_tokens[0][0]
        target = []
        for tgt, tag in tagged_tokens:
            if tgt in ["gripper", "peg"]:
                target.append(tgt)
        '''
        for word, tag in tagged_tokens:
            if tag == "NN":
                target = word.encode('ascii','ignore')
        '''
        return (action, target)

    '''
    def process_descrptions(self, tagged_tokens):
        subject = tagged_tokens[0]
        if subject[0]=="I":
            tagged_verb = tagged_tokens[1][1]
            if tagged_verb=="BEM":
                return robot.delete_agent() if tagged_tokens[2][0] == "leaving" else robot.new_interlocutor(tagged_tokens[2][0])
            elif tagged_tokens[1][0] == "leave":
                return robot.delete_agent()
            elif "CD" in [x[1] for x in tagged_tokens]:
                step = [x[0] for x in tagged_tokens if x[1] == "CD"]
                robot.modify_task_plan(step[0])
            else:
                pass
        elif subject[0]=="There":
             object = tagged_tokens[3][0]
             attribute = tagged_tokens[4][0]
             location = tagged_tokens[6][0]
             return robot.add_item(object, attribute, location)
        elif subject[1]=="CD":
            if "done" in [x[0] for x in tagged_tokens]:
                return StepCompleted(subject[0])
        else:
            pass
    '''

    def process_explanations(self, tagged_tokens):
        pass
