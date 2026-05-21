import os
import shutil
import ctypes
import sys

def is_admin():
    """Verifica se o script está rodando como Administrador."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def limpar_pasta(caminho_pasta, nome_etapa):
    """Remove todos os arquivos e pastas de um diretório específico."""
    print(f"\n[+] Iniciando limpeza: {nome_etapa}...")
    if not os.path.exists(caminho_pasta):
        print(f"[-] Caminho não encontrado ou não aplicável: {caminho_pasta}")
        return

    sucesso = 0
    falha = 0

    for item in os.listdir(caminho_pasta):
        caminho_completo = os.path.join(caminho_pasta, item)
        try:
            if os.path.isfile(caminho_completo) or os.path.islink(caminho_completo):
                os.unlink(caminho_completo)
            elif os.path.isdir(caminho_completo):
                shutil.rmtree(caminho_completo)
            sucesso += 1
        except Exception:
            # Arquivos em uso pelo sistema ou navegadores abertos serão ignorados
            falha += 1
            continue
            
    print(f"-> {nome_etapa} concluído. Itens limpos: {sucesso} | Itens em uso (ignorados): {falha}")

def main():
    if not is_admin():
        print("[!] ERRO: Este script PRECISA ser executado como Administrador.")
        print("Por favor, abra o Prompt de Comando/PowerShell como Administrador e execute o script.")
        input("\nPressione Enter para sair...")
        sys.exit()

    user_profile = os.environ.get("USERPROFILE")
    local_app_data = os.environ.get("LOCALAPPDATA")
    app_data = os.environ.get("APPDATA")

    caminhos_sistema = {
        "Temp (%temp%)": os.environ.get("TEMP"),
        "System Temp": os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "Temp"),
        "Prefetch": os.path.join(os.environ.get("SystemRoot", "C:\\Windows"), "Prefetch")
    }

                                         #caminhos de Cache dos Navegadores
    caminhos_navegadores = {
        "Google Chrome (Cache)": os.path.join(local_app_data, r"Google\Chrome\User Data\Default\Cache\Cache_Data"),
        "Mozilla Firefox (Cache)": os.path.join(local_app_data, r"Mozilla\Firefox\Profiles")
    }

    print("=== INICIANDO Linpeza NO WINDOWS ===")
    for nome, caminho in caminhos_sistema.items():
        if caminho:
            limpar_pasta(caminho, nome)

    print("\n=== INICIANDO LIMPEZA DOS NAVEGADORES ===")
    
    limpar_pasta(caminhos_navegadores["Google Chrome (Cache)"], "Google Chrome (Cache)")

    ff_base_path = caminhos_navegadores["Mozilla Firefox (Cache)"]
    if os.path.exists(ff_base_path):
        print("[+] Buscando perfis do Firefox...")
        for perfil in os.listdir(ff_base_path):
            caminho_cache_ff = os.path.join(ff_base_path, perfil, "cache2")
            if os.path.exists(caminho_cache_ff):
                limpar_pasta(caminho_cache_ff, f"Firefox Cache (Perfil: {perfil})")
    else:
        print("[-] Firefox não instalado ou caminho não encontrado.")

    print("\n=== FAXINA CONCLUÍDA COM SUCESSO! ===")
    input("\nPressione Enter para fechar...")

if __name__ == "__main__":
    main()