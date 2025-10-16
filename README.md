# Projeto Low Price

Uma aplicação web para comparação de preços entre diferentes plataformas de e-commerce, com rastreamento de preços em tempo real e análise histórica de preços.

## Visão Geral

Low Price é uma aplicação web full-stack que ajuda usuários a encontrar as melhores ofertas online através de:

- Agregação de informações de produtos de múltiplos e-commerces
- Comparação de preços em tempo real
- Capacidade de busca assíncrona com rastreamento de progresso

## Stack de Tecnologias

### Backend (Django)

- Django REST Framework para endpoints da API
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
2. Altere os seletores dentro dos spiders ecommerceA.py e ecommerceB.py

   ```
       SITE_CONFIG = {
           'base_url': "https://yoursite.com.br/search/", # URL de busca de produtos do seu site
           'selectors': {
               'container': 'Your selector CSS here', # Div que engloba todos os seletores filhos que deseja buscar
               'title': "Your selector CSS here", #Selector CSS referente ao titulo/descrição do produto
               'price': "Your selector CSS here::text", #Selector CSS referente ao preço do produto
               'img_data': 'Your selector CSS here::attr(data-src)', #Selector CSS referente ao img_data do produto
               'img_src': 'Your selector CSS here::attr(src)', #Selector CSS referente ao img_src do produto
               'link': "Your selector CSS here::attr(href)", #Selector CSS referente ao link do produto
               "next_page": "Your selector CSS here", #Selector CSS referente ao botão de proóxima página do produto
           }
       }

   ```
3. Inicie o ambiente de desenvolvimento:

   `docker-compose up -d`
4. Acesse as aplicações:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
