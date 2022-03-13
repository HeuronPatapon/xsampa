"""
Convert between XSAMPA and IPA data formats. 

Reference
---------
https://en.wikipedia.org/wiki/X-SAMPA
"""
import re
import unittest
import doctest


import hpat.ezre as ezre


__all__ = ("XSAMPA", )


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(__name__))
    return tests


class XSAMPA:
    XSAMPA_TO_IPA: dict[str, str] = {
        # Lower case symbols
        "a": "a",
        "b": "b",
        "b_<": "ɓ",
        "c": "c",
        "d": "d",
        "d`": "ɖ",
        "d_<": "ɗ",
        "e": "e",
        "f": "f",
        "g": "g",
        "g_<": "ɠ",
        "h": "h",
        "h\\": "ɦ",
        "h*": "ɦ",
        "i": "i",
        "j": "j",
        "j\\": "ʝ",
        "j*": "ʝ",
        "k": "k",
        "l": "l",
        "l`": "ɭ",
        "l\\": "ɺ",
        "l*": "ɺ",
        "m": "m",
        "n": "n",
        "n`": "ɳ",
        "o": "o",
        "p": "p",
        "p\\": "ɸ",
        "p*": "ɸ",
        "q": "q",
        "r": "r",
        "r`": "ɽ",
        "r\\": "ɹ",
        "r*": "ɹ",
        "r\\`": "ɻ",
        "r*`": "ɻ",
        "s": "s",
        "s`": "ʂ",
        "s\\": "ɕ",
        "s*": "ɕ",
        "t": "t",
        "t`": "ʈ",
        "u": "u",
        "v": "v",
        "v\\": "ʋ",
        "v*": "ʋ",
        "w": "w",
        "x": "x",
        "x\\": "ɧ",
        "x*": "ɧ",
        "y": "y",
        "z": "z",
        "z`": "ʐ",
        "z\\": "ʑ",
        "z*": "ʑ",

        # Capital symbols
        "A": "ɑ",
        "B": "β",
        "B\\": "ʙ",
        "B*": "ʙ",
        "C": "ç",
        "D": "ð",
        "E": "ɛ",
        "F": "ɱ",
        "G": "ɣ",
        "G\\": "ɢ",
        "G*": "ɢ",
        "G\\_<": "ʛ",
        "G*_<": "ʛ",
        "H": "ɥ",
        "H\\": "ʜ",
        "H*": "ʜ",
        "I": "ɪ",
        "I\\": "ᵻ",
        "I*": "ᵻ",
        "J": "ɲ",
        "J\\": "ɟ",
        "J*": "ɟ",
        "J\\_<": "ʄ",
        "J*_<": "ʄ",
        "K": "ɬ",
        "K\\": "ɮ",
        "K*": "ɮ",
        "L": "ʎ",
        "L\\": "ʟ",
        "L*": "ʟ",
        "M": "ɯ",
        "M\\": "ɰ",
        "M*": "ɰ",
        "N": "ŋ",
        "N\\": "ɴ",
        "N*": "ɴ",
        "O": "ɔ",
        "O\\": "ʘ",
        "O*": "ʘ",
        "P": "ʋ",
        "Q": "ɒ",
        "R": "ʁ",
        "R\\": "ʀ",
        "R*": "ʀ",
        "S": "ʃ",
        "T": "θ",
        "U": "ʊ",
        "U\\": "ᵿ",
        "U*": "ᵿ",
        "V": "ʌ",
        "W": "ʍ",
        "X": "χ",
        "X\\": "ħ",
        "X*": "ħ",
        "Y": "ʏ",
        "Z": "ʒ",

        # Other symbols
        # ".": ".",  # CAUTION: keep as-is
        '"':    "ˈ",
        "%": "ˌ",
        "'": "ʲ",
        ":": "ː",
        ":\\": "ˑ",
        ":*": "ˑ",
        # "-":    "",  # CAUTION: used as a separator; keep as-is
        "@": "ə",
        "@\\": "ɘ",
        "@*": "ɘ",
        "@`": "ɚ",
        "{": "æ",
        "}": "ʉ",
        "1": "ɨ",
        "2": "ø",
        "3": "ɜ",
        "3\\": "ɞ",
        "3*": "ɞ",
        "4": "ɾ",
        "5": "ɫ",
        "6": "ɐ",
        "7": "ɤ",
        "8": "ɵ",
        "9": "œ",
        "&": "ɶ",
        "?": "ʔ",
        "?\\": "ʕ",
        "?*": "ʕ",
        # "/":    "...",  # TODO: French symbol indeterminate
        # "<":    "...",
        "<\\": "ʢ",
        "<*": "ʢ",
        # ">":    "...",
        ">\\": "ʡ",
        ">*": "ʡ",
        "^": "ꜛ",
        "!": "ꜜ",
        "!\\": "ǃ",
        "!*": "ǃ",
        # "|": "|",  # CAUTION: keep as-is
        "|\\": "ǀ",
        "|*": "ǀ",
        "||": "‖",
        "|\\|\\": "ǁ",
        "|*|*": "ǁ",
        "=\\": "ǂ",
        "=*": "ǂ",
        "-\\": "‿",
        "-*": "‿",

        # Diacritics
        '_"':   "̈",
        "_+": "̟",
        "_-": "̠",
        "_/": "̌",
        "_0": "̥",
        # "_<":   "implosive",  # TODO: map to actual symbols in IPA
        "=": "̩",
        "_=": "̩",
        "_>": "ʼ",
        "_?\\": "ˤ",
        "_?*": "ˤ",
        "_\\": "̂",
        "_*": "̂",
        "_^": "̯",
        "_}": "̚",
        "`": "˞",
        "~": "̃",
        "_~": "̃",  # CAUTION: keep the shortest convention, "~"
        "_A": "̘",
        "_a": "̺",
        "_B": "̏",
        "_B_L": "᷅",
        "_c": "̜",
        "_d": "̪",
        "_e": "̴",
        "<F>": "↘",
        "_F": "̂",
        "_G": "ˠ",
        "_H": "́",
        "_H_T": "᷄",
        "_h": "ʰ",
        "_j": "ʲ",
        "_k": "̰",
        "_L": "̀",
        "_l": "ˡ",
        "_M": "̄",
        "_m": "̻",
        "_N": "̼",
        "_n": "ⁿ",
        "_O": "̹",
        "_o": "̞",
        "_q": "̙",
        "<R>": "↗",
        "_R": "̌",
        "_R_F": "᷈",
        "_r": "̝",
        "_T": "̋",
        "_t": "̤",
        "_v": "̬",
        "_w": "ʷ",
        "_X": "̆",
        "_x": "̽",
    }

    xsampa_symbol = ezre.Ezre.from_sequence(XSAMPA_TO_IPA).group("symbol")
    xsampa_pattern = xsampa_symbol.compiled

    IPA_TO_XSAMPA = {value: key for key, value in XSAMPA_TO_IPA.items()}
    ipa_symbol = ezre.Ezre.from_sequence(IPA_TO_XSAMPA).group("symbol")
    ipa_pattern = ipa_symbol.compiled

    @classmethod
    def to_ipa(cls, string: str) -> str:
        """
        Convert a XSAMPA string to its IPA equivalent. 

        Examples
        --------
        >>> XSAMPA.to_ipa("a b E s a~ t")
        'a b ɛ s ã t'
        >>> XSAMPA.to_ipa("R e y n i s a Z @")
        'ʁ e y n i s a ʒ ə'
        >>> XSAMPA.to_ipa('["fweM\\\\o]')
        '[ˈfweɰo]'
        >>> XSAMPA.to_ipa('["fweM*o]')
        '[ˈfweɰo]'
        >>> XSAMPA.to_ipa('[Go"nia]')
        '[ɣoˈnia]'
        >>> XSAMPA.to_ipa('["r\\\\oUz1z]')
        '[ˈɹoʊzɨz]'
        >>> XSAMPA.to_ipa('[i:!\\\\a:!\\\\a]')
        '[iːǃaːǃa]'
        >>> XSAMPA.to_ipa('[x\\\\}:]')
        '[ɧʉː]'
        >>> XSAMPA.to_ipa('[x\\\\&d`]')
        '[ɧɶɖ]'
        >>> XSAMPA.to_ipa('[t-S1]')
        '[t-ʃɨ]'
        >>> XSAMPA.to_ipa('[le-\\\\zami]')
        '[le‿zami]'
        >>> XSAMPA.to_ipa('[?\\\\Ajn]')
        '[ʕɑjn]'
        """
        return re.sub(
            cls.xsampa_pattern,
            lambda m: cls.XSAMPA_TO_IPA[m.group("symbol")],
            string)

    @classmethod
    def from_ipa(cls, string: str) -> str:
        """
        Convert an IPA string to its XSAMPA equivalent. 

        Examples
        --------
        >>> XSAMPA.from_ipa('a b ɛ s ã t')  # do not use 'a~' shortcut
        'a b E s a_~ t'
        >>> XSAMPA.from_ipa('ʁ e y n i s a ʒ ə')
        'R e y n i s a Z @'
        >>> XSAMPA.from_ipa('[ˈfweɰo]')  # use '*' not '\\' variant
        '["fweM*o]'
        >>> XSAMPA.from_ipa('[ɣoˈnia]')
        '[Go"nia]'
        >>> XSAMPA.from_ipa('[ˈɹoʊzɨz]')
        '["r*oUz1z]'
        >>> XSAMPA.from_ipa('[iːǃaːǃa]')
        '[i:!*a:!*a]'
        >>> XSAMPA.from_ipa('[ɧʉː]')
        '[x*}:]'
        >>> XSAMPA.from_ipa('[ɧɶɖ]')
        '[x*&d`]'
        >>> XSAMPA.from_ipa('[tʃɨ]')  # ambiguity of 'tS' in X-SAMPA
        '[tS1]'
        >>> XSAMPA.from_ipa('[le‿zami]')
        '[le-*zami]'
        >>> XSAMPA.from_ipa('[ʕɑjn]')
        '[?*Ajn]'
        """
        return re.sub(
            cls.ipa_pattern,
            lambda m: cls.IPA_TO_XSAMPA[m.group("symbol")],
            string)


if __name__ == '__main__':
    doctest.testmod()
