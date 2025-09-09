import csv
import os
import progressbar
from io import StringIO
from .subject import Subject
from .variables import format_message
from .variables import dict_uris
from .request import try_to_request


class Project(dict):
    def __init__(self, url_xnat, interface, level_verbose, level_tab, **kwargs):
        super().__init__(**kwargs)
        self.url_xnat = url_xnat
        self.interface = interface
        self.level_verbose = level_verbose
        self.level_tab = level_tab
        self.dict_subjects = dict()

    def get_list_subjects(self, verbose):
        output = StringIO()

        if verbose:
            print(
                format_message(
                    self.level_verbose,
                    self.level_tab,
                    "Project: {}".format(self["secondary_ID"]),
                ),
                flush=True,
            )
        output.write(
            try_to_request(
                self.interface, self.url_xnat + dict_uris["subjects"](self["ID"])
            ).text
        )
        output.seek(0)
        reader = csv.DictReader(output)
        for row in reader:
            row["project"] = self
            self.dict_subjects[row["ID"]] = Subject(
                self.level_verbose + 1, self.level_tab + 1, **row
            )
        output.close()

    def download(
        self,
        path_download,
        subject_list={},
        overwrite=False,
        verbose=False,
    ):
        
        path_download = path_download.joinpath(self["ID"], "sourcedata")
        # print("\033[5;0H\u001b[0K", end="",flush=True)
        self.get_list_subjects(verbose)
        if subject_list:
            subjects_to_download = {
                subject_id: content
                for subject_id, content in self.dict_subjects.items()
                if content["label"] in subject_list.keys()
            }
            if not self.dict_subjects:
                print(
                            format_message(
                                self.level_verbose + 13,
                                self.level_tab,
                                f"There are no subjects in the table provided for the project {self['secondary_ID']}.",
                            ),
                            flush=True,
                        )
                return

            list_labels = [content["label"] for content in subjects_to_download.values()]
            missing_subjects = [key for key in subject_list.keys() if key not in list_labels]
            if missing_subjects:
                print(
                        format_message(
                            self.level_verbose + 14,
                            self.level_tab,
                            f"The following subjects do not exist in the table provided for the project {len(missing_subjects)}",
                        ),
                        flush=True,
                    )
                return
            self.dict_subjects = subjects_to_download
            
        # print(
        #     format_message(self.level_verbose + 12, self.level_tab, f"Subject:{self.dict_subjects.keys()}"),
        #     end="",
        #     flush=True,
        # )
        # move the cursor
        print("\033[4;0H", end="",flush=True)
        bar_subject = progressbar.ProgressBar(
            maxval=len(self.dict_subjects),
            prefix=format_message(self.level_verbose - 1, 0, ""),
        ).start()
        for iter, subject_obj in enumerate(self.dict_subjects.values()):
            subject_obj.download(
                path_download,
                overwrite=overwrite,
                sessions_list=subject_list.get(subject_obj["label"], {"sessions":[]})["sessions"],
                verbose=verbose
            )
            print(format_message(self.level_verbose - 1, 0, ""))
            bar_subject.update(iter + 1)
        print(format_message(self.level_verbose - 1, 0, ""))
        bar_subject.finish()
