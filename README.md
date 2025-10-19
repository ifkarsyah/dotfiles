# Ifkarsyah Dotfiles

This repository contains my personal configuration files (dotfiles) for various development tools and environments. It is designed to be portable and easy to set up on new machines.

## References: 
- [The Developer’s Guide to Dot Files](https://mskadu.medium.com/the-developers-guide-to-dot-files-versioning-your-development-environment-a4b642216680)
- ChatGPT

## Structures
```
dotfiles/
├── git/           # gitconfig, gitignore, etc.
├── shell/         # bashrc, zshrc, aliases
├── vim/           # vimrc, plugins
├── vscode/        # settings.json, extensions list
├── ssh/           # config, keys (optional)
├── docker/        # config.json
└── README.md
```

Each folder contains configuration files arranged so that the paths **mirror their target locations** in your home directory.

---

## Installation

### 1. Install GNU Stow

```bash
brew install stow
```
### 2. Install this Repo
```bash
git clone https://github.com/ifkarsyah/dotfiles.git ~/dotfiles
cd ~/dotfiles
```

### 3. Brew
If you don't have Homebrew installed, run:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
Then, install the packages listed in the Brewfile:
```bash
cd ~/dotfiles
brew bundle --file=Brewfile
```
✅ This will install all packages, casks, and taps listed in the Brewfile automatically.

Whenever you install a new package, update the Brewfile:
```bash
brew bundle dump --file=~/dotfiles/Brewfile --force
```
Commit the updated Brewfile to your repo.

### 4. Stow your dotfiles
```bash
stow git
stow shell
stow vim
stow vscode
stow ssh
stow docker
```

✅ This will create symlinks in your home directory pointing to the files in this repository.

For example:
```bash
~/.gitconfig -> ~/dotfiles/git/.gitconfig
~/.zshrc -> ~/dotfiles/shell/.zshrc
~/.vimrc -> ~/dotfiles/vim/.vimrc
~/Library/Application Support/Code/User/settings.json -> ~/dotfiles/vscode/Library/Application Support/Code/User/settings.json
~/.ssh/config -> ~/dotfiles/ssh/.ssh/config
~/.docker/config.json -> ~/dotfiles/docker/.docker/config.json
```

If you want to remove the symlinks created by Stow:
```bash
stow -D git
stow -D vim
```
This removes the symlinks without touching the repository files.