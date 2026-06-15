#!/bin/bash

echo "[*] Checking Python..."

python -m venv venv

echo "[*] Activating virtual environment..."

source venv/Scripts/activate

echo "[*] Upgrading pip..."
python -m pip install --upgrade pip

echo "[*] Installing dependencies..."
pip install -r requirements.txt

echo
echo "[+] Installation complete"
echo "[+] Activate with:"
echo "source venv/Scripts/activate"
echo "[+] Run with:"
echo "python main.py"