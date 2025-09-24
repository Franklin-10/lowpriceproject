from celery import shared_task
import subprocess
import os

@shared_task
def run_scrapy_spider(search_term, search_id):
    """
    Uma tarefa do Celery para iniciar um spider do Scrapy, garantindo o ambiente correto
    e salvando a saída em um arquivo JSON para validação.
    """
    print(f"TASK: Iniciando spider para o termo: {search_term}", flush=True)
    
    # Caminho para a raiz do projeto Django dentro do contêiner
    django_root_path = '/djangoapp'
    # Caminho para a pasta onde o comando 'scrapy crawl' será executado
    scrapy_project_path = os.path.join(django_root_path, 'utils', 'scrapy', 'tutorial')
    
    # Define um nome de arquivo único para cada busca
    output_file = f'output_{search_term.replace(" ", "_")}.json'
    
    # --- Configuração do Ambiente ---
    env = os.environ.copy()
    env['PYTHONPATH'] = f"{django_root_path}:{scrapy_project_path}:{env.get('PYTHONPATH', '')}"
    env['SCRAPY_SETTINGS_MODULE'] = 'tutorial.settings'
    
    spider_name = 'kabum'
    
    # --- Comando para o Scrapy com o output em arquivo ---
    command = [
        'scrapy', 'crawl', spider_name,
        '-a', f'search_term={search_term}',
        '-a', f'search_id={search_id}',
        '-o', output_file, # A flag que salva o arquivo
    ]
    
    # Executa o comando com o ambiente corrigido
    process = subprocess.run(
        command, 
        cwd=scrapy_project_path, 
        capture_output=True, 
        text=True,
        env=env
    )
    
    # Imprime os logs para depuração
    print(f"TASK: Spider finalizado. Código de saída: {process.returncode}", flush=True)
    if process.stdout:
        print("--- Saída Padrão (STDOUT) do Scrapy ---", flush=True)
        print(process.stdout, flush=True)
    if process.stderr:
        print("--- Saída de Erro (STDERR) do Scrapy ---", flush=True)
        print(process.stderr, flush=True)

    if process.returncode == 0:
        return f"Sucesso. Resultados salvos em {output_file}"
    else:
        return "Falha na execução do spider."