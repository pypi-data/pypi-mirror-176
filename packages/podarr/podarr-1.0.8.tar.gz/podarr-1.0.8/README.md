# What it is
podarr is a Python application to easily manage Plex Media Server and some of other applications through podman rootless containers. Other than the requirements and podarr itself, no other application is required in the user's system.

It is basically a collection of knowledge to make everything works the easier and safer way possible.

## Available services
For now, these are the supported services, but more could easily be added.

- Rclone
- MergerFS
- Plex Media Server
- Radarr
- Sonarr
- Lidarr
- Bazarr
- Prowlarr
- SABnzbd
- qBittorrent
- Auto Backup
- Auto Upload
- Web interface

# Requirements
- To enable podman rootless functionalities, a [few tweaks are necessary](https://wiki.archlinux.org/title/Podman#Rootless_Podman) (not necessary on Fedora):
```sh
touch /etc/subuid /etc/subgid
chmod 644 /etc/subuid /etc/subgid
usermod --add-subuids 100000-165535 --add-subgids 100000-165535 $USER
```

- podarr relies on user's systemd services to control the applications. So, in order to allow user systemd services to run when it's not logged in, user lingering must be enabled. To check if linger is enabled for the current user, type `ls /var/lib/systemd/linger` in the terminal and check if the user is in the list. To enable lingering for the current user:
```sh
loginctl enable-linger $USER
```

- For now, if your Linux distribution is shipped with SELinux, it must be set to permissive or disabled. I'm looking for a workaround on this ([let me know if you can help](https://github.com/podman-arr/podarr-cli/issues/new)). To set SELinux to permissive `sudo nano /etc/selinux/config` and change `SELINUX=enforcing` to `SELINUX=permissive` or `SELINUX=disabled`. A reboot is required.

- podman: podarr is basically a wrapper for podman. So, in order for it to work, podman must be installed in the system. Podman comes out of box with many Linux distributions, mainly Fedora). You can check [their official website](https://podman.io/getting-started/installation) for further instructions.
    - To install podman on Fedora: `sudo dnf install podman`
    - To install podman on Debian and Ubuntu: `sudo apt-get install podman`
    - To install podman on Arch Linux and Manjaro: `sudo pacman -S podman`
    - To install podman on Alpine: `sudo apk add podman`

- Rclone: it's required if you plan to use Rclone. Since it's version 1.58, Rclone is required to get authorization code of a remote. I'm working on a way to use the container to avoid the need to install this package. You can check [their official website](https://rclone.org/install/) for further instructions.
    - To install Rclone on Fedora: `sudo dnf install rclone`
    - To install Rclone on Debian and Ubuntu: `sudo apt-get install rclone`
    - To install Rclone on Arch Linux and Manjaro: `sudo pacman -S rclone`
    - To install Rclone on Alpine: `sudo apk add rclone`

- Python3 and Pip: podarr is an Python application, so it requires the latest version of Python to work. You will also need Pip if you want easily install it.
    - To install Python3 and Pip on Fedora: `sudo dnf install python3 python3-pip`
    - To install Python3 and Pip on Debian and Ubuntu: `sudo apt-get install python3 python3-pip`
    - To install Python3 and Pip on Arch Linux and Manjaro: `sudo pacman -S python python-pip`
    - To install Python3 and Pip on Alpine: `sudo apk add python3 py3-pip`

- When it comes down to podarr itself, as of the Python application, it requires the following Python modules to work, which are automatically installed when installed through Pip:

  - inquirer
  - fastapi
  - uvicorn
  - configobj
  - SQLAlchemy
  - pydantic
  - psutil
  - requests
  - fastapi-utils

If you'd like to see a podarr command to automatically set up the requirements, [let me know](https://github.com/podman-arr/podarr-cli/issues/new).
# Installation
Once requirements are met:

```sh
pip install podarr
```

# Setting up
- Type `podarr install` to choose the desired services and to continue to the installation process. Things should be self explanatory from there. Use space to select services and enter to continue.

![install command screenshot](docs/images/screenshot1.png)

- Type `podarr help` for further instructions.

## Setting up Rclone
Rclone can be used to mount a remote directory locally, allowing it to be used by the other services.

I plan to add more flexibility on how Rclone works inside podarr. For now, the remote directory (/media) has the following structure (safely created during setup):

```
├── backups
└── media
    ├── movies
    ├── music
    └── tv
```

If you choose Rclone during the setup, it will prompt you to configure Rclone. In the processes, it will be asked you to run a Rclone command to get the authorization code, which should be pasted back. I'm working on a way to allow the usage of an existing Rclone config. The config has the following structure and is located at `~/.podarr/rclone/rclone.conf`:

```
[remote]
type = drive
stop_on_download_limit = true
client_id = ...
client_secret = ...
team_drive = ...
scope = drive
token = ...

[remote-crypt]
type = crypt
password = ...
directory_name_encryption = true
filename_encryption = ...
remote = remote:
```
The media directory will be mounted at `~/.podarr/rclone/remote/library`, which will make a part of the MergerFS pool, as explained below.

The Auto Upload service will use Rclone to upload content.

# How it works
All data, settings and container configuration files are stored in the folder `.podarr`, located in the user's home directory:

podarr uses a [MergerFS](https://github.com/trapexit/mergerfs) container to center all files (local or remote) in a single folder: `~/.podarr/data/pool`. Therefore, a MergerFS container will always start prior other services (except Rclone).

For atomic move to work, Radarr, Sonarr and Lidarr requires Remote Path Mappings (planning to automatically set this up):
  - Remote Path: /data/local/usenet/complete/
  - Local Path: /data/pool/usenet/complete/

The containers of all services will have the correct permissions to read or read and write on that directory.

While services are running, user cannot perform write operation on most of `~/.podarr` subdirectories. This happens because the ownership of these folders are given to the user namespace. Once the service is stopped, ownership is revoked back to the user.

# The web service/interface
It's a work in progress.

I'm not good at design. Any help is welcome.

# Works to do
- Futurely, port this application to Rust.
- For now:
  - Allow usage of existing Rclone config.
  - Workaround for SELinux.
  - Perhaps, use Rclone and podman precompiled binaries.
  - Single container with all available services.
  - Bug fixes.