""" Classify the protein measurement experiments in Geiger, et al, https://www.mcponline.org/content/11/3/M111.014050

:Author: Arthur Goldberg <Arthur.Goldberg@mssm.edu>
:Date: 2016_12_06
:Copyright: 2019, Karr Lab
:License: MIT
"""

import os
import re
from pprint import pprint

EXPERIMENT_NAMES_FILE = os.path.join(os.path.dirname(__file__), 'data', 'Geiger_2012_experiments.txt')
HUMAN_PREFIX = '9606/9606-'
TEXT_SUFFIX = '.txt'
UNIPROT_SUFFIX = '_uniprot'
CITATION_SUFFIX = '_Geiger_2012'
CELL_LINES = 'A549 GAMG HEK293 HeLa HepG2 K562 MCF7 RKO U2OS LnCap Jurkat'.split()
METHODS = 'iBAQ'.split()

def main():
    with open(EXPERIMENT_NAMES_FILE) as f:
        experiment_names = f.readlines()

    # remove whitespace characters like `\n` from the end of each line
    experiment_names = [x.strip() for x in experiment_names]

    # remove generic info
    trimmed_names = [re.sub(f"^{HUMAN_PREFIX}", '', x) for x in experiment_names]
    trimmed_names = [re.sub(f"{TEXT_SUFFIX}$", '', x) for x in trimmed_names]
    trimmed_names = [re.sub(f"{UNIPROT_SUFFIX}$", '', x) for x in trimmed_names]
    trimmed_names = [re.sub(f"{CITATION_SUFFIX}$", '', x) for x in trimmed_names]
    print('\n'.join(trimmed_names))

    expt_properties = {}
    for name in trimmed_names:
        properties = name.split('_')
        cell_line = 'unknown'
        method = 'unknown'
        other = None
        for property in properties:
            if property in CELL_LINES:
                cell_line = property
            elif property in METHODS:
                method = property
            else:
                other = property
        expt_properties[name] = (('cell_line', cell_line), ('method', method), ('other', other))

    pprint(expt_properties)

if __name__ == "__main__":
    main()