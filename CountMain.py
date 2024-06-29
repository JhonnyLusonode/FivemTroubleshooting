import re
from collections import defaultdict

def remover_codigos_ansi(texto):
    """Remove códigos de escape ANSI do texto."""
    ansi_escape = re.compile(r'(?:\x1B[@-_][0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', texto)

def contar_avisos_por_resource(caminho_arquivo_log):
    # Dicionário para armazenar contagem de avisos por tipo e por resource
    contagem_avisos = defaultdict(lambda: defaultdict(int))

    # Definindo padrões regex para cada tipo de aviso
    padroes_avisos = {
        'could_not_find_file': re.compile(r'Warning: could not find file `(.+?)`'),
        'could_not_find_client_script': re.compile(r'Warning: could not find client_script `(.+?)`'),
        'could_not_find_server_script': re.compile(r'Warning: could not find server_script `(.+?)`'),
        'outdated_manifest': re.compile(r'Warning: (.+?) has an outdated manifest \((.+?)\)'),
        'exists_in_more_than_one_place': re.compile(r'Warning: (.+?) exists in more than one place \((.+?)\)'),
        'no_resource_manifest': re.compile(r'Warning: (.+?) does not have a resource manifest \((.+?)\)'),
        'could_not_find_resource': re.compile(r"Warning: Couldn't find resource (.+?)"),
    }

    with open(caminho_arquivo_log, 'r', encoding='utf-8') as arquivo:
        for linha in arquivo:
            linha_limpa = remover_codigos_ansi(linha)
            for tipo, padrao in padroes_avisos.items():
                if padrao.search(linha_limpa):
                    match = padrao.search(linha_limpa)
                    if match:
                        inicio = linha_limpa.find('[') + 1
                        fim = linha_limpa.find(']')
                        resource_nome = linha_limpa[inicio:fim].strip()
                        mensagem_completa = linha_limpa.strip()
                        contagem_avisos[tipo][mensagem_completa] += 1

    return contagem_avisos

def salvar_resultados(caminho_arquivo_saida, contagem_avisos):
    with open(caminho_arquivo_saida, 'w', encoding='utf-8') as arquivo:
        for tipo_aviso, contagem_por_tipo in contagem_avisos.items():
            arquivo.write(f"[{tipo_aviso}]\n")
            for mensagem_completa, count in contagem_por_tipo.items():
                arquivo.write(f"{mensagem_completa}: {count}\n")
            arquivo.write("\n")

# Caminho para o arquivo de log do FXServer
caminho_arquivo_log = './fxserver.log'
# Caminho para o arquivo de saída
caminho_arquivo_saida = './fxserver_error_output.txt'

# Chamando a função para contar avisos por resource
contagem_avisos = contar_avisos_por_resource(caminho_arquivo_log)

# Salvando os resultados em um novo arquivo
salvar_resultados(caminho_arquivo_saida, contagem_avisos)

# Exibindo mensagem de conclusão
print(f"Contagem de avisos salva em {caminho_arquivo_saida}")
