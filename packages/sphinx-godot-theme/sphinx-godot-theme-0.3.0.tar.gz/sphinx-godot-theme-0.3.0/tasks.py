"""Run any of the tasks using invoke."""

from invoke import task


@task
def publish(c):
    """"""
    # c.run("python3 -m flit publish")
    c.run("python3 -m flit build")
    c.run("python3 -m twine upload dist/*")


# @task
# def release(c, version: str):
#     """"""
#     if version not in ["minor", "major", "patch"]:
#         print("Version can be either major, minor or patch.")
#         return
#
#     from sphinxgodottheme import __version_info__, __version__
#     _major, _minor, _patch = __version_info__
#
#     if version == "patch":
#         _patch = _patch + 1
#     elif version == "minor":
#         _minor = _minor + 1
#     elif version == "major":
#         _patch = _patch + 1
#
#     c.run(f"git checkout -b release-{_major}.{_minor}.{_patch} dev")
#     c.run(f"sed -i 's/{__version__}/{_major}.{_minor}.{_patch}/g' shark/__init__.py")
#     print(f"Update the readme for version {_major}.{_minor}.{_patch}.")
#     input("Press enter when ready.")
#     c.run(f"git add -u")
#     c.run(f'git commit -m "Update changelog version {_major}.{_minor}.{_patch}"')
#     c.run(f"git push --set-upstream origin release-{_major}.{_minor}.{_patch}")
#     c.run(f"git checkout master")
#     c.run(f"git merge --no-ff release-{_major}.{_minor}.{_patch}")
#     c.run(f'git tag -a {_major}.{_minor}.{_patch} -m "Release {_major}.{_minor}.{_patch}"')
#     c.run(f"git push")
#     c.run(f"git checkout dev")
#     c.run(f"git merge --no-ff release-{_major}.{_minor}.{_patch}")
#     c.run(f"git push")
#     c.run(f"git branch -d release-{_major}.{_minor}.{_patch}")
#     c.run(f"git push origin --tags")
