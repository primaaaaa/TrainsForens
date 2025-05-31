from ui.user_interface import UserInterface
try:
    from tabulate import tabulate
except ImportError:
    import subprocess
    import sys
    print("📦 Modul 'tabulate' belum terinstal. Menginstal terlebih dahulu...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "tabulate"])
    from tabulate import tabulate



def main():
    ui = UserInterface()
    ui.start()

if __name__ == "__main__":
    main()
