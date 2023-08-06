"""
The client
"""

# We import core class and modules here
import asyncio
from enum import Enum
from functools import cache, cached_property
from pathlib import Path
from typing import Any, Callable, Coroutine, Tuple, Union

# later the faust related objects
from faust import App, Worker, Record, uuid


# and at last all defined types
from .types import Deal, Duel, Offer, SexDigest, YellowPage, AuctionDigest

# ## The Client

# The client is just an object composition using faust


class Client:

    # We use this to know what models and kafka topics are allowed and how are related.
    allowed_records = {
        Deal: "deals",
        Duel: "duels",
        Offer: "offers",
        SexDigest: "sex_digest",
        YellowPage: "yellow_pages",
        AuctionDigest: "au_digest",
    }

    # and this to define versions of chat wars
    class Version(Enum):
        CW2 = "cw2"
        CW3 = "cw3"

    # The Client.**__init__** method can recieve

    # - id: just the client id
    # - version: client version
    # - broker: kafka address or broker
    # - loop: execution loop
    # - debug: for debuging with aiomonitor
    # - loglevel: the level of expecting logging info

    # This initialice a kafka consumer (carefull with this **is just a consumer**)
    # with a provided or self generated **id** that consume from a provided or
    # default (cw2) chat wars **version** topics. This consumer listen from a provided **broker**
    # and is executed in a provided or self generated **loop**.

    def __init__(
        self,
        id: str = None,
        version: "Client.Version" = None,
        broker: str = "kafka://digest-api.chtwrs.com:9092",
        work_dir: Union[str, Path] = "./.fchatwars",
        loop: asyncio.AbstractEventLoop = None,
        debug: bool = False,
        loglevel: Union[str, int] = "warning"
    ) -> None:

        self._loop = loop if loop is not None else asyncio.get_event_loop()
        self._version = version if version is not None else self.Version.CW2
        self._debug = debug
        self._logleve = loglevel

        self._app = App(
            id=uuid() if id is None else id,
            broker_consumer=broker,
            topic_disable_leader=True,
            web_enabled=False,
        )
        self._workdir = Path(work_dir)
        self._workdir.mkdir(exist_ok=True)


    # The properties are straigth forward so ... no explanations are needed

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return self._loop

    @property
    def workdir(self) -> Path:
        return self._workdir

    @property
    def version(self) -> "Client.Version":
        return self._version

    @property
    def debug(self)->bool:
        return self._debug

    @property
    def loglevel(self)->Union[str, int]:
        return self._logleve

    # This is a faust topic builder with some cache (*just for internal use*)
    @cache
    def _topic(self, record: Record):
        topic_name = f"{self.version.value}-{self.allowed_records[record]}"
        return self._app.topic(topic_name, value_type=record)

    # Partial exposition of the faust agent decorator, an agent is (in this case)
    # an asyncronous stream consumer
    def agent(self, record):
        assert record in self.allowed_records, "This is not an allowed Chat Wars Record"
        return self._app.agent(self._topic(record))

    # This is a very straigth forward exposition of faust timer function
    def timer(self, seconds):
        return self._app.timer(interval=seconds)

    # Return a function to start and a function to stop it (not for external use)
    @cached_property
    def _driven_functions(self) -> Tuple[Callable, Callable]:

        
        worker = Worker(
            self._app,
            loop=self.loop,
            debug=self.debug,
            loglevel=self.loglevel,
            workdir=self.workdir,
            quiet=True,
            redirect_stdouts=False,
        ) # We remove or preset not important setting when we create the worker

       
        worker.spinner = None  # Removing anoying spinner

        return lambda : self.loop.run_until_complete(worker.start()), worker.stop_and_shutdown

    # This method starts the app execution loop
    def start(self):
        return self._driven_functions[0]()

    # This method stops the app execution loop
    def stop(self):
        return self._driven_functions[1]()

    # This method run the app in a fancy controlled way
    def run(self):
        try:
            self.start()
        finally:
            self.stop()

    # A method for cli use ... if you want
    def cli(self):
        return self._app.main()


"""
I have some doubts about let **rockdb** faust integration or not.
I´m going to let it out for now.
"""

# Now we are ready for some testing 👋
