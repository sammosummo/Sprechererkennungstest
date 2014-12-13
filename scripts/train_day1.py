# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 14:04:14 2014

Sprechererkennungstest: Training script for day 1.

This is intended to train subjects to identify four male speakers fom their
voices alone. There are four parts. Part 1 starts by playing stories from two
of the speakers, then the listener performs a 2-alternative discrimination
test. Part 2 is the same but with two different speakers. Part 3 plays fours
stories, one by each speaker (each speaker speaks a different story to the one
they spoke earlier). Part 4 is a 4-alternative test.

@author: Sam Mathias
@version: 1.1
@version history:

1.1 Re-wrote most of the script to fix the bugs Carolin found. Seems to work
    fine now. Stories are switched off and instructions are in English.

1.2 Fixed bug where the wrong names are displayed whilst the stories are
    playing during part 2/4.
"""

import os
import sys
import numpy as np
import tools

# TODO: modify the following constants once all bugs are fixed ----------------
LANG = 'EN'  # Should be 'DE'
STORIES_OFF = True  # should be False
# -----------------------------------------------------------------------------

TEST_NAME = 'train_day1'
INSTRUCTIONS = tools.instructions.read_instructions(TEST_NAME, LANG)
NAME_POSITIONS = [-300, -100, 100, 300]
ITI = 1
MAX_CORR = [10, 10, None, 15]

STORIES = ['17_juni', 'apok', 'beruf', 'papier']
NAMES = ['Leon', 'Jonas', 'Felix', 'Moritz']
CODES = ['sp01', 'sp08', 'sp10', 'sp11']
KEYS =  range(1, 5)


def gen_control(proband_id, check=False):
    """Generates a control iterable for the session. Each item in the list is a
    tuple representing a single trial in the format: (proband_id, test_name,
    partn, type, trialn, f, speaker)."""
    pj, pd, cwd, ls = os.path.join, os.path.dirname, os.getcwd(), os.listdir
    story_path = pj(pd(cwd), 'stimuli', 'audio', 'stories')
    sentence_path = pj(pd(cwd), 'stimuli', 'audio', 'train')

    def story_trial(partn, i):
        """Generate info for a story trial."""
        if partn == 0:
            f = pj(story_path, CODES[i] + '_' + STORIES[i] + '.wav')
            return (proband_id, TEST_NAME, partn, 'story', i, f, NAMES[i])
        elif partn == 1:
            f = pj(story_path, CODES[i+2] + '_' + STORIES[i+2] + '.wav')
            return (proband_id, TEST_NAME, partn, 'story', i, f, NAMES[i+2])
        elif partn == 2:
            f = pj(story_path, CODES[i] + '_' + STORIES[3-i] + '.wav')
            return (proband_id, TEST_NAME, partn, 'story', i, f, NAMES[i])

    def test_trial(partn, i):
        """Generate info for a test trial."""
        f = pj(sentence_path, sentences[i])
        speaker = dict(zip(CODES, NAMES))[sentences[i].split('_')[0]]
        return (proband_id, TEST_NAME, partn, 'test', i, f, speaker)

    control = [story_trial(0, i) for i in xrange(2)]
    sentences = [f for f in ls(sentence_path) if '.wav' in f and \
                 f.split('_')[0] in CODES[:2]]
    np.random.shuffle(sentences)
    sentences = sentences[:50]
    print ls(sentence_path)
    control += [test_trial(0, i) for i in xrange(50)]
    control += [story_trial(1, i) for i in xrange(2)]
    sentences = [f for f in ls(sentence_path) if '.wav' in f and \
                 f.split('_')[0] in CODES[2:]]
    np.random.shuffle(sentences)
    sentences = sentences[:50]
    control += [test_trial(1, i) for i in xrange(50)]
    control += [story_trial(2, i) for i in xrange(4)]
    sentences = [f for f in ls(sentence_path) if '.wav' in f]
    np.random.shuffle(sentences)
    sentences = sentences[:100]
    control += [test_trial(3, i) for i in xrange(100)]
    if check:
        for t in control:
            print t
    return control


def session(proband_id):
    """Runs the session."""
    data = tools.data.load_data(proband_id, TEST_NAME)

    if not data.control and not data.data:
        data.control = gen_control(proband_id, check=False)
        data.data = []

    screen, font = tools.gui.create_screen(), tools.gui.create_font(size=24)
    m = INSTRUCTIONS.pop(0).decode('utf-8')
    tools.gui.splash(screen, font, m)

    while data.control and not data.test_done:
        trial_info = data.control.pop(0)
        trial_info = trial(data, screen, font, trial_info)
        if trial_info:
            data.data.append(trial_info)
        if proband_id != 'TEST':
            data.update()

    m = INSTRUCTIONS.pop().decode('utf-8')
    tools.gui.splash(screen, font, m)


def trial(data, screen, font, trial_info):
    """Runs a single trial."""
    proband_id, _, partn, part_type, trialn, f, speaker = trial_info
    print trial_info

    if part_type == 'story':

        m = INSTRUCTIONS.pop(0).decode('utf-8')
        tools.gui.splash(screen, font, m, mouse=False)
        tools.gui.splash(screen, font, speaker, wait=False)
        if not STORIES_OFF:
            tools.audio.play_sound(f, wait=True)
#        tools.gui.splash(screen, font, speaker, wait=True)
        return tuple(list(trial_info) + ['', ''])

    else:

        if trialn == 0:
            m = INSTRUCTIONS.pop(0).decode('utf-8')
            tools.gui.splash(screen, font, m, mouse=False)
            data.conseq_corr = 0

        max_corr = MAX_CORR[partn]

        tools.gui.wipe(screen)
        correct = False
        responses = []

        def display(rsp, corr):
            """Update the display."""
            tools.gui.wipe(screen)
            colours = [tools.gui.DEFAULT_TEXT_COLOUR] * 4
            feedback = INSTRUCTIONS[-4:-1]
            feedback_colours = [tools.gui.RED, tools.gui.GREEN]
            if not rsp:
                m = INSTRUCTIONS[-5].decode('utf-8')
                colour = tools.gui.DEFAULT_TEXT_COLOUR
            else:
                m = feedback[corr]
                colour = feedback_colours[corr]
                colours[int(rsp) - 1] = colour
            p = (screen, font, m, (0, 0), colour)
            tools.gui.blit_text(*p, update=False)
            for i in xrange(len(NAMES)):
                m = NAMES[i].decode('utf-8')
                x = NAME_POSITIONS[i]
                p = (screen, font, m, (x, 150), colours[i])
                tools.gui.blit_text(*p, update=False)
            m = INSTRUCTIONS[-2] % (trialn, data.conseq_corr)
            m = m.decode('utf-8')
            colour = tools.gui.DEFAULT_TEXT_COLOUR
            p = (screen, font, m, (0, -150), colour)
            tools.gui.blit_text(*p, update=False)
            tools.gui.update()

        while not correct:
            display(None, None)
            tools.audio.play_sound(f)
            keys = [str(k) for k in KEYS]
            rsp, rt = tools.events.wait_for_valid_keydown(keys, 'unicode')
            response = dict(zip(keys, NAMES))[rsp]
            correct = response == speaker
            responses.append(response)
            if not correct:
                data.conseq_corr = 0
            if correct and len(responses) == 1:
                data.conseq_corr += 1
            display(rsp, correct)
            tools.events.wait(ITI)

        if data.conseq_corr == max_corr:
            data.control = [c for c in data.control if c[2] != partn]

        return tuple(list(trial_info) + [len(responses)] + responses)


def main():
    if len(sys.argv) == 2:
        proband_id = sys.argv[1:]
    else:
        proband_id = raw_input('Type the subject ID>>>')
    session(proband_id)

if __name__ == '__main__':
    main()