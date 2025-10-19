#!/bin/bash
echo "Installing VSCode extensions..."

extensions=(
  # --- Git / GitHub ---
  "eamodio.gitlens"
  "github.copilot"
  "github.remotehub"

  # --- Programming Languages ---
  "golang.go"
  "hashicorp.terraform"
  "ms-python.python"
  "redhat.java"

  # --- Productivity / Editor Enhancements ---
  "bradlc.vscode-tailwindcss"
  "dsznajder.es7-react-js-snippets"
  "mechatroner.rainbow-csv"
  "pkief.material-icon-theme"
  "pomdtr.excalidraw-editor"
  "rslfrkndmrky.rsl-vsc-focused-folder"
  "tamasfe.even-better-toml"
  "technosophos.vscode-make"
  "vscodevim.vim"
  "wholroyd.jinja"
  "yzhang.markdown-all-in-one"

  # --- Kubernetes / Cloud ---
  "docker.docker"
  "ms-kubernetes-tools.vscode-kubernetes-tools"

  # --- Jupyter / Python Data Science ---
  "ms-toolsai.jupyter"
)

for ext in "${extensions[@]}"; do
  code --install-extension "$ext" || echo "Failed to install $ext"
done

echo "VSCode extensions installed!"
