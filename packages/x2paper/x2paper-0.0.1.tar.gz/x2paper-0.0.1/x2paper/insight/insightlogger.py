#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classes of InsightLogger.
"""

import numpy as np
from .utils import get_next_id
from .utils import ingraph
from .utils import parse_to_list
from .utils import parse_keywords
from .utils import parse_citations
from .utils import write_insight_log
from .utils import read_insight_log
from .utils import remove_insight_log


class InsightLogger(object):
    """
    Base InsightLogger class
    """

    def __init__(
        self,
        id=None,
        note=None,
        keywords=None,
        citations=None,
        relationships=None,
        save=False,
        load=False,
        **kwargs
    ):
        """[summary]

        Args:
            id ([type], optional): [description]. Defaults to None.
            note ([type], optional): [description]. Defaults to None.
            keywords ([type], optional): [description]. Defaults to None.
            citations ([type], optional): [description]. Defaults to None.
            relationships ([type], optional): [description]. Defaults to None.
            save (bool, optional): [description]. Defaults to False.
            load (bool, optional): [description]. Defaults to False.
        """

        if load:
            self.load(id)
        else:
            self.id = get_next_id()
            self.note = str(note) if note else note
            self.keywords = parse_keywords(keywords) if keywords else keywords
            self.citations = (
                parse_citations(citations, self.note) if citations else citations
            )
            self.relationships = relationships or []

        if save:
            self.save()

    def fields_to_dict(self):
        return {
            "id": self.id,
            "note": self.note,
            "keywords": self.keywords,
            "citations": self.citations,
            "relationships": self.relationships,
        }

    def save(self):
        """[summary]"""
        write_insight_log(self.fields_to_dict())

    def load(self, id: str):
        """[summary]

        Args:
            id (str): [description]
        """
        fields = read_insight_log(id)
        self.__init__(**fields)

    def empty(self, id: str):
        """[summary]

        Args:
            id (str): [description]
        """
        remove_insight_log(id)

    def add_citations(self, input):
        """[summary]

        Args:
            input ([type]): [description]
        """
        citations_to_add = parse_to_list(input)
        for citation in citations_to_add:
            if citation not in self.citations:
                self.citations.append(citation)

    def add_keywords(self, input):
        """[summary]

        Args:
            input ([type]): [description]
        """
        keywords_to_add = parse_citations(input)
        for keyword in keywords_to_add:
            if keyword not in self.keywords:
                self.keywords.append(keyword)

    def add_relationship(
        self, action: str, action_subjects, action_objects, directional=False
    ):
        """[summary]

        Args:
            action (str): [description]
            action_subjects ([type]): [description]
            action_objects ([type]): [description]
            directional (bool, optional): [description]. Defaults to False.
        """
        action_subjects_list = parse_to_list(action_subjects)
        action_objects_list = parse_to_list(action_objects)

        for action_subject in action_subjects_list:
            for action_object in action_objects_list:
                if ingraph(
                    graph=self.relationships,
                    action=action,
                    action_subject=action_subject,
                    action_object=action_object,
                ):
                    self.relationships.append([action, action_subject, action_object])
                if not directional and ingraph(
                    graph=self.relationships,
                    action=action,
                    action_subject=action_object,
                    action_object=action_subject,
                ):
                    self.relationships.append([action, action_object, action_subject])
