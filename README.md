# Sympla API Checker

Este aplicativo é uma ferramenta interativa desenvolvida com **Streamlit** para testar a **API Pública da Sympla**. Ele permite que os usuários consultem eventos, verifiquem detalhes como pedidos e participantes, avaliem o tempo de resposta da API e obtenham estatísticas detalhadas sobre as chamadas realizadas.

## 🚀 Funcionalidades

- **Autenticação**: Insira seu token de acesso à API da Sympla para autenticar as requisições.
- **Seleção de Versão da API**: Escolha entre diferentes versões da API (v3 ou v5) para interagir.
- **Busca de Eventos**: Busque e visualize a lista de eventos disponíveis.
- **Detalhes de Eventos**: Consulte pedidos ou participantes específicos de um evento selecionado.
- **Análise de Desempenho**: Visualize gráficos que mostram o tempo de resposta das chamadas à API e o número total de registros obtidos.
- **Download de Dados**: Exporte os dados obtidos em formato CSV para análises futuras.

## 📦 Pré-requisitos

- **Python 3.7 ou superior**: Certifique-se de ter o Python instalado em sua máquina. Você pode baixar a versão mais recente [aqui](https://www.python.org/downloads/).

## 🛠️ Configuração do Ambiente Local

Siga os passos abaixo para configurar e executar o aplicativo localmente:

### 1. Clonar o Repositório

Primeiro, clone este repositório para a sua máquina local:

```
git clone https://github.com/seu-usuario/sympla-api-checker.git
cd sympla-api-checker
```

### 2. Criar um Ambiente Virtual
É recomendado utilizar um ambiente virtual para gerenciar as dependências do projeto. Você pode criar e ativar um ambiente virtual utilizando o venv:

```
python -m venv venv
```

#### Ativar o ambiente virtual

##### No Windows:
```
venv\Scripts\activate
```

##### No macOS e Linux:
```
source venv/bin/activate
```

### 3. Instalar as Dependências
Com o ambiente virtual ativado, instale as dependências necessárias utilizando o arquivo requirements.txt:

```
pip install -r requirements.txt
```
### 4. Executar o Aplicativo Streamlit
Após a instalação das dependências, execute o aplicativo utilizando o Streamlit:
```
streamlit run app.py
```

Observação: Certifique-se de que o arquivo do aplicativo esteja nomeado como app.py. Se estiver com outro nome, substitua app.py pelo nome correto.

### 5. Acessar o Aplicativo
Após executar o comando acima, o Streamlit iniciará o servidor localmente. Abra o navegador e acesse o endereço fornecido, geralmente http://localhost:8501, para interagir com o aplicativo.

## 📄 Uso do Aplicativo
#### Configuração Inicial:

Insira seu Token de Acesso à API no campo correspondente na barra lateral.
Selecione a Versão da API que deseja utilizar (v3 ou v5).

#### Buscar Eventos:

Clique em `📥 Fetch Events` para obter a lista de eventos disponíveis.
Os eventos serão exibidos na aba `📥 Fetch Data`.

#### Consultar Detalhes de Eventos:

Insira o ID do Evento no campo fornecido.
Escolha entre `📦 Check Event Orders` ou `👥 Check Event Participants` para obter detalhes específicos.
Os resultados serão armazenados e exibidos na aba `📊 Results`, juntamente com gráficos de desempenho.

#### Download de Dados:
Utilize os botões de download para exportar os dados obtidos em formato CSV.

## 📝 Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests para melhorar este projeto.