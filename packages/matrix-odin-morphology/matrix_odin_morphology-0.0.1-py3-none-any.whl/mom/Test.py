import sys
import unittest
import argparse
import MainClasses,Choices
from mom.XigtifiedToolbox import XigtReader

parser = argparse.ArgumentParser(description="Loads a settings file and runs a set of tests.")

parser.add_argument("-s", "--settings", help="The name of the configuration file.")

parser.add_argument("-v", "--verbose", help="Verbose output", action='store_true')

args = parser.parse_args()

# Example test
class TestCaseConfigLoad(unittest.TestCase):
    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

# This test no longer works because the function is now written for node objects
# that have a get_id() functions (which integers do not).
# class TestCaseNodes2Tuples(unittest.TestCase):
#     def test_list2tuples(self):
#         l = [1,2,3]
#         target = 4
#         tuples = Choices.tuples_path(l,target)
#         self.assertEqual(len(tuples),3)
#         self.assertEqual(tuples[0], (1,2))
#         self.assertEqual(tuples[1], (2,3))
#         self.assertEqual(tuples[2], (3,4))

class TestCaseRemoveRedundantEdges(unittest.TestCase):
    # def test_redundant_real_lexicon(self):
    #     lexicon = create_lexicon()
    #     paths = lexicon.depth_first_traversal(list(lexicon.lexitems)[0])
    #     self.assertEqual(len(paths), 3)
    #     self.assertEqual(len(paths['verb-pc1']),1)
    #     self.assertEqual(len(paths['verb-pc2']),2)
    #     self.assertEqual(len(paths['verb-pc3']),4)
    #     lexicon.traverse_lexicon_llp()
    #     Choices.rebuild_lexicon(lexicon)
    #     # Now there should only be one long path in the graph.
    #     self.assertEqual(len(list(lexicon.lexitems)[0].outgoing_edges),1)
    #     self.assertEqual(len(list(lexicon.pcs)[0].outgoing_edges),1)
    #     self.assertEqual(len(list(lexicon.pcs)[1].outgoing_edges),1)
    #     self.assertEqual(len(list(lexicon.pcs)[2].outgoing_edges),0)
    # A graph with 3 nodes and one redundant edge
    def test_redundant1(self):
        lexicon = Choices.Lexicon(pos_tag='verb')
        lexicon.lexitems = set()
        lexicon.pcs = []
        li1 = Choices.LexicalItem(features=[],pos_tag='verb',id=1,transitivity=None,case_frame=None)
        pc1 = Choices.Position_Class(is_prefix=False,pos_tag='verb')
        pc2 = Choices.Position_Class(is_prefix=False,pos_tag='verb')
        pc1.id = 'verb-pc1'
        pc2.id = 'verb-pc2'
        li1.outgoing_edges.add(pc1)
        li1.outgoing_edges.add(pc2)
        pc1.outgoing_edges.add(pc2)
        pc2.inputs.add(pc1)
        pc2.inputs.add(li1)
        lexicon.lexitems.add(li1)
        lexicon.pcs.append(pc1)
        lexicon.pcs.append(pc2)
        lexicon.traverse_lexicon_llp()
        Choices.rebuild_lexicon(lexicon)
        self.assertEqual(len(li1.outgoing_edges),1)
        self.assertEqual(pc2 in li1.outgoing_edges, False)
        self.assertEqual(pc1 in li1.outgoing_edges, True)
        self.assertEqual(pc2 in pc1.outgoing_edges, True)
        self.assertEqual(pc1 in pc2.inputs, True)
        self.assertEqual(pc2 in pc1.inputs, False)
    # A graph with no redundant edges (no changes required)
    def test_redundant2(self):
        lexicon = Choices.Lexicon(pos_tag='verb')
        lexicon.lexitems = set()
        lexicon.pcs = []
        li1 = Choices.LexicalItem(features=[],pos_tag='verb',id=1,transitivity=None,case_frame=None)
        pc1 = Choices.Position_Class(is_prefix=False,pos_tag='verb')
        pc2 = Choices.Position_Class(is_prefix=False,pos_tag='verb')
        pc1.id = 'verb-pc1'
        pc2.id = 'verb-pc2'
        li1.outgoing_edges.add(pc1)
        pc1.inputs.add(li1)
        pc1.outgoing_edges.add(pc2)
        pc2.inputs.add(pc1)
        lexicon.traverse_lexicon_llp()
        Choices.rebuild_lexicon(lexicon)
        self.assertEqual(li1.outgoing_edges, {pc1})
        self.assertEqual(pc1.outgoing_edges, {pc2})
        self.assertEqual(pc1.inputs, {li1})
        self.assertEqual(pc2.inputs, {pc1})
    # A graph with 4 nodes and 2 redundant edges to remove
    def test_redundant3(self):
        lexicon = Choices.Lexicon(pos_tag='verb')
        lexicon.lexitems = set()
        lexicon.pcs = []
        li1 = Choices.LexicalItem(features=[],pos_tag='verb',id=1,transitivity=None,case_frame=None)
        pc1 = Choices.Position_Class(is_prefix=False,pos_tag='verb')
        pc2 = Choices.Position_Class(is_prefix=False,pos_tag='verb')
        pc3 = Choices.Position_Class(is_prefix=False,pos_tag='verb')
        pc1.id = 'verb-pc1'
        pc2.id = 'verb-pc2'
        pc3.id = 'verb-pc3'
        li1.outgoing_edges.add(pc1)
        li1.outgoing_edges.add(pc2)
        pc1.outgoing_edges.add(pc2)
        pc1.inputs.add(li1)
        pc2.inputs.add(pc1)
        pc2.inputs.add(li1)
        pc1.outgoing_edges.add(pc3)
        pc2.outgoing_edges.add(pc3)
        pc3.inputs.add(pc2)
        pc3.inputs.add(pc1)
        lexicon.lexitems.add(li1)
        lexicon.pcs.append(pc1)
        lexicon.pcs.append(pc2)
        lexicon.traverse_lexicon_llp()
        Choices.rebuild_lexicon(lexicon)
        self.assertEqual(len(li1.outgoing_edges),1)
        self.assertEqual(pc2 in li1.outgoing_edges, False)
        self.assertEqual(pc1 in li1.outgoing_edges, True)
        self.assertEqual(pc2 in pc1.outgoing_edges, True)
        self.assertEqual(pc2.inputs, {pc1})
        self.assertEqual(pc1.inputs, {li1})
        self.assertEqual(len(pc3.outgoing_edges), 0)
        self.assertEqual(pc3.inputs, {pc2})
        self.assertEqual(pc2.outgoing_edges,{pc3})
        self.assertEqual(pc1.outgoing_edges,{pc2})


def create_lexicon():
    settings = MainClasses.Settings('./config_files/eng_config')
    xigt_reader = XigtReader.Xigt_Reader(settings, verbose=args.verbose)
    xigt_reader.process_igts(settings.data_file)
    mom = MainClasses.MOM(name='AGG-MOM', output_dir=settings.out_dir, vectors=settings.vectors,
                          tag_sets=settings.pos_tags, verb_classes=settings.lexitem_classes,
                          precluster_only=settings.precluster_only)
    choices = mom.execute(pos_items=xigt_reader.items['verb'],settings=settings,
                                            patterns=settings.patterns,tarball=None,arc_name=None,
                                            ignore_affix_types=settings.ignore_affixes,verbose=args.verbose)

    return choices.lexicon

if __name__ == '__main__':
    unittest.main()
