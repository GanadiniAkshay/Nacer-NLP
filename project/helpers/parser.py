from __future__ import absolute_import
from __future__ import print_function

import os

from rasa_nlu.config import RasaNLUConfig
from rasa_nlu.model import Metadata, Interpreter

from project import db, cache, interpreters, trainer, nlp, d

class NLUParser(object):
    def __init__(self, model, config, builder=None):
        self.model = model
        self.metadata = Metadata.load(self.model)
        self.config = config
        if builder:
            self.interpreter = Interpreter.load(self.metadata, RasaNLUConfig(config),builder)
        else:
            self.interpreter = Interpreter.load(self.metadata, RasaNLUConfig(config))

    def parse(self, message):
        parsed_data = self.interpreter.parse(message)
        if parsed_data['intent']['confidence'] < 0.30:
            intent = 'None'
        else:
            intent = parsed_data['intent']['name']
        entities = []
        for ent in parsed_data['entities']:
            entities.append({"entity":ent['entity'],"value":ent['value'],"start":ent['start'],"end":ent['end']})
        duckling_entities = d.parse(message)
        for ent in duckling_entities:
            if ent['dim'] == 'time':
                if ent['value']['type'] == 'interval':
                    entities.append({"entity":'interval',"start":ent['start'],"end":ent['end'],"value":[{"from":ent['value']['from']['value'], "to":ent['value']['to']['value']}]})
                elif ent['value']['type'] == 'value':
                    entities.append({"entity":"date","start":ent['start'],"end":ent['end'],"value":ent['value']['value']})
        doc = nlp(message.title())
        spacy_entities = []
        for ent in doc.ents:
            if ent.label_ != 'DATE' and ent.label_ != 'ORDINAL' and ent.label_ != 'FAC' and ent.label_ != 'CARDINAL':
                start = message.title().find(ent.text)
                end = start + len(ent.text)
                entities.append({"entity": ent.label_, "start": start, "end": end,"value":ent.text})
        return intent,entities