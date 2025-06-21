# JupiterUSP_WebscrapJupiterUSP Web Scraper

O JupiterUSP Web Scraper é uma ferramenta projetada para extrair dados sobre cursos e disciplinas do portal JúpiterWeb da Universidade de São Paulo (USP).

Tecnologias Utilizadas
Linguagem: Python 3

Web Scraping: Selenium

Concorrência: Módulo concurrent.futures do Python

Navegador: Google Chrome (controlado pelo ChromeDriver)

## Configuração e Instalação
Siga estes passos para configurar e executar o projeto em sua máquina local.

###  Pré-requisitos
Python 3.8 ou superior

Google Chrome instalado

pip (instalador de pacotes do Python)

Passos para Instalação
Clonar o Repositório

git clone [https://github.com/theoriffel/JupiterUSP_Webscrap.git](https://github.com/theoriffel/JupiterUSP_Webscrap.git)
cd JupiterUSP_Webscrap

(Recomendado) Criar e Ativar um Ambiente Virtual (Virtual Environment)
> No macOS/Linux:

python3 -m venv venv
source venv/bin/activate

> No Windows:

python -m venv venv
.\venv\Scripts\activate

Em seguida, instale os pacotes usando o pip:

pip install -r requirements.txt

## Como Usar
Com a configuração concluída, você pode executar a aplicação a partir do diretório raiz do projeto.

Executando o Scraper

python src/main.py

Limitando a Coleta (para testes)
Você pode fornecer um argumento numérico opcional para limitar o número de unidades acadêmicas a serem coletadas. Isso é útil para testes rápidos. Por exemplo, para coletar apenas as 3 primeiras unidades:

python src/main.py 3

### Interface de Linha de Comando (CLI) Interativa
Após a conclusão do processo de coleta, será apresentado um menu de opções para consultar os dados:

Digite a opção de consulta:
    1) Lista de cursos por unidades
    2) Dados de um determinado curso
    3) Dados de todos os cursos
    4) Dados de uma disciplina, inclusive quais cursos ela faz parte
    5) Disciplinas que são usadas em mais de um curso
    6) Disciplinas com mais de 90 horas de carga horária
    7) Disciplinas de uma modalidade específica (Obrigatória, Livre ou Eletiva)

Digite a opção:
