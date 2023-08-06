# Development notes

## PyInstaller one dir
```pwsh
pyinstaller -w -D --icon=youtube_dl_gui/data/pixmaps/youtube-dl-gui.ico --add-data="youtube_dl_gui/data;youtube_dl_gui/data" --add-data="youtube_dl_gui/locale;youtube_dl_gui/locale" --exclude-module=tests --version-file=file_version_info.txt --noconfirm --name=yt-dlg youtube_dl_gui/__main__.py
```

## Docker
- [ PyInstaller on ManyLinux 2.24](https://github.com/oleksis/pyinstaller-manylinux)
```pwsh
docker run --name yt-dlg -it -d --workdir /src -v ${pwd}:/src pyinstaller-manylinux -w -F --add-data=youtube_dl_gui/data:youtube_dl_gui/data --add-data=youtube_dl_gui/locale:youtube_dl_gui/locale --add-binary=libcrypt.so.2:. --exclude-module=tests --name=yt-dlg youtube_dl_gui/__main__.py
```

- Interactive terminal typing (tty)
```pwsh
docker run --name ytdlg-pyenv -it --entrypoint bash --workdir /src -v ${pwd}:/src pyinstaller-manylinux
```

### Actions Setup-Python
GitHub Actions and [Azure UsePythonVersion](https://github.com/microsoft/azure-pipelines-tasks/blob/1be088a422530fbaa1a9ed7b5073ee665dcb8f53/Tasks/UsePythonVersionV0/installpythonversion.ts#LL11C23-L11C108)

[3.8.15, 3.9.9-win32-x64](https://raw.githubusercontent.com/actions/python-versions/main/versions-manifest.json)


## Winget tools
- RealVNC.VNCViewer
```pwsh
winget install -e --id RealVNC.VNCViewer
```

- Advanced Installer
```pwsh
winget install -e --id Caphyon.AdvancedInstaller
```

## Dev Containers
Use `devcontainer` with dev container Features: [Light-weight Desktop (desktop-lite)](https://github.com/devcontainers/features/tree/main/src/desktop-lite#light-weight-desktop-desktop-lite)

VNC Sever
  - user: vscode
  - password: vscode

### Public devcontainer to Packages (GHCR)
[Example of building and publishing an image](https://code.visualstudio.com/docs/remote/devcontainer-cli#_prebuilding)
```bash
export CR_PAT='YOUR_TOKEN'
echo $CR_PAT | docker login ghcr.io -u USERNAME --password-stdin
devcontainer build --workspace-folder . --push true --image-name ghcr.io/USERNAME/IMAGE-NAME:latest
devcontainer up --workspace-folder .
```

## Tox
Use `pip install tox==4.0.0a8` for test diferents Python versions from Microsoft Store (3.7, 3.8, 3.9, 3.10)

## Winget Packages
- Update package manifest

```pwsh
wingetcreate update --urls "https://github.com/oleksis/youtube-dl-gui/releases/download/v1.8.4/yt-dlg-20221113.1.msi|x64" --version 1.8.4 -s -t ghp_PERSONAL_TOKEN yt-dlg.yt-dlg
```

## Install Open Build Service in openSUSE Tumbleweed
- [Build RPMs in local from PyPI](https://gist.github.com/oleksis/cf45143457cb31f52ebfdcad77a895fe#build-rpms-in-local-from-pypi)

## Distros GNU/Linux with glibc 2.31
[Manylinux Timeline](https://mayeut.github.io/manylinux-timeline/)

- Fedora 32
- openSUSE Leap 15.3
- Debian 11 Bullseye
- Ubuntu 20.04 LTS (Focal Fossa)

## Extras
wxPython using Wayland
```bash
GDK_BACKEND=x11 ./dist/yt-dlg
```

- [GitHub Actions: Deprecating save-state and set-output commands](https://github.blog/changelog/2022-10-11-github-actions-deprecating-save-state-and-set-output-commands/)
