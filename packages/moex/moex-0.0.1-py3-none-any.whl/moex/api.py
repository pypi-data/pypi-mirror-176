# -*- coding: utf-8 -*-
from time import sleep
from rich.live import Live

from moex.design import CliDesigner
from moex.handlers import Handlers, AVAILABLE as available_handlers
from moex.templates import TemplatesRepository


__all__ = ("AIOMoex", )


class AIOMoex:
    """API interface for MoscowExchange
    """

    def __repr__(self):
        """Return AIOMoex representation

        Returns
        -------
        str
            AIOMoex representation
        """
        try:
            return f"{self}(handler={self.__handler}, templates={self.templates})"
        except AttributeError:
            return f"{self}()"

    def __str__(self):
        """Str method

        Returns
        -------
        str
            String representation
        """
        return self.__class__.__name__

    @property
    def templates(self):
        """Return set of templates identifieres

        Returns
        -------
        set
            Templates identifieres
        """
        return self.__templates_repository.ids

    def render_url(self, template_id, **template_vars):
        """Render url with jinja

        Parameters
        ----------
        template_id : int
            Template's identifier

        Returns
        -------
        str
            Rendered url
        """
        return self.__templates_repository.render_template(template_id, **template_vars)

    def find_template(self, search_pattern):
        """Find templates by pattern

        Parameters
        ----------
        search_pattern : str
            Regex or usual string

        Returns
        -------
        generator
            Templates generator
        """
        return self.__templates_repository.find_template_id(search_pattern)

    def get_template(self, template_id):
        """Get template by template identifier

        Parameters
        ----------
        template_id : int
            Template's identifier

        Returns
        -------
        Template
            Template dataclass
        """
        return self.__templates_repository.get_template(template_id)

    def show_templates(self):
        """Print table with templates identifiers and addresses
        """
        doc_table = CliDesigner.get_table("ID", "URI TEMPLATE")

        with Live(doc_table, refresh_per_second=6):
            for template_id in self.templates:
                doc_table.add_row(
                    f"{CliDesigner.random_color()}{template_id}",
                    f"{CliDesigner.random_color()}{self.get_template(template_id=template_id).path}"
                    )
                sleep(.321)

    async def show_template_doc(self, session, template_id):
        """Print docs from official web site

        Parameters
        ----------
        session : aiohttp.ClientSession
            Client session
        template_id : int
            Template's identifier
        """
        await self.__templates_repository.show_template_doc(session, template_id)

    async def execute(self, session, url, **params):
        """Call requested uri

        Parameters
        ----------
        session : aiohttp.ClientSession
            Client session
        url : str
            Api url

        Returns
        -------
        Any
            Dataclass instance
        """
        return await self.__handler.execute(session=session, url=url, **params)

    async def load(self, session, output_format):
        """Load required data

        Parameters
        ----------
        session : aiohttp.ClientSession
            Client session
        output_format : str
            Handler's format
        """
        handlers = self.__load_handlers()
        self.__templates_repository = await self.__load_templates(session)
        self.__handler = handlers.create(output_format=output_format)

    @staticmethod
    async def __load_templates(session):
        """Load uri templates from official web site

        Parameters
        ----------
        session : aiohttp.ClientSession
            Client session

        Returns
        -------
        TemplatesRepository
            Repository of templates
        """
        templates_repository = TemplatesRepository()
        await templates_repository.load_data(session)
        return templates_repository

    @staticmethod
    def __load_handlers():
        """Load available handlers

        Returns
        -------
        Handlers
            Handlers factory
        """
        handlers = Handlers()
        for handler in available_handlers:
            handlers.register(handler.EXTENSION, handler)
        return handlers
