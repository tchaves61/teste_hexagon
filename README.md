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
<img width="1280" height="659" alt="Screenshot 2025-08-06 190654" src="https://github.com/user-attachments/assets/82de0e31-e938-4e71-a4ce-f1435d3ae51b" />

- Clique com o botão direito em **Banco de Dados** → **Restaurar Banco de Dados**.
<img width="1273" height="667" alt="Screenshot 2025-08-10 184511" src="https://github.com/user-attachments/assets/03b288b3-2055-4c72-860e-9eb15a131f60" />

- Escolha **Dispositivo** → localize o `.bak` baixado.
<img width="1270" height="666" alt="Screenshot 2025-08-10 184632" src="https://github.com/user-attachments/assets/cac24043-115e-43ec-97e1-2cd1bdf3dbe7" />

- Restaure a base com o nome **AdventureWorks2022**.
<img width="849" height="649" alt="Screenshot 2025-08-10 184743" src="https://github.com/user-attachments/assets/7692416c-7f24-4fdf-8e8a-fb1a2375e0b2" />


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

  <img width="1274" height="667" alt="Screenshot 2025-08-10 184920" src="https://github.com/user-attachments/assets/11c1ec0a-a885-4fb9-ae61-6d6cb3350ea0" />
  <img width="1276" height="669" alt="Screenshot 2025-08-10 184935" src="https://github.com/user-attachments/assets/2125a59f-14c2-435c-b0b8-83430519aa08" />

