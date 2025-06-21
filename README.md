# JupiterUSP Web Scraper

O **JupiterUSP Web Scraper** é uma ferramenta projetada para extrair dados sobre cursos e disciplinas do portal JúpiterWeb da Universidade de São Paulo (USP).

---

## Tecnologias Utilizadas

* **Linguagem:** Python 3
* **Web Scraping:** Selenium
* **Concorrência:** Módulo `concurrent.futures` do Python
* **Navegador:** Google Chrome (controlado pelo ChromeDriver)

---

## Configuração e Instalação

Siga estes passos para configurar e executar o projeto em sua máquina local.

### Pré-requisitos

* Python 3.8 ou superior
* Google Chrome instalado
* `pip` (instalador de pacotes do Python)

### Passos para Instalação

1.  **Clonar o Repositório**
    ```bash
    git clone [https://github.com/theoriffel/JupiterUSP_Webscrap.git](https://github.com/theoriffel/JupiterUSP_Webscrap.git)
    cd JupiterUSP_Webscrap
    ```

2.  **(Recomendado) Criar e Ativar um Ambiente Virtual**

    * No **macOS/Linux**:
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```

    * No **Windows**:
        ```bash
        python -m venv venv
        .\venv\Scripts\activate
        ```

3.  **Instalar as Dependências**
    Instale os pacotes necessários usando o `pip`:
    ```bash
    pip install -r requirements.txt
    ```

---

## Como Usar

Com a configuração concluída, você pode executar a aplicação a partir do diretório raiz do projeto.

### Executando o Scraper

Para iniciar a coleta completa de dados, execute:
```bash
python src/main.py
```

### Limitando a Coleta (para testes)

Você pode fornecer um argumento numérico opcional para limitar o número de unidades acadêmicas a serem processadas. Isso é útil para testes rápidos.

Por exemplo, para coletar dados das **3 primeiras unidades**:
```bash
python src/main.py 3
```

### Interface de Linha de Comando (CLI) Interativa

Após a conclusão do processo de coleta, será apresentado um menu de opções para consultar os dados:

> **Digite a opção de consulta:**
>
> 1) Lista de cursos por unidades
> 2) Dados de um determinado curso
> 3) Dados de todos os cursos
> 4) Dados de uma disciplina (inclusive os cursos dos quais ela faz parte)
> 5) Disciplinas que são compartilhadas entre mais de um curso
> 6) Disciplinas com carga horária superior a 90 horas
> 7) Disciplinas de uma modalidade específica (Obrigatória, Livre ou Eletiva)

Basta digitar o número da opção desejada e pressionar Enter.
