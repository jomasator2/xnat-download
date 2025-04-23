#!/usr/bin/env  python   #iniciaize enviroment
# -*- coding: utf-8 -*-.
"""
Subdirección General de Sistemas de Información para la Salud

Centro de Excelencia e Innovación Tecnológica de Bioimagen de la Conselleria de Sanitat

http://ceib.san.gva.es/

María de la Iglesia Vayá -> delaiglesia_mar@gva.es or miglesia@cipf.es

Jose Manuel Saborit Torres -> jmsaborit@cipf.es

Jhon Jairo Saenz Gamboa ->jsaenz@cipf.es

Joaquim Ángel Montell Serrano -> jamontell@cipf.es

---

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 3 as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.

---

Prerequisites

Python --version >= 3.8

Description:
    This application allow the user to download one project on XNAT and
    transform this project in MIDS format

    
"""
###############################################################################
# Imports
###############################################################################

import argparse
from pathlib import Path

from .src.xnat_session import XnatSession

###############################################################################
# Functions
###############################################################################


def load_projects_and_subjects(file_path, project_key, subject_key, session_key=None, session_date_key=None, modality_key=None):
    """
    Load projects, subjects, and sessions from a file.
    Supports JSON, CSV, and TSV formats.
    """
    import json
    import csv

    file_ext = Path(file_path).suffix.lower()
    project_subjects = {}

    if file_ext == ".json":
        with open(file_path, "r") as f:
            data = json.load(f)
        for project, project_data in data["projects"].items():
            project_subjects[project] = {
                "subjects": {
                    subject: {
                        "sessions": details.get("sessions", {})
                    }
                    for subject, details in project_data["subjects"].items()
                },
                "metadata": {
                    key: value for key, value in project_data.items() if key != "subjects"
                }
            }
    elif file_ext in [".csv", ".tsv"]:
        delimiter = "\t" if file_ext == ".tsv" else ","
        with open(file_path, "r") as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            for row in reader:
                project_id = row.get(project_key)
                subject_id = row.get(subject_key)
                session_id = row.get(session_key)
                session_date = row.get(session_date_key)
                modality = row.get(modality_key)

                if project_id not in project_subjects:
                    project_subjects[project_id] = {"subjects": {}}
                if subject_id not in project_subjects[project_id]["subjects"]:
                    project_subjects[project_id]["subjects"][subject_id] = {"sessions": {}}
                if session_id:
                    project_subjects[project_id]["subjects"][subject_id]["sessions"][session_id] = {
                        "session_date": session_date,
                        "modality": modality,
                    }
    else:
        raise ValueError("Unsupported file format. Please use JSON, CSV, or TSV.")
    
    return project_subjects
    

def main():
    """
    This Fuction is de main programme
    """
    # Control of arguments of programme
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description="This sotfware allows the user to download one project from the XNAT platform",
    )
    parser.add_argument(
        "-w", "--web", type=str, default=None, help="The URL of the XNAT server"
    )
    parser.add_argument(
        "-u",
        "--user",
        type=str,
        default="guest",
        help="The username to login in XNAT. Default: guest",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        default=".",
        help="The directory where the files will be downloaded. Default: current directory",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="Path to a file containing the list of projects and subjects to download. Format: JSON or CSV.",
    )
    parser.add_argument(
        "--project_key",
        type=str,
        default="project_id",
        help="The key or column name for project IDs in the input file. Default: 'project_id'.",
    )
    parser.add_argument(
        "--subject_key",
        type=str,
        default="subject_id",
        help="The key or column name for subject IDs in the input file. Default: 'subject_id'.",
    )
    parser.add_argument(
        "--session_key",
        type=str,
        default="session_id",
        help="The key or column name for session IDs in the input file. Default: 'session_id'.",
    )
    parser.add_argument(
        "-v ",
        "--verbose",
        default=True,
        action="store_true",
        help="Enable verbose (show progress on terminal)",
    )
    parser.add_argument(
        "-ow",
        "--overwrite",
        default=False,
        action="store_true",
        help="Overwrite posibly existing files in output directory",
    )
    args = parser.parse_args()
    page = args.web
    user = args.user
    xnat_data_path = Path(args.output_dir).resolve()
    input_file = args.file
    project_key = args.project_key
    subject_key = args.subject_key
    session_key = args.session_key
    verbose = args.verbose
    overwrite = args.overwrite

    # Validate input file
    if input_file:
        if not Path(input_file).is_file():
            raise FileNotFoundError(f"The specified file '{input_file}' does not exist.")
        # Load projects, subjects, and sessions from file
        project_subjects = load_projects_and_subjects(input_file, project_key, subject_key, session_key)
    else:
        project_subjects = {}

    # Check if XNAT download can be executed
    if xnat_data_path and page:
        xnat_data_path.mkdir(exist_ok=True)
        xnat_sesion_object = XnatSession(page, user)
        with xnat_sesion_object as xnat_session:
            xnat_session.download_projects(
                xnat_data_path,
                with_department=True,
                project_subjects=project_subjects,
                overwrite=overwrite,
                verbose=verbose,
            )
            

if __name__ == "__main__":
    main()
