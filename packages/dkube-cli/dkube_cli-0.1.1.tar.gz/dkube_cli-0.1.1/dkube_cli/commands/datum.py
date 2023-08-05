from pprint import pprint

import click
from dkube.sdk.internal.dkube_api import DatumModel
from tabulate import tabulate


def get_datums(api, catagory, username):
    repos = api.list_repos(catagory, username, shared=False)
    datums = []
    for repo in repos[0]["datums"]:
        datums.append(repo["datum"]["name"])
    return datums


def delete_datums(api, username, catagory, name):
    datums = [name]
    if name == "all":
        datums = get_datums(api, catagory, username)

    if (len(datums)) == 0:
        print("No repos found")
        return

    print(f"deleting {len(datums)} repo ", " ".join(datums))

    api._api.datums_delete_by_class(username, catagory, {"datums": datums}, force=True)


def list_datums(data):
    repos = [["name", "owner", "source", "url", "last_updated", "status", "reason"]]
    for entry in data:
        for row in entry["datums"]:
            p = DatumModel(**row["datum"])
            repos.append(
                [
                    p.name,
                    entry["owner"],
                    p.source,
                    p.url,
                    p.generated["updated_time"]["end"],
                    p.generated["status"]["state"],
                    p.generated["status"]["reason"],
                ]
            )

    print(tabulate(repos, headers="firstrow", showindex="always"))


@click.group()
def code():
    """Code commands"""
    pass


@click.group()
def dataset():
    """Dataset commands"""
    pass


@click.group()
def model():
    """Model commands"""
    pass


@code.command("list")
@click.option("-a", "--all", is_flag=True, help="show all resources", default=False)
@click.pass_obj
def list_code(obj, all):
    list_datums(obj["api"].list_code(obj["username"], shared=all))


@code.command("get")
@click.pass_obj
@click.argument("name")
def get_code(obj, name):
    data = obj["api"].get_code(obj["username"], name)
    pprint(data, sort_dicts=True)


@code.command("delete")
@click.pass_obj
@click.argument("name")
def delete_code(obj, name):
    delete_datums(obj["api"], obj["username"], "program", name)


@dataset.command("list")
@click.pass_obj
@click.option("-a", "--all", is_flag=True, help="show all resources", default=False)
def list_datasets(obj, all):
    list_datums(obj["api"].list_datasets(obj["username"], shared=all))


@dataset.command("get")
@click.pass_obj
@click.argument("name")
def get_dataset(obj, name):
    data = obj["api"].get_dataset(obj["username"], name)
    pprint(data, sort_dicts=True)


@dataset.command("delete")
@click.pass_obj
@click.argument("name")
def delete_dataset(obj, name):
    delete_datums(obj["api"], obj["username"], "dataset", name)


@model.command("list")
@click.pass_obj
@click.option("-a", "--all", is_flag=True, help="show all resources", default=False)
def list_models(obj, all):
    list_datums(obj["api"].list_models(obj["username"], shared=all))


@model.command("get")
@click.pass_obj
@click.argument("name")
def get_model(obj, name):
    data = obj["api"].get_model(obj["username"], name)
    pprint(data, sort_dicts=True)


@model.command("delete")
@click.pass_obj
@click.argument("name")
def delete_model(obj, name):
    delete_datums(obj["api"], obj["username"], "model", name)
