# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 14:04:14 2014

Sprechererkennungstest: Training script for day 2.

This is intended to train subjects to identify four male speakers fom their
voices alone. There are four parts. Part 1 plays four stories. Part 2 is a
4-alternative test. Part 3 is another four stories, and part 4 is a final test.

@author: Sam Mathias
@version: 1.1
@version history:

1.1 Completely re-written and much shorter, importing much of its functionality
    from train_day1.py.
"""

import os
import numpy as np
import tools
import train_day1 as t


t.TEST_NAME = 'train_day2'
t.INSTRUCTIONS = tools.instructions.read_instructions(t.TEST_NAME, t.LANG)
t.STORIES = ['apok', '17_juni', 'papier', 'beruf']  # different order to day 1
t.MAX_CORR = [None, 15, None, 15]

def gen_control(proband_id, check=False):
    """Generates a control iterable for the session. Each item in the list is a
    tuple representing a single trial in the format: (proband_id, test_name,
    partn, type, trialn, f, speaker). This is slightly different from the
    function with the same name imported from train_day1.py, which it
    replaces."""
    pj, pd, cwd, ls = os.path.join, os.path.dirname, os.getcwd(), os.listdir
    story_path = pj(pd(cwd), 'stimuli', 'audio', 'stories')
    sentence_path = pj(pd(cwd), 'stimuli', 'audio', 'train')

    def story_trial(partn, i):
        """Generate info for a story trial."""
        if partn == 0:
            f = pj(story_path, t.CODES[i] + '_' + t.STORIES[i] + '.wav')
        elif partn == 2:
            f = pj(story_path, t.CODES[i] + '_' + t.STORIES[3-i] + '.wav')
        return (proband_id, t.TEST_NAME, partn, 'story', i, f, t.NAMES[i])

    def test_trial(partn, i):
        """Generate info for a test trial."""
        f = pj(sentence_path, sentences[i])
        speaker = dict(zip(t.CODES, t.NAMES))[sentences[i].split('_')[0]]
        return (proband_id, t.TEST_NAME, partn, 'test', i, f, speaker)

    control = [story_trial(0, i) for i in range(4)[::-1]]
    sentences = [f for f in ls(sentence_path) if '.wav' in f]
    np.random.shuffle(sentences)
    sentences = sentences[:100]
    control += [test_trial(1, i) for i in xrange(100)]
    control += [story_trial(2, i) for i in range(4)[::-1]]
    sentences = [f for f in ls(sentence_path) if '.wav' in f]
    np.random.shuffle(sentences)
    sentences = sentences[:100]
    control += [test_trial(3, i) for i in xrange(100)]

    if check:
        for c in control:
            print c
    return control

t.gen_control = gen_control

if __name__ == '__main__':
    t.main()