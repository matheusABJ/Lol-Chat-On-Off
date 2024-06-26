import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys
import ctypes

# Função para verificar se o script está sendo executado com privilégios de administrador
def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0

# Função para elevar os privilégios de administrador se necessário
def run_as_admin():
    if not is_admin():
        try:
            script = os.path.abspath(__file__)
            params = ' '.join([script] + sys.argv[1:])
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, f'"{script}"', None, 1
            )
            sys.exit()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao tentar obter privilégios de administrador: {e}")
            sys.exit()

# Função para executar comandos de firewall
def execute_script(option):
    if option == 1:
        commands = [
            'netsh advfirewall firewall add rule name="LoL Chat" dir=out remoteip=172.65.212.1 protocol=TCP action=block',
            'netsh advfirewall firewall add rule name="LoL Chat" dir=out remoteip=2606:4700:90:0:4813:607d:9c17:5972 protocol=TCP action=block'
        ]
        success_message = "Sucesso! As regras foram adicionadas, agora você estará jogando com o chat desativado."
    elif option == 2:
        commands = [
            'netsh advfirewall firewall delete rule name="LoL Chat"'
        ]
        success_message = "Sucesso! As regras foram removidas, agora você estará jogando com o chat ativado."
    else:
        messagebox.showerror("Erro", "Opção inválida.")
        return

    results = []
    for command in commands:
        try:
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                results.append(result.stdout.strip())
            else:
                results.append(result.stderr.strip())
        except Exception as e:
            results.append(str(e))
    
    return "\n".join(results), success_message if len(results) == len(commands) else ""

# Função para lidar com a escolha do usuário
def handle_choice(option):
    result, message = execute_script(option)
    if result:
        messagebox.showinfo("Resultado", result)
    if message:
        messagebox.showinfo("Sucesso", message)

# Verificar e elevar privilégios de administrador antes de criar a interface gráfica
run_as_admin()

# Criação da interface gráfica
def create_gui():
    root = tk.Tk()
    root.title("LOLBR Offline Chat")
    root.geometry("400x300")

    label = tk.Label(root, text="Escolha uma opção:")
    label.pack(pady=10)

    button_block = tk.Button(root, text="Aparecer como invisível (Bloquear Chat)", width=30, command=lambda: handle_choice(1))
    button_block.pack(pady=5)

    button_unblock = tk.Button(root, text="Aparecer como disponível (Ativar Chat)", width=30, command=lambda: handle_choice(2))
    button_unblock.pack(pady=5)

    root.mainloop()

# Criar a interface gráfica
create_gui()
