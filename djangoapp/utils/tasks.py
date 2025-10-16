from celery import shared_task, group
import subprocess
import os
from lowprice.models import Search, SearchSiteStatus
import time


@shared_task
def start_all_requests(search_term, search_id):
    spider_list = ['ecommerceA','ecommerceB']
    for site in spider_list:
        SearchSiteStatus.objects.create(search_id=search_id, site=site, status="PROCESSING")

    print(f"TASK MANAGER: Disparando {len(spider_list)} spiders para a busca ID {search_id}", flush=True)

    job = group(
        run_scrapy_spider.s(search_term, search_id, site) for site in spider_list
    )

    job.apply_async()

    return f"Grupo de {len(spider_list)} spiders iniciado."

@shared_task
def run_scrapy_spider(search_term, search_id, site):
    start_time = time.time()

    """
    Uma tarefa do Celery para iniciar um spider do Scrapy, atualizando o status da busca.
    """
    print(f"TASK: Iniciando spider para o termo: {search_term} (Busca ID: {search_id})", flush=True)

    try:
        search_instance = Search.objects.get(id=search_id)
        search_instance.status = 'PROCESSING'
        search_instance.save()
    except Search.DoesNotExist:
        print(f"TASK: ERRO - Busca com ID {search_id} não encontrada no banco de dados.")
        return f"Falha, busca com ID {search_id} não encontrada."
    
    django_root_path = '/djangoapp'
    scrapy_project_path = os.path.join(django_root_path, 'utils', 'scrapy', 'tutorial')
    output_file = f'output_{search_term.replace(" ", "_")}.json'
    env = os.environ.copy()
    env['PYTHONPATH'] = f"{django_root_path}:{scrapy_project_path}:{env.get('PYTHONPATH', '')}"
    env['SCRAPY_SETTINGS_MODULE'] = 'tutorial.settings'

    spider_name = site
    
    command = [
        'scrapy', 'crawl', spider_name,
        '-s', f'DNSCACHE_ENABLED=True',
        '-a', f'search_term={search_term}',
        '-a', f'search_id={search_id}',
        '-o', output_file,
    ]
    
    process = subprocess.run(
        command, 
        cwd=scrapy_project_path, 
        capture_output=True, 
        text=True,
        env=env
    )
    
    elapsed = time.time() - start_time
    print(f"Tempo de execução: {elapsed}")
    print(f"TASK: Spider finalizado. Código de saída: {process.returncode}", flush=True)
    if process.stdout:
        print("--- Saída Padrão (STDOUT) do Scrapy ---", flush=True)
        print(process.stdout, flush=True)
    if process.stderr:
        print("--- Saída de Erro (STDERR) do Scrapy ---", flush=True)
        print(process.stderr, flush=True)

    if process.returncode == 0:
        print("TASK: Spider terminou com sucesso. Atualizando status para COMPLETED.", flush=True)
        status_obj = SearchSiteStatus.objects.get(search_id=search_id, site=site)
        if status_obj:
            status_obj.status = "COMPLETED"
            status_obj.save()
        else:
            status_obj.status = "FAILED"
            status_obj.save()
        return f"Sucesso. Resultados salvos em {output_file}"
    else:
        print("TASK: Spider terminou com erro. Atualizando status para FAILED.", flush=True)
        search_instance.status = 'FAILED'
        search_instance.save()
        return "Falha na execução do spider."