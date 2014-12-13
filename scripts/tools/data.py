# -*- coding: utf-8 -*-
"""
Created on Thu Feb 27 17:42:52 2014

Generic routines for basic data-handling stuff. In its most basic form, data is
saved within instances of the Data class. There should be one such instance per
test and per proband. If a given proband does not complete a given test, their
previous data will be loaded.

To do:

1. Create Proband and Test classes that gather up Data classes for easy human-
   readable summaries.
2. Figure out a way of choosing whether to resume or restart a test if there is
   an incomplete data set already serialised.

@author: smathias
"""
import os, sys, cPickle
from datetime import datetime
import numpy as np

DATA_PATH = os.path.join(os.path.dirname(os.getcwd()), 'data')
ALREADY_DATA_WARNING_STR = """It looks like there was already some data for
this proband and test. The new data was probably just appended to the end of the
data.data iterable, but you should probably check this out."""

#
#tmp = sys.stdout
#data_path = os.path.join(os.getcwd(), 'data')
#logs_path = os.path.join(os.getcwd(), 'logs')

class Data:
    
    def __init__(self, proband_id, test_name):
        """Returns a data object that stores trial info and methods for saving/
        updating the data. Should be one instance per proband per test."""
        self.proband_id = proband_id
        self.test_name = test_name
        self.directory = DATA_PATH
        self.filename = '%s_%s.data' %(proband_id, test_name)
        self.abs_filename = os.path.join(self.directory, self.filename)
        self.control = None
        self.data = None
        self.test_done = False
        self.initialised = datetime.now()
        self.warnings = []
        self.log = []
    
    def check_if_exists(self):
        """Check if a data object for this proband and test already exists."""
        return os.path.exists(self.abs_filename)
    
    def begin_trial(self):
        """Pop and return the first item from the control iterable."""
        if self.control:
            trial = self.control.pop(0)
            return trial
    
    def update(self, trial=None):
        """Save the Data object in its current state. If a trial is passed,
        this is added to the data iterable."""
        if trial:
            self.data.append(trial)
        save_data(self) #check if this works...
        data2csv(self)
    
    def add_warning(self, w):
        """Add a warning to the warning list. All warnings will be tuples in
        the form (d, w), where d is a datetime object and w is the warning
        message."""
        self.warnings.append((datetime.now(), w))
                
def load_data(proband_id, test_name):
    """Load a data object, or create a new one if not found."""
    tmp = Data(proband_id, test_name)
    print tmp.abs_filename
    if os.path.exists(tmp.abs_filename):
        return cPickle.load(open(tmp.abs_filename, 'rb'))
    else:
        return tmp

def save_data(data):
    """Save a data object to the path specified within the object."""
    if not os.path.exists(data.directory):
        os.makedirs(data.directory)
    cPickle.dump(data, open(data.abs_filename, 'wb'))
        
def data2csv(data):
    """Convertthe data list to a csv and save."""
    lines = ''
    for row in data.data:
        line = str(row).strip('()').replace("'",'') + '\n'
        lines += line
    fw = open(data.abs_filename[:-4] + 'csv', 'wb')
    fw.write(lines)
    fw.close()
#    control, data = (None, None)
#    path = os.path.join(data_path, test_name, proband_id)
#    if not os.path.exists(path):
#        log_write(proband_id,
#                  test_name,
#                  'No folder found for %s on %s' %(proband_id, test_name))
#    else:
#        log_write(proband_id,
#                  test_name,
#                  'Folder found for %s on %s' %(proband_id, test_name))
#        for f in os.listdir(path):
#            if '.control' in f:
#                log_write(proband_id, test_name, 'Control file found.')
#                control = cPickle.load(open(os.path.join(path, f), 'r'))
#            if '.data' in f:
#                log_write(proband_id, test_name, 'Data file found.')
#                data = cPickle.load(open(os.path.join(path, f), 'r'))
#    return control, data
##                
#def save_stuff(proband_id, test_name, control, data):
#    """Save the control and data files within a proband- and test-specific
#    subdirectory of /data. If this is done after each *response*, there is no
#    need to reinstate the last trial, because the popped control iterable is
#    not saved."""
#    path = os.path.join(data_path, test_name, proband_id)
#    if not os.path.exists(path):
#        os.makedirs(path)
#    f = os.path.join(path, proband_id + '_' + test_name)
#    cPickle.dump(control, open(f + '.control', 'w'))
#    cPickle.dump(data, open(f + '.data', 'w'))
#    log_write(proband_id,
#              test_name,
#              'Written to %s.control and %s.data' %(f, f))
#
#def log_write(proband_id, test_name, s):
#    """Write something to a master log and a proband- and test-specific log."""
#    f = proband_id + '_' + test_name
#    s = '[%s] %s' %(datetime.now(), s)
#    path = os.path.join(data_path, test_name, proband_id)
#    if not os.path.exists(path):
#        os.makedirs(path)
#    places = [open(os.path.join(path, f + '.log'), 'a+'),
#              open(os.path.join(logs_path, 'log.txt'), 'a+'),
#              tmp]
#    for place in places:
#        sys.stdout = place
#        print s
#
#def read_instructions(test_name):
#    """Read the instructions for a given test from an external instructions.txt
#    file. The idea behind doing this is that this way they can be easily
#    translated without screwing about with the source code."""
#    divider_1 = '-----------------------------------------------------'
#    divider_2 = '-------------------------------'
#    all_instructions = open('instructions.txt', 'r').read().split(divider_1)
#    all_instructions = [f.replace('\r','') for f in all_instructions]
#    for instructions in all_instructions:
#        instr = [s.strip('\n') for s in instructions.split(divider_2)]
#        if test_name in instr or test_name + '\r' in instr:
#            return instr
#
#def test():
#    """Test out functions."""
#    proband_id = 'TEST_PROBAND'
#    test_name = 'SAMPLE_TEST'
#    save_stuff(proband_id, test_name, 'control file here.', 'data file here.')
#    control, data = load_stuff(proband_id, test_name)
#    print control, data
#
#def test2():
#    test_name = 'emotion_recognition'
#    instr = read_instructions(test_name)
#    for i in instr:
#        print i
#
#if __name__ == '__main__':
#    test2()    