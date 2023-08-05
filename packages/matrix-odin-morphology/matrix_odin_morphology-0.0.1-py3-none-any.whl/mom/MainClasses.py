import os
import sys
import tarfile

# parent_dir = os.path.join(os.getcwd(),os.pardir)
# sys.path.append(parent_dir)
from . import Choices
# from .Choices import build_matrix_choices
#from agg.mom import EvalAbuiMatrix
#from agg.mom import Abui


def set_filenames(filescount, settings):
    if not os.path.isdir(settings.out_dir):
        os.makedirs(settings.out_dir)
    tar_name = settings.out_dir + "choices" + settings.out_id + str(filescount) + ".tar"
    arc_name = "choices" + settings.out_id + str(filescount)
    while os.path.exists(tar_name):
        filescount += 1
        tar_name = settings.out_dir + "choices" + settings.out_id + str(filescount) + ".tar"
        arc_name = 'choices' + settings.out_id + str(filescount)
    fout_name = "results"
    return fout_name, tar_name, arc_name

#############
# Classes
#############

class Pos_Tag:
    def __init__(self, tag):
        tags = tag.split(',')
        self.settings = {"tags": tags,
                         "iso": ["$iso"]}

class MOM:
    def __init__(self, name, output_dir, gold_file=None,
                 compression=None,
                 tag_sets = 1,
                 lexitem_classes=True,all_bare=True,precluster_only=False,
                 toolbox=None,reftag='\\ref', toolbox_tags=None):
        self.settings = {"name": [name],
                         "compression": [compression],
                         "wordlist": [],
                         "output iso": ["$iso"],
                         "output dir": [output_dir],
                         "groups":["training"],
                         "iso":["language"],
                         "language":["$language"],
                         "gold_file": [gold_file],
                         "lexitem_classes": [lexitem_classes],
                         'all_bare': [all_bare],
                         'precluster_only': [precluster_only],
                         'toolbox': [toolbox],
                         'reftag': [reftag],
                         'toolbox tags': [toolbox_tags],
                         }
        self.output_files_count = 0
        self.tag_sets = tag_sets
        self.algorithm1 = None #TODO: reimplement
        self.algorithm2 = 'overlap'


    def execute(self, pos_items, settings, patterns, tarball,arc_name,ignore_affix_types,verbose,pos_tag='verb',
                escape_special_characters=False,agr_morphemes=None,ignore_features=False):
        sys.setrecursionlimit(10000) # 1000 does get exceeded by cycle_found() on large datasets with lots of morphemes
        output_files = []
        #choices_file.lexicon.visualize('original_graph', choices_file.lexicon.pcs,'inputs', output_files)
        iso = settings.iso
        mom_choices = Choices.Choices(iso, pos_items,
                                       hyphens = settings.hyphens, output_glosses = settings.glosses,
                                       output_dir=settings.out_dir, known_affix_types=patterns,
                                       lexitem_classes=settings.lexitem_classes, ignore_affix_types=ignore_affix_types,
                                       verbose=verbose,precluster_only=settings.precluster_only,pos_tag=pos_tag,
                                       escape_special_characters=escape_special_characters,agr_morphemes=agr_morphemes,
                                       ignore_features=ignore_features)
        print('Total valid words in the input IGT collection: ', len(pos_items))
        pcs_final = len(mom_choices.lexicon.pcs)
        if settings.compression:
            print ('Compressing affixes based on minimum PC overlap:', settings.compression)
            print('Starting from ', len(mom_choices.lexicon.pcs), ' PCs.')
            #mom_choices.lexicon.visualize(iso+'_before_graph', mom_choices.lexicon.pcs,'inputs',output_files)
            #mom_choices.lexicon.tabularize(iso+'_before_table', output_files)
            seen_pairs = set()
            mom_choices.lexicon.compact_lexicon(depth=0, min_overlap=settings.compression,seen_pairs=seen_pairs,first_call=True)
            pcs_final = len(mom_choices.lexicon.pcs)
            print('Finished with ', pcs_final, ' PCs.')
            print('Performing {0} rounds of affix and lexical class compression'.format(settings.compr_rounds))
            if settings.lexitem_classes:
                for i in range(0,settings.compr_rounds):
                    print('Round {0}'.format(str(i+1)))
                    print ('Compressing lexical classes based on minimum output overlap:', settings.compression)
                    print('Starting from ', len(mom_choices.lexicon.lexitems), ' lexical classes.')
                    first_call=True
                    mom_choices.lexicon.compact_lexitems(depth=0,min_overlap=settings.compression,first_call=first_call)
                    print('Finished with ', len(mom_choices.lexicon.lexitems), ' lexical classes.')
                    print ('Compressing affixes again based on minimum PC overlap:', settings.compression)
                    first_call = False
                    mom_choices.lexicon.compact_lexicon(depth=0, min_overlap=settings.compression,
                                                        seen_pairs=seen_pairs,first_call=first_call)
                    pcs_final = len(mom_choices.lexicon.pcs)
                    print('Finished with ', pcs_final, ' PCs.')
            # Find longest paths between each two nodes
            #print('Finding longest paths')
            #mom_choices.lexicon.traverse_lexicon_llp()
            # Remove all paths except the longest
            #print('Removing all paths except the longest')
            #Choices.rebuild_lexicon(mom_choices.lexicon)
            print('Building Matrix-style choices file')
            if settings.pos == 'verb':
                mom_choices.matrix_choices = Choices.build_matrix_choices(mom_choices.lexicon,None, settings)
            elif settings.pos == 'noun':
                mom_choices.matrix_choices = Choices.build_matrix_choices(None,mom_choices.lexicon, settings)
            if settings.output_graph:
                #nodes = list(mom_choices.lexicon.lexitems) + mom_choices.lexicon.pcs
                print('Saving as a graph')
                mom_choices.lexicon.visualize(iso+'_overlap_graph',
                                              mom_choices.matrix_choices,'inputs',output_files,pos_tag)
                #mom_choices.lexicon.tabularize(iso+'_overlap_table', output_files)
        if tarball:
            choices_file_name = self.print_output(self.algorithm2,tarball,settings,mom_choices.matrix_choices,arc_name)
        else:
            choices_file_name = 'No-tarfile-requested'

        for f in output_files:
            if os.path.exists(f):
                name = f
            elif os.path.exists(settings.out_dir + f):
                name = settings.out_dir + f
            else:
                print('Check the path for file {0}, cannot add it to the archive'.format(f))
                continue
            if '/' in name:
                arcname = f.split('/')[-1]
            else:
                arcname = name
            if tarball:
                tarball.add(name=name,arcname=arcname)
            os.remove(name)

        #return ","+str(compr)+","+choices_file_name.split("/")[-1], output_files, mom_choices
        #mom_choices.matrix_choices = mom_choices.build_matrix_choices()
        return mom_choices

    def print_output(self, algorithm, tarball, settings, matrix_choices,arc_name):
        output_filename = settings.iso + '_' + algorithm + '_' + str(self.output_files_count) + '.choices'
        with open (output_filename, 'w', encoding='utf-8') as f:
            #choices_file.print_to(f,settings.iso)
            f.write(str(matrix_choices))
        self.output_files_count = self.output_files_count + 1
        tarball.add(name=output_filename,arcname=arc_name)
        #choices = MatrixChoices.ChoicesFile(output_filename)
        os.remove(output_filename)
        return output_filename

class Settings:
    def __init__(self, filename):
        self.pos_tags = []
        self.output = None
        self.inference = False
        self.iso = None
        self.data_file = None
        self.compression = 1.0
        self.out_dir = './'
        self.out_id = 'test'
        self.hyphens = True
        self.glosses = True
        self.lexitem_classes = True
        self.precluster = None
        self.precluster_only = False
        self.use_gloss_to_precluster = False
        self.implicitg2morph = False
        self.ignore_affixes = []
        self.all_bare = True
        self.toolbox = None
        self.reftag = '\\ref'
        self.toolbox_tags=['\\t','\\m','\\g','\\p','\\f']
        self.language = None

        with open(filename, "r", encoding='utf-8') as file:
            for line in file:
                line = line.split("#",1)[0].strip()
                if line:
                    setting, value = line.split(":",1)[0].strip(), line.split(":",1)[1].strip()
                    setting = setting.strip()
                    if setting == 'pos':
                        self.pos = value
                    if setting == 'implicit gloss2morph alignment':
                        self.implicitg2morph = value == 'True'
                    if setting == 'compression':
                        self.compression = float(value)
                    if setting == 'compression rounds':
                        self.compr_rounds = int(value)
                    elif setting == 'lexitem nodes':
                        self.lexitem_classes = value == 'True'
                    elif setting == 'inference':
                        self.inference = value == 'True'
                    elif setting == "verb tags":
                        with open(value,'r', encoding='utf-8') as f:
                            tags = f.readlines()
                            self.verb_tags = [t.strip() for t in tags]
                    elif setting == "noun tags":
                        with open(value,'r', encoding='utf-8') as f:
                            tags = f.readlines()
                            self.noun_tags = [t.strip() for t in tags]
                    elif setting == "adp tags":
                        with open(value,'r', encoding='utf-8') as f:
                            tags = f.readlines()
                            self.adp_tags = [t.strip() for t in tags]
                    elif setting == 'iso':
                        self.iso = value
                    elif setting == 'language':
                        self.language = value
                    elif setting == 'data file':
                        self.data_file = value
                    elif setting == 'output dir':
                        self.out_dir = value
                        if self.out_dir[len(self.out_dir)-1] is not '//':
                            self.out_dir = self.out_dir + '/'
                    elif setting == 'output id':
                        self.out_id = value
                    elif setting == 'glosses':
                        self.glosses = value == 'True'
                    elif setting == 'precluster':
                        if not value=='None':
                            with open(value, 'r', encoding='utf-8') as f:
                                self.patterns = f.read().split('\n')
                        else:
                            self.patterns = None
                    elif setting == 'only precluster':
                        self.precluster_only = value == 'True'
                    elif setting == 'precluster_by':
                        self.use_gloss_to_precluster = value == 'gloss'
                    elif setting == 'hyphens':
                        self.hyphens = value == 'True'
                    elif setting == 'ignore affixes':
                        if value and value!='None':
                            with open (value, 'r', encoding='utf-8') as f:
                                self.ignore_affixes = f.readlines()
                        else:
                            self.ignore_affixes = []
                    elif setting == 'ignore igt':
                        if value and value!='None':
                            with open (value, 'r', encoding='utf-8') as f:
                                self.ignore_igt = f.readlines()
                        else:
                            self.ignore_igt = []
                    elif setting == 'ignore chars':
                        self.ignore_chars = value if value != 'None' else None
                    elif setting == 'ungrammatical':
                        self.ungrammatical = value
                    elif setting == 'allow difference':
                        self.allowed_diff = int(value)
                    elif setting == 'allomorphs':
                        self.allomorphs = []
                        if not value=='None':
                            with open(value,'r', encoding='utf-8') as f:
                                lines = f.readlines()
                            for ln in lines:
                                (s1, s2, position) = ln.split(',')
                                self.allomorphs.append((s1, s2, int(position.strip())))
                    elif setting == 'known glosses':
                        self.known_glosses_file = value if value!='None' else None
                    elif setting == 'pos tier':
                        self.pos_tier_id = value
                    elif setting == 'gloss tier':
                        self.gloss_tier_ids = value
                    elif setting == 'boundaries':
                        self.assume_morph_boundaries = value == 'True'
                    elif setting == 'all stems occur bare':
                        self.all_bare = value == 'True'
                    elif setting == 'choices only':
                        self.choices_only = value == 'True'
                    elif setting == 'toolbox':
                        self.toolbox = value
                    elif setting == 'reftag':
                        self.reftag = value
                    elif setting == 'language line':
                        self.lang_line_tag = value
                    elif setting == 'tags':
                        self.toolbox_tags = value.split(',')
                    elif setting == 'graph':
                        self.output_graph = value == 'True'
                    elif setting == 'escape special characters':
                        self.escape_special_characters = value



