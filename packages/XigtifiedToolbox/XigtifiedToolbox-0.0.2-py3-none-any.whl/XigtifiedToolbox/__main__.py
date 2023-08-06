import argparse
import os
import sys

parent_dir = os.path.join(os.getcwd(),os.pardir)
sys.path.append(parent_dir)
# Please have both XigtifiedToolbox and mom from aggregation/mom on your PYTHONPATH.
from mom import MainClasses
from . import XigtReader
from . import report_problems


parser = argparse.ArgumentParser(description="Loads a settings file and run a set of tests.")

parser.add_argument("-s", "--settings", help="The name of the configuration file.")

parser.add_argument("-v", "--verbose", help="Verbose output", action='store_true')

args = parser.parse_args()

def main():
    if len(sys.argv) < 2:
        print('AGG-MOM usage: mom -s config_file [-v (verbose)]')
        sys.exit(1)
    settings_file = args.settings
    print ("Loading Configuration File",settings_file)
    settings = MainClasses.Settings(settings_file)
    xigt_reader = XigtReader.Xigt_Reader(settings, verbose=args.verbose)
    xigt_reader.process_igts(settings.data_file)
    xigt_reader.print_skipped(settings.out_dir + '/skipped_items.txt')
    pr = report_problems.ProblemReport()
    pr.report_inconsistencies(settings.toolbox, settings.reftag, settings.lang_line_tag, settings.toolbox_tags,
                              xigt_reader.skipped_words,xigt_reader.full_xc)

if __name__ == '__main__':
    main()