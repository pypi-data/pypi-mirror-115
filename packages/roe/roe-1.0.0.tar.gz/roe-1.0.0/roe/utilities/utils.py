# Copyright 2021 Chainopt LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import shutil
import socket
import time
from contextlib import closing
from pathlib import Path

import click
import docker
import keyring
import numpy as np
import pandas as pd
import requests
import stdiomask
import yaml
from docker import APIClient
from docker.utils import kwargs_from_env

from roe.utilities import loader
from roe.utilities.errors import *

ROE_DIR = os.path.join(os.path.join(os.path.expanduser("~"), "Documents"), "ROE")


def load_yaml(stream) -> dict:
    yaml_file = open(stream, "r", encoding="utf-8")
    try:
        cred_yaml = yaml.load(yaml_file, Loader=yaml.Loader)
    except yaml.YAMLError:
        cred_yaml = None
    finally:
        yaml_file.close()
    return cred_yaml


def delete_both(base_url, package_name):
    delete_container(base_url, package_name)
    delete_package(base_url, package_name)
    return


def delete_package(base_url, package_name):
    response_delete = requests.get(base_url + '/packages/delete/?package_name=' + package_name)

    if response_delete.status_code == 200:
        pass
    else:
        click.echo("Unable to delete package: " + package_name)
    return


def delete_container(base_url, package_name):
    response_remove_container = requests.get(base_url + '/containers/remove/?package_name=' + package_name)

    if response_remove_container.status_code == 200:
        pass
    else:
        click.echo("Unable to shut down API for package: " + package_name)

    return


def check_port(port):
    if port:
        if 1023 < int(port) < 65535:
            if port_in_use(int(port)):
                raise BadPortError("The port " + port + " is already in use.")
        else:
            raise BadPortError()
    else:
        port = find_free_port()
    return port


def find_free_port():
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(('localhost', 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def port_in_use(port) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0


def get_roe_url() -> str:
    try:
        client = APIClient(**kwargs_from_env())
    except docker.errors.DockerException:
        raise DockerNotRunningError()
    roe_port = None
    for i in client.containers():
        if i['Names'][0] == '/roe-api':
            roe_port = i['Ports'][0]['PublicPort']
            break
    if roe_port:
        base_url = 'http://localhost:' + str(roe_port)
    else:
        begin(local=True, file=None)
        base_url = get_roe_url()
    return base_url


def get_package_url(package_name: str):
    response_running_containers = requests.get(get_roe_url() + '/containers/?include_stopped=true')
    dfAllContainers = pd.read_json(response_running_containers.text, orient='records')
    dfRunningContainers = dfAllContainers[dfAllContainers['State'] == 'running']
    launch_url = 'http://localhost:' + str(dfRunningContainers[dfRunningContainers['Names'] == package_name]
                                           .iloc[0]['Ports'].split(":")[1].split("-")[0])
    return launch_url


def get_package_state(package_name: str):
    response_all_containers = requests.get(get_roe_url() + '/containers/?include_stopped=true')
    dfAllContainers = pd.read_json(response_all_containers.text, orient='records')
    package_state = ""
    if package_name in dfAllContainers.Names.values:
        package_state = str(dfAllContainers[dfAllContainers['Names'] == package_name].iloc[0]['State'])
    return package_state


def uri_exists_stream(uri: str) -> bool:
    try:
        with requests.get(uri, stream=True) as response:
            try:
                response.raise_for_status()
                return True
            except requests.exceptions.HTTPError:
                return False
    except requests.exceptions.ConnectionError:
        return False


def begin(local, file):
    if local:

        # specify version here or use 'latest'
        api_version = 'latest'

        try:
            client, docker_creds = login(file, api_version)
        except docker.errors.DockerException:
            raise DockerNotRunningError()

        loader_animation = loader.Loader("Setting up local deployment services..",
                                         "ROE is now ready to deploy your model.",
                                         0.05).start()

        # Custom function in utils to find a free port on local
        roe_port = find_free_port()

        # check if ROE is already running locally. If it is, then remove it.
        myContainers = client.containers(all=True)
        for i in myContainers:
            if i['Names'][0] == '/roe-api':
                client.remove_container(i, force=True)

        # Create the "roe-packages" volume if it does not already exist
        volume_name = "roe-packages"

        # create the roe-api local deployment docker container and specify ports and volume bindings.
        container = client.create_container(name='roe-api', image='chainopt/roe-api:' + api_version,
                                            stdin_open=True,
                                            tty=True,
                                            environment=docker_creds,
                                            volumes=['/var/run/docker.sock', '/var/roe-packages'], ports=[80],
                                            host_config=client.create_host_config(binds={
                                                '/var/run/docker.sock': {'bind': '/var/run/docker.sock',
                                                                         'mode': 'rw', },
                                                volume_name: {'bind': '/var/roe-packages', 'mode': 'rw', }},
                                                port_bindings={80: roe_port}))

        client.start(container)

        while not uri_exists_stream(get_roe_url()):
            # wait for roe to start up
            pass

        loader_animation.stop()

    else:
        raise NoLocalFlagError()

    return


def login(file: str, api_version: str):
    """
    Handles the sequence of trying different credential files to gain access to DockerHub
    """

    # Instantiate the default credentials path and ROE folder
    if not os.path.isdir(ROE_DIR):
        os.mkdir(ROE_DIR)
    cred_path = os.path.join(ROE_DIR, "credentials.yaml")

    # Check if a filename was passed through
    if file:
        click.echo("Loading credentials from file: " + file)
        docker_creds = load_yaml(file)
        try:
            return cred_check(docker_creds, cred_path, api_version)
        except requests.exceptions.HTTPError:
            click.echo("Provided credentials file failed to authenticate.")
        except DockerHubAccountError:
            click.echo("Provided credentials do not have access to the API on Docker Hub."
                       " Please use the correct account.")

    # Check if credentials were previously successfully provided.
    if os.path.exists(cred_path):
        click.echo("Loading credentials from: " + cred_path)
        docker_creds = load_yaml(cred_path)
        docker_creds["docker_pw"] = keyring.get_password("ROE", docker_creds["docker_user"])
        try:
            return cred_check(docker_creds, cred_path, api_version)
        except requests.exceptions.HTTPError:
            click.echo("Saved credentials failed to authenticate.")
        except DockerHubAccountError:
            click.echo("Saved credentials do not have access to the API on Docker Hub. Please use the correct account.")
    # Final solution is to ask for credentials
    click.echo("These credentials are used to check if you have access to ChainOpt artifacts on Docker Hub.")
    docker_creds = dict()
    docker_creds["docker_user"] = input("Enter your Docker Username: ")
    docker_creds["docker_pw"] = stdiomask.getpass(prompt='Enter your Docker Password: ', mask='*')
    try:
        return cred_check(docker_creds, cred_path, api_version)
    except requests.exceptions.HTTPError:
        raise BadCredError()


def cred_check(docker_creds, cred_path, api_version):
    # Get local docker client setup
    client = APIClient(**kwargs_from_env())

    client.login(username=docker_creds.get("docker_user"), password=docker_creds.get("docker_pw"))

    # Check if account has access to Docker Hub API image
    try:
        client.pull('chainopt/roe-api', tag=api_version)
    except docker.errors.ImageNotFound:
        raise DockerHubAccountError()

    # Only save credentials to a file if they work.
    keyring.set_password("ROE", docker_creds["docker_user"], docker_creds["docker_pw"])
    with open(cred_path, 'w') as f:
        yaml.dump({"docker_user": docker_creds["docker_user"]}, f)
        click.echo("Credentials successfully authenticated and saved!")
        f.close()
    return client, docker_creds


def begin_packages(local):
    response_containers = requests.get(get_roe_url() + '/containers/?include_stopped=true')
    dfAllContainers = pd.read_json(response_containers.text, orient='records')
    if not dfAllContainers.empty:
        dfStoppedContainers = dfAllContainers[dfAllContainers['State'] == 'exited']
        if not dfStoppedContainers.empty:
            checkDelete = input("Would you like to start all stopped packages? Enter Y to confirm: ").lower()
            if checkDelete == 'y':
                start(local, package_name=None, all=True)


def end(local):
    if local:
        try:
            client = APIClient(**kwargs_from_env())
        except docker.errors.DockerException:
            raise DockerNotRunningError()

        myContainers = client.containers(all=True)
        for i in myContainers:
            # look for the roe-api container running locally and remove it.
            if i['Names'][0] == '/roe-api':
                list_packages(local)
                end_packages(local)
                client.remove_container(i, force=True)
                click.echo("ROE has ended. To restart, simply run the 'roe begin -l' command.")
                return
        raise AlreadyEndedError()
    else:
        raise NoLocalFlagError()


def end_packages(local):
    base_url = get_roe_url()

    response_containers = requests.get(base_url + '/containers/?include_stopped=true')
    dfAllContainers = pd.read_json(response_containers.text, orient='records')
    if not dfAllContainers.empty:
        dfRunningContainers = dfAllContainers[dfAllContainers['State'] == 'running']
        if not dfRunningContainers.empty:
            checkDelete = input("Would you like to stop all running packages? Enter Y to confirm: ").lower()
            if checkDelete == 'y':
                stop(local, package_name=None, all=True, quick_deploy=False)


def deploy(local, package_name, folder_path, port, quick_deploy):
    folder_name, full_path = package_path_check(folder_path)

    # Use folder name as package name if not specified
    if not package_name:
        package_name = folder_name

    # Check if deployment is local
    if not local:
        raise NoLocalFlagError()

    # create base url that for the roe api that is running locally to send requests
    base_url = get_roe_url()

    # Get list of packages deployed
    response_packages = requests.get(base_url + '/packages/')
    dfPackages = pd.read_json(response_packages.text, orient='records')

    # Check if there are packages or if the package is already deployed
    if dfPackages.empty:
        redeploy_bool = False
    elif package_name not in dfPackages.get("Name").values:
        redeploy_bool = False
    else:
        redeploy_bool = True
        click.echo("Package named '" + package_name + "' found.")
        if not quick_deploy:
            check_quick_deploy = input(
                "Would you like to redeploy the package? Enter Y to confirm: ").lower()
            if check_quick_deploy == 'y':
                quick_deploy = True
            else:
                raise DuplicatePackageError()

    # Check the port or create a new port designation if not a redeployment
    if not redeploy_bool:
        port = check_port(port)

    # loader shows progress with begin title, end title and timer. It has been customized.
    loader_text = ["D", "Red"][redeploy_bool] + "eploying Package:"
    loader1 = loader.Loader(loader_text,
                            "The `" + package_name + "` package is deployed!",
                            "`" + package_name + "` model API has failed to deploy.",
                            0.05).start()

    if redeploy_bool:
        response_all_containers = requests.get(base_url + '/containers/?include_stopped=true')
        dfAllContainers = pd.read_json(response_all_containers.text, orient='records')
        if not dfAllContainers.empty and package_name in dfAllContainers.Names.values:
            dfRunningContainers = dfAllContainers[dfAllContainers['State'] == 'running']
        else:
            delete_package(base_url, package_name)
            loader1.stop()
            deploy(local, package_name, folder_path, port, quick_deploy)
            return
        # Check if container exists/running/stopped
        if package_name in dfRunningContainers.Names.values:

            # Stop Container
            stop_response = requests.get(base_url + '/containers/stop/?package_name=' + package_name)
            if stop_response.status_code != 200:
                loader1.failed()
                raise PackageStopError(package_name)

        # delete the package
        delete_response = requests.get(base_url + '/packages/delete/?package_name=' + package_name)
        if delete_response.status_code != 200:
            loader1.failed()
            raise PackageDeletionError()

    # Upload the package
    upload_package(folder_path, folder_name, package_name, base_url)

    # Verify the package is good to run
    requirements_exists, model_successes, model_failures, non_model_folders = parse_verify(base_url, package_name)
    verify_failure = not requirements_exists or not model_successes or model_failures
    if verify_failure:
        loader1.failed()
        if not requirements_exists:
            click.secho("Requirements.txt needs to be configured at root of package.", bg="red", fg="white")
        if model_failures:
            click.secho("Failed model folders and issues:\n", bg="red", fg="white")
            click.secho(yaml.dump(model_failures), bg="red", fg="white")
        elif not model_successes:
            click.secho("Unable to find any properly model folders with a config.yaml file", bg="red", fg="white")
        delete_package(base_url, package_name)
        raise PackageVerifyError()

    if redeploy_bool:
        # restart the api container with updated package
        response = requests.get(base_url + '/containers/restart/?package_name=' + package_name)

        if response.status_code == 200:
            # get the local url of the redeployed package to show the user and launch.
            launch_url = get_package_url(package_name)
        else:
            loader1.failed()
            raise PackageStartError(package_name)
    else:
        launch_url = 'http://localhost:' + str(port)
        response_run = requests.get(base_url + '/deploy/?package_name=' + package_name + '&port=' + str(port))
        if response_run.status_code != 200:
            loader1.failed()
            delete_package(base_url, package_name)
            if response_run.status_code == 409:
                raise PackageNameConflictError()
            raise DeployAPIError()

    # check if the url is actually up.
    while not uri_exists_stream(launch_url):
        # If it doesn't come up and container fails, check if container has stopped.
        response_containers = requests.get(base_url + '/containers/?include_stopped=true')
        dfAllContainers = pd.read_json(response_containers.text, orient='records')
        if not dfAllContainers.empty:
            dfStoppedContainers = dfAllContainers[dfAllContainers['State'] == 'exited']
            if not dfStoppedContainers.empty:
                # If container has stopped save logs and clean up container garbage.
                if package_name in dfStoppedContainers.Names.values:
                    loader1.failed()
                    failure_state_logs(base_url, package_name)
                    return

    # once out of while loop, assign work based on url being up or down.
    loader1.stop()
    click.echo("URL: " + launch_url)
    if not quick_deploy:
        click.pause("Press any key to launch in browser!")
        click.launch(launch_url)
    return


def undeploy(local, package_name, all):
    if local:
        base_url = get_roe_url()
        # base_url returns none when roe api isn't running locally

        # if all isn't specified and a package_name is given
        if not all and package_name:
            # List of Docker containers deployed
            response_containers = requests.get(base_url + '/containers/?include_stopped=true')
            dfAllContainers = pd.read_json(response_containers.text, orient='records')

            # List of packages in the roe-packages volume
            response_packages = requests.get(base_url + '/packages/')
            dfPackages = pd.read_json(response_packages.text, orient='records')

            # Check if there's nothing
            if dfAllContainers.empty and dfPackages.empty:
                raise NoRunningPackagesError()
            # Ensures we don't get DataFrame errors
            elif not dfAllContainers.empty:
                if package_name in dfAllContainers.Names.values:
                    checkDelete = input("Would you like to stop and delete the package? Enter Y to confirm: ").lower()
                    if checkDelete == 'y':
                        delete_both(base_url, package_name)
                        click.echo(f"'{package_name}' package undeployed.")
                        return
                    else:
                        click.echo(f"'{package_name}' is still running.")
            # Checks for orphaned packages
            if package_name in dfPackages.Name.values:
                delete_package(base_url, package_name)
                click.echo(f"'{package_name}' package undeployed.")
            # Package must not exist in this case
            else:
                raise PackageExistenceError(package_name)

        # all is an optional flag that requests to  delete all packages
        elif all:
            checkUndeploy = input(
                "Are you sure you want to undeploy all packages? (This cannot be undone.) Enter Y to confirm: ").lower()
            if checkUndeploy == 'y':
                response_containers = requests.get(base_url + '/containers/?include_stopped=true')
                dfAllContainers = pd.read_json(response_containers.text, orient='records')
                if not dfAllContainers.empty:
                    response_stop_all = requests.get(base_url + '/containers/stop/all/')

                    if response_stop_all.status_code == 200:
                        pass
                    else:
                        click.echo("Unable to stop all packages.")

                    response_kill_all = requests.get(base_url + '/containers/kill/all/')

                    if response_kill_all.status_code == 200:
                        pass
                    else:
                        click.echo("Unable to kill all packages.")

                    response_packages = requests.get(base_url + '/packages/')
                    dfPackages = pd.read_json(response_packages.text, orient='records')
                    package_list = dfPackages['Name'].tolist()
                    for package_name in package_list:
                        if package_name in dfAllContainers.Names.values:
                            delete_container(base_url, package_name)
                            click.echo("Undeployed '" + package_name + "' package.")

                response_packages_prune = requests.get(base_url + '/packages/prune/')

                if response_packages_prune.status_code == 200:
                    click.echo("All packages undeployed.")
                else:
                    click.echo("Unable to delete all packages")
            else:
                click.echo("Undeploy all aborted.")
        else:
            raise MissingPackageInputError()
    else:
        raise NoLocalFlagError()

    return


def stop(local, package_name, all, quick_deploy):
    if local:
        base_url = get_roe_url()

        # get list of deployed packages that are running
        response_containers = requests.get(base_url + '/containers/?include_stopped=false')
        dfContainers = pd.read_json(response_containers.text, orient='records')
        if not dfContainers.empty:
            if all:
                for package in dfContainers.Names.values:
                    stop_package(base_url, package, quick_deploy)
            # check if package exists in list and stop it.
            elif package_name:
                if package_name in dfContainers.Names.values:
                    stop_package(base_url, package_name, quick_deploy)
                else:
                    raise PackageExistenceError(package_name)
            else:
                raise MissingPackageInputError()

        else:
            raise NoRunningPackagesError()
    else:
        raise NoLocalFlagError()

    return


def stop_package(base_url, package_name, quick_deploy):
    response = requests.get(base_url + '/containers/stop/?package_name=' + package_name)
    if response.status_code == 200:
        while not get_package_state(package_name) == 'exited':
            click.echo("Updating Status...")
        if not quick_deploy:
            click.echo("The '" + package_name + "' package has been stopped.")
    elif response.status_code == 404:
        click.echo("Unable to stop the '" + package_name + "' package.")


def start(local, package_name, all):
    if local:
        base_url = get_roe_url()

        # Get all containers
        response_containers = requests.get(base_url + '/containers/?include_stopped=true')
        dfContainers = pd.read_json(response_containers.text, orient='records')

        if not dfContainers.empty:
            if all:
                for package in dfContainers.Names.values:
                    start_package(base_url, package, all)
            # check if package exists in list and start it.
            elif package_name:
                if package_name in dfContainers.Names.values:
                    start_package(base_url, package_name, all)
                else:
                    raise PackageExistenceError(package_name)
            else:
                raise MissingPackageInputError()
            # check if the package shows up in the list
        else:
            raise NoRunningPackagesError()
    else:
        raise NoLocalFlagError()
    return


def start_package(base_url, package_name, all):
    response = requests.get(base_url + '/containers/restart/?package_name=' + package_name)
    if response.status_code == 200:
        launch_url = get_package_url(package_name)

        # wait till package starts up to confirm
        while not uri_exists_stream(launch_url):
            response_containers = requests.get(base_url + '/containers/?include_stopped=true')
            dfAllContainers = pd.read_json(response_containers.text, orient='records')
            if not dfAllContainers.empty:
                dfStoppedContainers = dfAllContainers[dfAllContainers['State'] == 'exited']

                # check if package container has errored out to stop waiting
                if not dfStoppedContainers.empty and package_name in dfStoppedContainers.Names.values:
                    click.echo("Failed to start the package.")
                    failure_state_logs(base_url, package_name)
                    return

        # once out of while loop, assign work based on url being up or down.
        click.echo("The '" + package_name + "' package has been started at: " + launch_url)
        if not all:
            checkLaunch = input(
                "Would you like to launch it in the default browser? Enter Y to confirm : ").lower()
            if checkLaunch == 'y':
                click.launch(launch_url)

    elif response.status_code == 404:
        click.echo("Unable to start the '" + package_name + "' package.")


def list_packages(local):
    if local:
        base_url = get_roe_url()

        # get list of uploaded packages
        response_packages = requests.get(base_url + '/packages/')
        dfPackages = pd.read_json(response_packages.text, orient='records')

        # get list of deployed packages
        response_containers = requests.get(base_url + '/containers/?include_stopped=true')
        dfContainers = pd.read_json(response_containers.text, orient='records')

        click.echo("--------------------")
        # somehow give a list back to the user, but only one consolidated list.
        if dfPackages.empty:
            if dfContainers.empty:
                click.echo("No packages deployed.")
            else:
                if len(dfContainers) == 1:
                    click.echo(str(len(dfContainers)) + ' package:')
                elif len(dfContainers) > 1:
                    click.echo(str(len(dfContainers)) + ' packages:')
                click.echo("--------------------")
                # list cleanup
                dfContainers['Ports'] = dfContainers['Ports'] \
                    .apply(
                    lambda x: 'http://localhost:' + str(x).split(":")[1].split("-")[0] if not pd.isnull(x) else '')
                dfContainers.drop(['Status', 'package_name'], axis=1, inplace=True)
                dfContainers = dfContainers.rename(
                    columns={"Names": "Name", "Ports": "url", "Created": "Last Started"})
                dfContainers = dfContainers.reset_index(drop=True)
                dfContainers.index = np.arange(1, len(dfContainers) + 1)
                click.echo(dfContainers)
                click.echo('Note: Showing limited information')
        else:

            if dfContainers.empty:
                if len(dfPackages) == 1:
                    click.echo(str(len(dfPackages)) + ' package:')
                elif len(dfPackages) > 1:
                    click.echo(str(len(dfPackages)) + ' packages:')
                click.echo("--------------------")
                dfPackages.index = np.arange(1, len(dfPackages) + 1)
                click.echo(dfPackages)
                click.echo('Note: Showing limited information')
            else:
                # Ideally, this is the list called on at all times.
                # Each package should map to a running or stopped container.
                if len(dfContainers) == 1:
                    click.echo(str(len(dfContainers)) + ' package:')
                elif len(dfContainers) > 1:
                    click.echo(str(len(dfContainers)) + ' packages:')
                click.echo("--------------------")
                dfResult = pd.merge(dfContainers, dfPackages, left_on=['Names'], right_on=['Name'], how='inner')
                # Create clean url that can be clicked.
                dfResult['Ports'] = dfResult['Ports'] \
                    .apply(lambda x: 'http://localhost:' + str(x)
                           .split(":")[1].split("-")[0] if not pd.isnull(x) else 'None')
                dfResult = dfResult.rename(columns={"Names": "Name", "Ports": "url", "Created": "Last Started",
                                                    "LastModified": "Last Updated"})
                dfResult = dfResult.reset_index(drop=True)
                # Number the packages properly
                dfResult.index = np.arange(1, len(dfResult) + 1)
                click.echo(dfResult)
        click.echo("--------------------")
    else:
        raise NoLocalFlagError()

    return


def logs(local, package_name, tail):
    if local:
        base_url = get_roe_url()

        # get all containers
        response_containers = requests.get(base_url + '/containers/?include_stopped=true')
        dfContainers = pd.read_json(response_containers.text, orient='records')

        # find the container to get logs from
        if not dfContainers.empty:
            if package_name in dfContainers.Names.values:
                generate_logs(base_url, package_name, tail)
            else:
                raise PackageExistenceError(package_name)
        else:
            raise NoRunningPackagesError()
    else:
        raise NoLocalFlagError()
    return


def failure_state_logs(base_url: str, package_name: str):
    """ Generates logs and cleans up package and container data """
    checkLogs = input("Would you like to save the logs? Enter Y to confirm: ").lower()
    if checkLogs == 'y':
        generate_logs(base_url, package_name)
    else:
        click.echo("Logs not generated")
    delete_both(base_url, package_name)
    return


def generate_logs(base_url: str, package_name: str, tail: str = None):
    """ Function for generating logs after a failed container method. """
    # Define the API URL
    api_call = base_url + '/containers/logs/?package_name=' + package_name

    # Ensure logs directory exists
    logs_dir = os.path.join(ROE_DIR, "logs")
    if not os.path.isdir(logs_dir):
        os.mkdir(logs_dir)

    # Add tail variable if needed
    if tail:
        response_logs = requests.get(api_call + '&tail=' + str(tail))
    else:
        response_logs = requests.get(api_call)

    if response_logs.status_code == 200:
        # Remove extraneous double newline whitespace
        logs_text = response_logs.text.replace("\n\n", "\n").replace("\n\n", "\n")
        # Generate filename with timestamp
        file_name = os.path.join(logs_dir, package_name + "-" + time.strftime("%Y%m%d-%H%M%S") + "-running-logs.txt")
        with open(file_name, "w", encoding="utf-8") as log_file:
            log_file.write(logs_text)
            log_file.close()
        click.echo("Logs are available at: " + file_name)
    else:
        raise LoggingError()


def package_path_check(folder_path):
    # Check if folder name exists
    full_path = Path(folder_path).resolve()
    if not full_path.is_dir():
        raise PackagePathError()
    # Get folder name from specified path
    folder_name = full_path.name
    return folder_name, full_path


def upload_package(folder_path, folder_name, package_name, base_url):
    target_dir = Path(folder_path).resolve().parent

    # Compress package
    archive_path = shutil.make_archive(folder_name, 'zip', target_dir, folder_name)

    # Mount package to shared path with local roe-api deployment at var/roe-packages
    # This is also known as the upload step
    url = base_url + '/upload/?package_name=' + package_name
    files = {'package': open(archive_path, 'rb')}
    response = requests.post(url, files=files)
    if response.status_code != 200:
        raise UploadAPIError()

    files["package"].close()
    os.remove(archive_path)
    return


def dupe_upload_handler(full_path, package_name, base_url):
    """ Handles duplicate package names when uploading the package """
    # Get list of all packages uploaded
    response_packages = requests.get(base_url + '/packages/')
    dfPackages = pd.read_json(response_packages.text, orient='records')

    # Checks for an empty list of packages and then if the package is a duplicate
    if not dfPackages.empty:
        if package_name in dfPackages["Name"].values:
            # We iterate through numbers to append to ensure that we have a unique package name.
            new_package_name = package_name
            append = 0
            while new_package_name in dfPackages["Name"].values:
                append += 1
                new_package_name = package_name + f"_{append}"
            new_full_path = os.path.dirname(full_path) + f"\\{new_package_name}"
            os.rename(full_path, new_full_path)
            upload_package(new_full_path, new_package_name, new_package_name, base_url)
            os.rename(new_full_path, full_path)
            return new_package_name
    upload_package(full_path, package_name, package_name, base_url)
    return package_name


def verify(local: bool, package_path: str):
    if not local:
        raise NoLocalFlagError()

    base_url = get_roe_url()

    # Checks and creates variables to upload the package
    package_name, full_path = package_path_check(package_path)

    # Uploads package to the
    package_name = dupe_upload_handler(full_path, package_name, base_url)

    requirements_exists, model_successes, model_failures, non_model_folders = parse_verify(base_url, package_name)

    # Delete the package once verification completes
    delete_package(base_url, package_name)

    if requirements_exists:
        click.secho("Requirements.txt successfully found.\n", bg="green", fg="white")
    else:
        click.secho("Requirements.txt needs to be configured at root of package.\n", bg="red", fg="white")
    if model_failures:
        click.secho("Failed model folders and issues:\n", bg="red", fg="white")
        click.secho(yaml.dump(model_failures), bg="red", fg="white")
    if model_successes:
        click.secho("Successfully verified model folders:", bg="green", fg="white")
        [click.secho(x, bg="green", fg="white") for x in model_successes]
    elif not model_failures:
        click.secho("No model folders with a config.yaml were found!", bg="red", fg="white")
    if non_model_folders:
        click.secho("\nThe following were seen as non-model folders:", bg="yellow", fg="white")
        [click.secho(x, bg="yellow", fg="white") for x in non_model_folders]
    return


def parse_verify(base_url, package_name):
    # Verify the package and return either the verbose output or simply the
    verify_url = base_url + '/verify/?package_name=' + package_name
    verify_response = requests.get(verify_url)

    # Check the verification response for failures
    return_code = verify_response.status_code
    if return_code != 200:
        delete_package(base_url, package_name)
        raise APIError("Verify")

    # Load the API response as a dictionary
    response_dict = json.loads(verify_response.text)
    # Generate containers for each of the directory checks
    model_successes = response_dict["model_successes"]
    model_failures = response_dict["model_failures"]
    non_model_folders = response_dict["non_model_folders"]
    requirements_exists = response_dict["requirements.txt"]
    return requirements_exists, model_successes, model_failures, non_model_folders
