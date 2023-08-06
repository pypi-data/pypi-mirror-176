import os
import sys
import readline
from glob import glob
from .charDef import *
from . import colors
from . import utils
from . import cursor
from . import keyhandler
from . import messages

def file_path_completer():
    def completer(text, n):
        return [i + '/' if os.path.isdir(i) else i + '\t' for i in glob(os.path.expanduser(text) + '*')][n]
    return completer

def directory_path_completer():
    def completer(text, n):
        return [i + '\t' for i in glob(os.path.expanduser(text) + '*') if os.path.isdir(i)][n]
    return completer

def choice_completer(completion_words, max_completions=None):
    def completer(text, n):
        completions = readline.get_line_buffer().split('\t')[:-1]
        if max_completions is None or len(completions) < max_completions:
            return [i + '\t' for i in completion_words if i.startswith(text) and i not in completions][n]
    return completer

class Prompt:
    def __init__(self):
        self.message = None
        self.optkeys = None
        self.options = None
        self.default = None
    def set_message(self, message):
        if isinstance(message, str):
            self.message = message
        else:
            raise TypeError('Message must be a string')
    def set_single_default(self, default):
        if self.options is None:
            raise ValueError('Options must be set before defaults') from None
        if default not in self.optkeys:
            raise ValueError('default must be an element of option keys') from None
        self.pos = self.optkeys.index(default)
    def set_multiple_defaults(self, defaults):
        if self.options is None:
            raise ValueError('Options must be set before defaults') from None
        if isinstance(defaults, (list, tuple)):
            if any([i not in self.optkeys for i in defaults]):
                raise ValueError('default list must be a subset of option keys')
            self.checked = [True if i in defaults else False for i in self.optkeys]
        else:
            raise ValueError('default must be a list or tuple')
    def set_binary_default(self, default):
        if default in (True, False):
            self.default = default
        else:
            raise ValueError('default must be True or False') from None
    def set_options(self, options):
        if isinstance(options, (list, tuple, dict)):
            if not options:
                raise ValueError('Options can not be empty')
            if isinstance(options, dict):
                self.optkeys = []
                self.options = []
                for key, value in options.items():
                    self.optkeys.append(key)
                    self.options.append(value)
            else:
                self.options = options
                self.optkeys = options
        else:
            raise TypeError('Options must be a list, tuple or dict')
        self.pos = 0
        self.checked = [False]*len(options)
    def set_true(self, options):
        if isinstance(options, (list, tuple)):
            if not options:
                raise ValueError('Options can not be empty')
            self.options_true = options
        else:
            raise TypeError('Options must be a list or tuple')
    def set_false(self, options):
        if isinstance(options, (list, tuple)):
            if not options:
                raise ValueError('Options can not be empty')
            self.options_false = options
        else:
            raise TypeError('Options must be a list or tuple')

class Completer(Prompt):
    def file_path(self):
        readline.set_completer_delims('\t\n')
        readline.parse_and_bind('tab: complete')
        readline.set_completer(file_path_completer())
        while True:
            print(self.message + ':')
            answer = input('')
            if answer:
                if os.path.isfile(answer):
                    return os.path.normpath(answer)
                elif os.path.exists(answer):
                    print('Path exists but is not a file, try again')
                else:
                    print('File does not exist, try again')
    def directory_path(self):
        readline.set_completer_delims('\t\n')
        readline.parse_and_bind('tab: complete')
        readline.set_completer(directory_path_completer())
        while True:
            print(self.message + ':')
            answer = input('')
            if answer:
                if os.path.isdir(answer):
                    return os.path.normpath(answer)
                elif os.path.exists(answer):
                    print('Path exists but is not a directory, try again')
                else:
                    print('Directory does not exist, try again')
    def single_choice(self):
        readline.set_completer_delims('\t\n')
        readline.parse_and_bind('tab: complete')
        readline.set_completer(choice_completer(self.options, 1))
        print(self.message)
        for option in self.options:
            print(' '*2 + option)
        message = 'Single choice (press TAB to autocomplete): '
        choice = input(message).strip()
        while True:
            if choice not in self.options:
                messages.warning('Invalid choice, try again')
            else:
                return self.optkeys[self.options.index(choice)]
    def multiple_choices(self):
        readline.set_completer_delims('\t\n')
        readline.parse_and_bind('tab: complete')
        readline.set_completer(self.choice_completer(self.options))
        print(self.message)
        for option in self.options:
            print(' '*2 + option)
        message = 'Multiple choice (press TAB to autocomplete): '
        choices = input(message).strip().split('\t')
        while True:
            if any([i not in self.options for i in choices]):
                messages.warning('Invalid choices, try again')
            else:
                return [self.optkeys[self.options.index(i)] for i in choices]
    def binary_choice(self):
        readline.set_completer_delims('\t\n')
        readline.parse_and_bind('tab: complete')
        readline.set_completer(self.choice_completer(self.options_true + self.options_false,1))
        while True:
            print(self.message, end='')
            answer = input(' ').strip()
            if answer:
                if answer in self.options_true:
                    return True
                elif answer in self.options_false:
                    return False
                else:
                    print('Invalid choice, type {} to accept or {} to reject'.format(
                        '/'.join(self.options_true), '/'.join(self.options_false)))
            elif self.default is not None:
                return self.default

@keyhandler.init
class Selector(Prompt):
    def __init__(
            self, 
            shift                     = 0,
            align                     = 0,
            indent                    = 0,
            margin                    = 1,
            pad_left                  = 1,
            pad_right                 = 1,
            radiobullet               = '>',
            checkbullet               = 'X',
            bullet_color              = colors.foreground['default'],
            bullet_on_switch          = colors.REVERSE,
            word_color                = colors.foreground['default'],
            word_on_switch            = colors.REVERSE,
            background_color          = colors.background['default'],
            background_on_switch      = colors.REVERSE,
        ):
        self.word_color = word_color
        self.word_on_switch = word_on_switch
        self.background_color = background_color
        self.background_on_switch = background_on_switch
        self.bullet_color = bullet_color
        self.bullet_on_switch = bullet_on_switch
        self.align = max(int(align), 0)
        self.shift = max(int(shift), 0)
        self.indent = max(int(indent), 0)
        self.margin = max(int(margin), 0)
        self.pad_left = max(int(pad_left), 0)
        self.pad_right = max(int(pad_right), 0)
        self.radiobullet = ' ' if radiobullet is None else radiobullet
        self.checkbullet = ' ' if checkbullet is None else checkbullet
        self.message = None
        self.optkeys = None
        self.options = None
    def printradio(self, idx):
        utils.forceWrite(' ' * (self.indent + self.align))
        back_color = self.background_on_switch if idx == self.pos else self.background_color
        word_color = self.word_on_switch if idx == self.pos else self.word_color
        bullet_color = self.bullet_on_switch if idx == self.pos else self.bullet_color
        utils.cprint(' ' * self.pad_left, on = back_color, end = '')
        if idx == self.pos:
            utils.cprint(self.radiobullet + ' ' * self.margin, bullet_color, back_color, end = '')
        else:
            utils.cprint(' ' * (len(self.radiobullet) + self.margin), bullet_color, back_color, end = '')
        utils.cprint(self.options[idx], word_color, back_color, end = '')
        utils.cprint(' ' * (self.max_width - len(self.options[idx])), on = back_color, end = '')
        utils.moveCursorHead()
    def toggleradio(self):
        pass
    def acceptradio(self):
        return self.optkeys[self.pos]
    def printcheck(self, idx):
        utils.forceWrite(' ' * (self.indent + self.align))
        back_color = self.background_on_switch if idx == self.pos else self.background_color
        word_color = self.word_on_switch if idx == self.pos else self.word_color
        bullet_color = self.bullet_on_switch if idx == self.pos else self.bullet_color
        utils.cprint(' ' * self.pad_left, on = back_color, end = '')
        if self.checked[idx]:
            utils.cprint(self.checkbullet + ' ' * self.margin, bullet_color, back_color, end = '')
        else:
            utils.cprint(' ' * (len(self.checkbullet) + self.margin), bullet_color, back_color, end = '')
        utils.cprint(self.options[idx], word_color, back_color, end = '')
        utils.cprint(' ' * (self.max_width - len(self.options[idx])), on = back_color, end = '')
        utils.moveCursorHead()
    def togglecheck(self):
        self.checked[self.pos] = not self.checked[self.pos]
        self.printcheck(self.pos)
    def acceptcheck(self):
        return [self.optkeys[i] for i, x in enumerate(self.checked) if x]
    @keyhandler.register(SPACE_CHAR)
    def toggle(self):
        self.toggle()
    @keyhandler.register(ARROW_UP_KEY)
    def moveUp(self):
        if self.pos - 1 < 0:
            return
        else:
            utils.clearLine()
            old_pos = self.pos
            self.pos -= 1
            self.print(old_pos)
            utils.moveCursorUp(1)
            self.print(self.pos)
    @keyhandler.register(ARROW_DOWN_KEY)
    def moveDown(self):
        if self.pos + 1 >= len(self.options):
            return
        else:
            utils.clearLine()
            old_pos = self.pos
            self.pos += 1
            self.print(old_pos)
            utils.moveCursorDown(1)
            self.print(self.pos)
    @keyhandler.register(NEWLINE_KEY)
    def accept(self):
        utils.moveCursorDown(len(self.options) - self.pos)
        return self.accept()
    @keyhandler.register(INTERRUPT_KEY)
    def interrupt(self):
        utils.moveCursorDown(len(self.options) - self.pos)
        raise KeyboardInterrupt
    def render(self):
        if self.message is None:
            raise ValueError('Message is not set')
        if self.options is None:
            raise ValueError('Options are not set')
        utils.forceWrite(' ' * self.indent + self.message + '\n')
        utils.forceWrite('\n' * self.shift)
        for i in range(len(self.options)):
            self.print(i)
            utils.forceWrite('\n')
        utils.moveCursorUp(len(self.options) - self.pos)
        with cursor.hide():
            while True:
                ret = self.handle_input()
                if ret is not None:
                    return ret
    def single_choice(self):
        self.print = self.printradio
        self.toggle = self.toggleradio
        self.accept = self.acceptradio
        self.max_width = len(max(self.options, key = len)) + self.pad_right
        return self.render()
    def multiple_choices(self):
        self.print = self.printcheck
        self.toggle = self.togglecheck
        self.accept = self.acceptcheck
        self.max_width = len(max(self.options, key = len)) + self.pad_right
        return self.render()
