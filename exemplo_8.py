import pandas as pd
import streamlit as st
import warnings
import matplotlib.pyplot as plt
import uuid

# Ignorar avisos desnecessários
warnings.filterwarnings("ignore", category=UserWarning)

class DashboardProjetos:
    
    def __init__(self):
        self.folder = "./"
        self.arq = "/Dados.xlsm"
        self.df = pd.read_excel(self.folder + self.arq, sheet_name="BASE DE DADOS")
        
        # Categorias com os tipos específicos dentro de cada uma
        self.categorias = {
            "ACESSÓRIO": ["ACESSÓRIO"],
            "CAMINHO MECÂNICO": ["CAMINHO MECÂNICO - PRIMÁRIO", "CAMINHO MECÂNICO - SECUNDÁRIO"],
            "PENETRAÇÕES": ["PENETRAÇÕES - COLAR", "PENETRAÇÕES - ROXTEC"]
        }
        self.areas = {
            'PROA': {'cod': [], 'quant': [], 'liberado': [], 'tipo': [], 'nome': []},
            'POPA': {'cod': [], 'quant': [], 'liberado': [], 'tipo': [], 'nome': []},
            'CASARIA': {'cod': [], 'quant': [], 'liberado': [], 'tipo': [], 'nome': []},
            'COMANDO': {'cod': [], 'quant': [], 'liberado': [], 'tipo': [], 'nome': []},
            'PM': {'cod': [], 'quant': [], 'liberado': [], 'tipo': [], 'nome': []}
        }
        self.selecionar_dados_areas()

    def carregar_css(self):
        st.set_page_config(layout="wide")
        
        with open("style.css") as f:
            css = f.read()

    # Injetando o CSS na aplicação
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

    def exibir_titulo(self):
        st.title("**DASHBOARD DOS PROJETOS**")
    
    def cria_chave(self,code):
        chave = f"{code}_{uuid.uuid4()}"
        return chave
    
    def carregar_imagem_sidebar(self):
        with st.sidebar:
            st.image("./dash.png")

    def selecionar_dados_areas(self):
        for i in range(self.df.shape[0]):
            local = self.df.iloc[i, 6]
            if local in self.areas:
                self.areas[local]['cod'].append(self.df.iloc[i, 0])
                self.areas[local]['quant'].append(self.df.iloc[i, 2])
                self.areas[local]['liberado'].append(self.df.iloc[i, 15])
                self.areas[local]['tipo'].append(self.df.iloc[i, 11])
                self.areas[local]['nome'].append(self.df.iloc[i, 4])
    
    #Modelo para a exibição geral e indiviudal por aba
    def EGG(self,tipos): #EGG -> exibir gráficos gerais
        plt.figure(figsize=(4, 4))
        indices_filtrados = self.df[self.df['ELEMENTO'].isin(tipos)]
        feito_count = sum(indices_filtrados['LIBERADO'] == "FEITO")
        total_count = len(indices_filtrados)
        
        if total_count > 0:
            plt.pie(
                [feito_count, total_count - feito_count],
                labels=['FEITO', ''],
                autopct='%0.0f%%',
                startangle=90,
                textprops={'fontsize': 9},
                wedgeprops=dict(width=0.3)
            )
            #plt.title(f"Status de {cat}")
        else:
            plt.text(0, 0, "Sem dados para exibir", ha='center', fontsize=14)

        st.pyplot(plt)
        plt.close()
    
    #Modelo para o gráfico de acordo com a filtragem: 
    def EGF(self,area,tipos): #EGF -> Exibir Gráficos Filtrados
        plt.figure(figsize=(4, 4))

        # Filtrando elementos por tipos para a área selecionada
        indices_filtrados = [
            i for i, tipo in enumerate(self.areas[area]['tipo']) if tipo in tipos
        ]

        feito_count = sum([self.areas[area]['liberado'][i] == "FEITO" for i in indices_filtrados])
        total_count = len(indices_filtrados)

        if total_count > 0:
            plt.pie(
                [feito_count, total_count - feito_count],
                labels=['FEITO', ''],
                autopct='%0.0f%%',
                startangle=90,
                textprops={'fontsize': 9},
                wedgeprops=dict(width=0.3)
            )
        else:
            plt.text(0, 0, "Sem dados para exibir", ha='center', fontsize=14)

        st.pyplot(plt)
        plt.close()

    def ELA(self,area,cat,ext,cont):
        st.markdown("""
            <style>
            .scrollable-container {
                max-height: 400px;
                overflow-y: auto;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
            }
            </style>
        """, unsafe_allow_html=True)

        st.header(f"**Dados gerais dos {cat}**:")
        opc = []

        if area in self.areas:
            for codigo, status, tipo in zip(self.areas[area]['cod'], self.areas[area]['liberado'], self.areas[area]['tipo']):
            
                if tipo in ext:
                    if status == "FEITO":
                        opc.append(f"{codigo} ✔️")
                    else:
                        opc.append(f"{codigo} ❌")
        

        #codigo_selecionado = st.selectbox(f"{cat}:", opcoes_codigos)
        # Se houver opções, exibir o selectbox
        chave = codigo
        if isinstance(codigo, str):
            chave = 111

        if opc:
            codigo_selecionado = st.selectbox("Selecione um código:", opc,key = chave + cont)
            print(codigo_selecionado)
            if st.button("Mais Informações", key=f"mais_info_{codigo_selecionado}"):
                st.warning(f"Redirecionado para mais informações de {codigo_selecionado}")
                st.markdown("[Clique aqui para mais informações](https://www.seu-site.com/detalhes)", unsafe_allow_html=True)
        cont = cont +1
        return cont

    def ELPCG(self, cat, ext,cont):  #cat -> categoria // ELPCG -> Exibir Lista Para os Códigos Gerais
        st.markdown("""
            <style>
            .scrollable-container {
                max-height: 400px;
                overflow-y: auto;
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
            }
            </style>
        """, unsafe_allow_html=True)

        st.header(f"**Dados gerais dos {cat}**:")

        opcoes_codigos = []

        for i in range(len(self.df)):  
            codigo = self.df.iloc[i, 0]
            status = self.df.iloc[i, 15]
            tipo = self.df.iloc[i, 11]

            if tipo in ext:
                if status == "FEITO":
                    opcoes_codigos.append(f"{codigo} ✔️")
                else:
                    opcoes_codigos.append(f"{codigo} ❌")

        #codigo_selecionado = st.selectbox(f"{cat}:", opcoes_codigos)
    # Se houver opções, exibir o selectbox
        if pd.isna(codigo):
            codigo = 000  # ou qualquer outra string padrão
        if opcoes_codigos:
            codigo_selecionado = st.selectbox("Selecione um código:", opcoes_codigos,key =codigo + cont)
            print(codigo_selecionado)

            if st.button("Mais Informações", key=f"mais_info_{codigo_selecionado}"):
                st.warning(f"Redirecionado para mais informações de {codigo_selecionado}")
                st.markdown("[Clique aqui para mais informações](https://www.seu-site.com/detalhes)", unsafe_allow_html=True)
        cont = cont +1
        return cont
    def exibir_dashboard(self):
        cont = 0
        cont_1 = 1000
        self.carregar_css()
        self.exibir_titulo()
        self.carregar_imagem_sidebar()

        # Inicializa a sessão para controlar se uma área foi selecionada
        if 'selecionou_area' not in st.session_state:
            st.session_state.selecionou_area = False

        # Inicializa a área selecionada no session_state
        if 'area_selecionada' not in st.session_state:
            st.session_state.area_selecionada = None

        # Seletor de área no sidebar
        with st.sidebar:
            if st.button("Geral"):
                st.session_state.selecionou_area = False
                st.session_state.area_selecionada = None  # Reseta a área selecionada ao voltar

            for area in self.areas:
                if st.button(area):
                    st.session_state.selecionou_area = True
                    st.session_state.area_selecionada = area  # Armazena a área selecionada

            

        # Inicializa o estado dos botões de categoria
        if 'button_A' not in st.session_state:
            st.session_state.button_A = False
        if 'button_C' not in st.session_state:
            st.session_state.button_C = False
        if 'button_P' not in st.session_state:
            st.session_state.button_P = False

        # Layout de colunas para dispor os botões de categoria horizontalmente
        with st.container(border=True):
            col1, col2, col3 = st.columns(3)

            # Botão para a categoria ACESSÓRIO
            with col1:
                if st.button("ACESSÓRIO",key="botao_vermelho"):
                    st.session_state.button_A = True
                    st.session_state.button_C = False
                    st.session_state.button_P = False

            # Botão para a categoria CAMINHO MECÂNICO
            with col2:
                if st.button("CAMINHO MECÂNICO"):
                    st.session_state.button_A = False
                    st.session_state.button_C = True
                    st.session_state.button_P = False

            # Botão para a categoria PENETRAÇÕES
            with col3:
                if st.button("PENETRAÇÕES"):
                    st.session_state.button_A = False
                    st.session_state.button_C = False
                    st.session_state.button_P = True

        # Atualiza a área selecionada para exibição
        area_selecionada = st.session_state.area_selecionada

        # Se a categoria ACESSÓRIO estiver selecionada
        if area_selecionada:
            st.header(area_selecionada)
        else:
            st.header("Geral")

        if st.session_state.button_A:
            col4, col5 = st.columns(2)
            with col4:
                if area_selecionada:
                    self.ELA(area_selecionada, "ACESSÓRIO", ["ACESSÓRIO"], cont_1)
                else:
                    self.ELPCG("ACESSÓRIO", ["ACESSÓRIO"], cont)
            with col5:
                if area_selecionada:
                    self.EGF(area_selecionada, ["ACESSÓRIO"])
                else:
                    self.EGG(["ACESSÓRIO"])

        # Se a categoria CAMINHO MECÂNICO estiver selecionada
        elif st.session_state.button_C:
            col6, col7 = st.columns(2)
            with col6:
                if area_selecionada:
                    self.ELA(area_selecionada, "CAMINHO MECÂNICO", ["CAMINHO MECÂNICO - PRIMÁRIO", "CAMINHO MECÂNICO - SECUNDÁRIO"], cont_1)
                else:
                    self.ELPCG("CAMINHO MECÂNICO", ["CAMINHO MECÂNICO - PRIMÁRIO", "CAMINHO MECÂNICO - SECUNDÁRIO"], cont)
            with col7:
                if area_selecionada:
                    self.EGF(area_selecionada, ["CAMINHO MECÂNICO - PRIMÁRIO", "CAMINHO MECÂNICO - SECUNDÁRIO"])
                else:
                    self.EGG(["CAMINHO MECÂNICO - PRIMÁRIO", "CAMINHO MECÂNICO - SECUNDÁRIO"])

        # Se a categoria PENETRAÇÕES estiver selecionada
        elif st.session_state.button_P:
            col8, col9 = st.columns(2)
            with col8:
                if area_selecionada:
                    self.ELA(area_selecionada, "PENETRAÇÕES", ["PENETRAÇÕES - COLAR", "PENETRAÇÕES - ROXTEC"], cont_1)
                else:
                    self.ELPCG("PENETRAÇÕES", ["PENETRAÇÕES - COLAR", "PENETRAÇÕES - ROXTEC"], cont)
            with col9:
                if area_selecionada:
                    self.EGF(area_selecionada, ["PENETRAÇÕES"])
                else:
                    self.EGG(["PENETRAÇÕES - COLAR", "PENETRAÇÕES - ROXTEC"])


# Executar o dashboard
if __name__ == "__main__":
    dashboard = DashboardProjetos()
    dashboard.exibir_dashboard()
