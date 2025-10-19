#!/bin/bash

# ==============================
#       Dotfiles Setup Script
# ==============================

set -e  # exit on error

echo "Starting dotfiles setup..."

# ------------------------------
# 1. Install Homebrew (if missing)
# ------------------------------
if ! command -v brew &> /dev/null; then
  echo "Homebrew not found. Installing..."
  /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
  echo "Homebrew already installed."
fi

# ------------------------------
# 2. Install Brewfile packages
# ------------------------------
if [ -f "./Brewfile" ]; then
  echo "Installing Brewfile packages..."
  brew bundle --file=./Brewfile
else
  echo "Brewfile not found!"
fi

# ------------------------------
# 3. Install VSCode extensions
# ------------------------------
if [ -f "./vscode/vscode_extensions.sh" ]; then
  echo "Installing VSCode extensions..."
  ./vscode_extensions.sh
else
  echo "VSCode extensions script not found!"
fi

echo "Dotfiles setup complete!"
