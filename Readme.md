# Python Stocks Screener

Stock Screener is an application that displays usefull data about specific stocks.

## Instalation

Create virtual environment 

```bash
python -m venv <venv_name>
```

Activate virtual environment

```bash
source <venv_name>/bin/activate
```

Install requirements

```bash
pip install -r requirements.txt
```
## Usage

Fill company_lists.csv file with the companies symbols you would like to screen for data.

Create key.py file with specific tdameritrade api key, for quering data.

Run 
```python
python stock-screener.py
```

## More features TBD