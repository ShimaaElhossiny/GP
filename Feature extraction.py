import nltk
import en_core_web_sm
import os
from py2neo import Graph, NodeMatcher
from py2neo import Node
from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, config
from py2neo.ogm import GraphObject, Property
from neo4j import GraphDatabase
from py2neo.data import Node, Relationship
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import conlltags2tree, tree2conlltags
from nltk.chunk import ne_chunk
from nltk.tree import *
from sklearn import tree
from nltk import RegexpParser
from collections import Counter
from wit import Wit

graph = Graph("bolt://localhost:11002", auth=("neo4j", "password"))
tx = graph.begin()

feature_ = []
params_ = []

def wit_ne(messsage):
    client = Wit('U5E2SCXLYY6ZFKQX3EBTLNPEAWOQA36B')
    resp = client.message(messsage)
    try: #music
        try:
            param = resp['entities']['notable_person'][0]['value']['name']
            params_.append(param)
            
        except:
            feature = resp['entities']['intent'][0]['value']
            params = resp['entities']['artist_name'][0]['entities']['notable_person'][0]['value']['name']
            feature_.append(feature)
            params_.append(params)
            
    except KeyError:
        try:    #movies
            feature = resp['entities']['intent'][0]['value']
            params = resp['entities']['movie_name'][0]['value']
            feature_.append(feature)
            params_.append(params)
            
        except KeyError:    #weather
            feature = resp['entities']['intent'][0]['value']
            param1 = resp['entities']['location'][0]['resolved']['values'][0]['coords']['lat']
            param2 = resp['entities']['location'][0]['resolved']['values'][0]['coords']['long']
            feature_.append(feature)   
            params_.append(param1)
            params_.append(param2)
            
    except:
                feature = resp['entities']['intent'][0]['value']
                params = resp['entities']['track_name'][0]['value']
                feature_.append(feature)
                params_.append(params)
               
    feat_par_dict = {
                     'feature': feature_,
                     'params': params_
                    }
    return feat_par_dict

def tokenize(msg):
    noun_list = []
    verb_list = []
    msg_lower = msg.lower()
    tokens = nltk.word_tokenize(msg_lower)
    
    tag = nltk.pos_tag(tokens)
    print(tag)
   
    # pattern = """ 
    # feature:{<DT><NN>?}
    #     {<TO><VB>?}
    # """

    # cp = nltk.RegexpParser(pattern)
    # cs = cp.parse(tag)

    
    for i in (tag):
        for j in i:
            if j == 'NN':
                noun_list.append(i[0])

                print(i[0])
            if j == 'VB':
                verb_list.append(i[0])
                print(i[0]) 
    
    print(noun_list)
    print(verb_list)
    noun_list.extend(verb_list)
    NV = noun_list
    
    print(NV)    
    return NV

# album listen song ep music track symphony

def ext_feature(NV):
    matcher = NodeMatcher(graph)
    name = ""   #the first entity from the user input
    for i in range(0, len(NV)):
        name = NV[i]
        input_node = Node(name)
        matched_feat_node = matcher.match(name).first() 
        if matched_feat_node is not None:
            class matches(Relationship): pass
            r = matches(input_node, matched_feat_node)
            break
    return dict(matched_feat_node)['feature']

def movies_keywords():
    a = Node("cenima", feature = "movies")
    b = Node("watch", feature = "movies")
    c = Node("movie", feature = "movies")
    d = Node("theatre", feature = "movies")

    graph.create(a)
    graph.create(b)
    graph.create(c)
    graph.create(d)

def param_plot(dict):
    for i in range(len(dict['params'])):
        #print(dict['params'][i])
        a = Node('')


param_plot(wit_ne("where can i watch parasite"))
# client = Wit('U5E2SCXLYY6ZFKQX3EBTLNPEAWOQA36B')
# resp = client.message("where to lispten to bach?")

# print(resp)
