# **********************************************************************************************************************
# coding=utf-8
#
# Name: Ritesh Jawale
#
# CSCI 561
#
# Homework 3 : Bayesian Inference
#
# Problem Statement:
#           Compute the inference in a Bayesian network. For this homework, you don’t need to worry about decision
#           nodes or utility nodes. Your task would be to use variable elimination or enumeration to calculate joint
#           probabilities, marginal probabilities, or conditional probabilities.
#
# Algorithm : Enumeration Algorithm
#
# **********************************************************************************************************************


# Python Package for system calls and functions ( Input file name as a command line argument)

import sys
import copy

# *************************   Opening the file with filename as command line argument **********************************

inputFile = open(sys.argv[-1], "r")

# ****************************************  Reading the File line by line **********************************************

fileContents = inputFile.read().splitlines()

# *******************************************   Declaration    *********************************************************

t1 = []
topological_order = []
query_list = []
node_list = []
bayes_net = []
record = {}

# ************************************* Display function ***************************************************************


def display(data):
    for record in data:
        print record

# ***************************************  Extracting Data    **********************************************************


def finding_nodes(item):

    node = ''

    if "(" in item:

        pos = item.find("(")
        pos += 1
        while item[pos] != ' ':
            node += item[pos]
            pos += 1
        # print node
        if "+" in item:
            state = '+'
        else:
            state = '-'
        # print state
        temp_dict = {'node': node, 'flag': state}
        return temp_dict
        # print temp_dict
    else:
        pos = 1
        node = ''
        while item[pos] != " ":
            node += item[pos]
            pos += 1
        # print node
        if "+" in item:
            state = '+'
        else:
            state = '-'
        # print state
        temp_dict = {'node': node, 'flag': state}
        return temp_dict

# *******************************  Function to check if string is all numbers   ****************************************


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


# **********************************Reading file line by line***********************************************************
#
#           Line 1 gives the Number of Queries in te file
#           Next n lines are the actual queries where n is number of queries on line 1
#           From line n+1 to the end of file is the Bayesian Network with all the probabilities of nodes in the network
#
# **********************************************************************************************************************

for line_no, data in enumerate(fileContents):

    if line_no == 0:
        no_of_queries = int(data)

# ********************************* Finding the Queries from input File ************************************************
    if 0 < line_no <= no_of_queries:
        if "|" not in data:
            d = data.split(",")
            temp = []
            for event in d:
                # print item
                t = finding_nodes(event)
                temp.append(t)
            record = {'events': temp, 'evidence': []}
            query_list.append(record)
        else:
            d = data.split("|")
            item1 = []
            temp = []
            counter = 0
            for j, event in enumerate(d):
                # print event
                if "," in event:
                    it = event.split(",")
                    for i in it:
                        item1.append(i)
                        if j == 0:
                            counter += 1
                else:
                    item1.append(event)
                    if j == 0:
                        counter += 1
            temp = []
            for i, node in enumerate(item1):
                t = finding_nodes(node)
                temp.append(t)
                if i == counter - 1:
                    record = {'events': temp, 'evidence': []}
                    temp = []

            record['evidence'] = temp

            query_list.append(record)


# *******************************************   Bayesian Net   *********************************************************

    if line_no > no_of_queries:

        # *********************  End of Table  *****************************************************

        if data == "***":
            if t1:
                temp['prob'] = t1
            bayes_net.append(temp)

            temp = {}
            t1 = []
            continue

        # ***********************  Bayes net *******************************************************

        if "|" in data:
            node_list = data.split("|")
            # print node_list
            for i, nodes in enumerate(node_list):

                if i == 0:
                    n = nodes.replace(" ", '')
                    temp = {'node': n}
                    if n not in topological_order:
                        topological_order.append(n)
                else:
                    parent_list = nodes.split(" ")
                    del parent_list[0]
                    temp['parent'] = parent_list
            temp['prob'] = {}
        else:
            if data.isalpha():
                temp = {'node': data, 'parent': [], 'prob': {}}
                if data not in topological_order:
                    topological_order.append(data)

        if is_number(data):
            p = float(data)
            if not temp['parent']:
                # temp['prob'] = [p]
                temp['prob']['+'] = p
        elif '+' in data or '-' in data:
            d = data.split(" ")
            key = ''
            for item in d:
                if is_number(item):
                    pro = float(item)
                else:

                    key += item
            temp['prob'][key] = pro
bayes_net.append(temp)

# ***********************************   Computing probability   ********************************************************


def pr(variable, value, bn, E):

    #  bn       =>  bayesian network
    #  variable =>  The variable event for probability
    #  value    =>  value of the event i.e whether it occurred(+) or not occurred(-)
    #  E        =>  Evidence list

    true_prob = -1
    for record in bn:
        if variable in record['node']:
            if not record['parent']:
                true_prob = record['prob']['+']
                # print true_prob
            else:
                if len(record['parent']) == 1:
                    for parent in record['parent']:
                        if parent in e.keys():
                            parent_value = e[parent]
                            true_prob = record['prob'][parent_value]
                else:
                    parent_value = ''
                    for parent in record['parent']:
                        if parent in e.keys():
                            parent_value += e[parent]

                    true_prob = record['prob'][parent_value]
    if value == "+":
        return true_prob
    else:
        return 1 - true_prob

# *********************************************** Output File **********************************************************

output_file = open("output.txt", "w")

# ****************************************  Enumeration Algorithm ******************************************************


def enumerate_all(vars, bn, E):

    if not vars:
        return 1

    y = vars.pop()

    #  f is temporary flag
    f = 0

    if y in E.keys():
        result = 0
        f = 1
        result = pr(y, E[y], bn, E) * enumerate_all(vars, bn, E)
        vars.append(y)
        return result

    if f == 0:
        result = 0
        for value in ['+', '-']:

            e[y] = value
            m = pr(y, value, bn, E) * enumerate_all(vars, bn, E)
            result += m
            if value == '-':
                del e[y]
        vars.append(y)
        return result


def enumeration_ask(X, e, bn, vars):
        #  qx  => distribution of Query variable X over it values

        qx = enumerate_all(vars, bn, e)
        return qx

#  ******************* Topological Ordering of Nodes in Bayesian Network ***********************************************
topological_order_copy = copy.deepcopy(topological_order)
topological_order_copy.reverse()

#  ******************* Calculating Probability for each Query **********************************************************

for query in query_list:
    e = {}
    if not query['evidence']:
        #  ********************* Building Evidence list => e **********************************************

        for event in query['events']:
            e[event['node']] = event['flag']
        probability = enumeration_ask(query['events'], e, bayes_net, topological_order_copy)
        # ********************  Final probability *****************************

        probability = format(probability, '.2f')
        # print probability

        #  ******************* Writing to File  ***********************************************************
        output_file.write(probability)
        if query != query_list[-1]:
            output_file.write("\n")

    else:

        #  ********************* Building Evidence list => e **********************************************

        for evidence in query['evidence']:
            e[evidence['node']] = evidence['flag']

        for event in query['events']:
            e[event['node']] = event['flag']

        #  ******************* Calculating Probability for Numerator Part *********************************

        qx_numerator = enumeration_ask(query['events'], e, bayes_net, topological_order_copy)

        #  ******************* Calculating Probability for Numerator Part *********************************

        e = {}
        for evidence in query['evidence']:
            e[evidence['node']] = evidence['flag']

        qx_denominator = enumeration_ask(n, e, bayes_net, topological_order_copy)

        # *************************  Final probability ****************************************************

        probability = format((qx_numerator/qx_denominator), '.2f')
        # print probability

        #  ******************* Writing to File  ************************************************************

        output_file.write(probability)
        if query != query_list[-1]:
            output_file.write("\n")

output_file.close()
