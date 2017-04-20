#!/usr/bin/env python
import argparse
import glob
import socket
from subprocess import call

def merge_files(output, patterns=[], comment="#"):
    filenames = []
    for pattern in patterns:
        filenames.extend(glob.glob(pattern))

    open(output, 'w').close()
    config = open(output, 'a')

    config.write("{}\n{} Combined using github.com/laxd/dotfiles setup\n{}\n".format(comment*40, comment, comment*40))

    for file_name in filenames:
        file = open(file_name, "r")
        config.write("\n{} {} {}\n\n".format(comment*15, file.name, comment*15))
        config.write(file.read())
        file.close()

    config.close()

def is_installed(package):
    return not call(["pacman", "-Qs", "^{}$".format(package)])

packages=["git", "binutils", "gcc", "make", "fakeroot", "tmux", "i3", "xscreensaver", "newsbeuter", "rxvt-unicode", "urxvt-perls", "scrot", "feh", "base-devel", "expac", "sysstat", "imagemagick", "xautolock", "dex", "zsh"]

parser = argparse.ArgumentParser()
parser.add_argument("-A", "--all", help="Perform a full setup including ALL options", action="store_true")
parser.add_argument("-a", "--aur", help="Install AUR packages", action="store_true")
parser.add_argument("-c", "--confirm", help="Confirm actions", action="store_true")
parser.add_argument("-d", "--dotfiles", help="Symlink dotfiles", action="store_true")
parser.add_argument("-f", "--force", help="Overwrite files, even if they exist", action="store_true")
parser.add_argument("-P", "--install-pacaur", help="Install pacaur", action="store_true")
parser.add_argument("-i", "--configure-i3", help="Configure i3", action="store_true")
parser.add_argument("-m", "--configure-mutt", help="Configure Mutt", action="store_true")
parser.add_argument("-p", "--install-packages", help="Install packages", action="store_true")
parser.add_argument("-v", "--verbose", help="Increase logging", action="store_true")
parser.add_argument("-w", "--wallpapers", help="Copy wallpapers", action="store_true")
args = parser.parse_args()

if args.configure_i3:
    print("Configuring i3")
    merge_files(".config/i3/config", [".config/i3/*-all.config", ".config/i3/*-{}.config".format(socket.gethostname())])

if args.install_packages:
    print("Installing packages")
    install_targets = [package for package in packages if not is_installed(package)]

    if install_targets:
        print("Found packages to install: {}".format(", ".join(install_targets)))
        call(["sudo", "pacman", "--noconfirm", "-S"] + install_targets)

print("Done!")