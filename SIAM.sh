#!/bin/bash
clear
echo -e "\e[1;36m=== SIAM CODEX AUTOMATIC SERVER INSTALLER ===\e[0m"

pkg update -y && pkg install python git -y
pip install flask flask-cors requests

mkdir -p $HOME/siam_server_hub
cd $HOME/siam_server_hub

curl -sL -o main.py https://raw.githubusercontent.com/Siam-codex/Siam-Codex-info-ban-web/refs/heads/main/main.py

mkdir -p $TMPDIR/shm
export TMPDIR=$TMPDIR/shm

python main.py
