#!/bin/bash

# ১. টাইপিং অ্যানিমেশন ফাংশন
type_effect() {
    local text="$1"
    local delay=0.03
    for ((i=0; i<${#text}; i++)); do
        echo -n "${text:$i:1}"
        sleep $delay
    done
    echo ""
}

# ২. লোডিং স্পিনার অ্যানিমেশন ফাংশন
loading_spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

clear

# ৩. কমান্ড স্টার্ট অ্যানিমেশন
echo -e "\e[1;36m==================================================\e[0m"
type_effect "  👑 🔥 WELCOME TO SIAM CODEX SERVER SYSTEM 🔥 👑  "
echo -e "\e[1;36m==================================================\e[0m"
sleep 0.5

echo -e "\n\e[1;33m[+] Initializing installer components...\e[0m"
sleep 1

# ৪. রিকোয়ারমেন্ট ইনস্টল অ্যানিমেশন (হিজিবিজি লেখা হাইড করে লোডিং দেখাবে)
echo -n -e "\e[1;32m[+] Installing dependencies & Python packages...\e[0m"
(
    pkg update -y && pkg install python git -y
    pip install flask flask-cors requests
) > /dev/null 2>&1 &

loading_spinner $!
echo -e "\e[1;32m [ DONE ]\e[0m"

# ৫. প্রজেক্ট সেটআপ
echo -n -e "\e[1;32m[+] Creating secure workspace...\e[0m"
mkdir -p $HOME/siam_server_hub
cd $HOME/siam_server_hub
sleep 1
echo -e "\e[1;32m [ DONE ]\e[0m"

echo -n -e "\e[1;32m[+] Fetching main.py from GitHub...\e[0m"
curl -sL -o main.py https://raw.githubusercontent.com/Siam-codex/Siam-Codex-info-ban-web/refs/heads/main/main.py &
loading_spinner $!
echo -e "\e[1;32m [ DONE ]\e[0m"

# ৬. সার্ভার বুট অ্যানিমেশন
echo -e "\n\e[1;35m[*] Booting up the intelligence core...\e[0m"
mkdir -p $TMPDIR/shm
export TMPDIR=$TMPDIR/shm
sleep 1.5

# সার্ভার রান
python main.py
