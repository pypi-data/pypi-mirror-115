import os
import sys

from graphviz import Digraph

# parent_dir = os.path.join(os.getcwd(),os.pardir)
# sys.path.append(parent_dir)
import MatrixChoices


def read_choices(choices_path):
    cr = MatrixChoices.ChoicesFile(choices_path)
    pcs = cr.get('verb-pc')
    stems = list(cr.get('verb'))
    imported_entries = cr.get('imported-entry')
    nodes, edges = choices_pcs2nodes(pcs, stems, list(imported_entries),cr)
    return nodes, edges

def build_graph(nodes, edges,title,dir):
    dot = Digraph(comment=title,directory=dir)
    for v in nodes:
        dot.node(v[0], v[1])
    dot.edges(edges)
    dot.render(title, view=False,cleanup=True)


def choices_pcs2nodes(pcs, stems, imported_entries, cr):
    nodes = set()
    edges = set()
    skip_nodes = set()
    for s in stems:
        node_name = s.full_key
        orths = []
        for ie in imported_entries:
            if ie['lextype'] == s.full_key:
                orths.append((ie['pred'], ie['orth']))
        for item in list(s['stem']):
            orths.append((item['pred'],item['orth']))
        node_comment = node_name + '\n' + orths[0][1] + '/' + orths[0][0] # only grabs the first one
        nodes.add((node_name,node_comment))
    for pc in pcs:
        node_name = pc.full_key
        node_comments = []
        lrts = pc['lrt']
        for lrt in lrts:
            node_comment = node_name +'\n' + pc['name'] + ' | '
            for lri in list(lrt['lri']):
                node_comment += lri['orth'] + '/'
                for feat_spec in list(lrt['feat']):
                    node_comment += feat_spec['name'] + ':' + feat_spec['value']
                node_comments.append(node_comment.strip('/'))
        comment = node_comments[0] if len(node_comments) > 0 else node_name# grab first
        #comment = ' | '.join(node_comments) if len(node_comments) > 0 else node_name
        nodes.add((node_name,comment))
        prev = (node_name,comment)
        if len(lrts) > 0:
            skip_nodes.add(node_name)
    for node_name,comment in nodes:
        inputs = cr[node_name]['inputs'].split(',')
        for head in inputs:
            if head.strip():
                edges.add((head.strip(),node_name))
    return nodes,edges

nodes, edges = read_choices(sys.argv[1])
build_graph(nodes,edges,'ctn-oracle.pdf',sys.argv[2])
