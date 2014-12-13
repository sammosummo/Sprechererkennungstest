# -*- coding: utf-8 -*-
"""
Created on Tue Jun 03 14:19:17 2014

Functions for handling buttons and key presses, and test-specific functions
related to events.

@author: Sam Mathias
"""

import pygame, sys

Clock = pygame.time.Clock

def wait(t):
    """Just wait (literally do nothing) for t seconds."""
    pygame.time.delay(int(t*1000))

def wait_for_keydown(escape=True, clear=False):
    """Idle until a key is pressed. Optionally kills python if it detects
    Esc. Returns the event and the length of time since the function was
    called."""
    if clear:
        pygame.event.clear()
    pygame.event.set_allowed(None)
    pygame.event.set_allowed(pygame.KEYDOWN)
    clock = Clock()
    clock.tick_busy_loop()
    while 1:
        event = pygame.event.wait()
        if escape and event.key == pygame.K_ESCAPE:
            sys.exit()
        else:
            return event, clock.tick_busy_loop()

def poll_for_valid_keydown(valid_responses, check_type, escape=True):
    """Poll the event list for a keydown with a key in valid_responses. This
    is useful in tasks where trials are time-limited. Returns None each time
    no response is found. Note that this function does not return reaction
    times. Those should be recorded in the loop that calls this function."""
    try:
        event = pygame.event.poll()
    except:
        return None
    if event.type == pygame.KEYDOWN:
        if escape and event.key == pygame.K_ESCAPE:
            sys.exit()
        if check_type=='unicode' and event.unicode in valid_responses:
            return event.unicode
        if check_type=='key' and event.key in valid_responses:
            return event.key
    else:
        return None
            
def wait_for_valid_keydown(valid_responses, check_type, escape=True):
    """Idle until a valid key is pressed. Requires a list of possible responses
    and whether those are unicodes or pygame keys. Optionally kills python if
    it detects Esc."""
    while 1:
        event, rt = wait_for_keydown(escape)
        if check_type=='unicode' and event.unicode in valid_responses:
            return event.unicode, rt
        if check_type=='key' and event.key in valid_responses:
            return event.key, rt

def wait_for_arrowkey(labels=None):
    """A specific variety of valid_keydown check that returns the arrowkey
    label. If the argument is omitted or None, the default is to assume the
    labels are yes/np"""
    if not labels:
        labels = ['Yes', 'No']
    keys = {pygame.K_LEFT: labels[0], pygame.K_RIGHT: labels[1]}
    key, rt = wait_for_valid_keydown(keys.keys(), 'key')
    return keys[key], rt

def wait_for_mouse_click(escape=True, clear=False):
    """Idle until the mouse is clicked. Optionally kills python if it detects
    Esc."""
    pygame.mouse.set_visible(True)
    if clear:
        pygame.event.clear()
    pygame.event.set_allowed(None)
    pygame.event.set_allowed([pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN])
    clock = Clock()
    clock.tick_busy_loop()
    while 1:
        event = pygame.event.wait()
        if event.type == pygame.KEYDOWN:
            if escape and event.key == pygame.K_ESCAPE:
                sys.exit()
        else:
            return event, clock.tick_busy_loop()

def wait_for_valid_mouse_click(screen, button, zones, escape=True):
    """Idle until a mouse click is made within a valid zone. 'Zones' is a list
    of pygame Rects. Returns the zone index (e.g., 0 for zone 1, 1 for zone 2,
    etc)."""
    while 1:
        event, rt = wait_for_mouse_click(escape)
        if event.button == button:
            for i, zone in enumerate(zones):
                if zone.collidepoint(event.pos):
                    return i, rt