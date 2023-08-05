import argparse
import os
import sys
import tarfile

# parent_dir = os.path.join(os.getcwd(),os.pardir)
# sys.path.append(parent_dir)
import MainClasses, MatrixChoices
from XigtifiedToolbox import XigtReader

#import XigtReader
#from mom import Cluster
#from agg.mom import Choices
#import Choices
#from mom import EvalAbuiMatrix
#from mom import Abui


#############
# Arguments
#############
parser = argparse.ArgumentParser(description="Loads a settings file and run a set of tests.")

parser.add_argument("-s", "--settings", help="The name of the configuration file.")

parser.add_argument("-v", "--verbose", help="Verbose output", action='store_true')

parser.add_argument("-p", "--pos", help="POS if not in config file")

args = parser.parse_args()



#############
# Main
#############

def reset_results_filename(fout_name, results_file_name, settings):
    if os.path.exists(results_file_name):
        bonus_id = 0
        results_file_name = settings.out_dir + fout_name + settings.out_id + "-" + str(bonus_id) + ".csv"
        while os.path.exists(results_file_name):
            bonus_id += 1
            results_file_name = settings.out_dir + fout_name + settings.out_id + "-" + str(bonus_id) + ".csv"
    return results_file_name


def main():
    if len(sys.argv) < 2:
        print('AGG-MOM usage: mom -s config_file [-v (verbose)]')
        sys.exit(1)
    settings_file = args.settings
    print ("Loading Configuration File",settings_file)
    settings = MainClasses.Settings(settings_file)

    # ...sigh... if the config file doesn't specify a POS, use the arg
    if not hasattr(settings, 'pos'):
        settings.pos = args.pos

    filescount = 0
    fout_name, tar_name, arc_name = MainClasses.set_filenames(filescount, settings)
    xigt_reader = XigtReader.Xigt_Reader(settings, verbose=args.verbose)
    xigt_reader.process_igts(settings.data_file)
    mom = MainClasses.MOM(name='AGG-MOM', output_dir=settings.out_dir,
                          tag_sets=settings.pos_tags, lexitem_classes=settings.lexitem_classes,
                          precluster_only=settings.precluster_only)
    xigt_reader.print_skipped(settings.out_dir + '/skipped_items.txt')
    with tarfile.open(tar_name, 'a') as tarball:
        choices = mom.execute(pos_items=xigt_reader.items[settings.pos],settings=settings,
                                            patterns=settings.patterns,tarball=tarball,arc_name=arc_name,
                                            ignore_affix_types=settings.ignore_affixes,verbose=False,
                              pos_tag=settings.pos)
        tarball.add(name=settings.out_dir + '/skipped_items.txt',arcname='skipped_items.txt')
        os.remove(settings.out_dir + '/skipped_items.txt')
    print('tar name: ', tar_name)


if __name__ == "__main__":
    main()
