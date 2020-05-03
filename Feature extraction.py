from py2neo import Graph, NodeMatcher
from py2neo import Node
from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, config
from py2neo.ogm import GraphObject, Property
from neo4j import GraphDatabase
from py2neo.data import Node, Relationship
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.chunk import conlltags2tree, tree2conlltags
from pprint import pprint
from nltk.chunk import ne_chunk
from nltk.tree import *
from sklearn import tree
from nltk import RegexpParser
import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm

graph = Graph("bolt://localhost:11002", auth=("neo4j", "password"))
tx = graph.begin()

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
            #print( dict(matched_feat_node)['feature'])
            class matches(Relationship): pass
            r = matches(input_node, matched_feat_node)
            #print(r)
            break
    return dict(matched_feat_node)['feature']



#graph.create(x)

print(ext_feature(tokenize("send me the song abcd")))
# a = Node("Person", name="Alice")
# b = Node("Person", name="Bob")
# ab = Relationship(a, "KNOWS", b)

# #graph.create(a)
# graph.create(b)
# graph.create(ab)
