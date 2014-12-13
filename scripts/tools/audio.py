# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 15:20:47 2013

For drawing to the screen. Contains a bunch of functions; some are generic and
are used by almost every test, others are test-specific.

@author: smathias
"""

import pygame, os, events

PRELOADED_FEEDBACK = False

def load_sounds(l):
    """Loads all sounds in l. May prevent parachute errors."""
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    sounds = [pygame.mixer.Sound(f) for f in l]
    return dict(zip(l, sounds))
    

def play_sound(f, wait=False, dic=None):
    """Play sound. Just a wrapper around the pygame rountine. If a dictionary
    is supplied, this will look to see if a preloaded sound object is inside.
    """
    if not pygame.mixer.get_init():
        pygame.mixer.init()
    if dic:
        sound = dic[f]
    else:
        sound = pygame.mixer.Sound(f)
    sound.play()
    if wait:
        while pygame.mixer.get_busy():
            events.wait(0.01)
    return sound

def play_feedback(corr):
    """Play the correct or incorrect sound depending on the Boolean corr."""
    if not PRELOADED_FEEDBACK:
        global FEEDBACK_SOUNDS
        p = os.path.join(os.path.dirname(os.getcwd()), 'stimuli', 'audio')
        FEEDBACK_SOUNDS = [pygame.mixer.Sound(os.path.join(p, 'Wrong.wav')),
                           pygame.mixer.Sound(os.path.join(p, 'Correct.wav'))]
    FEEDBACK_SOUNDS[corr].play()