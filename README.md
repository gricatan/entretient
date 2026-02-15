
# Entretien avec Misral AI (Vocal)

## I / Installation

### 1 Fork [https://github.com/gricatan/entretien](https://github.com/gricatan/entretien) → Dans GH, avec *TON_USER_COMPTE*

### 2 En CLI, dans le dossier de ton choix

```bash
Git clone git@github.com:TON_USER-COMPTE/entretien.git
cd entretien
```

### 3 Dans ton .venv : Utilises python3.12 max & installes-y les libs

Exemple pour Win (Adaptes si autre OS !) :

1. Décompresses [https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.zip](https://www.python.org/ftp/python/3.12.10/python-3.12.10-amd64.zip) dans  **C:\Python312\\**

2. Fais ton virtual environment (.VEnv) avec ce 'vieux' Python, upgrades le pip et poses-y les libs utiles

    ```bash
    C:\Python312\python.exe -m venv .venv

    .venv\Scripts\activate

    py -m pip install --upgrade pip

    pip install -r .\requirements
    ```

### 4 Renommes .env_example en .env et renseignes y ton MISTRAL_API_KEY

(Au besoin, génères en une sur [https://console.mistral.ai/codestral/cli?workspace_dialog=apiKeys](https://console.mistral.ai/codestral/cli?workspace_dialog=apiKeys))

## II / Enjoy ! 😊

```bash
python A_SCRIPT.py
```
