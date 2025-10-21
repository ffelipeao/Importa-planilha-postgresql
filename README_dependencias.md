# 📦 Instalação de Dependências - Importa-planilha-postgresql

Este projeto requer várias bibliotecas Python para funcionar corretamente. Siga as instruções abaixo para instalar todas as dependências.

## 🚀 Instalação Rápida

### Instalação Direta (Não Recomendado)
```bash
pip install -r requirements.txt
```

### Instalação com Ambiente Virtual (Recomendado)
```bash
# Criar ambiente virtual com virtualenv
virtualenv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

Veja as seções específicas para [Windows](#-instalação-no-windows) e [Linux](#-instalação-no-linux) abaixo.

## 📋 Dependências Principais

| Biblioteca | Versão | Descrição |
|------------|--------|-----------|
| `pandas` | >=1.5.0 | Manipulação de dados e planilhas |
| `psycopg2-binary` | >=2.9.0 | Conexão com PostgreSQL |
| `python-dotenv` | >=0.19.0 | Gerenciamento de variáveis de ambiente |
| `unidecode` | >=1.3.0 | Processamento de caracteres especiais |
| `chardet` | >=4.0.0 | Detecção de codificação de arquivos |
| `geopandas` | >=0.12.0 | Dados geoespaciais |
| `gdal` | >=3.4.0 | Geoprocessamento |
| `openpyxl` | >=3.0.0 | Manipulação de arquivos Excel |

## 🔧 Dependências de Desenvolvimento (Opcional)

Para desenvolvimento e testes, você pode instalar dependências adicionais:
```bash
pip install -r requirements-dev.txt
```

**Nota**: O arquivo `requirements-dev.txt` inclui todas as dependências principais mais ferramentas de desenvolvimento como pytest, black, flake8, mypy, sphinx e jupyter.

## ⚠️ Requisitos do Sistema

- **Python**: 3.8 ou superior (recomendado 3.9+)
- **PostgreSQL**: 12 ou superior
- **Sistema Operacional**: Windows, Linux ou macOS

## 🪟 Instalação no Windows

### Opção 1: Usando virtualenv (Recomendado)

```powershell
# 1. Instalar virtualenv (se não tiver)
pip install virtualenv

# 2. Criar ambiente virtual
virtualenv venv

# 3. Ativar ambiente virtual
venv\Scripts\activate

# 4. Atualizar pip
python -m pip install --upgrade pip

# 5. Instalar dependências
pip install -r requirements.txt

# 6. Para desativar o ambiente virtual (quando terminar)
deactivate
```

### Opção 2: Usando venv

```powershell
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar ambiente virtual
venv\Scripts\activate

# 3. Atualizar pip
python -m pip install --upgrade pip

# 4. Instalar dependências
pip install -r requirements.txt

# 5. Para desativar o ambiente virtual (quando terminar)
deactivate
```

### Opção 3: Usando conda

```powershell
# 1. Criar ambiente virtual com conda
conda create -n projeto_postgresql python=3.9

# 2. Ativar ambiente virtual
conda activate projeto_postgresql

# 3. Instalar dependências principais
pip install -r requirements.txt

# 4. Instalar GDAL via conda (recomendado para Windows)
conda install gdal

# 5. Para desativar o ambiente virtual
conda deactivate
```

## 🐧 Instalação no Linux

### Opção 1: Usando virtualenv (Recomendado)

```bash
# 1. Instalar virtualenv (se não tiver)
pip3 install virtualenv

# 2. Criar ambiente virtual
virtualenv venv

# 3. Ativar ambiente virtual
source venv/bin/activate

# 4. Atualizar pip
python -m pip install --upgrade pip

# 5. Instalar dependências do sistema (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3-dev libpq-dev gdal-bin libgdal-dev

# 6. Instalar dependências Python
pip install -r requirements.txt

# 7. Para desativar o ambiente virtual
deactivate
```

### Opção 2: Usando venv

```bash
# 1. Criar ambiente virtual
python3 -m venv venv

# 2. Ativar ambiente virtual
source venv/bin/activate

# 3. Atualizar pip
python -m pip install --upgrade pip

# 4. Instalar dependências do sistema (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install python3-dev libpq-dev gdal-bin libgdal-dev

# 5. Instalar dependências Python
pip install -r requirements.txt

# 6. Para desativar o ambiente virtual
deactivate
```

### Opção 3: Usando conda

```bash
# 1. Criar ambiente virtual com conda
conda create -n projeto_postgresql python=3.9

# 2. Ativar ambiente virtual
conda activate projeto_postgresql

# 3. Instalar dependências principais
pip install -r requirements.txt

# 4. Instalar GDAL via conda
conda install gdal

# 5. Para desativar o ambiente virtual
conda deactivate
```

### Dependências do Sistema (Linux)

#### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install python3-dev libpq-dev gdal-bin libgdal-dev
```

#### CentOS/RHEL/Fedora:
```bash
sudo yum install python3-devel postgresql-devel gdal gdal-devel
# ou para versões mais recentes:
sudo dnf install python3-devel postgresql-devel gdal gdal-devel
```

#### Arch Linux:
```bash
sudo pacman -S python python-pip postgresql-libs gdal
```

## 🔧 Gerenciamento de Ambientes Virtuais

### Comandos Úteis

#### Listar ambientes virtuais:
```bash
# Para virtualenv/venv
ls venv/

# Para conda
conda env list
```

#### Remover ambiente virtual:
```bash
# Para virtualenv/venv
rm -rf venv/  # Linux/macOS
rmdir /s venv  # Windows

# Para conda
conda env remove -n projeto_postgresql
```

#### Atualizar dependências no ambiente virtual:
```bash
# Ativar ambiente primeiro
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Depois atualizar
pip install --upgrade -r requirements.txt
```

## 🐛 Solução de Problemas

### Problemas com Ambiente Virtual

#### Ambiente não ativa:
```bash
# Verificar se o Python está instalado
python --version
python3 --version

# Recriar ambiente virtual
rm -rf venv/
virtualenv venv
```

#### Erro de permissão no Windows:
```powershell
# Executar PowerShell como Administrador
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Erro com GDAL

#### Windows:
```bash
# Instale via conda (recomendado)
conda install gdal

# Ou baixe os binários pré-compilados
pip install GDAL-3.4.0-cp39-cp39-win_amd64.whl
```

#### Linux:
```bash
# Instalar dependências do sistema primeiro
sudo apt-get install gdal-bin libgdal-dev

# Depois instalar via pip
pip install gdal
```

### Erro com psycopg2
```bash
# Use a versão binary
pip install psycopg2-binary

# Ou instale dependências do sistema (Linux)
sudo apt-get install libpq-dev
pip install psycopg2
```

### Problemas de Permissão
```bash
# Use --user para instalar apenas para o usuário atual
pip install --user -r requirements.txt

# Ou use ambiente virtual (recomendado)
virtualenv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Problemas com pandas/openpyxl
```bash
# Atualizar pip primeiro
python -m pip install --upgrade pip

# Instalar dependências uma por uma
pip install pandas
pip install openpyxl
pip install xlsxwriter
```

## 📁 Estrutura de Arquivos

```
projeto/
├── requirements.txt          # Dependências principais
├── requirements-dev.txt      # Dependências de desenvolvimento (opcional)
└── README_dependencias.md    # Este arquivo
```

## ✅ Verificação da Instalação

### Verificação Básica
```python
# Teste básico
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import geopandas as gpd

print("✅ Todas as dependências foram instaladas com sucesso!")
```

### Verificação Completa
```python
# Teste completo com versões
import pandas as pd
import psycopg2
from dotenv import load_dotenv
import geopandas as gpd
import numpy as np
import unidecode
import chardet
import openpyxl

print("📋 Versões das bibliotecas instaladas:")
print(f"  pandas: {pd.__version__}")
print(f"  psycopg2: {psycopg2.__version__}")
print(f"  geopandas: {gpd.__version__}")
print(f"  numpy: {np.__version__}")
print(f"  openpyxl: {openpyxl.__version__}")
print("✅ Todas as dependências foram instaladas com sucesso!")
```

### Script de Verificação Automática
Crie um arquivo `teste_instalacao.py`:
```python
#!/usr/bin/env python3
"""
Script para verificar se todas as dependências estão instaladas corretamente
"""

def testar_dependencias():
    dependencias = [
        'pandas',
        'psycopg2',
        'dotenv',
        'geopandas',
        'numpy',
        'unidecode',
        'chardet',
        'openpyxl'
    ]
    
    print("🔍 Verificando dependências...")
    print("=" * 50)
    
    for dep in dependencias:
        try:
            if dep == 'dotenv':
                import dotenv
                print(f"✅ {dep}: OK")
            else:
                __import__(dep)
                print(f"✅ {dep}: OK")
        except ImportError as e:
            print(f"❌ {dep}: FALHOU - {e}")
    
    print("=" * 50)
    print("🎉 Verificação concluída!")

if __name__ == "__main__":
    testar_dependencias()
```

Execute o teste:
```bash
python teste_instalacao.py
```

## 🔄 Atualização de Dependências

Para atualizar todas as dependências:
```bash
pip install --upgrade -r requirements.txt
```

Para atualizar apenas uma dependência específica:
```bash
pip install --upgrade nome_da_biblioteca
```

## 📞 Suporte

Se encontrar problemas na instalação:
1. Verifique a versão do Python: `python --version`
2. Atualize o pip: `python -m pip install --upgrade pip`
3. Verifique se há conflitos: `pip check`
4. Consulte a documentação específica de cada biblioteca
