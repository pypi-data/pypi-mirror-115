#!/usr/bin/env python3
# -*- coding: utf-8 -*-
################################################################################
#    MusaMusa-MusTextFile Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of MusaMusa-MusTextFile.
#    MusaMusa-MusTextFile is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    MusaMusa-MusTextFile is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with MusaMusa-MusTextFile.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
   MusaMusa-MusTextFile project : mustextfile.py

   Main file of the project (MusTextFile class)

   ____________________________________________________________________________

   o  MusTextFile class
"""

# TODOs
#   que faire avec une ligne ?
#     - yield ETRLine
#     - yield AText
#     - yield AText regroupé (nouvel objet à ajouter ?)
import json
import os.path
import logging
import re

from musamusa_errors.error_messages import ListOfErrorMessages
from musamusa_textref.textrefdefault import TextRefDefault
from musamusa_atext.annotatedstring import AnnotatedString
from musamusa_etr.etr import ETR

LOGGER = logging.getLogger("activity")


class MusTextFile:
    def __init__(self):
        self.context_options = {}
        self.errors = ListOfErrorMessages()
        self.etr = None

    def read(self,
             filename: str):

        if not os.path.exists(filename):
            # TODO
            #self.errors.append("!")
            return
        
        self.etr = ETR()
        self.etr.options["read line:variable:event"] = self.read_event_variable

        if not self.read__choose_context(os.path.join("musamusa_mustextfile", "contexts", "default.json")):
            # TODO
            #self.errors.append()
            print("ERROR")
            return 

        for etr_line in self.etr.read(filename):
            #LOGGER.debug(f"A new line has been read, namely '{line}'.")
            textsegment_text = re.search(self.context_options["read textsegment/text(regex)"],
                                         etr_line.line)
            if textsegment_text:
                yield from self.read__new_textsegment_text(etr_line,
                                                           textsegment_text)

            # textsegment_translation = re.search(self.context_options["read textsegment/translation(regex)"],
            #                                     etr_line.line)
            # if textsegment_translation:
            #     LOGGER.info("new text segment translation"+etr_line.line)
            #      # yield ... TODO
            #     #LOGGER.info("???"+etr_line.line)

            # textsegment_detail = re.search(self.context_options["read textsegment/detail(regex)"],
            #                                etr_line.line)
            # if textsegment_detail:
            #     pass
            #     #LOGGER.info("new text segment detail"+etr_line.line)
            #      # yield ... TODO
            #     #LOGGER.info("???"+etr_line.line)

        # TODO
        # à quoi sert cette ligne ?
        yield None

    def read__choose_context(self,
                             context_name):
        """
        RETURNED VALUE: (bool)success
        """
        # context_name: contexts/default.json
        if not os.path.exists(context_name):
            # TODO
            print("ERROR", context_name)
            return False

        LOGGER.info(f"switching to reading context '{context_name}'")

        self.context_options = json.loads(open(context_name).read())

        # let's re.compile() every key ending with '(regex)':
        for key, value in self.context_options.items():
            if key.endswith("(regex)"):
                self.context_options[key] = re.compile(value)

        LOGGER.info(f".context_options content:")
        for key, value in self.context_options.items():
            LOGGER.info(f"o  '{key}' : '{value}'")

        return True

    def read_event_variable(self,
                            tlff,
                            details):
        LOGGER.info("Variable ! "+details['variable_name']+" : "+details['variable_value'])

    def read__new_textsegment_text(self,
                                   etr_line,
                                   textsegment_text):
        LOGGER.debug("new text segment text"+etr_line.line)

        reference = TextRefDefault().init_from_str(textsegment_text.group("reference"))
        if reference.errors:
            # TODO
            pass

        atext = AnnotatedString(textsegment_text.group("content"))
        print(reference, atext)
        print(atext.improved_str())

        yield etr_line.line
