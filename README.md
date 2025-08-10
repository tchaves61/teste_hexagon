# Painel Interativo de Vendas - AdventureWorks2022

Este projeto é um **painel interativo** desenvolvido em **Python** com **Streamlit**, utilizando a base de dados **AdventureWorks2022** (SQL Server) para explorar e visualizar dados de vendas de forma simples e visual.

---

## 🛠 Pré-requisitos

Antes de começar, você precisa instalar e configurar alguns programas no seu computador.

### 1. Instalar o SQL Server e a base AdventureWorks2022

#### Instalar o SQL Server Developer (gratuito)
- Baixe aqui: [https://www.microsoft.com/pt-br/sql-server/sql-server-downloads](https://www.microsoft.com/pt-br/sql-server/sql-server-downloads)
- Escolha **Developer Edition** (grátis para desenvolvimento).
- Siga a instalação padrão.

#### Baixar e restaurar o AdventureWorks2022
- Baixe o arquivo `.bak` aqui:  
  [https://github.com/Microsoft/sql-server-samples/releases/tag/adventureworks](https://github.com/Microsoft/sql-server-samples/releases/tag/adventureworks)
- Abra o **SQL Server Management Studio (SSMS)** ([download aqui](https://aka.ms/ssmsfullsetup)).
- Clique com o botão direito em **Databases** → **Restore Database**.
  <img width="1273" height="667" alt="Screenshot 2025-08-10 184511" src="https://github.com/user-attachments/assets/06c87483-aeeb-4fed-822b-e0cfd63e19a5" />

- Escolha **Device** → localize o `.bak` baixado.
  <img width="1270" height="666" alt="Screenshot 2025-08-10 184632" src="https://github.com/user-attachments/assets/2f3d7e1f-4270-4a49-87bb-c65f51e170f1" />

- Restaure a base com o nome **AdventureWorks2022**.
  <img width="849" height="649" alt="Screenshot 2025-08-10 184743" src="https://github.com/user-attachments/assets/176b336b-8567-4929-87d7-7d0cbb17dc44" />

---

### 2. Instalar o ODBC Driver 18 (necessário para conectar ao SQL Server)
- Baixe aqui: [https://learn.microsoft.com/pt-br/sql/connect/odbc/download-odbc-driver-for-sql-server](https://learn.microsoft.com/pt-br/sql/connect/odbc/download-odbc-driver-for-sql-server)
- Escolha a versão **ODBC Driver 18 for SQL Server** e instale normalmente.

---

### 3. Instalar o Python
- Baixe o Python 3.10 ou superior aqui: [https://www.python.org/downloads/](https://www.python.org/downloads/)
- Durante a instalação, **marque a opção "Add Python to PATH"**.
- Para confirmar que está instalado, abra o **Prompt de Comando** e digite:
  ```bash
  python --version
  ```
  
---

### 4. 📦 Instalando as bibliotecas
  - Dentro da pasta do projeto, abra o Prompt de Comando e rode:
    ```bash
    pip install streamlit pandas pyodbc sqlalchemy plotly
    ```
  - Isso instalará: <br>
  . Streamlit (interface interativa)<br>
  . Pandas (análise de dados)<br>
  . PyODBC (conexão com SQL Server)<br>
  . Plotly (gráficos)<br>
  
---

### 5. ▶ Rodando o projeto
  - No Prompt de Comando, estando na pasta do projeto:
    ```bash
    python3 -m streamlit run teste_hexagon.py
    ```
  - O navegador abrirá automaticamente. <br>
    Se não abrir, acesse: http://localhost:8501
    
<img width="1274" height="667" alt="Screenshot 2025-08-10 184920" src="https://github.com/user-attachments/assets/bdf5dc8d-75ee-4247-a899-1f296a3252e2" />
<img width="1276" height="669" alt="Screenshot 2025-08-10 184935" src="https://github.com/user-attachments/assets/80e2fc91-9d80-4676-adc2-d55d99c5f21c" />
