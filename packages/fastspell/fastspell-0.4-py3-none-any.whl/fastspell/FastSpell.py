import os
import yaml
from sacremoses import MosesTokenizer
import fasttext
import hunspell
import logging
import urllib.request
import pathlib



#Removes punctuation and propernouns to avoid 
#Hunspell error rates too high
#and focus only on "normal" words.
def remove_non_alpha_and_propernouns(tokens):
    newtokens = []
    isfirsttoken=True
    for token in tokens:
        if token.upper() != token.lower() and (isfirsttoken or token[0]!=token[0].upper()):    
            newtokens.append(token.lower())
        isfirsttoken=False    
    return newtokens        

class FastSpell:
    
    threshold = 0.25 #Hunspell max error rate allowed in a sentence
    prefix = "__label__" #FastText returns langs labeled as __label__LANGCODE
    
    #load config
    cur_path = os.path.dirname(__file__)
    #similar languages
    similar_yaml_file = open(cur_path+"/config/similar.yaml")
    similar_langs = yaml.safe_load(similar_yaml_file)["similar"]
    #special tokenizers
    special_tokenizers_file = open(cur_path+"/config/tokenizers.yaml")
    special_tokenizers = yaml.safe_load(special_tokenizers_file)["tokenizers"]
    #hunspell 
    hunspell_codes_file = open(cur_path+"/config/hunspell.yaml")
    hunspell_config = yaml.safe_load(hunspell_codes_file) 
    hunspell_codes = hunspell_config["hunspell_codes"]
    dictpath = hunspell_config["dictpath"]

 
    hunspell_objs = {}
    tokenizers={}

    def __init__(self, lang, mode="cons"):
        assert (mode=="cons" or mode=="aggr"), "Unknown mode. Use 'aggr' for aggressive or 'cons' for conservative"

        self.lang = lang
        self.mode = mode
        
        ft_model_path = os.path.join(self.cur_path, "lid.176.bin") #The model should be in the same directory

        try:
            self.model = fasttext.load_model(ft_model_path)  #FastText model
        except ValueError as ex:
            logging.warning("Downloading FastText model...")
            urllib.request.urlretrieve("https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin", ft_model_path)
            self.model = fasttext.load_model(ft_model_path) 

        self.similar = self.similar_langs.get(lang)

        #If there are languages that can be mistaken 
        #with the target language: prepare an array of Hunspell spellcheckers
        #for all the similar languages
        if self.similar != None:
            for l in self.similar:
                #load dicts
                dict = self.dictpath+self.hunspell_codes.get(l)
                hunspell_obj = hunspell.HunSpell(dict+'.dic', dict+'.aff') 
                self.hunspell_objs[l] = hunspell_obj
                #load tokenizers
                if l in self.special_tokenizers.keys():
                    self.tokenizers[l] = eval(self.special_tokenizers.get(l))
                else:
                    self.tokenizers[l] = MosesTokenizer(l)    
                


    def getlang(self, sent):
        sent=sent.strip()
        prediction = self.model.predict(sent, k=1)[0][0][len(self.prefix):]
        #classic norwegian ñapa
        if prediction == "no":
            prediction = "nb"
        #TODO: Confidence score?

        if self.similar == None or prediction not in self.similar:
        #Non mistakeable language: just return FastText prediction
            return(prediction)
        else:
        #The target language is mistakeable
            spellchecked = {}
            for l in self.hunspell_objs:
                #Get spellchecking for all the mistakeable languages
                logging.debug(l)
                dec_sent = sent.encode(encoding='UTF-8',errors='strict').decode('UTF-8') #Not 100% sure about this...
                raw_toks = self.tokenizers.get(l).tokenize(dec_sent, escape=False)
                toks = remove_non_alpha_and_propernouns(raw_toks)
                try:
                    correct_list = list(map(self.hunspell_objs.get(l).spell, toks))
                except UnicodeEncodeError: #...because it sometimes fails here for certain characters
                    correct_list = []
                corrects = sum(correct_list*1)
                logging.debug("Tokens: " +str(toks))
                logging.debug("Corrects: " + str(correct_list))
                logging.debug("Total: " + str(len(toks)))
                if corrects > 0:
                    error_rate = 1-(corrects/len(toks))
                else:
                    error_rate = 1
                logging.debug("error_rate: " + str(error_rate))
                if error_rate < self.threshold: #we don't keep it if the error rate is above the threshold
                    spellchecked[l] =  error_rate
                logging.debug("----------------")

            if len(spellchecked) > 0:
                #at least one of the spellchecks was below the threshold            
                #get best values and keys
                best_value = min(spellchecked.values())
                best_keys = [k for k, v in spellchecked.items() if v == best_value]
                if len(best_keys)==1:
                    #Only one language scoring the best
                    return(best_keys[0])
                else:
                    #It's a tie!
                    if self.mode == "aggr":
                        #Aggressive approach: if the targetted language is among the best scoring, take it
                        if self.lang in best_keys:
                            return(self.lang)
                        elif prediction in best_keys:
                            #the targetted language is not in the best ones, and the prediction?
                            return(prediction)
                        else:
                            #Just take one
                            return(best_keys[0])
                    if self.mode == "cons":
                        #Conservative: just keep it as unknown
                        return("unk")
            else:
                #Nothing in the spellchecking list
                if self.mode == "aggr":
                    return(prediction)
                else:
                    return("unk")


