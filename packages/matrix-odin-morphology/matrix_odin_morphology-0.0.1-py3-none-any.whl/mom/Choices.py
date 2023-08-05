#!/opt/python-3.4/bin/python3.4
# -*- coding: utf-8 -*-
import copy
import os
import queue
import re
import sys
from collections import defaultdict,OrderedDict

# parent_dir = os.path.join(os.getcwd(),os.pardir)
# sys.path.append(parent_dir)
from . import MatrixChoices
from XigtifiedToolbox import FeatDict
import json

class noinsertdict(defaultdict):
    def __missing__(self, key):
        return self.default_factory()

###########
# Variables
###########


feat_dict = FeatDict.FeatureDictionary()
feat_dict.validate_dictionary()

FAKE_TRANSITIVITY = 'trans,comps1'
###########
# classes
###########


class CustomEncoder(json.JSONEncoder):

     def default(self, o):

         if isinstance(o, LexicalItem):

             return {'__datetime__': o.replace(microsecond=0).isoformat()}

         return {'__{}__'.format(o.__class__.__name__): o.__dict__}


class Choices:
    def __init__(self, iso, xigt_items, hyphens=False, output_glosses=False,
                 algorithm='overlap',
                 output_dir='.', known_affix_types=None, lexitem_classes=True, ignore_affix_types=[],
                 verbose=False, precluster_only=False,pos_tag='verb',escape_special_characters=False,
                 agr_morphemes=None, ignore_features=False):
        self.iso = iso
        self.algorithm = algorithm
        self.lexicon = Lexicon(pos_tag=pos_tag, hyphens=hyphens, output_glosses=output_glosses,
                               output_dir=output_dir, known_affix_types=known_affix_types,
                               lexitem_classes=lexitem_classes,verbose=verbose,
                               use_only_preclustered=precluster_only,precluster_type='orth',
                               escape_special_characters=escape_special_characters,
                               agr_morphemes=agr_morphemes,ignore_features=ignore_features)
        self.pos_tag = pos_tag
        self.lexicon.build_lexitem_lexicon(xigt_items, ignore_affix_types,pos_tag)


class Lexicon:
    def __init__(self, pos_tag, hyphens=False, output_glosses = False, output_dir='.',
                 known_affix_types=None, lexitem_classes = True, verbose=False,
                 precluster_type='gloss',use_only_preclustered=False,escape_special_characters=False,
                 agr_morphemes=None,ignore_features=False):
        self.verbose = verbose
        self.lexitems = set()
        self.lexitem_ids = set()
        self.known_affix_types = known_affix_types
        self.precluster_type = precluster_type
        self.preclustered_only = use_only_preclustered
        self.relevant_pcs = []
        self.lexitems_to_prefixes = {}
        # was here for debugging a weird crash; is not being called
        def tracing_lexitems(frame, msg, arg):
            if msg != 'call': return
            if frame.f_code.co_filename.startswith("/Library/Frameworks/Python.framework/"): return
            sys.stderr.write("--------- "+ frame.f_code.co_name + "   " + frame.f_code.co_filename)
            sys.stderr.write('start foo ' + str(len(self.lexitems)) + '\n')
            lst = list(self.lexitems)
            self.lexitems = lst
            sys.stderr.write('end foo ' + str(len(self.lexitems)) + '\n')
        # sys.settrace(tracing_lexitems)
        self.possible_features = set()
        self.possible_glosses = set()
        self.possible_orths = set()
        self.possible_roots = set()
        self.possible_preds = set()
        self.pos_tag = pos_tag
        self.pcs = []
        self.id_to_pc = {}
        self.affix_obs = []
        self.MOM_labels = []
        self.pc_to_affix_obs = {}
        self.overlap_table = OrderedDict()
        self.pc_to_overlaps = OrderedDict()
        self.lexitem_overlap_table = {}
        self.lexitem_to_overlaps = {}
        self.lexitem_lexitem_overlap = {}
        self.pc_pc_overlap = OrderedDict()
        self.prefixes_to_lexitems = {}
        self.copy_pcs = {}
        self.hyphens = hyphens
        self.output_glosses = output_glosses
        self.output_dir = output_dir
        self.lexitem_classes = lexitem_classes
        self.escape_special_characters = escape_special_characters
        self.agr_morphemes = agr_morphemes
        self.zero_marked_features = []
        self.ignore_features = ignore_features

    def print_overlap_table(self):
        s = [ [ row.get_id()+"||"] + [ e[0].get_id()[5:]+":"+str(e[1])[:6] for e in self.overlap_table[row] ]
              for row in self.overlap_table ]
        lens = [max(map(len,col)) for col in zip(*s)]
        fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        print ('\n'.join(table))

    '''
    Traverse the lexicon graph and find a longest path between any two nodes.
    The paths are stored in a dictionary within each node, e.g.:
    node1.longest_paths will look like {node2_id: llp between node1 and node2}.
    '''
    def traverse_lexicon_llp(self):
        nodes2paths = {}
        for n in self.lexitems:
            self.find_longest_path(n, nodes2paths)
        for n in self.pcs:
            self.find_longest_path(n, nodes2paths)

    def find_longest_path(self, n, nodes2paths):
        nodes2paths[n.get_id()] = self.depth_first_traversal(n)
        n.longest_paths = {}
        for target in nodes2paths[n.get_id()]:
            llp = []
            for p in nodes2paths[n.get_id()][target]:
                if len(p) > len(llp):
                    llp = p
            n.longest_paths[target] = llp

    def depth_first_traversal(self,start):
        if not (start):
            raise Exception('DFS called on an null start.')
        path = []
        stack = []
        stack.append((start,path))
        start.paths = {}
        while len(stack) > 0:
            (n,path) = stack.pop()
            if n.get_id() != start.get_id():
                if n.get_id() not in start.paths:
                    start.paths[n.get_id()] = []
                start.paths[n.get_id()].append(path)
            path = list(path) + [n]
            for i in n.outgoing_edges:
                stack.append((i,path))
        return(start.paths)

    def create_overlap_tables(self,lexitem,min_over=0.0):
        processed = set()
        if lexitem:
            lst = list(self.lexitems)
            table_a = self.lexitem_overlap_table
            table_b = self.lexitem_to_overlaps
            table_c = self.lexitem_lexitem_overlap
        else:
            lst = self.pcs
            table_a = self.overlap_table
            table_b = self.pc_to_overlaps
            table_c = self.pc_pc_overlap
        for node_i in lst:
            if self.verbose:
                print ("Processing ", node_i.id)
            if node_i not in table_c:
                table_c[node_i] = noinsertdict(float)
            if not node_i in table_b:
                table_b[node_i] = list()
            for node_j in lst:
                if node_j not in table_c:
                    table_c[node_j] = noinsertdict(float)
                if not node_j in table_b:
                    table_b[node_j] = list()
                if not node_i == node_j:
                    if (node_i,node_j) not in processed or (node_j,node_i) not in processed:
                        overlap = node_i.compute_overlap(node_2=node_j)
                        if overlap >= min_over:
                            table_c[node_i][node_j] = overlap
                            table_c[node_j][node_i] = overlap
                            if not overlap in table_a:
                                table_a[overlap] = OrderedDict()
                            if not node_i in table_a[overlap]:
                                table_a[overlap][node_i] = list()
                            table_a[overlap][node_i].append(node_j)
                            if not node_j in table_a[overlap]:
                                table_a[overlap][node_j] = list()
                            table_a[overlap][node_j].append(node_i)
                            table_b[node_i].append(overlap)
                            table_b[node_j].append(overlap)
                        processed.add((node_i,node_j))
                        processed.add((node_j,node_i))
        new_table = OrderedDict()
        for over in table_a:
            new_table[over] = OrderedDict()
            for k in table_a[over]:
                new_table[over][k] = sorted(table_a[over][k], key=lambda  t: t.id)
        final_table = OrderedDict()
        for over in new_table:
            new_row = OrderedDict(sorted(new_table[over].items(), key=lambda t: t[0].id))
            final_table[over] = new_row
        table_a = final_table

    def update_overlap_tables(self,node_update,node_remove,lexitem,min_over=0.0):
        if lexitem:
            lst = list(self.lexitems)
            table_a = self.lexitem_overlap_table
            table_b = self.lexitem_to_overlaps
            table_c = self.lexitem_lexitem_overlap
        else:
            lst = self.pcs
            table_a = self.overlap_table
            table_b = self.pc_to_overlaps
            table_c = self.pc_pc_overlap
        keys = set(table_b.pop(node_remove))
        cur_over = table_c[node_update][node_remove]
        table_b[node_update].remove(cur_over)
        for k in keys:
            table_a[k].pop(node_remove)
            row = table_a[k]
            for col in row:
                if node_remove in row[col]:
                    row[col].remove(node_remove)
                    try:
                        table_b[col].remove(k)
                    except:
                        raise Exception('list.remove(x): x not in list')
            new_row = OrderedDict()
            for col in row:
                if len(row[col]) > 0:
                    new_row[col] = row[col]
            if len(new_row) > 0:
                table_a[k] = new_row
            else:
                table_a.pop(k)
        table_c.pop(node_remove)
        for row in table_c:
            if node_remove in table_c[row]:
                table_c[row].pop(node_remove)
        nodes_to_update = [node_update]
        if not lexitem:
            nodes_to_update.extend(node_update.outgoing_edges)
        processed = set()
        for node_i in nodes_to_update:
            for node_j in lst:
                if node_i != node_j:
                    if (node_i,node_j) not in processed or (node_j,node_i) not in processed:
                        new_over = node_i.compute_overlap(node_2=node_j)
                        if node_i in table_c:
                            old_over = table_c[node_i][node_j]
                        else:
                            old_over = 0.0
                        if new_over != old_over:
                            if old_over > 0:
                                if old_over in table_a:
                                    if node_i in table_a[old_over] and node_j in table_a[old_over][node_i]:
                                        table_a[old_over][node_i].remove(node_j)
                                        if len(table_a[old_over][node_i]) == 0:
                                            table_a[old_over].pop(node_i)
                                    if node_j in table_a[old_over] and node_i in table_a[old_over][node_j]:
                                        table_a[old_over][node_j].remove(node_i)
                                        if len(table_a[old_over][node_j]) == 0:
                                            table_a[old_over].pop(node_j)
                                    if len(table_a[old_over]) == 0:
                                        table_a.pop(old_over)
                                if old_over in table_b[node_i]:
                                    table_b[node_i].remove(old_over)
                                if old_over in table_b[node_j]:
                                    table_b[node_j].remove(old_over)
                            if new_over >= min_over:
                                if new_over not in table_a:
                                    table_a[new_over] = OrderedDict()
                                if node_i not in table_a[new_over]:
                                    table_a[new_over][node_i] = list()
                                table_a[new_over][node_i].append(node_j)
                                if node_j not in table_a[new_over]:
                                    table_a[new_over][node_j] = list()
                                table_a[new_over][node_j].append(node_i)
                                if node_i not in table_b:
                                    table_b[node_i] = list()
                                table_b[node_i].append(new_over)
                                if node_j not in table_b:
                                    table_b[node_j] = list()
                                table_b[node_j].append(new_over)
                                if not node_i in table_c:
                                    table_c[node_i] = noinsertdict(float)
                                table_c[node_i][node_j] = new_over
                                if not node_j in table_c:
                                    table_c[node_j] = noinsertdict(float)
                                table_c[node_j][node_i] = new_over
                            else:
                                if node_j in table_c[node_i]:
                                    table_c[node_i].pop(node_j)
                                if node_i in table_c[node_j]:
                                    table_c[node_j].pop(node_i)
                        processed.add((node_i,node_j))
                        processed.add((node_j,node_i))

    def cleanup_table(self,table,key1, key2):
        if len(table[key1][key2]) == 0:
            table[key1].pop(key2)
            if len(table[key1]) == 0:
                table.pop(key1)

    def create_copy_pc(self, new_id,pc):
        new_pc = copy.copy(pc)
        new_pc.setID(new_id)
        for e in new_pc.outgoing_edges:
            e.inputs = set(e.inputs)
            e.inputs.add(new_pc)
        for input in new_pc.inputs:
            input.outgoing_edges = set(input.outgoing_edges)
            input.outgoing_edges.add(new_pc)
        self.pcs.append(new_pc)
        return new_pc

    def visualize(self, title, matrix_choices, edges_name, file_list, pos):
        import Digraph
        #print("Output directory for graph: ", self.output_dir)
        dg = Digraph.Graphviz(title, matrix_choices, edges_name, pos, self.output_dir)
        #dg.dot_to_choices(self.output_dir + title + '.dot') # testing the function
        file_list.append(title + '.pdf')
        file_list.append(title + '.dot')

    def tabularize(self, title, file_list):
        tbl = self.build_table()
        with open(title+'.txt', 'w', encoding='utf-8') as f:
            for ln in tbl:
                f.write(ln + '\n')
        file_list.append(title + '.txt')

    def build_table(self):
        tbl = []
        for count,lexitem in enumerate(self.lexitems):
            ln = ''
            for position in range(len(lexitem.maximal_construct['prefix']),0,-1):
                ln += str(position) + '\t'
            ln += 'stem' + str(count) + '\t'
            for position in range(len(lexitem.maximal_construct['suffix']),0,-1):
                ln += str(position) + '\t'
            ln = ln.strip()
            ln += '\n'
            tbl.append(ln)
            ln = ''
            for position in range(len(lexitem.maximal_construct['prefix']),0,-1):
                pc = lexitem.maximal_construct['prefix'][position]
                orth = pc.lexical_rule_types[0].instances[0].orth
                ln += orth + '\t'
            ln += lexitem.stems[0].orth + '\t'
            for position in range(len(lexitem.maximal_construct['suffix']),0,-1):
                pc = lexitem.maximal_construct['suffix'][position]
                orth = pc.lexical_rule_types[0].instances[0].orth
                ln += orth + '\t'
            ln = ln.strip()
            tbl.append(ln)
        return tbl


    '''
    Merge Lexical Items based on how much output they share.
    By default, consider prefix overlap.
    '''
    def compact_lexitems(self,depth, min_overlap=1.0, first_call=False):
        if first_call:
            self.lexitem_overlap_table = {}
            self.create_overlap_tables(lexitem=True,min_over=min_overlap)
        #print ("compact lexitem lexicon depth=",depth)
        (node1, node2, overlap) = self.get_best_overlap(lexitem=True)
        if node1 and node2:
            if self.verbose:
                print("best overlap was ", str(overlap), "lexitem1:", node1.id, "lexitem2:", node2.id)
            if overlap >= min_overlap:
                node1.merge(node2)
                self.replace_lexitem(node1, node2)
                self.update_overlap_tables(node_update=node1, node_remove=node2, lexitem=True,
                                           min_over=min_overlap)
                # self.visualize('tmp',self.pcs,'inputs')
                self.compact_lexitems(depth=depth + 1, min_overlap=min_overlap, first_call=False)

    def check_tables(self):
        for pc in self.pc_pc_overlap:
            if len(self.pc_pc_overlap[pc]) != len(self.pc_to_overlaps[pc]):
                raise Exception('Lengths not equal: pc' + str(pc.id))

    def compact_lexicon(self, depth, min_overlap=1.0,seen_pairs=set(),first_call=False):
        #print ("compact lexicon depth=",depth)
        if first_call:
            self.overlap_table = {}
            self.create_overlap_tables(lexitem=False,min_over=min_overlap)
        (pc1, pc2, overlap) = self.get_best_overlap(lexitem=False)

        if pc1 and pc2:
            #self.check_tables() # debug
            if self.verbose:
                print ("best overlap was ",str(overlap),"pc1:",pc1.id,"pc2:",pc2.id)
            if overlap >= min_overlap:
                pc1.merge(pc2)
                self.replace(pc1, pc2)
                self.update_overlap_tables(node_update=pc1,node_remove=pc2,lexitem=False,
                                       min_over=min_overlap)
                self.compact_lexicon(depth=depth + 1, min_overlap=min_overlap,seen_pairs=seen_pairs,first_call=False)

    def merge_and_replace(self,pc1,pc2, sacrifice_inputs=False):
        if sacrifice_inputs:
            self.merge_and_reset_node(pc1,pc2)
        else:
            pc1.merge(pc2)
            for pc in self.pcs:
                if not pc1 in pc.cycles_found:
                    if pc1 in pc.cycles_checked:
                        pc.cycles_checked.remove(pc1)
            self.replace(pc1, pc2)

    def replace_lexitem(self,node1, node2):
        tmp = list(self.lexitems)
        self.lexitems = set()
        maximal2 = len(node2.maximal_construct['prefix']) + len(node2.maximal_construct['suffix'])
        maximal1 = len(node1.maximal_construct['prefix']) + len(node1.maximal_construct['suffix'])
        if maximal2 > maximal1:
            node1.maximal_construct = node2.maximal_construct
        for pc in list(self.pcs):
            if node2 in pc.inputs:
                pc.add_input(node1)
                res = pc.remove_input(node2)
                if not res:
                    print('Cannot remove ', node2.id, 'from ', pc.id)
                    node2.cannot_remove = True
                else:
                    if node2 in tmp:
                        tmp.remove(node2)
        self.lexitems = set(tmp)

    def replace(self, pc1, pc2):
        for pc in self.pcs:
            if pc.has_input(pc2):
                pc.add_input(pc1)
                res = pc.remove_input(pc2)
                if not res:
                    print('Cannot remove ', pc2.get_id(), 'from ', pc.get_id())
                    pc2.cannot_remove = True
        if not pc2.cannot_remove:
            self.remove_pc(pc2)
        for node in self.lexitems:
            key = 'prefix' if pc2.is_prefix else 'suffix'
            for position in node.maximal_construct[key]:
                if node.maximal_construct[key][position].id == pc2.id:
                    node.maximal_construct[key][position] = pc1
            if pc2 in node.outgoing_edges:
                node.outgoing_edges.remove(pc2)
                if not pc1 in node.outgoing_edges:
                    node.outgoing_edges.add(pc1)
            if pc2 in node.relevant_outputs:
                node.relevant_outputs.remove(pc2)
                if not pc1 in node.relevant_outputs and (pc1.known_type or not self.known_affix_types):
                    node.relevant_outputs.add(pc1)
        for node in self.pcs:
            if pc2 in node.outgoing_edges:
                node.outgoing_edges.remove(pc2)
                if not pc1 in node.outgoing_edges:
                    node.outgoing_edges.add(pc1)


    def remove_pc(self,pc):
        if pc not in self.pcs:
            raise Exception("Trying to remove what is not there")
        assert pc in self.pcs
        self.pcs.remove(pc)


    def get_best_overlap(self, lexitem):
        best_1 = None
        best_2 = None
        best_over = -1
        if lexitem:
            table = self.lexitem_overlap_table
            table_b = self.lexitem_to_overlaps
        else:
            table = self.overlap_table
            table_b = self.pc_to_overlaps
        keys = list(table.keys())
        if len(keys) > 0:
            best_over = max(keys)
            if len(table[best_over]) > 0:
                (best_1, best_2s) = table[best_over].popitem(False)
                if len(best_2s) > 0:
                    best_2 = list(best_2s).pop(0)
                    best_2s.remove(best_2)
                    if len(best_2s) > 0:
                        table[best_over][best_1] = best_2s
                        table[best_over].move_to_end(best_1,False)
                else:
                    table[best_over].pop(best_1,best_2s)
                    table_b[best_1].remove(best_over)
            else:
                best_over = -1.0
        return (best_1, best_2, best_over)


    # original function: definitely bug-free but inefficient
    # uncomment when need to make sure the result is correct

    # def get_best_overlap_original(self, lst):
    #     best_1 = None;
    #     best_2 = None;
    #     best_over = -1;
    #     for i in range(len(lst)):
    #         for j in range(i+1,len(lst)):
    #             over = lst[i].compute_overlap(lst[j]);
    #             if over > best_over:
    #                 best_1 = lst[i]
    #                 best_2 = lst[j]
    #                 best_over = over
    #     return (best_1, best_2, best_over)

    def collect_zero_marked_features(self, xigt_items, pos):
        for xigt_item in xigt_items:
            root_morph = xigt_item.ordered_morphemes[0]
            if root_morph.features:
                if has_lemma(root_morph.glosses):
                    zero_marked_features = self.aligned_features(root_morph.features, '', pos)
                    if zero_marked_features:
                        if not any([x for x in self.zero_marked_features if all([True for f in x if f in zero_marked_features])]):
                            self.zero_marked_features.append(zero_marked_features)

    def build_lexitem_lexicon(self,xigt_items, ignore_affix_types = [], pos='verb'):
        bare_lexitem_list = []
        no_valence = 0
        self.collect_zero_marked_features(xigt_items, pos)
        for xigt_item in xigt_items:
            if pos == 'verb' and xigt_item.transitivity and not xigt_item.case_frame:
                raise Exception('No case frame but valid transitivity in IGT {0}'.format(xigt_item.parent_igt.id))
            if pos == 'verb' and not xigt_item.transitivity:
                no_valence += 1
                xigt_item.transitivity = FAKE_TRANSITIVITY
            rightmost_root = xigt_item.root
            (lexitem_features, pred) = self.aligned_lexitem_features(xigt_item,pos)
            for f in lexitem_features:
                self.possible_features.add(f.value)
            assert pred is not None, "No predicate aligned with lexical item"
            for g in pred.glosses:
                pred_value = strip_grams(g,pos) # KPH added to remove grams from pred values
                pred_value = re.sub('\'|\"','',pred_value) # quotations in the pred break customization
                pred_value = re.sub('\n','',pred_value)
                self.possible_preds.add(pred_value.lower())
            self.possible_roots.add(pred.orth.lower())
            prev_input = self.add_lexitem(pred_value.lower(), rightmost_root.orth.lower(), # KPH changed rightmost_root.glosses[0] to pred_value to be consistent with what we are adding to possible_glosses
                                          lexitem_features,self.lexitem_classes,xigt_item, bare_lexitem_list)
            lexitem = copy.copy(prev_input)
            if len(xigt_item.ordered_morphemes) == 1:
                if len([x for x in bare_lexitem_list if (x.transitivity == prev_input.transitivity and  x.case_frame == prev_input.case_frame)]) == 0:
                    bare_lexitem_list.append(prev_input)
            if not lexitem in self.lexitems_to_prefixes:
                self.lexitems_to_prefixes[lexitem] = {}
            prefix_count = 0
            suffix_count = 0
            # add any zero-marked morphosyntactic position classes:
            # root_morph = xigt_item.ordered_morphemes[0]
            # if root_morph.features:
            #     if has_lemma(pred.glosses):
            #         zero_marked_features = self.aligned_features(root_morph.features,'',pos)
            #         if zero_marked_features:
            #             input = self.add_position_class(root_morph,zero_marked_features,prev_input, False,rightmost_root.orth,is_zero=True)
            #             prev_input = input
            for affix in xigt_item.prefixes+xigt_item.suffixes:
                is_prefix = affix.type == 'prefix'
                #is_prefix = (affix.type == 'prefix' or affix.type == 'proclitic')
                if affix.type == 'root':
                    is_prefix = False
                if isinstance(prev_input,Position_Class) and prev_input.known_type in ignore_affix_types:
                    prev_input = lexitem
                affix_features = self.aligned_features(affix.features,affix.orth,pos)
                input = self.add_position_class(affix, affix_features,prev_input,is_prefix, rightmost_root.orth)
                if is_prefix: #TODO: should be applicable to suffixes as well, this is Abui-specific
                    prefix_count += 1
                    lexitem.maximal_construct['prefix'][prefix_count] = input
                    if affix.known_affix_type and affix.known_affix_type not in ignore_affix_types:
                        if not prefix_count in self.lexitems_to_prefixes[lexitem]:
                            self.lexitems_to_prefixes[lexitem][prefix_count] = []
                        self.lexitems_to_prefixes[lexitem][prefix_count].append(affix.known_affix_type)
                        if not affix.known_affix_type in self.prefixes_to_lexitems:
                            self.prefixes_to_lexitems[affix.known_affix_type] = {}
                        if not prefix_count in self.prefixes_to_lexitems[affix.known_affix_type]:
                            self.prefixes_to_lexitems[affix.known_affix_type][prefix_count] = []
                        self.prefixes_to_lexitems[affix.known_affix_type][prefix_count].append(lexitem)
                else:
                    suffix_count += 1
                    lexitem.maximal_construct['suffix'][suffix_count] = input
                prev_input = input
                #if len(lexitem.relevant_outputs) == 0:
                #    print("No relevant outputs in pos_word {0} from igt {1}".format(xigt_item.root.orth,xigt_item.parent_igt.id))
        #if pos == 'verb':
        #    print('{0} verbs out of {1} did not have a valence frame'.format(no_valence,len(xigt_items)))
        self.lexitems = list(self.lexitems)

    def aligned_lexitem_features(self, lexitem,pos):
        features = []
        pred = lexitem.root
        if not self.ignore_features:
            features.extend(self.aligned_case_features(lexitem,pos))
        return(features,pred)


    def aligned_case_features(self, word_or_morpheme, pos):
        features = []
        if pos == 'verb':
            if word_or_morpheme.case_frame and len(word_or_morpheme.case_frame) > 0:
                for arg in word_or_morpheme.case_frame:
                    if word_or_morpheme.case_frame[arg] in feat_dict.dictionaries['caseFeatures']:
                        case_val = feat_dict.dictionaries['caseFeatures'][word_or_morpheme.case_frame[arg]]
                    else:
                        #print ('A case feature {0} not in FeatDict.py; '
                        #       'please update.'.format(word_or_morpheme.case_frame[arg]))
                        case_val = word_or_morpheme.case_frame[arg]
                    f = Feature('case', arg, case_val)
                    features.append(f)
        return features


    def get_feature_head(self, feats, orth):
        # KPH This method takes advantage of subject and object agreement markers that were identified by argument
        # optionality inference to detirmine whether png features on verbs mark the subject or object
        # If the morpheme isn't known, it tries to guess based on the presence of the same kinds of features
        head = ''
        orth = re.sub('-', '', orth)
        orth = re.sub('=', '', orth)
        if self.agr_morphemes:
            subj_morphs = self.agr_morphemes['subj_morphemes']
            obj_morphs = self.agr_morphemes['obj_morphemes']
            pmt_morphs = self.agr_morphemes['portmanteau_morphemes']
            if orth in subj_morphs:
                head = 'subj'
            elif orth in obj_morphs:
                head = 'obj'
            elif orth in pmt_morphs:
                head = 'both'
        if head == '':
            per_count = 0
            num_count = 0
            gen_count = 0
            for feat in feats:
                if feat in feat_dict.dictionaries['perNumFeatures']:
                    per_count += 1
                    num_count += 1
                elif feat in feat_dict.dictionaries['perGenFeatures']:
                    per_count += 1
                    gen_count += 1
                elif feat in feat_dict.dictionaries['perFeatures']:
                    per_count += 1
                elif feat in feat_dict.dictionaries['numFeatures']:
                    num_count += 1
                elif feat in feat_dict.dictionaries['genFeatures']:
                    gen_count += 1
                elif feat in feat_dict.dictionaries['perNumGenFeatures']:
                    per_count += 1
                    num_count += 1
                    gen_count += 1
                elif feat in feat_dict.dictionaries['perNumInclFeatures']:
                    per_count += 1
                    num_count += 1
            if per_count > 1 or num_count > 1 or gen_count > 1:
                head = 'both'
            else:
                head = 'subj'
        return head

    def aligned_features(self, feats, orth, pos):
        features = []
        if self.ignore_features:
            return features
        headarg = self.get_feature_head(feats, orth)
        marked_subj = False
        # KPH a feature to keep track of whether the subject has agr yet.
        # in the case portmanteau morphemes that mark both the subj and obj,
        # we assume that the first set of feats is the subj, then the obj
        if pos == 'verb':
            for feat in feats:
                agr_feat = False
                if headarg == 'both':
                    if marked_subj:
                        feathead = 'obj'
                    else:
                        feathead = 'subj'
                else:
                    feathead = headarg
                if feat in feat_dict.dictionaries['negFeatures']:
                    val = feat_dict.dictionaries['negFeatures'][feat]
                    name = 'negation'
                    head = 'verb'
                    features.append(Feature(name,head,val))
                elif feat in feat_dict.dictionaries['perNumFeatures']:
                    person, number = feat_dict.dictionaries['perNumFeatures'][feat]
                    name = 'person'
                    val = person
                    head = feathead
                    f = Feature(name,head,val)
                    features.append(f)
                    name = 'number'
                    val = number
                    f = Feature(name,head,val)
                    features.append(f)
                    marked_subj = True
                    agr_feat = True
                elif feat in feat_dict.dictionaries['perGenFeatures']:
                    person,gender = feat_dict.dictionaries['perGenFeatures'][feat]
                    name = 'person'
                    val = person
                    head = feathead
                    f = Feature(name,head,val)
                    features.append(f)
                    name = 'gender'
                    val = gender
                    f = Feature(name,head,val)
                    features.append(f)
                    marked_subj = True
                    agr_feat = True
                elif feat in feat_dict.dictionaries['perNumGenFeatures']:
                    person,number,gender = feat_dict.dictionaries['perNumGenFeatures'][feat]
                    name = 'person'
                    val = person
                    head = feathead
                    f = Feature(name,head,val)
                    features.append(f)
                    name = 'number'
                    val = number
                    f = Feature(name, head, val)
                    features.append(f)
                    name = 'gender'
                    val = gender
                    f = Feature(name,head,val)
                    features.append(f)
                    marked_subj = True
                    agr_feat = True
                elif feat in feat_dict.dictionaries['perGenHeadFeatures']:
                    person,gender,head = feat_dict.dictionaries['perGenHeadFeatures'][feat]
                    name = 'person'
                    val = person
                    f = Feature(name,head,val)
                    features.append(f)
                    name = 'gender'
                    val = gender
                    f = Feature(name,head,val)
                    features.append(f)
                    marked_subj = True
                    agr_feat = True
                elif feat in feat_dict.dictionaries['perNumHeadFeatures']:
                    person,number,head = feat_dict.dictionaries['perNumHeadFeatures'][feat]
                    name = 'person'
                    val = person
                    f = Feature(name,head,val)
                    features.append(f)
                    name = 'number'
                    val = number
                    f = Feature(name,head,val)
                    features.append(f)
                    marked_subj = True
                    agr_feat = True
                elif feat in feat_dict.dictionaries['perHeadFeatures']:
                    person,head = feat_dict.dictionaries['perHeadFeatures'][feat]
                    name = 'person'
                    val = person
                    f = Feature(name,head,val)
                    features.append(f)
                    marked_subj = True
                    agr_feat = True
                elif feat in feat_dict.dictionaries['perFeatures']:
                    person = feat_dict.dictionaries['perFeatures'][feat]
                    name = 'person'
                    head = feathead
                    val = person
                    f = Feature(name,head,val)
                    features.append(f)
                    marked_subj = True
                    agr_feat = True
                elif feat in feat_dict.dictionaries['numFeatures']:
                    name = 'number'
                    val = feat_dict.dictionaries['numFeatures'][feat]
                    head = feathead
                    f = Feature(name,head,val)
                    features.append(f)
                    marked_subj = True
                    agr_feat = True
                elif feat in feat_dict.dictionaries['genFeatures']:
                    name = 'gender'
                    val = feat_dict.dictionaries['genFeatures'][feat]
                    head = feathead
                    f = Feature(name,head,val)
                    features.append(f)
                    marked_subj = True
                    agr_feat = True
                elif feat.lower() in feat_dict.dictionaries['perNumInclFeatures']:
                    p, n, i = feat_dict.dictionaries['perNumInclFeatures'][feat.lower()]
                    name = 'pernum'
                    if 'non' in p:
                        p = 'n'
                    else:
                        p = re.sub('[a-z]', '', p)
                    val = p + n + '_' + i
                    head = feathead
                    f = Feature(name,head,val)
                    features.append(f)
                    marked_subj = True
                    agr_feat = True
                elif feat.lower() in feat_dict.dictionaries['perNumInclHeadFeatures']:
                    p, n, i, head = feat_dict['perNumInclHeadFeatures'][feat.lower()]
                    name = 'pernum'
                    if 'non' in p:
                        p = 'n'
                    else:
                        p = re.sub('[a-z]', '', p)
                    val = p + n + '_' + i
                    f = Feature(name,head,val)
                    features.append(f)
                    marked_subj = True
                    agr_feat = True
                elif feat in feat_dict.dictionaries['tenseFeatures']:
                    val = feat_dict.dictionaries['tenseFeatures'][feat]
                    name = 'tense'
                    head = 'verb'
                    features.append(Feature(name,head,val))
                elif feat in feat_dict.dictionaries['aspectFeatures']:
                    val = feat_dict.dictionaries['aspectFeatures'][feat]
                    name = 'aspect'
                    head = 'verb'
                    features.append(Feature(name,head,val))
                elif feat in feat_dict.dictionaries['moodFeatures']:
                    val = feat_dict.dictionaries['moodFeatures'][feat]
                    name = 'mood'
                    head = 'verb'
                    features.append(Feature(name,head,val))
                # removing because aux inference is not inferring whether the complement is finite or not, but posits finite (because it has to posit something). leaving form underspecified improves coverage
                # elif feat in feat_dict.dictionaries['formFeatures']:
                #     if feat_dict.dictionaries['formFeatures'][feat] == 'fin':
                #         val = feat_dict.dictionaries['formFeatures'][feat]
                #     else:
                #         val = feat_dict.dictionaries['formFeatures']['nonfin']
                #     name = 'form'
                #     head = 'verb'
                #     features.append(Feature(name,head,val))

        elif pos == 'noun':
            for feat in feats:
                if feat in feat_dict.dictionaries['caseFeatures']:
                    case = feat_dict.dictionaries['caseFeatures'][feat]
                    f = Feature('case',None,case)
                    features.append(f)
                elif feat in feat_dict.dictionaries['numFeatures']:
                    num = feat_dict.dictionaries['numFeatures'][feat]
                    f = Feature('number',None,num)
                    features.append(f)
                # elif feat in feat_dict.dictionaries['perFeatures']:
                #     per = feat_dict.dictionaries['perFeatures'][feat]
                #     f = Feature('person',None,per)
                #     features.append(f)
                # elif feat in feat_dict.dictionaries['genFeatures']:
                #     gen = feat_dict.dictionaries['genFeatures'][feat]
                #     f = Feature('gender',None,gen)
                #     features.append(f)
                # elif feat in feat_dict.dictionaries['perNumFeatures']:
                #     per, num = feat_dict.dictionaries['perNumFeatures'][feat]
                #     f = Feature('number', None, num)
                #     features.append(f)
                #     f = Feature('person', None, per)
                #     features.append(f)
                # elif feat in feat_dict.dictionaries['perGenFeatures']:
                #     per, gen = feat_dict.dictionaries['perGenFeatures'][feat]
                #     f = Feature('person',None,per)
                #     features.append(f)
                #     f = Feature('gender',None,gen)
                #     features.append(f)
                # elif feat in feat_dict.dictionaries['perNumGenFeatures']:
                #     per, num, gen = feat_dict.dictionaries['perNumGenFeatures'][feat]
                #     f = Feature('person', None, per)
                #     features.append(f)
                #     f = Feature('number', None, num)
                #     features.append(f)
                #     f = Feature('gender', None, gen)
                #     features.append(f)
                # elif feat.lower() in feat_dict.dictionaries['perNumInclFeatures']:
                #     p, n, i = feat_dict.dictionaries['perNumInclFeatures'][feat.lower()]
                #     if 'non' in p:
                #         p = 'n'
                #     else:
                #         p = re.sub('[a-z]', '', p)
                #     val = p + n + '_' + i
                #     f = Feature('pernum', None, val)
                #     features.append(f)
        return features


    def add_lexitem(self, pred, orth, features, lexitem_classes,xigt_item, bare_lexitem_list):
        orth = re.sub('~~~','-',orth) #KPH xigtreader changes - to ~~~ to prevent tokenization issues. I'm changing them back here
        stem = Stem(pred, orth, self.pos_tag)
        id = len(self.lexitems) + 1
        if lexitem_classes:
            new_lexitem = LexicalItem(features, self.pos_tag, id,xigt_item.transitivity, xigt_item.case_frame)
            new_lexitem.add_stem(stem)
            new_lexitem.set_parent(self)

            # if there is only one morpheme in the xigt_item, then it's bare (has no affixes)
            if len(xigt_item.ordered_morphemes) == 1:
                bare_lexitem = None
                # look for an existing lexitem (i.e. word class) that has the same transitivity and case frame as this xigt_item
                for bli in bare_lexitem_list:
                    # if found, add the current stem to that lexitem
                    if bli.transitivity == xigt_item.transitivity and bli.case_frame == xigt_item.case_frame:
                        bare_lexitem = bli
                        bare_lexitem.add_stem(stem)
                        #KPH removed the following because keeping fake transitivity items seperate reduces ambiguity. Besides, how would we choose between intrans and trans
                        #if not bare_lexitem.case_frame and xigt_item.case_frame:
                        #    bare_lexitem.case_frame = xigt_item.case_frame
                        #    other_item_features = self.aligned_case_features(xigt_item,'verb')
                        #    for f in other_item_features:
                        #        bare_lexitem.add_feature(f)
                        #if (bare_lexitem.transitivity == None or bare_lexitem.transitivity == FAKE_TRANSITIVITY) \
                        #        and xigt_item.transitivity != FAKE_TRANSITIVITY:
                        #    bare_lexitem.transitivity = xigt_item.transitivity
                # if no compatible bare_lexitem was found, make a new lexitem, add the stem
                if not bare_lexitem:
                    bare_lexitem = new_lexitem
                    bare_lexitem.is_bare = True
                    self.lexitems.add(bare_lexitem)
                    if self.verbose:
                        print('Creating new lexitem for bare stem {0} glossed {1}'.format(orth, pred))
                return bare_lexitem

            # if it's not bare, check existing lexitems for a compatible lexitem for this orth+pred pair
            for lexitem in list(self.lexitems):
                    for stem in lexitem.stems:
                        if stem.orth == orth and stem.basic_pred == pred:
                            if same_case_frame(lexitem,xigt_item) and same_transitivity(lexitem,xigt_item):
                                lexitem.add_stem(stem)
                                if not lexitem.case_frame and xigt_item.case_frame:
                                    lexitem.case_frame = xigt_item.case_frame
                                    other_item_features = self.aligned_case_features(xigt_item,'verb')
                                    for f in other_item_features:
                                        lexitem.add_feature(f)
                                if (not lexitem.transitivity) or lexitem.transitivity == FAKE_TRANSITIVITY:
                                    lexitem.transitivity = xigt_item.transitivity
                                return lexitem
                            #else:
                                #print('Different case frame or transitivity: '
                                #      'igt {0}, word {1} ({2})'.format(xigt_item.parent_igt.id,
                                #                                       xigt_item.original_id,orth))
        else:
            new_lexitem = LexicalItem(features, self.pos_tag, id,xigt_item.transitivity, xigt_item.case_frame)
            if len(self.lexitems) == 0:
                if not stem in new_lexitem.stems:
                    new_lexitem.add_stem(stem)
                self.lexitems.add(new_lexitem)
                if self.verbose:
                    print('Creating new lexitem for stem {0} glossed {1}'.format(orth,pred))
                self.lexitem_ids.add(new_lexitem.id)
                return new_lexitem
            else:
                li = list(self.lexitems)[0]
                if not stem in li.stems:
                    li.add_stem(stem)
                return li
        if new_lexitem.id in self.lexitem_ids:
            raise Exception("id {0} is already in lexitems".format(new_lexitem.id))
        self.lexitems.add(new_lexitem)
        if self.verbose:
            print('Creating new lexitem for stem {0} glossed {1}'.format(orth,pred))
        self.lexitem_ids.add(new_lexitem.id)
        return new_lexitem

    def add_position_class(self, affix, affix_features,input, is_prefix, root, is_zero=False):
        affix.orth = re.sub('~~~','-',affix.orth) #KPH xigtreader changes - to ~~~ to prevent tokenization issues. I'm changing them back here
        is_clitic = affix.type == "enclitic" # KPH 4/12/19 Changed clitic to enclitic
        # (although this can probably be deleted because where Lexical_Rule_Instance
        # was checking to add = or - was redundant and has been removed
        lri = Lexical_Rule_Instance(affix.orth, is_prefix, is_clitic, self.hyphens, self.escape_special_characters,
                                    inflecting=not is_zero)
        known_type = affix.known_affix_type if not is_zero else None
        if self.output_glosses:
            lrt = Lexical_Rule_Type(features=affix_features, root=root, glosses=affix.glosses,
                                    is_prefix=is_prefix,is_zero=is_zero)
        else:
            lrt = Lexical_Rule_Type(features=affix_features, root=root, glosses=None,
                                    is_prefix=is_prefix,is_zero=is_zero)
        lrt.add_instance(lri)
        zero_lrts = []
        all_zero_feats = []
        zero_marked_features_copy = copy.deepcopy(self.zero_marked_features)
        if affix_features:
            for fs in zero_marked_features_copy:
                for f in fs:
                    if f not in all_zero_feats:
                        all_zero_feats.append(f)
            # first look for a perfect match of individual or portmanteau features
            for zero_feature_set in zero_marked_features_copy:
                if matching_feature_types(zero_feature_set, affix_features) and not same_feature_values(
                        zero_feature_set, affix_features):
                    non_infl_lri = Lexical_Rule_Instance('', is_prefix, is_clitic, False,
                                                         self.escape_special_characters,
                                                         inflecting=False)
                    non_infl_lrt = Lexical_Rule_Type(features=zero_feature_set, root=root, glosses=None,
                                                     is_prefix=is_prefix, is_zero=True)
                    non_infl_lrt.add_instance(non_infl_lri)
                    zero_lrts.append(non_infl_lrt)
                    is_zero = True
            # if we didn't find a perfect match, look for a zero feat in the overt portmanteau feat set
            if not is_zero:
                for zero_feature_set in zero_marked_features_copy:
                    for zero_feat in zero_feature_set:
                        if any([True for affix_feat in affix_features if matching_feature_types([zero_feat], \
                                        [affix_feat]) and not same_feature_values([zero_feat], [affix_feat])]):
                            non_infl_lri = Lexical_Rule_Instance('', is_prefix, is_clitic, False,
                                                                 self.escape_special_characters,
                                                                 inflecting=False)
                            non_infl_lrt = Lexical_Rule_Type(features=[zero_feat], root=root, glosses=None,
                                                             is_prefix=is_prefix, is_zero=True)
                            non_infl_lrt.add_instance(non_infl_lri)
                            if non_infl_lrt not in zero_lrts:
                                zero_lrts.append(non_infl_lrt)
                                is_zero = True

        for pc in self.pcs:
            match = False
            if pc.known_type:
                for g in affix.glosses:
                    precluster_match_string = g if self.precluster_type == 'gloss' else affix.orth
                    match = re.match(pc.known_type,precluster_match_string)
                    if match:
                        break
            if (pc.known_type and match):
                res = pc.add_input(input)
                if res:
                    if not lrt in pc.lexical_rule_types:
                        pc.add_lexical_rule_type(lrt)
                        for zero_lrt in zero_lrts:
                            if not zero_lrt in pc.lexical_rule_types:
                                pc.add_lexical_rule_type(zero_lrt)
                        pc.is_oblig = is_zero
                    return pc
                else:
                    new_pc = self.get_copy_pc(is_prefix, lrt, input, pc)
                    new_pc.known_type = pc.known_type
                    for zero_lrt in zero_lrts:
                        if not zero_lrt in new_pc.lexical_rule_types:
                            new_pc.add_lexical_rule_type(zero_lrt)
                    new_pc.is_oblig = is_zero
                    self.relevant_pcs.append(new_pc)
                    return new_pc
            elif pc.has_lexical_rule_type(lrt) and pc.is_prefix == is_prefix:
                #KPH in this case I don't think it's necessary to add the zero, because presumably it was already added
                res = pc.add_input(input)
                if res:
                    pc.is_oblig = is_zero
                    return pc
                else:
                    new_pc = self.get_copy_pc(is_prefix, lrt, input, pc)
                    new_pc.is_oblig = is_zero
                    return new_pc
        new_pc = self.add_new_pc_for_input(is_prefix,lrt,input, known_type)
        for zero_lrt in zero_lrts:
            if not zero_lrt in new_pc.lexical_rule_types:
                new_pc.add_lexical_rule_type(zero_lrt)
        new_pc.is_oblig = is_zero
        self.pcs.append(new_pc)
        if new_pc.known_type or not self.preclustered_only:
            self.relevant_pcs.append(new_pc)
        if self.verbose:
            print('Creating new PC for {0}'.format(affix.orth))
        return new_pc

    def get_copy_pc(self,is_prefix, lrt, input, pc):
        if pc in self.copy_pcs:
            for copy_pc in self.copy_pcs[pc]:
                res = copy_pc.add_input(input)
                if res:
                    return copy_pc
            new_pc = self.add_new_pc_for_input(is_prefix,lrt,input)
            if self.verbose:
                print ('Creating an additional copy of PC to avoid a cycle: {0} -> {1}'.format(pc.id, new_pc.id))
            self.pcs.append(new_pc)
            if (new_pc.known_type or not self.known_affix_types): # can this logically happen?
                self.relevant_pcs.append(new_pc)
            self.copy_pcs[pc].append(new_pc)
            return new_pc
        else:
            self.copy_pcs[pc] = []
            new_pc = self.add_new_pc_for_input(is_prefix,lrt,input)
            if self.verbose:
                print ('Creating an additional copy of PC to avoid a cycle: {0} -> {1}'.format(pc.id, new_pc.id))
            self.pcs.append(new_pc)
            if (new_pc.known_type or not self.known_affix_types): # can this logically happen?
                self.relevant_pcs.append(new_pc)
            self.copy_pcs[pc].append(new_pc)
            return new_pc

    def add_new_pc_for_input(self, is_prefix, lrt, input, known_type=None):
        new_pc = Position_Class(is_prefix, self.pos_tag, known_type=known_type,patterns=self.known_affix_types)
        id = len(self.pcs) + 1 #self.pc_total
        new_pc.setID(id)
        new_pc.add_lexical_rule_type(lrt)
        new_pc.add_input(input)
        new_pc.set_parent(self)
        return new_pc

    def get_id(self):
        return None

    def index(self, object):
        if object in self.lexitems:
            return list(self.lexitems).index(object)
        elif object in self.pcs:
            return self.pcs.index(object)
        else:
            raise Exception("Object not in Lexicon\n",str(object))

class Choice:
    def set_parent(self, parent):
        self.parent = parent

    def get_id(self):
        if self.parent.get_id() is not None:
            return self.parent.get_id()+"_"+self.get_name()+str(self.parent.index(self)+1)
        else:
            return self.get_name()+str(self.parent.index(self)+1)

    def get_name(self):
        raise Exception("Prototype Function undefined")

class Feature(Choice):
    def __init__(self, name, head, value):
        self.name = name
        self.head = head
        self.value = value

    def __str__(self):
        return self.name + ' ' + self.value + ' ' + self.head

    def __repr__(self):
        return self.name + ' ' + self.value + ' ' + self.head

    def __eq__(self, object):
        if isinstance(object, Feature):
            if self.get_value() == object.get_value():
                return True
            else:
                return False
        else:
            return False

    def get_value(self):
        return self.value

    def get_name(self):
        return "feat"

class Stem(Choice):
    def __init__(self, pred, orth, pos_tag):
        self.orth = re.sub('\"','\'',orth.strip('.,')).lower()
        match = re.match("(_\w+)_\w_rel", pred)
        if match:
            self.pred = pred
            self.basic_pred = match.groups(1)
        else:
            self.basic_pred = pred
            #TODO: this will screw up things like "adv"
            if "V" in pos_tag or "v" in pos_tag:
                self.pred = "_"+pred+"_v_rel"
            elif "N" in pos_tag or "n" in pos_tag:
                self.pred = "_"+pred+"_n_rel"

    def __eq__(self, object):
        if isinstance(object, Stem):
            if self.orth == object.get_orth() and self.pred == object.get_pred():
                return True
            else:
                return False
        else:
            return False

    def get_orth(self):
        return self.orth

    def get_pred(self):
        return self.pred

    def get_name(self):
        return "stem"

class LexicalItem(Choice):
    def __init__(self, features, pos_tag, id, transitivity, case_frame):
        self.pos_tag = pos_tag
        self.is_bare = False
        self.is_pc = False
        self.maximal_construct = {'prefix':OrderedDict(), 'suffix':OrderedDict()}
        self.features = []
        self.stems = []
        self.inputs = set()
        self.outgoing_edges = set()
        self.relevant_outputs = set() # if need to compute overlap only in terms of specific outputs
        self.good_edges = set()
        if id == 0:
            raise Exception("Lexical Item ID must not be 0 to support defaultdict")
        self.id = id#*(-10) #to distinguish from position classes
        self.cannot_remove = False
        for feature in features:
            self.add_feature(feature)
        self.transitivity = transitivity
        self.case_frame = case_frame

    def __eq__(self, object):
        if isinstance(object, LexicalItem):
            #if self.matches_features(object.features) and self.matches_stems(object.stems):
            #    return True
            #else:
            #    return False
            return self.id == object.id
        elif isinstance(object,Position_Class):
            return False
        else:
            raise Exception("Trying to compare a Lexical Item to something else.")

    def __hash__(self):
        return hash(self.id)
        #return hash(self.get_id())

    def __str__(self):
        return 'lexitem' + str(self.id)

    def __repr__(self):
        return 'lexitem' + str(self.id)

    def indegree(self):
        return 0

    def outdegree(self):
        return len(self.outgoing_edges)

    def compute_overlap(self, node_2):
        if not (same_transitivity(self,node_2) or same_case_frame(self,node_2)):
            return 0.0
        shared = 0
        lst1 = list(self.relevant_outputs)
        lst2 = list(node_2.relevant_outputs)
        total1 = len(lst1)
        total2 = len(lst2)
        for edge in lst1:
            if edge in lst2:
                shared += 1
        if total2 + total1 - shared == 0:
            return 0.0 #TODO: what to do here?
        return float(shared)/float(total2 + total1 - shared)


    def merge(self,other):
        if self.transitivity == FAKE_TRANSITIVITY \
                and other.transitivity != FAKE_TRANSITIVITY and other.transitivity is not None:
            #print('Assigning transitivity via merge.')
            self.transitivity = other.transitivity
            if not self.case_frame and other.case_frame is not None:
                self.case_frame = other.case_frame
                for f in other.features:
                    self.add_feature(f)
        for stem in other.stems:
            if not stem in self.stems:
                if stem.orth == 'chaina':
                    print('Adding CHAINA to transitivity {0}'.format(self.transitivity))
                self.stems.append(stem)
                stem.parent = self

    def matches_features(self, features):
        if len(features) != len(self.features):
            return False
        for feature in features:
            if not self.has_feature(feature):
                return False
        return True

    def has_feature(self, feature):
        for feat in self.features:
            if feature == feat:
                return True
        return False

    def add_feature(self, feature):
        feature.set_parent(self)
        self.features.append(feature)

    def matches_stems(self, stems):
        if len(stems) != len(self.stems):
            return False
        for stem in stems:
            if not self.has_stem(stem):
                return False
        return True

    def has_stem(self, s):
        for stem in self.stems:
            if stem == s:
                return True
        return False

    def add_stem(self, new_stem):
        for stem in self.stems:
            if stem == new_stem:
                return stem
        new_stem.set_parent(self)
        self.stems.append(new_stem)
        return new_stem

    def get_id(self):
        return self.get_name() + str(self.id)

    def get_name(self):
        #TODO: fix this for adv
        if "V" in self.pos_tag or "v" in self.pos_tag:
            return "verb"
        else:
            return "noun"

    def index(self, object):
        if object in self.features:
            return self.features.index(object)
        elif object in self.stems:
            return self.stems.index(object)
        else:
            raise Exception("Object not in verb or noun")

class Lexical_Rule_Instance(Choice):
    def __init__(self, orth, is_prefix, is_clitic, hyphens, escape_special_characters, inflecting=True):
        self.orth = orth.strip('.,').lower() if inflecting else None
        self.inflecting = inflecting
        self.is_prefix = is_prefix
        self.hyphens = hyphens
        if escape_special_characters:
            chars = ['!', '\(', '\)', '\%']
            if self.orth:
                for char in chars:
                    self.orth = re.sub(char, '\\' + char, self.orth)

    def __eq__(self, object):
        if isinstance(object, Lexical_Rule_Instance):
            if self.orth == object.orth and self.inflecting == object.inflecting:
                return True
            else:
                return False
        else:
            return False

    def __str__(self):
        return self.orth

    def __repr__(self):
        return self.orth

    def get_name(self):
        return "lri"

class Lexical_Rule_Type(Choice):
    def __init__(self, features, root, glosses=None, is_prefix=None, is_zero=False):
        self.features = []
        self.instances = []
        self.root = root
        self.is_zero = is_zero
        self.glosses = '.'.join(g for g in glosses) if not is_zero else '.'.join(f.value for f in features)
        self.all_glosses = glosses if glosses else []
        for feature in features:
            self.add_feature(feature)
        is_prefix = is_prefix
        self.parent = None

    def __str__(self):
        return self.root  +' ' + self.glosses

    def __repr__(self):
        return self.root  +' ' + self.glosses

    def __eq__(self, object):
        if isinstance(object, Lexical_Rule_Type):
            if object.matches_features(self.features) and object.matches_instances(self.instances):
                return True
            else:
                return False
        else:
            return False

    def __hash__(self):
        return hash(id(self))

    def merge(self, other):
        assert self.matches_features(other.get_features()), "weird merge..."
        for instance in other.get_instances():
            self.add_instance(instance)
        self.all_glosses.append(other.glosses)

    def matches_instances(self, instances):
        if len(instances) != len(self.instances):
            return False
        for instance in instances:
            if not self.has_instance(instance):
                return False
        return True

    def has_instance(self, instance):
        for inst in self.instances:
            if inst == instance:
                return True
        return False

    def matches_features(self, features):
        if len(features) != len(self.features):
            return False
        for feature in features:
            if not self.has_feature(feature):
                return False
        return True

    def has_feature(self, feature):
        for feat in self.features:
            if feature == feat:
                return True
        return False

    def add_feature(self, feature):
        if not self.has_feature(feature):
            feature.set_parent(self)
            self.features.append(feature)

    def add_instance(self, instance):
        if not self.has_instance(instance):
            assert self.is_zero != instance.inflecting
            instance.set_parent(self)
            self.instances.append(instance)

    def get_name(self):
        return "lrt"

    def get_features(self):
        return self.features

    def get_instances(self):
        return self.instances

    def index(self, object):
        if object in self.features:
            return self.features.index(object)
        elif object in self.instances:
            return self.instances.index(object)
        else:
            raise Exception("Object not in lrt")

class Position_Class(Choice):
    def __init__(self, is_prefix, pos_tag, known_type=None,patterns=None,all_relevant=True):
        self.id = -1
        self.is_pc = True
        self.known_type = known_type
        self.patterns = patterns
        self.all_relevant = all_relevant
        self.inputs = set() #incoming edges
        self.outgoing_edges = set()
        self.good_edges = set()  # outgoing edges form a spanning tree
        self.pos_tag = pos_tag
        self.cycles_checked = set()
        self.cycles_checked.add(self)
        self.cycles_found = set()
        self.cycles_found.add(self)
        self.lexical_rule_types = []
        self.feature_types = set()
        self.is_prefix = is_prefix
        self.mirrorred = None
        self.cannot_remove = False

    def outdegree(self):
        return len(self.outgoing_edges)

    def indegree(self):
        return len(self.inputs)

    def copy_node_with_no_edges(self):
        copy_pc = Position_Class(self.is_prefix,self.pos_tag,patterns=self.patterns)
        copy_pc.lexical_rule_types = self.lexical_rule_types.copy()
        copy_pc.feature_types = self.feature_types.copy()
        return copy_pc

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not (isinstance(other,Position_Class) or isinstance(other, LexicalItem)):
            raise Exception("Trying to compare a position class to something else.")
        return id(self) == id(other)


    def __str__(self):
        return 'pc' + str(self.id)

    def __repr__(self):
        return 'pc' + str(self.id)

    def setID(self,id):
        if id == 0:
            raise Exception("Position class ID must not be 0 to support defaultdict")
        self.id = id

    def get_int_id(self):
        return self.id

    def get_id(self):
        pos = "NONE"
        #TODO: fix this for "adv"
        if "V" in self.pos_tag or "v" in self.pos_tag:
            pos = "verb"
        if "N" in self.pos_tag or "n" in self.pos_tag:
            pos = "noun"
        return pos + "-pc" + str(self.id)

    def add_lexical_rule_type(self, lrt):
        if not self.has_lexical_rule_type(lrt):
            lrt.set_parent(self)
            self.lexical_rule_types.append(lrt)
            for feature in lrt.features:
                self.feature_types.add(feature.name)

    def has_feature_type(self, feat_name):
        return feat_name in self.feature_types


    def merge(self, other):
        for input in other.get_inputs():
            self.add_input(input)
        for lrt in other.get_lexical_rule_types():
            match_found = False
            for own_lrt in self.lexical_rule_types:
                if lrt.matches_features(own_lrt.get_features()) and lrt.is_zero == own_lrt.is_zero:
                    own_lrt.merge(lrt)
                    match_found = True
            if not match_found:
                self.add_lexical_rule_type(lrt)

    def compute_overlap(self, node_2):
        if intransitive_input(node_2) and comp_features(self):
            return 0.0
        if intransitive_input(self) and comp_features(node_2):
            return 0.0
        if self.is_prefix != node_2.is_prefix \
                or self.cycle_found(0, node_2) \
                or node_2.cycle_found(0, self):
            return 0.0
        else:
            shared = 0
            for input in self.get_inputs():
                if node_2.has_input(input):
                    shared += 1
            if len(node_2.get_inputs())+len(self.inputs)-shared == 0:
                return 0.0 #TODO What to do here?
            return float(shared)/float(len(node_2.get_inputs())+len(self.inputs)-shared)

    def add_input(self, input):
        if id(self) == id(input):
            #print ("Cannot add self as input to self: {0}".format(self.get_id()))
            return False
        if not self.has_input(input):
            if issubclass(input.__class__, Position_Class):
                if not input.cycle_found(0, self):
                    self.inputs.add(input)
                    input.outgoing_edges.add(self)
                    return True
                else:
                    assert self not in input.outgoing_edges
                    #print ("Cannot add input: cycle found between {0} and {1}".format(self.get_id(),input.get_id()))
                    return False
            else:
                self.inputs.add(input)
                input.outgoing_edges.add(self)
                if (self.known_type or not self.patterns) or self.all_relevant:
                    input.relevant_outputs.add(self)
                return True
        else: #already has it as input
            input.outgoing_edges.add(self)
            if isinstance(input,LexicalItem) and (self.known_type or not self.patterns):
                input.relevant_outputs.add(self)
            return True


    def cycle_found_original(self, depth, node):
        #print "SELF:"+str(self.get_id());
        #try:
        #print "NODE:"+str(node.get_id());
        #except:
        #print "NEW NODE:"+str(node);
        #        print("PC1: ", self.id)
        #        if depth > 100:
        #            print('stop')
        #        print("PC2: ", node.id)
        #        print ("depth: ", depth)
        depth +=1
        if self.has_input(node):
            return True;
        for input in self.get_inputs():
            if issubclass(input.__class__, Position_Class):
                if input.cycle_found(depth, node):
                    return True;
        return False;


    def cycle_found(self,depth, target):
        path = []
        marked = []
        qu = queue.Queue()
        marked.append(self)
        qu.put(self)
        while not qu.empty():
            n = qu.get()
            path.append(n)
            if isinstance(n, Position_Class) and isinstance(target,Position_Class):
                if n.id == target.id:
                    return True
            for i in n.inputs:
                if not i in marked:
                    marked.append(i)
                    qu.put(i)
        return False



    def remove_input(self, input):
        assert input in self.inputs, "Can't remove what isn't there."
        if len(self.inputs) == 1:
            #print('Cannot delete last input from ', input.get_id())
            return False
        else:
            self.inputs.remove(input)
            return True

    def has_input(self, input):
        if input in self.inputs:
            return True
        else:
            return False

    def get_lexical_rule_types(self):
        return self.lexical_rule_types

    def get_inputs(self):
        return self.inputs

    def has_lexical_rule_type(self, lrt):
        for lexical_rule_type in self.lexical_rule_types:
            if lrt == lexical_rule_type:
                return True
        return False

    def get_name(self):
        #TODO: fix this for adv
        if "V" in self.pos_tag or "v" in self.pos_tag:
            return "verb"
        else:
            return "noun"

    def index(self, object):
        if object in self.inputs:
            return self.inputs.index(object)
        elif object in self.lexical_rule_types:
            return self.lexical_rule_types.index(object)
        else:
            raise Exception("Object not in pc")


def same_case_frame(lexitem,xigt_item):
    if not lexitem.case_frame or not xigt_item.case_frame:
        return True

    # ECC: if the number of keys in the two case frames isn't the same then they don't have the same frame
    if len(lexitem.case_frame.keys()) != len(xigt_item.case_frame.keys()):
        return False

    for key in xigt_item.case_frame:
        if not (key in lexitem.case_frame and lexitem.case_frame[key] == xigt_item.case_frame[key]):
            return False
    return True

def same_transitivity(lexitem,xigt_item):
    if not lexitem.transitivity or not xigt_item.transitivity:
        return True
    if lexitem.transitivity == FAKE_TRANSITIVITY or xigt_item.transitivity == FAKE_TRANSITIVITY:
        return True
    return lexitem.transitivity == xigt_item.transitivity


def validate_feature(gram):
    feature = gram.lower()
    if feature in feat_dict.internal_feature_name:
        feature = feature+"_feat"
    assert feature is not None, "None isn't a valid feature."
    return feature

def combine_feature_values(features):
    # KPH the GM will not allow multiple separate featurs with the same name. Instead they should be listed as
    # multiple values under the same feature. Then the GM will create a disjunctive type for the feature values
    combined_features = []
    for f in features:
        if any((f.name == cf.name and f.head == cf.head) for cf in combined_features):
            for cf in combined_features:
                if f.name == cf.name and f.head == cf.head:
                    if ', ' + f.value not in cf.value and not cf.value.startswith(f.value+','):
                        cf.value = cf.value + ', ' + f.value
        else:
            combined_features.append(f)
    return combined_features

def most_common(lst):
    return max(set(lst), key=lst.count)

def build_matrix_choices(verb_lex,noun_lex, settings):
    mc = MatrixChoices.ChoiceDict()
    if verb_lex:
        for lexitem in verb_lex.lexitems:
            homonyms = {}
            homonyms[lexitem.get_id()] = {}
            mc[lexitem.get_id()+'_name'] = lexitem.get_id()
            #if len(lexitem.features) == 0 and lexitem.transitivity != FAKE_TRANSITIVITY:
                #print('NO FEATURES ON A VERB {0}'.format(lexitem.get_id()))
            process_orths_and_val(homonyms, lexitem, mc, 'v', settings.inference)
            combined_features = combine_feature_values(lexitem.features)
            for f in combined_features:
                if f.name and f.value and f.head:
                    mc[f.get_id() + '_name'] = f.name
                    mc[f.get_id() + '_value'] = f.value
                    mc[f.get_id() + '_head'] = f.head
        build_matrix_pcs(verb_lex, 'verb', mc)
    if noun_lex:
        for lexitem in noun_lex.lexitems:
            mc[lexitem.get_id()+'_name'] = lexitem.get_id()
            homonyms = {}
            homonyms[lexitem.get_id()] = {}
            process_orths_and_val(homonyms, lexitem, mc, 'n', settings.inference)
        build_matrix_pcs(noun_lex, 'noun', mc)
    return mc


def build_matrix_pcs(lexicon, pos, mc):
     for pc in lexicon.pcs:
        mc[pc.get_id() + '_name'] = pc.get_id()
        mc[pc.get_id() + '_order'] = 'prefix' if pc.is_prefix else 'suffix'
        mc[pc.get_id() + '_inputs'] = ', '.join([ i.get_id() for i in pc.inputs])
        if pc.is_oblig:
            mc[pc.get_id() + '_obligatory'] = 'on'
        for lrt in pc.lexical_rule_types:
            mc[lrt.get_id() + '_name'] = lrt.get_id()
            combined_features = combine_feature_values(lrt.features)
            for f in combined_features:
                if pos == 'verb' and not f.head:
                    continue
                if f.name and f.value:
                    mc[f.get_id() + '_name'] = f.name
                    mc[f.get_id() + '_value'] = f.value
                if f.head:
                    mc[f.get_id() + '_head'] = f.head
            for lri in lrt.instances:
                if lri.orth:
                    mc[lri.get_id() + '_inflecting'] = 'yes'
                    mc[lri.get_id() + '_orth'] = lri.orth
                else:
                    mc[lri.get_id() + '_inflecting'] = 'no'


def process_orths_and_val(homonyms, lexitem, mc, pos, inference):

    rel_str = '_' + pos + '_rel'
    for s in lexitem.stems:
        if not s.orth in homonyms[lexitem.get_id()]:
            homonyms[lexitem.get_id()][s.orth] = []
        homonyms[lexitem.get_id()][s.orth].append(s.basic_pred)
    for i, orth in enumerate(homonyms[lexitem.get_id()]):
        if lexitem.transitivity == FAKE_TRANSITIVITY and inference:
            new_orth = orth + '~'
            valence = 'trans'
        else:
            new_orth = orth
            valence = lexitem.transitivity if (lexitem.transitivity and not lexitem.transitivity == FAKE_TRANSITIVITY) \
                else 'trans'
        mc[lexitem.get_id()+'_valence'] = valence
        mc[lexitem.get_id() + '_' + 'stem' + str(i + 1) + '_' + 'orth'] = new_orth
        mc[lexitem.get_id() + '_' + 'stem' + str(i + 1) + '_' + 'pred'] \
            = '_' + '-or-'.join(sorted(homonyms[lexitem.get_id()][orth])) + rel_str

'''
Rebuild the lexicon using only longest paths between nodes
'''
def rebuild_lexicon(lexicon):
    for lexitem in lexicon.lexitems:
        rebuild_inputs_outputs(lexitem)
    for pc in lexicon.pcs:
        rebuild_inputs_outputs(pc)

def rebuild_inputs_outputs(lexitem):
    llp_list = []
    for e in lexitem.longest_paths:
        llp_e = lexitem.longest_paths[e]
        llp_e_tuples = tuples_path(llp_e, e)
        llp_list.extend(llp_e_tuples)
    llp_set = set(llp_list)
    for e in list(lexitem.outgoing_edges):
        if (lexitem.get_id(), e.get_id()) not in llp_set:
            lexitem.outgoing_edges.remove(e)
            e.inputs.remove(lexitem)


'''
Turn a list of nodes into list of tuples,
e.g.
input: [lexitem1,verb-pc1,verb-pc2], verb-pc3
output: [(lexitem1, verb-pc1), (verb-pc1,verb-pc2), (verb-pc2,verb-pc3)]
This is useful to figure out if a specific edge is on the longest path in the graph.
'''
def tuples_path(path, target):
    tuples = []
    for i,node in enumerate(path):
        if i < len(path)-1:
            tuples.append((node.get_id(),path[i+1].get_id()))
        else:
            tuples.append((node.get_id(),target))
    return tuples

def strip_grams(gloss,pos):
    pred_value = ''
    glosses = re.split('\.',gloss)
    pronoun_features = {}
    pronoun_features.update(feat_dict.dictionaries['caseFeatures'].copy())
    pronoun_features.update(feat_dict.dictionaries['perFeatures'].copy())
    pronoun_features.update(feat_dict.dictionaries['numFeatures'].copy())
    pronoun_features.update(feat_dict.dictionaries['genFeatures'].copy())
    pronoun_features.update(feat_dict.dictionaries['perGenFeatures'].copy())
    pronoun_features.update(feat_dict.dictionaries['perNumFeatures'].copy())
    pronoun_features.update(feat_dict.dictionaries['perNumGenFeatures'].copy())
    pronoun_features.update(feat_dict.dictionaries['perGenHeadFeatures'].copy())
    pronoun_features.update(feat_dict.dictionaries['perNumHeadFeatures'].copy())
    pronoun_features.update(feat_dict.dictionaries['perNumCaseFeatures'].copy())
    pronoun_features.update(feat_dict.dictionaries['perNumInclFeatures'].copy())
    pronoun_features.update(feat_dict.dictionaries['perHeadFeatures'].copy())
    pronoun_features.update(feat_dict.dictionaries['perNumInclHeadFeatures'].copy())
    # KPH construct a new pred value without grams
    for g in glosses:
        if g != '':
            if g.lower() not in feat_dict.all_keys:
                pred_value += g+'.'
            else:
                if pos == 'noun': #this is an attempt to preserve pronoun features so that they can be added to the lexical items in inference
                    if g.lower() in pronoun_features:
                        pred_value += g + '.'
    # KPH if the origional pred only contained grams, include them in the pred value
    if pred_value == '':
        pred_value = gloss
    if pred_value != '':
        if pred_value[-1] == '.':
            pred_value = pred_value[:-1]
    return pred_value

def has_lemma(glosses):
    lemma = False
    for gloss in glosses:
        gloss_list = re.split('\.', gloss)
        for g in gloss_list:
            if g != '':
                if g.lower() not in feat_dict.all_keys:
                    lemma = True
    return lemma

def intransitive_input(node):
    intrans_input = False
    for input in node.inputs:
        if type(input) == LexicalItem:
            if input.transitivity == 'intrans':
                intrans_input = True
    return intrans_input

def comp_features(node):
    comp_feat = False
    for lrt in node.lexical_rule_types:
        for feat in lrt.features:
            if feat.head == 'obj':
                comp_feat = True
    return comp_feat

def matching_feature_types(feature_set_1, feature_set_2):
    match = True
    if len(feature_set_1) != len(feature_set_2):
        return False
    for feat1 in feature_set_1:
        for feat2 in feature_set_2:
            if feat1.head != feat2.head:
                return False
            if feat1.name != feat2.name:
                return False
    return match

def same_feature_values(feature_set_1, feature_set_2):
    match = True
    for feat1 in feature_set_1:
        for feat2 in feature_set_2:
            if feat1.value != feat2.value:
                return False
    return match
