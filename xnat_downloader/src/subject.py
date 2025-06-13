import csv
from io import StringIO
from .session import Session
from .variables import format_message
from .variables import dict_uris
from .request import try_to_request


class Subject(dict):
    def __init__(self, level_verbose, level_tab, **kwargs):
        super().__init__(**kwargs)
        self.level_verbose = level_verbose
        self.level_tab = level_tab

    def get_list_experiments(self, verbose):
        output = StringIO()
        if verbose:
            print(
                format_message(
                    self.level_verbose, self.level_tab, f"Subject: {self['label']}"
                ),
                flush=True,
            )
        output.write(
            try_to_request(
                self["project"].interface,
                self["project"].url_xnat
                + dict_uris["experiments"](self["project"]["ID"], self["label"]),
            ).text
        )
        output.seek(0)
        reader = csv.DictReader(output)
        self.dict_sessions = dict()
        for row in reader:
            self.dict_sessions[row["label"]] = Session(
                self, self.level_verbose + 1, self.level_tab + 1, **row
            )
        output.close()

    def download(
        self,
        path_download,
        sessions_list=[],
        overwrite=False,
        verbose=False,
    ):
        print("\033[6;0H\u001b[0K", end="", flush=True)
        self.get_list_experiments(verbose)

        if sessions_list:
            sessions_to_download = {
                session_id: content
                for session_id, content in self.dict_sessions.items()
                if content["label"] in sessions_list
            }
            if not self.dict_sessions:
                print(
                    format_message(
                        self.level_verbose+7,
                        self.level_tab,
                        "No sessions to download",
                    ),
                    flush=True,
                )
                return
            self.dict_sessions = sessions_to_download
        # move the cursor
        for session_obj in self.dict_sessions.values():
            # if "MR" in session_obj["label"]:
            session_obj.download(
                path_download, overwrite=overwrite, verbose=verbose
            )

        print(
            format_message(self.level_verbose, self.level_tab, "\u001b[0K"),
            end="",
            flush=True,
        )
