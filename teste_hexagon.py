import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import sys

# Configurações da página
st.set_page_config(
    page_title="📊 Dashboard de Vendas - AdventureWorks",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados (mantido igual)
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: black;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    .stMetric:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    .stMetric label {
        font-size: 1rem !important;
        color: #ffffff !important;
    }
    .stMetric div {
        font-size: 1.8rem !important;
        font-weight: bold !important;
        color: #ffffff !important;
    }
    .css-1v0mbdj {
        border-radius: 10px;
        overflow: hidden;
    }
    .sidebar .sidebar-content {
        background-color: #2c3e50;
        color: white;
    }
    .st-bq {
        border-radius: 10px;
    }
    .css-1aumxhk {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    /* Ajuste para números muito grandes */
    .stMetric div[data-testid="stMetricValue"] {
        font-size: 1.5rem !important;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }
</style>
""", unsafe_allow_html=True)

# Função para conectar ao banco de dados (versão híbrida)
@st.cache_resource
def conectar_banco():
    # Configurações de conexão (substitua com suas credenciais)
    server = "localhost\\SQLEXPRESS"  # Para cloud, use "seu_servidor.database.windows.net"
    database = "AdventureWorks2022"
    username = None  # Para autenticação Windows local
    password = None  # Para autenticação Windows local
    
    # Se estiver no Cloud, use estas credenciais
    if os.environ.get("IS_CLOUD", "false").lower() == "true":
        username = "seu_usuario_cloud"
        password = "sua_senha_cloud"
    
    try:
        # Tenta pyodbc primeiro (local)
        if os.environ.get("IS_CLOUD", "false").lower() != "true":
            try:
                import pyodbc
                conn = pyodbc.connect(
                    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
                    f"SERVER={server};"
                    f"DATABASE={database};"
                    f"Trusted_Connection=yes;"
                    f"Encrypt=no;"
                )
                st.success("Conectado via pyodbc (ambiente local)")
                return conn
            except Exception as pyodbc_error:
                st.warning(f"pyodbc não disponível, tentando pymssql... ({pyodbc_error})")
        
        # Fallback para pymssql (Cloud)
        import pymssql
        conn = pymssql.connect(
            server=server,
            user=username,
            password=password,
            database=database
        )
        st.success("Conectado via pymssql (ambiente cloud)")
        return conn
        
    except Exception as e:
        st.error(f"Erro na conexão com o banco de dados: {str(e)}")
        return None

# Verifica se está no Cloud (Streamlit Sharing, Heroku, etc.)
if 'HOSTNAME' in os.environ or 'DEPLOY_ENVIRONMENT' in os.environ:
    os.environ['IS_CLOUD'] = "true"

# Restante do seu código (mantido igual a partir daqui)
# Função para carregar os dados com JOINs otimizados
@st.cache_data
def carregar_dados():
    try:
        conn = conectar_banco()
        if conn is None:
            return pd.DataFrame()
            
        query = """
        SELECT 
            soh.SalesOrderID,
            soh.OrderDate,
            soh.TotalDue,
            sp.Name AS StateProvinceName,
            p.Name AS ProductName,
            p.ProductNumber,
            pc.Name AS ProductCategory,
            sod.OrderQty,
            sod.UnitPrice,
            sod.LineTotal,
            YEAR(soh.OrderDate) AS Year,
            MONTH(soh.OrderDate) AS Month,
            FORMAT(soh.OrderDate, 'yyyy-MM') AS YearMonth
        FROM Sales.SalesOrderHeader AS soh
        INNER JOIN Sales.SalesOrderDetail AS sod ON soh.SalesOrderID = sod.SalesOrderID
        INNER JOIN Production.Product AS p ON sod.ProductID = p.ProductID
        INNER JOIN Production.ProductSubcategory AS psc ON p.ProductSubcategoryID = psc.ProductSubcategoryID
        INNER JOIN Production.ProductCategory AS pc ON psc.ProductCategoryID = pc.ProductCategoryID
        INNER JOIN Person.Address AS addr ON soh.ShipToAddressID = addr.AddressID
        INNER JOIN Person.StateProvince AS sp ON addr.StateProvinceID = sp.StateProvinceID
        """
        
        df = pd.read_sql(query, conn)
        df["OrderDate"] = pd.to_datetime(df["OrderDate"])
        return df
        
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()

# Carrega os dados
with st.spinner('Carregando dados do banco de dados...'):
    df = carregar_dados()

if df.empty:
    st.error("Não foi possível carregar os dados. Verifique a conexão com o banco.")
    st.stop()

# SIDEBAR - Filtros
st.sidebar.title("🔍 Filtros Avançados")

# Filtro de data
date_range = st.sidebar.date_input(
    "Selecione o período",
    [df["OrderDate"].min(), df["OrderDate"].max()],
    min_value=df["OrderDate"].min(),
    max_value=df["OrderDate"].max()
)

# Filtro de seleção
with st.sidebar.expander("Filtros de Produto"):
    categorias = st.multiselect(
        "Categorias de Produto",
        df["ProductCategory"].unique(),
        default=df["ProductCategory"].unique()
    )
    produtos = st.multiselect(
        "Produtos",
        df["ProductName"].unique(),
        default=df["ProductName"].unique()
    )

with st.sidebar.expander("Filtros Regionais"):
    regioes = st.multiselect(
        "Estados/Províncias",
        df["StateProvinceName"].unique(),
        default=df["StateProvinceName"].unique()
    )

# Aplica os filtros
if len(date_range) == 2:
    mask = (
        (df["OrderDate"] >= pd.to_datetime(date_range[0])) &
        (df["OrderDate"] <= pd.to_datetime(date_range[1])) &
        (df["ProductCategory"].isin(categorias)) &
        (df["ProductName"].isin(produtos)) &
        (df["StateProvinceName"].isin(regioes))
    )
    df_filtrado = df.loc[mask].copy()
else:
    df_filtrado = df.copy()

# MAIN PAGE
st.title("📊 Dashboard de Vendas - AdventureWorks")

# Formatação de valores para simplicidade
def formatar_valor(valor):
    if valor >= 1_000_000:
        return f"${valor/1_000_000:.1f}M"
    elif valor >= 1_000:
        return f"${valor/1_000:.1f}K"
    else:
        return f"${valor:,.2f}"
    
# KPIs
col1, col2, col3, col4 = st.columns(4)
with col1:
    total_vendas = df_filtrado["LineTotal"].sum()
    st.metric("💰 Total de Vendas", formatar_valor(total_vendas))
    
with col2:
    qtd_pedidos = df_filtrado["SalesOrderID"].nunique()
    st.metric("📦 Pedidos Realizados", f"{qtd_pedidos:,}")
    
with col3:
    ticket_medio = total_vendas / qtd_pedidos if qtd_pedidos > 0 else 0
    st.metric("💳 Ticket Médio", f"${ticket_medio:,.2f}")
    
with col4:
    produtos_unicos = df_filtrado["ProductName"].nunique()
    st.metric("🛍️ Produtos Vendidos", produtos_unicos)

st.markdown("---")

# VISUALIZAÇÕES
tab1, tab2, tab3 = st.tabs(["📈 Análise Temporal", "📊 Análise por Produto", "🗺️ Análise Geográfica"])

with tab1:
    st.subheader("Vendas ao Longo do Tempo")
    
    # Agrupar por período selecionado
    periodo = st.radio(
        "Agrupar por:",
        ["Mês", "Trimestre", "Ano"],
        horizontal=True
    )
    
    if periodo == "Mês":
        group_col = "YearMonth"
    elif periodo == "Trimestre":
        df_filtrado["Quarter"] = df_filtrado["OrderDate"].dt.to_period("Q").astype(str)
        group_col = "Quarter"
    else:
        group_col = "Year"
    
    vendas_tempo = df_filtrado.groupby(group_col)["LineTotal"].sum().reset_index()
    
    fig_tempo = px.line(
        vendas_tempo,
        x=group_col,
        y="LineTotal",
        markers=True,
        labels={"LineTotal": "Total de Vendas ($)", group_col: "Período"},
        height=500
    )
    fig_tempo.update_layout(
        hovermode="x unified",
        xaxis_title=None,
        yaxis_title="Total de Vendas ($)"
    )
    st.plotly_chart(fig_tempo, use_container_width=True)

with tab2:
    st.subheader("Desempenho por Produto")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        top_n = st.slider(
            "Mostrar top N produtos",
            5, 50, 10
        )
        
        vendas_produto = df_filtrado.groupby(["ProductCategory", "ProductName"])["LineTotal"].sum().reset_index()
        vendas_produto = vendas_produto.sort_values("LineTotal", ascending=False).head(top_n)
        
        fig_produto = px.bar(
            vendas_produto,
            x="ProductName",
            y="LineTotal",
            color="ProductCategory",
            labels={"LineTotal": "Total de Vendas ($)", "ProductName": "Produto"},
            height=600
        )
        fig_produto.update_layout(
            xaxis_title=None,
            yaxis_title="Total de Vendas ($)",
            showlegend=True
        )
        st.plotly_chart(fig_produto, use_container_width=True)
    
    with col2:
        st.subheader("Distribuição por Categoria")
        fig_pie = px.pie(
            vendas_produto,
            names="ProductCategory",
            values="LineTotal",
            hole=0.4
        )
        st.plotly_chart(fig_pie, use_container_width=True)

with tab3:
    st.subheader("Desempenho por Região")
    
    vendas_regiao = df_filtrado.groupby("StateProvinceName")["LineTotal"].sum().reset_index()
    vendas_regiao = vendas_regiao.sort_values("LineTotal", ascending=False)
    
    fig_regiao = px.bar(
        vendas_regiao,
        x="StateProvinceName",
        y="LineTotal",
        color="LineTotal",
        labels={"LineTotal": "Total de Vendas ($)", "StateProvinceName": "Estado/Província"},
        height=500
    )
    fig_regiao.update_layout(
        xaxis_title=None,
        yaxis_title="Total de Vendas ($)",
        coloraxis_showscale=False
    )
    st.plotly_chart(fig_regiao, use_container_width=True)

st.markdown("---")

# DADOS BRUTOS
with st.expander("🔍 Visualizar Dados Brutos", expanded=False):
    st.dataframe(
        df_filtrado.sort_values("OrderDate", ascending=False),
        column_config={
            "OrderDate": st.column_config.DatetimeColumn("Data do Pedido"),
            "ProductName": "Produto",
            "StateProvinceName": "Estado/Província",
            "LineTotal": st.column_config.NumberColumn("Total", format="$%.2f")
        },
        hide_index=True,
        use_container_width=True
    )

# FOOTER
st.markdown("""
---
**Dashboard desenvolvido por** Thiago Chaves  
Dados: AdventureWorks 2022 | Última atualização: {}
""".format(datetime.now().strftime("%d/%m/%Y %H:%M")))