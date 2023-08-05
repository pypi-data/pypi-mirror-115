from graphviz import Digraph
import os
import sys
# parent_dir = os.path.join(os.getcwd(),os.pardir)
# sys.path.append(parent_dir)
import itertools
import json
import copy
from pydot import graph_from_dot_file
import re
import MatrixChoices

'''
 Example

dot = Digraph(comment='The Round Table')

dot.node('A', 'King Arthur')
dot.node('B', 'Sir Bedevere the Wise')
dot.node('L', 'Sir Lancelot the Brave')

dot.edges(['AB', 'AL'])
dot.edge('B', 'L', constraint='false')

print(dot.source)

dot.render('round-table.gv', view=True)

'''



class Graphviz:
    def __init__(self, title, matrix_choices, edges_name, pos, dir='.'):
        (self.vertices, self.edges) = self.extract_visual(matrix_choices, edges_name,pos)
        dot = Digraph(comment=title,directory=dir)
        for v in self.vertices:
            dot.node(v[0], v[1])
        dot.edges(self.edges)
        dot.render(title, view=False,cleanup=True)
        dot.save(filename=title + '.dot')

    def extract_visual(self,matrix_choices, edges_name, pos):
        vertices = set()
        edges = set()
        copy_choices = copy.copy(matrix_choices)
        copy_choices[pos].extend(copy_choices[pos+'-pc'])
        for n in copy_choices[pos]:
            node_comment, node_name = self.build_node_name_comment(n)
            vertices.add((node_name, node_comment))
            head = node_name
            if edges_name == 'good_edges':
                for e in n.good_edges:
                    tail = e.get_id()
                    edges.add((head,tail))
            elif edges_name == 'clustered_inputs':
                tail = node_name
                for e in n.clustered_inputs:
                    head = e.get_id()
                    edges.add((head,tail))
            elif edges_name == 'inputs':
                tail = node_name
                if len(n.get('inputs',[])) > 0:
                    for e in n['inputs'].split(','):
                        head = e
                        edges.add((head,tail))
        return(vertices, edges)

    def build_node_name_comment(self, n):
        node_name = n.full_key
        node_comment = json.dumps(n)
        node_comment = re.sub('\"','_QT_',node_comment) # so that it can be loaded by network vis.js
        return node_comment, node_name


    def dot_to_choices(self,dotfile):
        g = graph_from_dot_file(dotfile)
        nodes = self.graph_to_dictlist(g[0])
        mc = MatrixChoices.ChoiceDict(python_dicts=nodes)
        with open('dot2choices.txt', 'w') as f:
            f.write(str(mc))

    def graph_to_dictlist(self, g):
        nodes = []
        for key in g.obj_dict['nodes']:
            n = g.obj_dict['nodes'][key]
            label = n[0]['attributes']['label']
            label = re.sub('_QT_','"',label).strip('"')
            d = json.loads(label)
            nodes.append(d)
        return nodes

    '''
    Old version which was lossy with respect to the choices file format.
    '''
    def build_node_name_comment2(self, n):
    # modified by KPH 5/17 to take a choices object instead of a node object.
        node_name = n.full_key
        node_name = node_name.strip(' ')
        if 'pc' in node_name:
            pc_type = n['order']
            lris = list(s['lri']['0'] for s in n['lrt'])
            orths = list(set([ l['orth'] for l in lris if 'orth' in l]))
            orth_str = '\\n'.join(orths)
            lrts = list(s for s in n['lrt'])
            feats = list([lrt['feat'] for lrt in lrts if 'feat' in lrt])
            feat_list = list([l for l in feats])
            features_name_value = list(set([ f['name']+'_'+f['value'] for l in feat_list for f in l]))
            feat_str = '\\n'.join(features_name_value)
            if feat_str == '':
               feat_str = '_'
            pc_type = n['order']
            node_comment = node_name + '\\n' + pc_type + '\\n' + feat_str + '\\n' + orth_str
        else:
            orths = list(set([ s['orth'] for s in n['stem'] ]))
            features = [] #list(set([ s. for s in n.features ]))
            preds = list(set([ s['pred'] for s in n['stem'] ]))
            node_comment = node_name + '\\n' + '\\n'.join(orths) \
                               + '\\n' + '\\n'.join(preds)
                               #+ '\\n' + '\\n'.join(features)

        return node_comment, node_name
