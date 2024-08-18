@echo off

IF EXIST venv GOTO :EXISTS
python -m venv venv
:EXISTS

call venv\Scripts\activate
pip install -r requirements.txt

flask run
