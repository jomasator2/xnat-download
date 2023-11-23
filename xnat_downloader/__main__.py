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
from .src.variables import types_files_xnat

###############################################################################
# Functions
###############################################################################


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
    verbose = args.verbose
    overwrite = args.overwrite
    # Comprobation if Xnat dowload can be execute
    if xnat_data_path and page:
        xnat_data_path.mkdir(exist_ok=True)
        xnat_sesion_object = XnatSession(page, user)
        with xnat_sesion_object as xnat_session:
            xnat_session.download_projects(
                xnat_data_path,
                with_department=True,
                bool_list_resources=[True for char in types_files_xnat],
                overwrite=overwrite,
                verbose=verbose,
            )
        project_list = xnat_sesion_object.project_list


if __name__ == "__main__":
    main()
