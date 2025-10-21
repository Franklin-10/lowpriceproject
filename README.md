# Projeto Low Price

Uma aplicação web para comparação de preços entre diferentes plataformas de e-commerce, com rastreamento de preços em tempo real.

**⚠️ Aviso Importante**

> Este projeto foi desenvolvido para fins puramente educacionais e como uma demonstração de habilidades técnicas em web scraping e arquitetura de software.
>
> - **Uso Ético:** Nenhum código aqui contido tem a intenção de prejudicar ou sobrecarregar terceiros.
> - **Privacidade:** Em conformidade com as melhores práticas e para evitar o uso indevido, os seletores CSS e configurações específicas de sites-alvo foram omitidos.
> - **Adaptação:** Sinta-se à vontade para utilizar a arquitetura e os spiders como base para seus próprios estudos, aplicando-os a um site de sua escolha.

## Visão Geral

Low Price é uma aplicação web full-stack que ajuda usuários a encontrar as melhores ofertas online através de:

- Agregação de informações de produtos de múltiplos e-commerces
- Comparação de preços em tempo real
- Capacidade de busca assíncrona com rastreamento de progresso

## Stack de Tecnologias

### Backend (Django)

- Django para endpoints da API
- Celery para processamento assíncrono de tarefas
- Scrapy para web scraping
- PostgreSQL para persistência de dados

### Frontend (React)

- Vite como ferramenta de build
- CSS Modules para estilização
- Hooks customizados para busca de dados
- Arquitetura baseada em componentes

### Infraestrutura

- Docker e Docker Compose para containerização
- Nginx para deploy em produção

## Estrutura do Projeto

```
.
├── djangoapp/
│   ├── lowprice/           # Aplicação principal Django
│   │   ├── models.py       # Modelos do banco de dados
│   │   ├── views.py        # Views da API
│   │   └── urls.py         # Roteamento de URLs
│   ├── utils/
│   │   ├── tasks.py        # Tarefas Celery
│   │   └── scrapy/         # Spiders para web scraping
│   └── project/            # Configurações do projeto Django
│
├── reactapp/
│   ├── src/
│   │   ├── Components/     # Componentes React
│   │   ├── Hooks/         # Hooks customizados
│   │   └── Helper/        # Componentes utilitários
│   └── docker-compose.yml # Orquestração container react
│   └── public/            # Arquivos estáticos
│
└── docker-compose.yml     # Orquestração de containers
```

## Instalação e Configuração

### Pré-requisitos

- Docker e Docker Compose
- Git

### Configuração de Desenvolvimento

1. Clone o repositório:

   ```bash
   git clone https://github.com/Franklin-10/lowpriceproject.git
   cd lowpriceproject
   ```
2. Adicione e configure seu .env conforme exemplo dentro de [dotenv_files](https://github.com/Franklin-10/lowpriceproject/tree/main/dotenv_files)
3. Altere os seletores dentro dos spiders [ecommerceA.py](https://github.com/Franklin-10/lowpriceproject/blob/main/djangoapp/utils/scrapy/tutorial/tutorial/spiders/ecommerceA.py) e [ecommerceB](https://github.com/Franklin-10/lowpriceproject/blob/main/djangoapp/utils/scrapy/tutorial/tutorial/spiders/ecommerceB.py)
   **ATENÇÃO** devido a políticas de privacidade, não estarei colocando os códigos aqui, mas você é livre pra procurar e achar um site que se encaixe.

   ```
   SITE_CONFIG = {
           'base_url': "https://yoursite.com.br/search/{}", # URL de busca de produtos do seu site
           'selectors': {
               # Os seletores que deseja buscar preencha ex: li.identificador
               'container': 'Your selector CSS here', 
               'title': "Your selector CSS here::text", #Selector CSS referente ao titulo/descrição do produto
               'price': "Your selector CSS here::text", #Selector CSS referente ao preço do produto
               'img_src': 'Your selector CSS here::attr(src)', #Selector CSS referente ao img_src do produto
               'link': "Your selector CSS here::attr(href)", #Selector CSS referente ao link do produto
               "next_page": "Your selector CSS here", #Selector CSS referente ao botão de proóxima página do produto
           }
       }
   ```
4. Inicie o ambiente de desenvolvimento:

   `docker-compose up --build`
5. Acesse as aplicações:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000

## Dicas para uso do projeto

### Tracer

1. Use o **Trace** para visualizar como o seu scraper esta atuando nos sites se esta pegando os seletores corretamente, onde esta parando com algum erro etc. economiza muito tempo! Dê uma olhada no [ecommerceB](https://github.com/Franklin-10/lowpriceproject/blob/main/djangoapp/utils/scrapy/tutorial/tutorial/spiders/ecommerceB.py) como exemplo.
   * Ative o trace dentro do seu scrapper

```python
Coloque no inicio da função parse:
await page.context.tracing.start(screenshots=True, snapshots=True, sources=True)

Coloque no finally da mesma função:
await page.context.tracing.stop(path=f"trace.zip")
```

2. Copie o arquivo .zip do seu docker após você realizar a busca do produto

  ``docker-compose cp djangoapp:djangoapp//utils/scrapy/tutorial/trace.zip .\trace.zip``

3. Pra não precisar instalar as dependencias em um venv no seu computador local, recomendo rodar
   neste site próprio do Playwright Trace, só realizar o upload do seu trace.zip nesse site [Playwright Trace](https://trace.playwright.dev/)

### Console(web browser)

1. Quando você realizar a busca deixei o retorno no console.log do fetch do ***resultsData** * , possibilitando visualização dos retorno dos produto

   ![Retorno console web](reactapp/src/assets/console_web.png)
