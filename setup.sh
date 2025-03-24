#!/bin/bash

# Detect OS (Mac or Linux)
OS="$(uname)"

if [[ "$OS" == "Darwin" ]]; then
    echo "Detected macOS. Installing dependencies using Homebrew..."
    # Check if Homebrew is installed
    if ! command -v brew &> /dev/null; then
        echo "Homebrew not found. Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    # Install dependencies using Homebrew
    brew install mecab mecab-ipadic swig
    brew tap homebrew/cask-fonts
    brew install --cask font-ipaexfont # Japanese font

elif [[ "$OS" == "Linux" ]]; then
    echo "Detected Linux. Installing dependencies using apt-get..."
    # Update package list
    sudo apt update
    # Install dependencies using apt
    sudo apt install -y mecab swig libmecab-dev mecab-ipadic-utf8 fonts-ipaexfont

else
    echo "Unsupported OS: $OS"
    exit 1
fi

echo "System dependencies installed successfully!"
