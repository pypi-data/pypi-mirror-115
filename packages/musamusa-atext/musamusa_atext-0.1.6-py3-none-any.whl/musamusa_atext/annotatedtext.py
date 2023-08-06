#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#    MusaMusa-AnnotatedText Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of MusaMusa-AnnotatedText.
#    MusaMusa-AnnotatedText is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MusaMusa-AnnotatedText is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with MusaMusa-AnnotatedText.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
   MusaMusa-AnnotatedText project : musamusa_atext/annotatedtext.py

   AnnotatedText object allows to store pairs of (textref, AnnotatedString) and
   to yield over with sorted textrefs.

   See the main documentation for more explanations.

   ____________________________________________________________________________

   CONSTANT:
   o  DEFAULT_OPTIONS

   CLASS:
   o  AnnotatedText class
"""
import copy
import importlib

from iaswn.iaswn import Iaswn

from musamusa_errors.error_messages import ListOfErrorMessages, MusaMusaError
from musamusa_textref.semisortedtextrefsdict import SemiSortedTextRefsDict

from musamusa_atext.annotatedstring import AnnotatedString
from musamusa_atext.annotatedstring import DEFAULT_OPTIONS as ASTRING__DEFAULT_OPTIONS
from musamusa_atext.annotatedstring import PARSINGTOOLS as ASTRING__PARSINGTOOLS

# (pimydoc)AnnotatedText.options
# ⋅A dict (str:...) modifying the way AnnotatedText.__init__() and AnnotatedText.add()
# ⋅work.
# ⋅
# ⋅o  "AnnotatedText:TextRef class": (str)class name used by AnnotatedStrings objects
# ⋅                    special format: "module.submodule.subsubmodule:classname"
# ⋅                    e.g. "musamusa_textref.textrefdefault:TextRefDefault"
# ⋅                    see "AnnotatedText:TextRef class(type)"
# ⋅
# ⋅o  "AnnotatedText:TextRef class(type)": (None|type)
# ⋅                          type of the class used by AnnotatedStrings objects
# ⋅                          Automatically derived by AnnotatedText.__init__()
# ⋅                          from "AnnotatedText:TextRef class"
# ⋅
# ⋅o  "AnnotatedString:options": copy.deepcopy(ASTRING__DEFAULT_OPTIONS)
# ⋅                              see format in annotatedstring.py
# ⋅
# ⋅o  "AnnotatedString:parsingtools": copy.deepcopy(ASTRING__PARSINGTOOLS)
# ⋅                                   see format in annotatedstring.py
# ⋅
# ⋅o  "AnnotatedText:textrefs limits": (None or a TextRef* object)
# ⋅                      Every textrefs stored in the AnnotatedText has to
# ⋅                      be inside .options["AnnotatedText:textrefs limits"]
# ⋅                      If None, there are no textrefs limits.
DEFAULT_OPTIONS = {
    "AnnotatedString:options": copy.deepcopy(ASTRING__DEFAULT_OPTIONS),
    "AnnotatedString:parsingtools": copy.deepcopy(ASTRING__PARSINGTOOLS),
    "AnnotatedText:TextRef class": "musamusa_textref.textrefdefault:TextRefDefault",
    "AnnotatedText:TextRef class(type)": None,
    "AnnotatedText:textrefs limits": None,
    }


class AnnotatedText(Iaswn):
    """
        AnnotatedText class

        (pimydoc)about AnnotatedText objects
        ⋅Use this class to store pairs of (TextRef, AnnotatedString).
        ⋅
        ⋅An AnnotatedText is linked to one TextRef* type, stored in
        ⋅.options["AnnotatedText:TextRef class(type)" .
        ⋅
        ⋅You can discard references outside certain limits: use
        ⋅.options["AnnotatedText:textrefs limits"] to accept only the
        ⋅textual references that are inside .options["AnnotatedText:textrefs limits"] .
        _______________________________________________________________________

        METHODS:
        o  __init__(self, options=None)
        o  _get_textref_object(self, source_string: str = None)
        o  add_str(self, textref_str, text_str)
        o  improved_str(self, rightpadding=True)
        o  set_limits(self, limits=None, limits_str=None)
        o  yield_sorted_textrefs(self, definition2str=False)
    """
    def __init__(self,
                 options=None):
        """
            AnnotatedText.__init__()
            ___________________________________________________________________

            ARGUMENT:
            o  options (None or dict, see DEFAULT_OPTIONS)

                options is an update of DEFAULT_OPTIONS, i.e. <options> may contain only one
                value which will modify the copy of DEFAULT_OPTIONS.

               (pimydoc)AnnotatedText.options
               ⋅A dict (str:...) modifying the way AnnotatedText.__init__() and AnnotatedText.add()
               ⋅work.
               ⋅
               ⋅o  "AnnotatedText:TextRef class": (str)class name used by AnnotatedStrings objects
               ⋅                    special format: "module.submodule.subsubmodule:classname"
               ⋅                    e.g. "musamusa_textref.textrefdefault:TextRefDefault"
               ⋅                    see "AnnotatedText:TextRef class(type)"
               ⋅
               ⋅o  "AnnotatedText:TextRef class(type)": (None|type)
               ⋅                          type of the class used by AnnotatedStrings objects
               ⋅                          Automatically derived by AnnotatedText.__init__()
               ⋅                          from "AnnotatedText:TextRef class"
               ⋅
               ⋅o  "AnnotatedString:options": copy.deepcopy(ASTRING__DEFAULT_OPTIONS)
               ⋅                              see format in annotatedstring.py
               ⋅
               ⋅o  "AnnotatedString:parsingtools": copy.deepcopy(ASTRING__PARSINGTOOLS)
               ⋅                                   see format in annotatedstring.py
               ⋅
               ⋅o  "AnnotatedText:textrefs limits": (None or a TextRef* object)
               ⋅                      Every textrefs stored in the AnnotatedText has to
               ⋅                      be inside .options["AnnotatedText:textrefs limits"]
               ⋅                      If None, there are no textrefs limits.
        """
        self.errors = ListOfErrorMessages()

        self.options = copy.deepcopy(DEFAULT_OPTIONS)
        if options:
            self.options.update(options)

        module, classname = self.options["AnnotatedText:TextRef class"].split(":")
        try:
            self.options["AnnotatedText:TextRef class(type)"] = getattr(
                importlib.import_module(module),
                classname)
        except AttributeError as err:
            # (pimydoc)error::ANNOTATEDTEXT-ERRORID012
            # ⋅Can't create an AnnotatedText object due to the unknown type stored in
            # ⋅options['AnnotatedText:TextRef class(type)']. This value is itself computed from
            # ⋅self.options["AnnotatedText:TextRef class"] .
            error = MusaMusaError()
            error.msgid = "ANNOTATEDTEXT-ERRORID012"
            error.msg = "Can't create AnnotatedText from given options " \
                f"since options['AnnotatedText:TextRef class(type)'] is " \
                f"'{self.options['AnnotatedText:TextRef class(type)']}' " \
                f"an unknown type. Python error is '{err}'. " \
                "self.options['AnnotatedText:TextRef class'] is equal to " \
                f"{self.options['AnnotatedText:TextRef class']}."
            self.errors.append(error)
            return

        self.annotatedstrings = SemiSortedTextRefsDict(
            textrefclass=self.options["AnnotatedText:TextRef class(type)"])

    def __eq__(self,
               other):
        """
            AnnotatedText.__eq__()

            This method is primarily used for testing.
            ___________________________________________________________________

            ARGUMENT: <other>, an AnnotatedText object

            RETURNED VALUE: True if <self> and <other> are equal, False otherwise.
        """
        return self.errors == other.errors and \
            self.options == other.options and \
            self.annotatedstrings == other.annotatedstrings

    def _get_textref_object(self,
                            source_string: str = None):
        """
            AnnotatedText._get_textref_object()

            Internal method: create and return the TextReff* object whose type
            is stored in .options["AnnotatedText:TextRef class(type)"]

            ___________________________________________________________________

            ARGUMENT:
            o  source_string: (None|str) if not None argument passed to .init_from_str()

            RETURNED VALUE: the new TexRef* object that has been created
        """
        if source_string:
            res = self.options["AnnotatedText:TextRef class(type)"]()
            res.init_from_str(source_string)
            return res

        return self.options["AnnotatedText:TextRef class(type)"]()

    def add_str(self,
                textref_str,
                text_str):
        """
            AnnotatedText.add_str()

            Add a pair of (TextRef, AnnotatedString) to <self>, both being
            described by (str)source strings.
            ___________________________________________________________________

            ARGUMENTS:
            o  textref_str: (str) textual reference
            o  text_str:    (str) text given to the AnnotatedString class

            RETURNED VALUE: (bool)True if the textref has been added to <self>.
        """
        textref = self._get_textref_object()
        textref.init_from_str(textref_str)

        if textref.errors:
            # (pimydoc)error::ANNOTATEDTEXT-ERRORID010
            # ⋅The call to AnnotatedText.add_str() raised an error due to an incorrect
            # ⋅textual reference.
            error = MusaMusaError()
            error.msgid = "ANNOTATEDTEXT-ERRORID010"
            error.msg = f"Can't add ('{textref_str}', '{text_str}' to this AnnotatedText object " \
                f"since the TextRef object created from '{textref_str}' contains error(s)."
            error.suberrors = textref.errors
            self.errors.append(error)
            return False

        # If .options["AnnotatedText:textrefs limits"] is defined, we check that <textref> is
        # inside .options["AnnotatedText:textrefs limits"]:
        if self.options["AnnotatedText:textrefs limits"] is not None and \
           not textref.is_inside(self.options["AnnotatedText:textrefs limits"]):
            return False

        astring = AnnotatedString(
            parsingtools=self.options["AnnotatedString:parsingtools"],
            options=self.options["AnnotatedString:options"]).init_from_str(text_str)

        if astring.errors:
            # (pimydoc)error::ANNOTATEDTEXT-ERRORID013
            # ⋅Can't create an AnnotatedText object due to an error in the new AnnotatedString
            # ⋅object.
            error = MusaMusaError()
            error.msgid = "ANNOTATEDTEXT-ERRORID013"
            error.msg = f"Can't add ('{textref_str}', '{text_str}' to this AnnotatedText object " \
                f"since the new AnnotatedText has an error due to the AnnotatedString object."
            error.suberrors = astring.errors
            self.errors.append(error)
            return False

        return self.annotatedstrings.add(textref, astring)

    def improved_str(self,
                     rightpadding=True):
        """
            AnnotatedText.improved_str()

            Return an improved representation of <self>.
            ___________________________________________________________________

            ARGUMENTS:
            o  rightpadding:  (bool) argument passed to each AnnotatedString.improved_str()
                              (see infra astring.textref2data[textref].improved_str())

            RETURNED VALUE: (str)the improved representation of <self>.
        """
        res = []

        if self.errors:
            res.append("ERROR/WARNINGS:")
            for error in self.errors:
                res.append("* "+str(error.improved_str()))

        astrings = self.annotatedstrings

        if astrings.is_empty():
            res.append("Empty AnnotatedText")
        else:
            res.append(
                f"textrefs={astrings.sorted_textrefs.definition2str()} "
                "(reduced="
                f"{astrings.sorted_textrefs.definition2str(reduced=True, keep_iter_infos=False)})")

            for textref in self.annotatedstrings.sorted_textrefs:
                res.append(f"*  {textref.definition2str()}:"
                           f"\n{astrings.textref2data[textref].improved_str(rightpadding)}")
                res.append("")

        return "\n".join(res)

    def set_limits(self,
                   limits=None,
                   limits_str=None):
        """
            AnnotatedText.set_limits()

            Initialize self.options["AnnotatedText:textrefs limits"].

            You may either use <limits> (=you have a TextRef* object) either
            <limits_str> (=a TextRef* object will be created through a call to
            .init_from_str() ).

            If both arguments are given, only <limits> is used.
            ___________________________________________________________________

            ARGUMENTS:
            o  limits: TextRef* object to be directly stored in
                self.options["AnnotatedText:textrefs limits"] .
                It is assumed and checked that the TextRef* object in <limits> is a
                .options["AnnotatedText:TextRef class(type)"] object .

            o  limits_str: a source_string describing a TextRef* object

            RETURNED VALUE: (bool)True if the limits have successfully been set.
        """
        if limits:
            if limits.__class__.__name__ != \
               self.options["AnnotatedText:TextRef class(type)"].__class__.__name__:
                # (pimydoc)error::ANNOTATEDTEXT-ERRORID011
                # ⋅If you set the limit to an AnnotatedText object and if you use the <limits>
                # ⋅argument to set it, <limits> must be a TextRef* object whose type is identical
                # ⋅to atext.options["AnnotatedText:TextRef class(type)"].
                # ⋅In other words you can't set limits using a TextRefOEVerses object to an
                # ⋅AnnotatedText object whose .options["AnnotatedText:TextRef class(type)"] is
                # ⋅TextRefDefault .
                error = MusaMusaError()
                error.msgid = "ANNOTATEDTEXT-ERRORID011"
                error.msg = "Can't set limits to an AnnotatedText object: " \
                    f"the object <limits> ({limits}) " \
                    f"isn't of the same type (={limits.__class__.__name__}) as " \
                    f"the type linked to the AnnotatedText object " \
                    "defined in self.options['AnnotatedText:TextRef class(type)'] " \
                    f"(={self.options['AnnotatedText:TextRef class(type)']}"
                self.errors.append(error)
                return False

            self.options["AnnotatedText:textrefs limits"] = limits
            return True

        if limits_str:
            _limits = self._get_textref_object(source_string=limits_str)
            _limits.init_from_str(limits_str)
            if _limits.errors.zero_error_or_warning():
                self.options["AnnotatedText:textrefs limits"] = _limits
                return True
            return False

        # can't set self.options["AnnotatedText:textrefs limits"]:
        return False

    def yield_sorted_textrefs(self,
                              definition2str=False):
        """
            AnnotatedText.yield_sorted_textrefs()

            (Generator)Generate the textrefs stored in self.annotatedstrings.sorted_textrefs .

            By example, if you have:
                atext = AnnotatedText()
                atext.add_str("MyBook.2.c", "...")
                atext.add_str("MyBook.2.a", "...")
                atext.add_str("MyBook.1.b", "...")
                atext.add_str("MyBook.1.a", "...")

            This method will yield:
                * definition2str == False
                        ((((None, 'MyBook'), ('int', 1), ('a-z(1)', 1)), None),)
                        ((((None, 'MyBook'), ('int', 1), ('a-z(1)', 2)), None),)
                        ((((None, 'MyBook'), ('int', 2), ('a-z(1)', 1)), None),)
                        ((((None, 'MyBook'), ('int', 2), ('a-z(1)', 3)), None),)

                * definition2str == True
                        'MyBook.1.a'
                        'MyBook.1.b'
                        'MyBook.2.a'
                        'MyBook.2.c'

            ___________________________________________________________________

            ARGUMENT: (bool)definition2str, True if the yielded textref are passed
                      to .definition2str().

            YIELDED VALUE: the textrefs stored in self.annotatedstrings.sorted_textrefs .
        """
        for textref in self.annotatedstrings.sorted_textrefs:
            if definition2str is True:
                yield textref.definition2str()
            else:
                yield textref
