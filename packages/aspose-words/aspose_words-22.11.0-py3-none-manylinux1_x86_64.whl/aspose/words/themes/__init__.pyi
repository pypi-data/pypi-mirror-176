﻿import aspose.words
import aspose.pydrawing
import datetime
import decimal
import io
import uuid
from typing import Iterable

class Theme:
    '''Represents document Theme, and provides access to main theme parts including :attr:`Theme.major_fonts`, :attr:`Theme.minor_fonts` and :attr:`Theme.colors`To learn more, visit the `Working with Styles and Themes <https://docs.aspose.com/words/net/working-with-styles-and-themes/>` documentation article.'''
    
    def __init__(self):
        ...
    
    @property
    def major_fonts(self) -> aspose.words.themes.ThemeFonts:
        '''Allows to specify the set of major fonts for different languages.'''
        ...
    
    @property
    def minor_fonts(self) -> aspose.words.themes.ThemeFonts:
        '''Allows to specify the set of minor fonts for different languages.'''
        ...
    
    @property
    def colors(self) -> aspose.words.themes.ThemeColors:
        '''Allows to specify the set of theme colors for the document.'''
        ...
    
    ...

class ThemeColors:
    '''Represents the color scheme of the document theme which contains twelve colors.
    
    :class:`ThemeColors` object contains six accent colors, two dark colors, two light colors
    and a color for each of a hyperlink and followed hyperlink.'''
    
    ...

class ThemeFonts:
    '''Represents a collection of fonts in the font scheme, allowing to specify different fonts for different languages :attr:`ThemeFonts.latin`, :attr:`ThemeFonts.east_asian` and :attr:`ThemeFonts.complex_script`.
    To learn more, visit the `Working with Styles and Themes <https://docs.aspose.com/words/net/working-with-styles-and-themes/>` documentation article.'''
    
    @property
    def latin(self) -> str:
        '''Specifies font name for Latin characters.'''
        ...
    
    @latin.setter
    def latin(self, value: str):
        ...
    
    @property
    def east_asian(self) -> str:
        '''Specifies font name for EastAsian characters.'''
        ...
    
    @east_asian.setter
    def east_asian(self, value: str):
        ...
    
    @property
    def complex_script(self) -> str:
        '''Specifies font name for ComplexScript characters.'''
        ...
    
    @complex_script.setter
    def complex_script(self, value: str):
        ...
    
    ...

class ThemeColor:
    '''Specifies the theme colors for document themes.
    To learn more, visit the `Working with Styles and Themes <https://docs.aspose.com/words/net/working-with-styles-and-themes/>` documentation article.
    
    The specified theme color is a reference to one of the predefined theme colors, located in the
    document's Theme part, which allows color information to be set centrally in the document.'''
    
    NONE: int
    DARK1: int
    LIGHT1: int
    DARK2: int
    LIGHT2: int
    ACCENT1: int
    ACCENT2: int
    ACCENT3: int
    ACCENT4: int
    ACCENT5: int
    ACCENT6: int
    HYPERLINK: int
    FOLLOWED_HYPERLINK: int
    TEXT1: int
    TEXT2: int
    BACKGROUND1: int
    BACKGROUND2: int

class ThemeFont:
    '''Specifies the types of theme font names for document themes.
    
    Specifies a theme font type which can be referenced as a theme font within the parent object properties.
    This theme font is a reference to one of the predefined theme fonts, located in the document's
    Theme part, which allows for font information to be set centrally in the document.'''
    
    NONE: int
    MAJOR: int
    MINOR: int

