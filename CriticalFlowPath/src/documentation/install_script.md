```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nginx -y

python3 -m venv venv

pip install Flask
pip install pandas
pip install openpyxl
pip install plotly

cd ~/
mkdir CFA_Results_Remote
# vim config/paths.py

```