import csv
from io import StringIO
from .scan import Scan
from .session_resource import SessionResource
from .assessor import Assessors
from .variables import format_message
from .variables import dict_uris
from .request import try_to_request


class Session(dict):
    def __init__(self, subject, level_verbose, level_tab, **kwargs):
        super().__init__(**kwargs)
        self["subject"] = subject
        self.level_verbose = level_verbose
        self.level_tab = level_tab

    def get_list_scans(self, verbose):
        output = StringIO()
        if verbose:
            print(
                format_message(
                    self.level_verbose, self.level_tab, f"Session: {self['label']}"
                ),
                flush=True,
            )
        output.write(
            try_to_request(
                self["subject"]["project"].interface,
                self["subject"]["project"].url_xnat
                + dict_uris["scans"](
                    self["subject"]["project"]["ID"], self["subject"]["ID"], self["ID"]
                ),
            ).text
        )
        output.seek(0)
        reader = csv.DictReader(output)
        self.dict_scans = dict()
        for row in reader:
            try:
                self.dict_scans[row["ID"]] = Scan(
                    self, self.level_verbose + 1, self.level_tab + 1, **row
                )

            except KeyError:
                continue
        output.close()

    def get_list_session_resources(self, path_download, overwrite=False, verbose=False):
        output = StringIO()
        if verbose:
            print(
                format_message(
                    self.level_verbose, self.level_tab, f"Session: {self['ID']}"
                ),
                flush=True,
            )
        u = self["subject"]["project"].url_xnat + dict_uris["session_resources"](
            self["subject"]["project"]["ID"], self["subject"]["ID"], self["ID"]
        )
        output.write(
            try_to_request(
                self["subject"]["project"].interface,
                self["subject"]["project"].url_xnat
                + dict_uris["session_resources"](
                    self["subject"]["project"]["ID"], self["subject"]["ID"], self["ID"]
                ),
            ).text
        )
        output.seek(0)
        reader = csv.DictReader(output)
        self.dict_resources = dict()
        for row in reader:
            try:
                self.dict_resources[row["label"]] = SessionResource(
                    self, self.level_verbose + 1, self.level_tab + 1, **row
                )

            except KeyError:
                continue
        output.close()

    def get_list_assessors(self, verbose):
        output = StringIO()
        if verbose:
            print(
                format_message(
                    self.level_verbose, self.level_tab, f"Assessors:  {self['ID']}"
                ),
                flush=True,
            )
        output.write(
            try_to_request(
                self["subject"]["project"].interface,
                self["subject"]["project"].url_xnat
                + dict_uris["assessors"](
                    self["subject"]["project"]["ID"], self["subject"]["ID"], self["ID"]
                ),
            ).text
        )
        output.seek(0)
        reader = csv.DictReader(output)
        self.dict_assessors = dict()
        for row in reader:
            try:
                self.dict_assessors[row["ID"]] = Assessors(
                    self, self.level_verbose + 1, self.level_tab + 1, **row
                )
            except Exception as e:
                print(e)
                # sys.exit(2)
                continue
        output.close()

    def download(
        self,
        path_download,
        overwrite=False,
        verbose=False,
    ):
        print("\033[7;0H\u001b[0K", end="",flush=True)
        self.get_list_scans(verbose)
        for scan_obj in self.dict_scans.values():
            # if "anat" in scan_obj["ID"]:
            scan_obj.download(
                path_download,
                overwrite=overwrite,
                verbose=verbose,
            )

        self.get_list_assessors(verbose)
        for resource_obj in self.dict_assessors.values():

            resource_obj.download(
                path_download,
                overwrite=overwrite, verbose=verbose)

        self.get_list_session_resources(verbose)
        for resource_obj in self.dict_resources.values():
            resource_obj.download(
                path_download,
                overwrite=overwrite,
                verbose=verbose,
            )
        print(
            format_message(self.level_verbose, self.level_tab, "\u001b[0K"),
            end="",
            flush=True,
        )
