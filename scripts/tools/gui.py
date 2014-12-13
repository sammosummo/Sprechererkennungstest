# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 15:20:47 2013

Some generic and some task-specific functions for drawing to the screen. All of
these are essentially just shortcuts built around pygame functions.

@author: smathias
"""

import os, pygame
import events

#colours
BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREY = 190, 190, 190
DARK_GREY = 125, 125, 125
SLATE = 109, 132, 155
RED = 150, 0, 0
GREEN = 0, 150, 0
YELLOW = 255,255,0
BLUE = 0, 0, 255
BG_COLOUR = GREY
DEFAULT_TEXT_COLOUR = BLACK

#shortcuts
flip = pygame.display.flip
update = pygame.display.update

#others
STIM_PATH = os.path.join(os.path.dirname(os.getcwd()), 'stimuli', 'visual')
PRELOADED_ARROWKEYS = False
PRELOADED_SYMBOLS = False
PRELOADED_CLICKABLE_WORDS = False
PRELOADED_SPACEBAR = False
WINDOW = 800, 800

def create_screen(window_size=None, full=True):
    """Create a new pygame window. Optionally specify the window size and
    whether to run full-screen. If full and no window size is given (default
    option), the screen will be set to native resolution."""
    pygame.init()
    if window_size:
        window = window_size
    elif full:
        info = pygame.display.Info()
        window = (info.current_w, info.current_h)
    else:
        window = WINDOW
    if full:
        screen = pygame.display.set_mode(window, pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode(window)
    screen.fill(BG_COLOUR)
    return screen

def create_font(style='Courier', size=36, bold=True, italic=False):
    """Create a new pygame font. Uses system fonts."""
    pygame.font.init()
    return pygame.font.SysFont(style, size, bold=bold, italic=italic)

def wipe(screen, r=None, update=True):
    """Wipe (fill with background colour) either the entire screen if r is
    None, or an area defined by r, which should be a pygame Rect."""
    if r:
        if hasattr(r, '__iter__'):
            [screen.fill(BG_COLOUR, a) for a in r]
        else:
            screen.fill(BG_COLOUR, r)
        if update:
            pygame.display.update(r)
    else:
        screen.fill(BG_COLOUR)
        if update:
            pygame.display.flip()

def blit_text(screen, font, s, pos, colour=None, blit=True, update=True,
              pos_rel_centre=True):
    """Blit a single line of text s to the screen. Also requires the screen
    and the font objects, and a tuple to determine the xy coordinates. If no
    colour argument is specified, the deault colour is used. Optionally updates
    the screen just in the rectangular area containing the text. Returns the
    rect of the text (this is sometimes handy)."""
    if not colour:
        colour = DEFAULT_TEXT_COLOUR
    q = font.render(s, True, colour)
    r = q.get_rect()
    if pos_rel_centre:
        x, y = screen.get_rect().center
        r.center = x + pos[0], y + pos[1]
    else:
        r.x, r.y = pos
    screen.fill(BG_COLOUR, r)
    if blit:
        screen.blit(q, r)
    if update:
        pygame.display.update(r)
    return q, r

def splash(screen, font, s, wait=True, mouse=False, clear_events=True):
    """Make a splash screen. Typically these are used for displaying task
    instructions or demarking the begining/end of one phase of a test. Splashes
    clear all the previous content and are drawn to the centre of the screen.
    The message string s can contain multiple lines, which are parsed and
    blitted separately. Standard python line breaks (\\n) are handled. Can also
    clear events, hide/display the mouse, and wait for a key press to continue."""
    if clear_events:
        pygame.event.clear()
    if not mouse:
        pygame.mouse.set_visible(False)
    else:
        pygame.mouse.set_visible(True)
    screen.fill(BG_COLOUR)
    S = s.split('\n')
    x, y = (0, 0)
    X = [x] * len(S)
    Y = [y + i * font.get_linesize() for i in xrange(len(S))]
    Y = [int(y - float(sum(Y)/float(len(Y)))) for y in Y]
    [blit_text(screen, font, s, xy, update=False) for s, xy in zip(S, zip(X, Y))]
    pygame.display.flip()
    if wait:
        events.wait_for_keydown()

def blit_image(screen, image, pos, update=True, pos_rel_centre=True):
    """Draw a single image to the screen. 'image' can be a string representing
    the path of an image or a pygame surface. Technically this should work for
    any surface object. Returns the rect. PNGs are preferred."""
    if type(image) == str:
        image = pygame.image.load(image)
        image = image.convert_alpha()
    r = image.get_rect()
    if pos_rel_centre:
        x, y = screen.get_rect().center
        r.center = x + pos[0], y + pos[1]
    else:
        r.x, r.y = pos
    screen.fill(BG_COLOUR, r)
    screen.blit(image, r)
    if update:
        pygame.display.update(r)
    return r

def preload_arrowkeys(labels):
    """Arrow keys are used in a number of tests to represent 'yes' and 'no'
    responses. Pre-loading them saves some time."""
    global PRELOADED_ARROWKEYS, ARROWKEYS
    img = lambda f: pygame.image.load(f).convert_alpha()
    p = os.path.join(STIM_PATH, 'keyboard_keys')
    ARROWKEYS = {labels[0]: {DEFAULT_TEXT_COLOUR:img(os.path.join(p,
                                                               'gauche.png')),
                             RED:img(os.path.join(p, 'gauche_rouge.png')),
                             GREEN:img(os.path.join(p, 'gauche_vert.png')),
                             BLUE:img(os.path.join(p, 'gauche_bleu.png'))},
                 labels[1]:{DEFAULT_TEXT_COLOUR:img(os.path.join(p,
                                                               'droite.png')),
                            RED:img(os.path.join(p, 'droite_rouge.png')),
                            GREEN:img(os.path.join(p, 'droite_vert.png')),
                            BLUE:img(os.path.join(p, 'droite_bleu.png'))}}
    PRELOADED_ARROWKEYS = True

def draw_arrowkeys(screen, font, colours, labels, s, s_clr, flip=True):
    """Draw arrow keys, along with labels and instructions. Returns the
    instructions rect so it can be cleared easily later."""
    if not PRELOADED_ARROWKEYS:
        preload_arrowkeys(labels)
    images = (ARROWKEYS[labels[0]][colours[0]],
              ARROWKEYS[labels[1]][colours[1]])
    positions = [(-100, 300), (100, 300)]
    q, r = blit_text(screen, font, s, (0,200), s_clr, update=False)
    arrows = []
    for image, pos, label, colour in zip(images, positions, labels, colours):
        arrows.append(blit_image(screen, image, pos, update=False))
        arrows.append(blit_text(screen, font, label, (pos[0],pos[1]+80), colour, update=False)[1])
    if flip:
        pygame.display.flip()
    else:
        pygame.display.update(arrows)
    return r

def preload_spacebar():
    """The spacebar is  used in a number of tests to represent 'yes' and 'no'
    responses. Pre-loading them saves some time."""
    global PRELOADED_SPACEBAR, SPACEBAR
    img = lambda f: pygame.image.load(f).convert_alpha()
    p = os.path.join(STIM_PATH, 'keyboard_keys')
    SPACEBAR = {DEFAULT_TEXT_COLOUR:img(os.path.join(p,'espace.png')),
                RED:img(os.path.join(p,'espace_rouge.png')),
                GREEN:img(os.path.join(p,'espace_vert.png')),
                BLUE:img(os.path.join(p,'espace_bleu.png'))}
    PRELOADED_SPACEBAR = True

def draw_spacebar(screen, font, colour, s, s_clr, flip=True):
    """Draw spacebar and instructions. Returns the rects so they can be cleared
    easily later."""
    if not PRELOADED_SPACEBAR:
        preload_spacebar()
    r2 = blit_image(screen, SPACEBAR[colour], (0, 300), update=False)
    q, r1 = blit_text(screen, font, s, (0, 200), s_clr, update=False)
    if flip:
        pygame.display.flip()
    return r1, r2

def define_zones(screen, rect, draw=True, flip=False):
    """Defines clickable zones on-screen. For the matrix-reasoning task, rect
    is a pygame Rect that is divided horizontally into five square areas with
    borders printed. For the emotion-recognition task, rect is a list of five
    words that are printed to the screen and their Rects are treated as zones.
    """
    w, h, x, y = rect.w/5, rect.h, rect.x, rect.y
    zones = []
    for i in xrange(5):
        zone = pygame.Rect(x + i*w, y, w, h)
        if draw:
            pygame.draw.rect(screen, BLACK, zone, 3)
        zones.append(zone)
    if flip:
        pygame.display.flip()
    return zones

def preload_symbols(test_name='digit_symbol'):
    """The digit-symbol test was particularly sluggish on my iMac when coding.
    This Pre-loads the symbols. Also works for the IPCPTS test."""
    global PRELOADED_SYMBOLS, SYMBOLS
    img = lambda f: pygame.image.load(f).convert_alpha()
    p = os.path.join(STIM_PATH, test_name)
    SYMBOLS = sorted([f for f in os.listdir(p) if 'sym' in f and '.bmp' in f])
    SYMBOLS = [img(os.path.join(p, f)) for f in SYMBOLS]
    PRELOADED_SYMBOLS = True

def draw_digsym_array(screen, font, digit=True, symbol=True, flip=True):
    """Specifically for the digit-symbol test. Draw the symbols, digits, and
    black borders; preload if not already."""
    if not PRELOADED_SYMBOLS:
        preload_symbols()
    spacing = 100
    x, y = screen.get_rect().center
    X = range(-spacing*4, spacing*5, spacing)
    rects = []
    for i in xrange(9):
        r = pygame.Rect(x+X[i]-40, y-350, spacing-19, 165)
        pygame.draw.rect(screen, BLACK, r, 3)
        if digit:
            blit_image(screen, SYMBOLS[i], (X[i], -300), update=False)
        else:
            blit_text(screen, font, '?', (X[i], -300), DEFAULT_TEXT_COLOUR, update=False)
        if symbol:
            blit_text(screen, font, str(i+1), (X[i], -220), DEFAULT_TEXT_COLOUR, update=False)
        else:
            blit_text(screen, font, '?', (X[i], -220), DEFAULT_TEXT_COLOUR, update=False)
        rects.append(r)
    if flip:
        pygame.display.flip()
    return rects

def draw_ipcpts_trial(screen, font, symbols, m, colour):
    """Draw the three symbols to the centre of the screen."""
    if not PRELOADED_SYMBOLS:
        preload_symbols('ipcpts')
    rects = []
    if symbols:
        for i, symbol in enumerate(symbols):
            r = blit_image(screen, SYMBOLS[symbol], (-200+(200*i), 0), update=False)
            rects.append(r)
    rects += list(draw_spacebar(screen, font, colour, m, colour, flip=False))
    pygame.display.update(rects)
    return rects

def draw_digsym_trial(screen, font, f, digit, flip=True):
    """Specifically for the digit-symbol test. Draw the trial symbol and
    digit."""
    if f:
        blit_image(screen, f, (0,-100), update=False)
    if digit:
        blit_text(screen, font, str(digit), (0,0), update=False)
    if flip:
        pygame.display.flip()

def clickable_words(screen, font, words, colours=None, spacing=100, blit=True):
    """Pre-load a clickable word set for the emotion-recognition test. Prints
    the words to the screen and creates a global variable ZONES containing
    pygame Rects that define the clickable areas."""
    print colours
    global PRELOADED_CLICKABLE_WORDS, ZONES
    x, y = screen.get_rect().center
    widths, txt, ZONES = [], [], []
    if not colours:
        colours = [DEFAULT_TEXT_COLOUR] * len(words)
    for word, colour in zip(words, colours):
        q, r = blit_text(screen, font, word, (0,300), colour, blit=False,
                         update=False)
        widths += [r.w, spacing]
        txt.append(q)
        ZONES.append(r)
    left = x - int((sum(widths)-spacing)/2)
    for i in xrange(len(ZONES)):
        if i == 0:
            ZONES[i].left = left
        else:
            ZONES[i].left = left + i*spacing + sum(ZONES[j].w for j in xrange(i))
        screen.fill(BG_COLOUR, ZONES[i])
        if blit:
            screen.blit(txt[i], ZONES[i])
#        pygame.display.update(ZONES[i])
    PRELOADED_CLICKABLE_WORDS = True

def blit_semitrans_rect(screen, rect, colour, update=False, alpha=125):
    """Blit a semi-transparent rectangle to the screen."""
    colour = list(colour) + [alpha]
    q = pygame.Surface((rect.w, rect.h), flags=pygame.SRCALPHA)
    q.fill(colour)
    screen.blit(q, rect)
    if update:
        pygame.display.update(rect)


class CVLTGUI:

    """Special class for gui for the CVLT task."""

    def __init__(self, screen, font, words):
        self.y_unit = int(font.get_linesize() * 2)
        self.x_unit = int(x_unit / 2)
        x0, y0 = screen.get_rect().center
        self.x0 -= (8 * font.get_linesize())
        self.y0 -= (9 * font.get_linesize())
        self.X = [0, 0, 0, 0, 5, 5, 5, 5]*2
        self.Y = [0, 2, 4, 6, 0, 2, 4, 6, 9, 11, 13, 15, 9, 11, 13, 15]
        self.words = words
        self.buttons = [Button(i, word) for i, word in enumerate(words)]
        # set up screen
        screen.fill(BG_COLOUR)
        [button.blit() for button in self.buttons]
        instr.blit()

    class Button:
        """Clickable button for the CVLT task."""
        def __init__(self, i, label):
            self.i = i
            self.label = label
            x0, y0 = screen.get_rect().center

            h = font.get_linesize()
            w = font.get_linesize() * 4




#def ready_screen(screen, font, t):
#    """Wait for t seconds, with a countdown timer."""
#    screen.fill(BG_COLOUR)
#    s = lambda t: 'Test will begin in: %i' %(t+1)
#    clock = Clock()
#    ct = 0
#    while ct < t:
#        splash(screen, font, s(t - ct), wait=False)
#        ct += (clock.tick()/1000.)