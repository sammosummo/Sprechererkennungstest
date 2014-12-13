# -*- coding: utf-8 -*-
"""
Created on Tue Apr 22 14:04:14 2014

Sprechererkennungstest: tDCS script for day 1.

This is intended to test subjects' speaker-recognition abilities fom their
voices alone. Subjects perform two tasks (speaker and speech) in alternating
order. Each task involves listening to a sentence followed by a 4-alternative
decision. There are 40 trials per block and 6 blocks per task.

There are a total of 134 unique, useable words in the corpus. We drop two of
these to make 132. We then assign 44 words to each of the two sessions. Within
one task, 28 of these words will be spoken four times (once per speaker), and
16 with be spoken eight times (twice per speaker), making 240 trials per task
per session. This method ensures no repetition of a stimulus across the three
test sessions.

@author: Sam Mathias
@version: 1.3
@version history:

1.1    There is a weird graphical bug in Carolin's version. Not sure what's
       causing it. Tried calling the screen wipe function at the beginning of
       the trial instead.

1.2    Under Windows. Fixed the weird graphical problem. Unclear whether the
       seqmentation fault is still present.

1.3    Segmentation faults and graphical bugs fixed.
"""

from itertools import product
import os
import sys
import numpy as np
import tools
from train_day1 import NAMES, CODES, KEYS, NAME_POSITIONS

# TODO: modify the following constants once all bugs are fixed ----------------
LANG = 'EN'
ITI = .2  # should be 3.
IBI = 1.  # should be 10.
# -----------------------------------------------------------------------------

np.random.seed(1)

TEST_NAME = 'tdcs_day1'
INSTRUCTIONS = tools.instructions.read_instructions(TEST_NAME, LANG)
TASKS = ['Sprecher', 'Sprache']
TRIALS_PER_BLOCK = 40
BLOCKS_PER_TASK = 6
PRACTICE_TRIALSN = 10
WORDS = [None, 'baut', 'beißt', 'beizt', 'bleibt', 'bleicht', 'braut', 'campt',
         'feilt', 'feixt', 'ficht', 'fischt', 'fliegt', 'flieht', 'fröhnt',
         'frönt', 'fühlt', 'führt', 'füllt', 'gibt', 'gießt', 'grimmt',
         'grinst', 'hackt', 'harkt', 'herrscht', 'herzt', 'hockt', 'hofft',
         'jobbt', 'joggt', 'kämmt', 'kämpft', 'kauft', 'kaut', 'klaubt',
         'klaut', 'knurrt', 'kreischt', 'kreist', 'kühlt', 'kürt', 'kurt',
         'lärmt', 'lernt', 'liebt', 'liegt', 'liest', 'lügt', 'mahnt', 'malt',
         'naht', 'narrt', 'nickt', 'nippt', 'packt', 'parkt', 'patzt',
         'platzt', 'prahlt', 'prallt', 'raubt', 'raucht', 'raunt', 'rauscht',
         'reibt', 'reicht', 'reift', 'reimt', 'reist', 'reizt', 'rückt',
         'rügt', 'ruft', 'ruht', 'sägt', 'sät', 'säuft', 'saugt', 'saust',
         'schiebt', 'schielt', 'schießt', 'schläft', 'schlägt', 'schleckt',
         'schleicht', 'schleift', 'schleppt', 'schmollt', 'schmort',
         'schnaubt', 'schnauft', 'schnitzt', 'schraubt', 'schreibt', 'schreit',
         'schweigt', 'schweißt', 'schwimmt', 'schwingt', 'schwitzt', 'seufzt',
         'siebt', 'siecht', 'siegt', 'sieht', 'singt', 'sinkt', 'speist',
         'speit', 'steigt', 'stellt', 'stelzt', 'stiehlt', 'stockt', 'stoppt',
         'strafft', 'straft', 'strahlt', 'streicht', 'streikt', 'stürzt',
         'stützt', 'stupst', 'stutzt', 'tankt', 'tanzt', 'taucht', 'tauscht',
         'taut', 'tickt', 'tippt', 'tränkt', 'trennt', 'trifft', 'trimmt',
         'trinkt', 'tritt', 'weilt', 'weint', 'wirbt', 'wirft', 'wirkt',
         'würgt', 'würzt', 'zählt', 'zähmt', 'zielt', 'zieht', 'weiß', 'weist']
WORDS_DICT = {'baut': ['baut', 'braut', 'braucht', 'braust'],
              'braut': ['braut', 'baut', 'braucht', 'braust'],
              'bleibt': ['bleibt', 'bleicht', 'blickt', 'blecht'],
              'bleicht': ['bleicht', 'bleibt', 'blickt', 'blecht'],
              'fliegt': ['fliegt', 'flieht', 'fleht', 'fließt'],
              'flieht': ['flieht', 'fliegt', 'fleht', 'fließt'],
              'fühlt': ['fühlt', 'führt', 'füllt', 'friert'],
              'führt': ['führt', 'fühlt', 'füllt', 'friert'],
              'füllt': ['füllt', 'führt', 'fühlt', 'friert'],
              'gibt': ['gibt', 'gießt', 'giert', 'gilt'],
              'gießt': ['gießt', 'gibt', 'giert', 'gilt'],
              'grimmt': ['grimmt', 'grinst', 'grient', 'grillt'],
              'grinst': ['grinst', 'grimmt', 'grient', 'grillt'],
              'hackt': ['hackt', 'harkt', 'harrt', 'hat'],
              'harkt': ['harkt', 'hackt', 'harrt', 'hat'],
              'herrscht': ['herrscht', 'herzt', 'härtet', 'hetzt'],
              'herzt': ['herzt', 'herrscht', 'härtet', 'hetzt'],
              'hockt': ['hockt', 'hofft', 'holt', 'horcht'],
              'hofft': ['hofft', 'hockt', 'holt', 'horcht'],
              'kämmt': ['kämmt', 'kämpft', 'kennt', 'kehrt'],
              'kämpft': ['kämpft', 'kämmt', 'kennt', 'kehrt'],
              'kauft': ['kauft', 'kaut', 'klaut', 'klaubt'],
              'kaut': ['kaut', 'kauft', 'klaut', 'klaubt'],
              'klaut': ['klaut', 'kauft', 'kaut', 'klaubt'],
              'klaubt': ['klaubt', 'klaut', 'kauft', 'kaut'],
              'knurrt': ['knurrt', 'kurt', 'knufft', 'knüpft'],
              'kurt': ['kurt', 'knurrt', 'knufft', 'knüpft'],
              'kreischt': ['kreischt', 'kreist', 'kriegt', 'kreuzt'],
              'kreist': ['kreist', 'kreischt', 'kriegt', 'kreuzt'],
              'kühlt': ['kühlt', 'kürt', 'küsst', 'kürzt'],
              'kürt': ['kürt', 'kühlt', 'küsst', 'kürzt'],
              'lärmt': ['lärmt', 'lernt', 'lässt', 'lehnt'],
              'lernt': ['lernt', 'lärmt', 'lässt', 'lehnt'],
              'liebt': ['liebt', 'liegt', 'liest', 'lügt'],
              'liegt': ['liegt', 'liebt', 'liest', 'lügt'],
              'liest': ['liest', 'liegt', 'liebt', 'lügt'],
              'lügt': ['lügt', 'liest', 'liegt', 'liebt'],
              'mahnt': ['mahnt', 'malt', 'mag', 'meint'],
              'malt': ['malt', 'mahnt', 'mag', 'meint'],
              'nickt': ['nickt', 'nippt', 'niest', 'nimmt'],
              'nippt': ['nippt', 'nickt', 'niest', 'nimmt'],
              'packt': ['packt', 'parkt', 'plagt', 'paart'],
              'parkt': ['parkt', 'packt', 'plagt', 'paart'],
              'patzt': ['patzt', 'platzt', 'protzt', 'putzt'],
              'platzt': ['platzt', 'patzt', 'protzt', 'putzt'],
              'prahlt': ['prahlt', 'prallt', 'plant', 'prellt'],
              'prallt': ['prallt', 'prahlt', 'plant', 'prellt'],
              'raubt': ['raubt', 'raucht', 'raunt', 'rauscht'],
              'raucht': ['raucht', 'raubt', 'raunt', 'rauscht'],
              'raunt': ['raunt', 'raucht', 'raubt', 'rauscht'],
              'rauscht': ['rauscht', 'raunt', 'raucht', 'raubt'],
              'reibt': ['reibt', 'reicht', 'reimt', 'riecht'],
              'reicht': ['reicht', 'reibt', 'reimt', 'riecht'],
              'reimt': ['reimt', 'reicht', 'reibt', 'riecht'],
              'reist': ['reist', 'reizt', 'reift', 'reitet'],
              'reizt': ['reizt', 'reist', 'reift', 'reitet'],
              'reift': ['reift', 'reizt', 'reist', 'reitet'],
              'rückt': ['rückt', 'rügt', 'ringt', 'rührt'],
              'rügt': ['rügt', 'rückt', 'ringt', 'rührt'],
              'ruft': ['ruft', 'ruht', 'rußt', 'rumst'],
              'ruht': ['ruht', 'ruft', 'rußt', 'rumst'],
              'sägt': ['sägt', 'sät', 'setzt', 'senst'],
              'sät': ['sät', 'sägt', 'setzt', 'senst'],
              'säuft': ['säuft', 'seufzt', 'säugt', 'säubert'],
              'seufzt': ['seufzt', 'säuft', 'säugt', 'säubert'],
              'saugt': ['saugt', 'saust', 'sorgt', 'suhlt'],
              'saust': ['saust', 'saugt', 'sorgt', 'suhlt'],
              'schiebt': ['schiebt', 'schielt', 'schießt', 'schindet'],
              'schielt': ['schielt', 'schiebt', 'schießt', 'schindet'],
              'schießt': ['schießt', 'schielt', 'schiebt', 'schindet'],
              'schläft': ['schläft', 'schlägt', 'schleckt', 'schleppt'],
              'schlägt': ['schlägt', 'schläft', 'schleckt', 'schleppt'],
              'schleckt': ['schleckt', 'schleppt', 'schlägt', 'schläft'],
              'schleppt': ['schleppt', 'schleckt', 'schlägt', 'schläft'],
              'schleicht': ['schleicht', 'schleift', 'schreibt', 'schreit'],
              'schleift': ['schleift', 'schleicht', 'schreibt', 'schreit'],
              'schreibt': ['schreibt', 'schleift', 'schleicht', 'schreit'],
              'schreit': ['schreit', 'schleift', 'schleicht', 'schreibt'],
              'schmollt': ['schmollt', 'schmort', 'schwört', 'schnorrt'],
              'schmort': ['schmort', 'schmollt', 'schwört', 'schnorrt'],
              'schnauft': ['schnauft', 'schnaubt', 'schraubt', 'schrabt'],
              'schnaubt': ['schnaubt', 'schnauft', 'schraubt', 'schrabt'],
              'schraubt': ['schraubt', 'schnaubt', 'schnauft', 'schrabt'],
              'schweigt': ['schweigt', 'schweißt', 'schwitzt', 'schmeißt'],
              'schweißt': ['schweißt', 'schweigt', 'schwitzt', 'schmeißt'],
              'schwitzt': ['schwitzt', 'schweißt', 'schweigt', 'schmeißt'],
              'schwimmt': ['schwimmt', 'schwingt', 'schwänkt', 'schminkt'],
              'schwingt': ['schwingt', 'schwimmt', 'schwänkt', 'schminkt'],
              'siebt': ['siebt', 'siecht', 'sieht', 'siegt'],
              'siecht': ['siecht', 'siebt', 'sieht', 'siegt'],
              'sieht': ['sieht', 'siecht', 'siebt', 'siegt'],
              'siegt': ['siegt', 'sieht', 'siecht', 'siebt'],
              'speist': ['speist', 'speit', 'steigt', 'steift'],
              'speit': ['speit', 'speist', 'steigt', 'steift'],
              'steigt': ['steigt', 'speist', 'speit', 'steift'],
              'stockt': ['stockt', 'stoppt', 'stopft', 'staut'],
              'stoppt': ['stoppt', 'stockt', 'stopft', 'staut'],
              'stelzt': ['stelzt', 'stellt', 'stiehlt', 'steht'],
              'stellt': ['stellt', 'stelzt', 'stiehlt', 'steht'],
              'stiehlt': ['stiehlt', 'stelzt', 'stellt', 'steht'],
              'strafft': ['strafft', 'straft', 'strahlt', 'schafft'],
              'straft': ['straft', 'strafft', 'stelzt', 'schafft'],
              'stelzt': ['stelzt', 'straft', 'strafft', 'schafft'],
              'streicht': ['streicht', 'streikt', 'streift', 'streitet'],
              'streikt': ['streikt', 'streicht', 'streift', 'streitet'],
              'stürzt': ['stürzt', 'stützt', 'stupst', 'stutzt'],
              'stützt': ['stützt', 'stürzt', 'stupst', 'stutzt'],
              'stupst': ['stupst', 'stützt', 'stürzt', 'stutzt'],
              'stutzt': ['stutzt', 'stützt', 'stürzt', 'stupst'],
              'tankt': ['tankt', 'tanzt', 'tagt', 'trabt'],
              'tanzt': ['tanzt', 'tankt', 'tagt', 'trabt'],
              'taucht': ['taucht', 'tauscht', 'taut', 'traut'],
              'tauscht': ['tauscht', 'taucht', 'taut', 'traut'],
              'taut': ['taut', 'taucht', 'tauscht', 'traut'],
              'tickt': ['tickt', 'tippt', 'tippelt', 'tilgt'],
              'tippt': ['tippt', 'tickt', 'tippelt', 'tilgt'],
              'tränkt': ['tränkt', 'trennt', 'trägt', 'tränt'],
              'trennt': ['trennt', 'tränkt', 'trägt', 'tränt'],
              'trimmt': ['trimmt', 'trinkt', 'trübt', 'trügt'],
              'trinkt': ['trinkt', 'trimmt', 'trübt', 'trügt'],
              'trifft': ['trifft', 'tritt', 'trieft', 'triezt'],
              'tritt': ['tritt', 'trifft', 'trieft', 'triezt'],
              'weilt': ['weilt', 'weint', 'weiß', 'weist'],
              'weint': ['weint', 'weilt', 'weiß', 'weist'],
              'weiß': ['weiß', 'weint', 'weilt', 'weist'],
              'weist': ['weist', 'weilt', 'weint', 'weiß'],
              'wirft': ['wirft', 'wirkt', 'wirbt', 'wird'],
              'wirkt': ['wirkt', 'wirft', 'wirbt', 'wird'],
              'wirbt': ['wirbt', 'wirft', 'wirkt', 'wird'],
              'würgt': ['würgt', 'würzt', 'wühlt', 'winkt'],
              'würzt': ['würzt', 'würgt', 'wühlt', 'winkt'],
              'zählt': ['zählt', 'zähmt', 'zielt', 'zieht'],
              'zähmt': ['zähmt', 'zählt', 'zielt', 'zieht'],
              'zielt': ['zielt', 'zählt', 'zähmt', 'zieht'],
              'zieht': ['zieht', 'zählt', 'zähmt', 'zielt']}
OK_WORDS = []
for i, word in enumerate(WORDS):
    if word in WORDS_DICT.keys():
        OK_WORDS.append(word)
ALL_TRIALS = [i for i in product(NAMES, ['qu2', 'st2'], OK_WORDS)]
np.random.shuffle(ALL_TRIALS)
ALL_TRIALS, PRACTICE_TRIALS = ALL_TRIALS[:720], ALL_TRIALS[720:]
TRIALS_THIS_SESSION = ALL_TRIALS[:240]

SOUND_PATH = os.path.join(os.path.dirname(os.getcwd()), 'stimuli', 'audio', 'test')
SOUND_FILES = [os.path.join(SOUND_PATH, f) for f in os.listdir(SOUND_PATH) if '.wav' in f]
SOUND_FILES = tools.audio.load_sounds(SOUND_FILES)

def gen_control(proband_id, stimulation):
    """Generates a control iterable. Each item in the list is a tuple that
    represents a trial in the format: (proband_id, test_name, stimulation,
    phase, blockn, task, trialn, speaker, intonation, word, f, ans, alt1, alt2,
    alt3, alt4)."""
    pj, pd, cwd = os.path.join, os.path.dirname, os.getcwd()
    sentence_path = pj(pd(cwd), 'stimuli', 'audio', 'test')

    speaker_trials = list(TRIALS_THIS_SESSION)
    np.random.shuffle(speaker_trials)
    speech_trials = list(TRIALS_THIS_SESSION)
    np.random.shuffle(speech_trials)

    def get_f(speaker, intonation, word):
        """Determines the filename given the speaker, intonation, or word."""
        a = dict(zip(NAMES, CODES))[speaker]
        b = intonation
        c = ''
        i = WORDS.index(word)
        if i < 100:
            c += '0'
        if i < 10:
            c += '0'
        c += str(i)
        return pj(sentence_path, '_'.join([a, b, c]) + '.wav')

    def test_trial(blockn, trialn):
        """Determines the trial info for a particular trial."""
        if blockn % 2 == 0:
            task = TASKS[0]
            speaker, intonation, word = speaker_trials.pop(0)
            ans = speaker
            alt1, alt2, alt3, alt4 = NAMES
        else:
            task = TASKS[1]
            speaker, intonation, word = speech_trials.pop(0)
            ans = word
            alt1, alt2, alt3, alt4 = sorted(WORDS_DICT[word])
        f = get_f(speaker, intonation, word)
        phase = 'test'
        return (proband_id, TEST_NAME, stimulation, phase, blockn, task,
                trialn, speaker, intonation, word, f, ans, alt1, alt2, alt3,
                alt4)

    def prac_trial(blockn, trialn):
        """Determines the trial info for a particular trial."""
        speaker, intonation, word = PRACTICE_TRIALS.pop(0)
        if blockn % 2 == 0:
            task = TASKS[0]
            ans = speaker
            alt1, alt2, alt3, alt4 = NAMES
        else:
            task = TASKS[1]
            ans = word
            alt1, alt2, alt3, alt4 = sorted(WORDS_DICT[word])
        f = get_f(speaker, intonation, word)
        phase = 'practice'
        return (proband_id, TEST_NAME, stimulation, phase, blockn, task,
                trialn, speaker, intonation, word, f, ans, alt1, alt2, alt3,
                alt4)

    control = []
    for blockn in [-2, -1]:
        t = [prac_trial(blockn, trialn) for trialn in xrange(PRACTICE_TRIALSN)]
        control += t
    for blockn in xrange(len(TASKS) * BLOCKS_PER_TASK):
        t = [test_trial(blockn, trialn) for trialn in xrange(TRIALS_PER_BLOCK)]
        control += t

    return control


def session(proband_id, stimulation):
    """Runs the session."""
    data = tools.data.load_data(proband_id, TEST_NAME)

    if not data.control and not data.data:
        data.control = gen_control(proband_id, stimulation)
        data.data = []

    screen, font = tools.gui.create_screen(), tools.gui.create_font(size=24)
    m = INSTRUCTIONS.pop(0).decode('utf-8')
    tools.gui.splash(screen, font, m, wait=True)

    while data.control and not data.test_done:
        trial_info = data.control.pop(0)
        trial_info = trial(data, screen, font, trial_info)
        if trial_info:
            data.data.append(trial_info)
        if proband_id != 'TEST':
            data.update()

    m = INSTRUCTIONS.pop().decode('utf-8')
    tools.gui.splash(screen, font, m, wait=True)


def trial(data, screen, font, trial_info):
    """Runs a single trial."""
    (_, _, _, phase, blockn, task, trialn, _, _, _, f, _, alt1, alt2, alt3,
     alt4) = trial_info
    alts = (alt1, alt2, alt3, alt4)
    print trial_info
    print 'trial started'

    def display_alternatives(rsp):
        """Shortcut function that updates the display on a trial."""
        colours = [tools.gui.DEFAULT_TEXT_COLOUR] * 4
        if rsp:
            colours[rsp - 1] = tools.gui.BLUE
        R = []
        for x, alt, colour in zip(NAME_POSITIONS, alts, colours):
            p = (screen, font, alt.decode('utf-8'), (x, 150), colour)
            _, r = tools.gui.blit_text(*p, update=False)
            R.append(r)
        tools.gui.update()
        print len(R)

    if trialn == 0 and blockn < 1:
        print 'splashing'
        m = INSTRUCTIONS.pop(0).decode('utf-8')
        tools.gui.splash(screen, font, m, mouse=False, wait=True)

        m = INSTRUCTIONS.pop(0).decode('utf-8')
        time_left = 5.
        clock = tools.events.Clock()
        while time_left > 0:
            time_left = time_left - clock.tick_busy_loop() / 1000.
            s = m % int(round(time_left))
            tools.gui.splash(screen, font, s, wait=False)
            tools.events.wait(.5)
        print 'got through splash'
    print 'setting up trial gui'
    tools.gui.wipe(screen, update=False)
    m = INSTRUCTIONS[-4: -2][TASKS.index(task)]
    p = (screen, font, m.decode('utf-8'), (0, 0), tools.gui.DEFAULT_TEXT_COLOUR)
    tools.gui.blit_text(*p, update=False)
    m = INSTRUCTIONS[-2] % (blockn, trialn)
    p = (screen, font, m.decode('utf-8'), (0, -150), tools.gui.DEFAULT_TEXT_COLOUR)
    tools.gui.blit_text(*p, update=False)
    display_alternatives(None)
    print 'gui set up'

    print 'waiting for response', blockn, trialn
    responses = []
    rsp = None
    current_time = 0.
    print 'making clock'
    clock = tools.events.Clock()
    keys = [str(k) for k in KEYS]
    print 'playing sound'
    tools.audio.play_sound(f, dic=SOUND_FILES)
    print 'initiating loop'
    while current_time < ITI * 1000:
        current_time += clock.tick_busy_loop()
        rsp = tools.events.poll_for_valid_keydown(keys, 'unicode')
        if rsp:
            responses.append(alts[int(rsp) - 1])
            responses.append(current_time)
            display_alternatives(int(rsp))
            tools.events.wait(.05)
            display_alternatives(None)
    if blockn >= 0 and trialn == (TRIALS_PER_BLOCK - 1):
        m = INSTRUCTIONS[-5].decode('utf-8')
        time_left = IBI
        clock = tools.events.Clock()
        while time_left > 0:
            time_left = time_left - clock.tick_busy_loop() / 1000.
            s = m % int(round(time_left))
            tools.gui.splash(screen, font, s, wait=False)
            tools.events.wait(.5)
    print 'ending trial'

    return tuple(list(trial_info) + responses)


def main():
    if len(sys.argv) == 3:
        proband_id, pn = sys.argv[1:]
    else:
        proband_id = raw_input('Type the subject ID>>>')
        m = 'Type the type of tDCS stimulation (AN, CA, or SH)>>>'
        stimulation = raw_input(m)
    session(proband_id, stimulation)


if __name__ == '__main__':
    main()