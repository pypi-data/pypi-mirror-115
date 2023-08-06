# jupyterlab-requirements
# Copyright(C) 2020, 2021 Francesco Murdaca
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""Requirements API for jupyterlab requirements."""

import json
import os
import logging
import subprocess

from pathlib import Path

from jupyter_server.base.handlers import APIHandler
from tornado import web

from thoth.python import Project

_LOGGER = logging.getLogger("jupyterlab_requirements.dependencies_files_handler")


class DependenciesStoredHandler(APIHandler):
    """Dependencies files handler to retrieve dependencies files."""

    @web.authenticated
    def post(self):
        """Get requirements file from disk."""
        input_data = self.get_json_body()

        kernel_name: str = input_data["kernel_name"]
        home = Path.home()
        store_path: Path = home.joinpath(".local/share/thoth/kernels")

        env_path = Path(store_path).joinpath(kernel_name)

        _LOGGER.info("Path used to get dependencies is: %r", env_path.as_posix())

        # Delete and recreate folder
        if env_path.exists():
            _ = subprocess.call(f"rm -rf ./{kernel_name} ", shell=True, cwd=Path(store_path))

        requirements_format = "pipenv"

        pipfile_path = env_path.joinpath("Pipfile")
        pipfile_lock_path = env_path.joinpath("Pipfile.lock")

        if requirements_format == "pipenv":
            _LOGGER.debug("Get Pipfile/Pipfile.lock in %r", env_path)
            project = Project.from_files(pipfile_path=pipfile_path, pipfile_lock_path=pipfile_lock_path)

        requirements = project.pipfile.to_dict()
        requirements_locked = project.pipfile_lock.to_dict()

        self.finish(json.dumps({"requirements": requirements, "requirements_lock": requirements_locked}))


class DependenciesFilesHandler(APIHandler):
    """Dependencies files handler to store dependencies files."""

    @web.authenticated
    def post(self):
        """Store requirements file to disk."""
        initial_path = Path.cwd()
        input_data = self.get_json_body()

        # Path of the repo where we need to store
        path_to_store: str = input_data["path_to_store"]

        kernel_name: str = input_data["kernel_name"]
        requirements: str = input_data["requirements"]
        requirements_lock: str = input_data["requirement_lock"]
        complete_path: str = input_data["complete_path"]

        env_path = Path(complete_path).joinpath(path_to_store).joinpath(kernel_name)

        _LOGGER.info("Path used to store dependencies is: %r", env_path.as_posix())

        # Delete and recreate folder
        if env_path.exists():
            _ = subprocess.call(f"rm -rf ./{kernel_name} ", shell=True, cwd=Path(complete_path).joinpath(path_to_store))

        env_path.mkdir(parents=True, exist_ok=True)

        os.chdir(env_path)

        requirements_format = "pipenv"

        project = Project.from_strings(requirements, requirements_lock)

        pipfile_path = env_path.joinpath("Pipfile")
        pipfile_lock_path = env_path.joinpath("Pipfile.lock")

        if requirements_format == "pipenv":
            _LOGGER.debug("Writing to Pipfile/Pipfile.lock in %r", env_path)
            project.to_files(pipfile_path=pipfile_path, pipfile_lock_path=pipfile_lock_path)

        os.chdir(initial_path)
        self.finish(json.dumps({"message": f"Successfully stored requirements at {env_path}!"}))
