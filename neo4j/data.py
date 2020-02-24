#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from py2neo import Node, Graph, Relationship, NodeMatcher, RelationshipMatcher

def get_drug(symptomname):  # 由疾病名称查询对症药物和药品(task1 uses only)
    graph = Graph("bolt://localhost:7687", username="neo4j", password="123456")
    # nodematcher=NodeMatcher(graph)
    # relamatcher=RelationshipMatcher(graph)
    # node=nodematcher.match('symptom',name=symptomname).first()#找到了该疾病
    # relamatcher.match((node,),r_type='适用于')

    str = 'MATCH a=(symptom{name:\'' + symptomname + '\'})-[:canuse]->(drug) return drug.name'
    # print(str)
    result_list = list(graph.run(str).data())
    result_drug=[]
    products={}

    for oneresult in result_list:
        result_drug.append(oneresult['drug.name'])
        products[oneresult['drug.name']]=get_drug_product(oneresult['drug.name'])
    # print(products)
    return result_drug,products

def get_drug_product(drugname):  #由药物名查询药品
    graph=Graph("bolt://localhost:7687", username="neo4j", password="123456")
    str = 'MATCH a=(drug{name:\'' + drugname + '\'})-[:haveproduct]->(product) return product.name,product.size'
    # print(str)
    result_list = list(graph.run(str).data())
    result_product=[]
    for results in result_list:
        result_product.append('药品名称：'+results['product.name']+' 制剂规格：'+results['product.size'])
    return result_product

def get_drug_from_symptom(symptomname): #由疾病名称查询对症药物
    graph = Graph("bolt://localhost:7687", username="neo4j", password="123456")
    str = 'MATCH a=(symptom{name:\'' + symptomname + '\'})-[:canuse]->(drug) return drug.name'
    result_list = list(graph.run(str).data())
    result_drug = []
    for oneresult in result_list:
        result_drug.append(oneresult['drug.name'])
    return result_drug

def get_drug_from_product(productname): #由药品查药物
    graph = Graph("bolt://localhost:7687", username="neo4j", password="123456")
    str = 'MATCH a=(product{name:\'' + productname + '\'})-[:productfor]->(drug) return drug.name'
    result_list = list(graph.run(str).data())
    result_drug = []
    for oneresult in result_list:
        result_drug.append(oneresult['drug.name'])
    return result_drug

def get_usage_from_product(productname): #由药品查用法
    graph = Graph("bolt://localhost:7687", username="neo4j", password="123456")
    strr = 'MATCH a=(product{name:\'' + productname + '\'})-[:haveuse]->(use) return use.frequency,use.useage,use.consumption,use.notes'
    result_list = list(graph.run(strr).data())
    for index in result_list:
        result_usage={}
        result_usage['frequency']=index['use.frequency']
        result_usage['usage']=index['use.useage']
        result_usage['consumption']=index['use.consumption']
        result_usage['notes']=index['use.notes']
        print(result_usage)
        return result_usage

def get_caution_people_from_drug(drugname): #由药物查慎用人群
    graph = Graph("bolt://localhost:7687", username="neo4j", password="123456")
    str = 'MATCH a=(drug{name:\'' + drugname + '\'})-[:caution_people]->(people) return people.name'
    result_list = list(graph.run(str).data())
    result_people = []
    for oneresult in result_list:
        result_people.append(oneresult['people.name'])
    return result_people

def get_prohibit_people_from_drug(drugname): #由药品查禁用人群
    graph = Graph("bolt://localhost:7687", username="neo4j", password="123456")
    str = 'MATCH a=(drug{name:\'' + drugname + '\'})-[:prohibition_people]->(people) return people.name'
    result_list = list(graph.run(str).data())
    result_people = []
    for oneresult in result_list:
        result_people.append(oneresult['people.name'])
    return result_people

def get_caution_symptom_from_drug(drugname): #由药物查慎用疾病
    graph = Graph("bolt://localhost:7687", username="neo4j", password="123456")
    str = 'MATCH a=(drug{name:\'' + drugname + '\'})-[:慎用]->(symptom) return symptom.name'
    result_list = list(graph.run(str).data())
    result_symptom = []
    for oneresult in result_list:
        result_symptom.append(oneresult['symptom.name'])
    return result_symptom

def get_prohibit_symptom_from_drug(drugname): #由药物查禁用疾病
    graph = Graph("bolt://localhost:7687", username="neo4j", password="123456")
    str = 'MATCH a=(drug{name:\'' + drugname + '\'})-[:禁用]->(symptom) return symptom.name'
    result_list = list(graph.run(str).data())
    result_symptom = []
    for oneresult in result_list:
        result_symptom.append(oneresult['symptom.name'])
    return result_symptom

def get_caution_drug_from_drug(drugname): #由药物查慎用药物
    graph = Graph("bolt://localhost:7687", username="neo4j", password="123456")
    str = 'MATCH a=(drug{name:\'' + drugname + '\'})-[:caution_drug]->(drug) return drug.name'
    result_list = list(graph.run(str).data())
    result_drug = []
    for oneresult in result_list:
        result_drug.append(oneresult['drug.name'])
    return result_drug

def get_prohibit_drug_from_drug(drugname): #由药物查禁用药物
    graph = Graph("bolt://localhost:7687", username="neo4j", password="123456")
    str = 'MATCH a=(drug{name:\'' + drugname + '\'})-[:prohibition_drug]->(drug) return drug.name'
    result_list = list(graph.run(str).data())
    result_drug = []
    for oneresult in result_list:
        result_drug.append(oneresult['drug.name'])
    return result_drug