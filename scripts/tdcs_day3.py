# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 14:04:14 2014

Sprechererkennungstest: tDCS script for day 3.

This is intended to test subjects' speaker-recognition abilities fom their
voices alone. Subjects perform two tasks (speaker and speech) in alternating
order. Each task involves listening to a sentence followed by a 4-alternative
decision. There are 40 trials per block and 6 blocks per task.

This is almost identical to day2, except that different stimuli are used.

@author: Sam Mathias
@version: 1.0
@version history:


"""

from itertools import product
import os
import sys
import numpy as np
import tools
import tdcs_day1 as d1

d1.TEST_NAME = 'tdcs_day3'
d1.TRIALS_THIS_SESSION = d1.ALL_TRIALS[480:]
d1.INSTRUCTIONS = tools.instructions.read_instructions(d1.TEST_NAME, d1.LANG)


def gen_control(proband_id, stimulation):
    """Generates a control iterable. Each item in the list is a tuple that
    represents a trial in the format: (proband_id, test_name, stimulation,
    phase, blockn, task, trialn, speaker, intonation, word, f, ans, alt1, alt2,
    alt3, alt4)."""
    pj, pd, cwd = os.path.join, os.path.dirname, os.getcwd()
    sentence_path = pj(pd(cwd), 'stimuli', 'audio', 'test')

    speaker_trials = list(d1.TRIALS_THIS_SESSION)
    np.random.shuffle(speaker_trials)
    speech_trials = list(d1.TRIALS_THIS_SESSION)
    np.random.shuffle(speech_trials)

    def get_f(speaker, intonation, word):
        """Determines the filename given the speaker, intonation, or word."""
        a = dict(zip(d1.NAMES, d1.CODES))[speaker]
        b = intonation
        c = ''
        i = d1.WORDS.index(word)
        if i < 100:
            c += '0'
        if i < 10:
            c += '0'
        c += str(i)
        return pj(sentence_path, '_'.join([a, b, c]) + '.wav')

    def test_trial(blockn, trialn):
        """Determines the trial info for a particular trial."""
        if blockn % 2 == 0:
            task = d1.TASKS[0]
            speaker, intonation, word = speaker_trials.pop(0)
            ans = speaker
            alt1, alt2, alt3, alt4 = d1.NAMES
        else:
            task = d1.TASKS[1]
            speaker, intonation, word = speech_trials.pop(0)
            ans = word
            alt1, alt2, alt3, alt4 = sorted(d1.WORDS_DICT[word])
        f = get_f(speaker, intonation, word)
        phase = 'test'
        return (proband_id, d1.TEST_NAME, stimulation, phase, blockn, task,
                trialn, speaker, intonation, word, f, ans, alt1, alt2, alt3,
                alt4)

    control = []
    for blockn in xrange(len(d1.TASKS) * d1.BLOCKS_PER_TASK):
        t = [test_trial(blockn, trialn) for trialn in \
             xrange(d1.TRIALS_PER_BLOCK)]
        control += t
    return control

d1.gen_control = gen_control

if __name__ == '__main__':
    d1.main()