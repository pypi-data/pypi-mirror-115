#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classes of PaperLogger.
"""

import numpy as np
from .utils import parse_authors
from .utils import write_paper_log
from .utils import read_paper_log
from .utils import remove_paper_log


class PaperLogger(object):
    """
    Base PaperLogger class
    """

    def __init__(
        self,
        id=None,
        title=None,
        authors=None,
        venue=None,
        year=None,
        papertype="research",
        bib=None,
        abstract=None,
        save=False,
        load=False,
        **kwargs
    ):
        """[summary]

        Args:
            id ([type], optional): [description]. Defaults to None.
            title ([type], optional): [description]. Defaults to None.
            authors ([type], optional): [description]. Defaults to None.
            venue ([type], optional): [description]. Defaults to None.
            year ([type], optional): [description]. Defaults to None.
            papertype (str, optional): [description]. Defaults to "research".
            bib ([type], optional): [description]. Defaults to None.
            abstract ([type], optional): [description]. Defaults to None.
            save (bool, optional): [description]. Defaults to False.
            load (bool, optional): [description]. Defaults to False.
        """
        self.loaded = load
        
        #TODO needs to figure out the relationship between save and load
        if load:
            self.load(id)
        else:
            self.id = id
            self.title = str(title) if title else title
            self.authors = str(authors) if authors else authors
            self.authors_list = parse_authors(authors)
            self.venue = str(venue) if venue else venue
            self.year = int(year) if year else year
            self.papertype = str(papertype) if papertype else papertype
            self.bib = str(bib) if bib else bib
            self.abstract = str(abstract) if abstract else abstract
            self.other_variables = kwargs

        if save:
            self.save()

    def fields_to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "authors": self.authors,
            "authors_list": self.authors_list,
            "venue": self.venue,
            "year": self.year,
            "papertype": self.papertype,
            "bib": self.bib,
            "abstract": self.abstract,
        }

        
    def save(self):
        """[summary]"""
        fields_dict = self.fields_to_dict()
        other_variables = self.other_variables
        write_paper_log({**fields_dict, **other_variables})

    def load(self, id: str):
        """[summary]

        Args:
            id (str): [description]
        """
        fields = read_paper_log(id)
        self.__init__(**fields)

    def empty(self, id: str):
        """[summary]

        Args:
            id (str): [description]
        """
        remove_paper_log(id)

    def update_id(self, id:str):
        """[summary]"""
        #TODO needs fixing
        
        fields_dict = self.fields_to_dict()
        fields_dict['id']
        other_variables = self.other_variables
        write_paper_log({**fields_dict, **other_variables})