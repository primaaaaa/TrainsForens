import os
from system.train_ticket_system import TrainTicketSystem
import datetime
import json
from tabulate import tabulate

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_separator(char='-', length=50):
    print(char * length)

def print_header(text):
    print_separator()
    print(f"{text:^50}")
    print_separator()

def pause():
    input("\nTekan Enter untuk melanjutkan...")

class UserInterface:
    def __init__(self):
        self.system = TrainTicketSystem()
    
    def start(self):
        while True:
            self.show_login_menu()
            
            if self.system.is_admin:
                self.show_admin_menu()
            elif self.system.current_user:
                self.show_user_menu()
    
    def show_login_menu(self):
        while not self.system.current_user:
            clear_screen()
            print_header(r"""
 ______  ____    ____  ____  ____   _____ _____   ___   ____     ___  ____   _____
|      ||    \  /    ||    ||    \ / ___/|     | /   \ |    \   /  _]|    \ / ___/
|      ||  D  )|  o  | |  | |  _  (   \_ |   __||     ||  D  ) /  [_ |  _  (   \_ 
|_|  |_||    / |     | |  | |  |  |\__  ||  |_  |  O  ||    / |    _]|  |  |\__  |
  |  |  |    \ |  _  | |  | |  |  |/  \ ||   _] |     ||    \ |   [_ |  |  |/  \ |
  |  |  |  .  \|  |  | |  | |  |  |\    ||  |   |     ||  .  \|     ||  |  |\    |
  |__|  |__|\_||__|__||____||__|__| \___||__|    \___/ |__|\_||_____||__|__| \___|
                                                                                  
"""
)
            print("1. 🔐 Login")
            print("2. 📝 Register (Pelanggan)")
            print("0. 🔙 Keluar")

            print_separator()
            
            choice = input("Pilih menu (0-2): ")
            
            if choice == "1":
                self.login()
            elif choice == "2":
                self.register()
            elif choice == "0":
                print("Terima kasih telah menggunakan sistem ini.")
                exit(0)
            else:
                print("Input tidak valid!")
                pause()
    
    def login(self):
        clear_screen()
        print_header("LOGIN")
        username = input("Username: ")
        password = input("Password: ")
        
        if self.system.login(username, password):
            print(f"\nLogin berhasil! Selamat datang, {username}!")
            if self.system.is_admin:
                print("Anda login sebagai ADMIN")
            else:
                print("Anda login sebagai PELANGGAN")
            pause()
        else:
            print("\nUsername atau password salah!")
            pause()
    
    def register(self):
        clear_screen()
        print_header("REGISTRASI PELANGGAN")
        username = input("Username: ")
        password = input("Password: ")
        
        if self.system.register(username, password):
            print("\nRegistrasi berhasil! Silakan login.")
            pause()
        else:
            print("\nUsername sudah digunakan!")
            pause()
    
    def show_admin_menu(self):
        while self.system.current_user and self.system.is_admin:
            clear_screen()
            print(r"""
 ______  ____    ____  ____  ____   _____ _____   ___   ____     ___  ____   _____
|      ||    \  /    ||    ||    \ / ___/|     | /   \ |    \   /  _]|    \ / ___/
|      ||  D  )|  o  | |  | |  _  (   \_ |   __||     ||  D  ) /  [_ |  _  (   \_ 
|_|  |_||    / |     | |  | |  |  |\__  ||  |_  |  O  ||    / |    _]|  |  |\__  |
  |  |  |    \ |  _  | |  | |  |  |/  \ ||   _] |     ||    \ |   [_ |  |  |/  \ |
  |  |  |  .  \|  |  | |  | |  |  |\    ||  |   |     ||  .  \|     ||  |  |\    |
  |__|  |__|\_||__|__||____||__|__| \___||__|    \___/ |__|\_||_____||__|__| \___|
                                                                                  
"""
)
            print_header(f"MENU ADMIN - {self.system.current_user}")
            print("1. 📅 Lihat Semua Jadwal")
            print("2. ➕ Tambah Jadwal")
            print("3. ✏️ Perbarui Jadwal")
            print("4. ❌ Hapus Jadwal")
            print("5. 👥 Lihat Jumlah Pengguna yang Membuat Rencana")
            print("0. 🔙 Logout")


            print_separator()
            
            choice = input("Pilih menu (0-5): ")
            
            if choice == "1":
                self.admin_view_schedules()
            elif choice == "2":
                self.admin_add_schedule()
            elif choice == "3":
                self.admin_update_schedule()
            elif choice == "4":
                self.admin_delete_schedule()
            elif choice == "5":
                self.admin_view_user_plans()
            elif choice == "0":
                self.system.logout()
                print("\nLogout berhasil!")
                pause()
            else:
                print("Input tidak valid!")
                pause()
    
    def admin_view_schedules(self):
        clear_screen()
        print_header("DAFTAR JADWAL KERETA")
        schedules = self.system.get_all_schedules()
        
        if not schedules:
            print("Belum ada jadwal tersedia.")
        else:
            # Siapkan data dalam format list of list (baris dan kolom)
            table_data = []
            for schedule in schedules:
                row = [
                    schedule['schedule_id'],
                    schedule['departure'],
                    schedule['destination'],
                    schedule['train_name'],
                    schedule['date'],
                    schedule['departure_time'],
                    schedule['arrival_time'],
                    f"{schedule['price']:.2f}",
                    schedule['available_seats']
                ]
                table_data.append(row)
            
            # Header kolom tabel
            headers = [
    "🆔 ID", 
    "🏠 Keberangkatan", 
    "🎯 Tujuan", 
    "🚆 Kereta", 
    "📅 Tanggal", 
    "⏰ Jam Berangkat", 
    "🕒 Jam Tiba", 
    "💰 Harga", 
    "💺 Kursi"
]

            
            # Cetak tabel dengan tabulate, gunakan format 'fancy_grid' agar lebih jelas
            print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
        
        pause()

    
    def admin_add_schedule(self):
        clear_screen()
        print_header("TAMBAH JADWAL KERETA")
        
        departure = input("Stasiun Keberangkatan: ")
        destination = input("Stasiun Tujuan: ")
        train_name = input("Nama Kereta: ")
        date = input("Tanggal Keberangkatan (YYYY-MM-DD), Masukkan 0 jika hari ini: ")
        departure_time = input("Waktu Keberangkatan (HH:MM): ")
        arrival_time = input("Waktu Kedatangan (HH:MM): ")
        
        if date == "0":
            date = datetime.datetime.now().strftime("%Y-%m-%d")
        else:
            try:
                datetime.datetime.strptime(date, "%Y-%m-%d") 
            except ValueError:
                print("Format tanggal tidak valid")
                pause()
                return


        try:
            price = float(input("Harga Tiket: "))
            available_seats = int(input("Jumlah Kursi Tersedia: "))
        except ValueError:
            print("\nInput harga atau jumlah kursi tidak valid!")
            pause()
            return
        
        if self.system.add_schedule(departure, destination, train_name, date, departure_time, arrival_time, price, available_seats):
            print("\nJadwal berhasil ditambahkan!")
        else:
            print("\nGagal menambahkan jadwal!")
        
        pause()
    
    def admin_update_schedule(self):
        clear_screen()
        print_header("PERBARUI JADWAL KERETA")
        
        schedules = self.system.get_all_schedules()
        if not schedules:
            print("Belum ada jadwal tersedia.")
            pause()
            return
        else:
            # Siapkan data dalam format list of list (baris dan kolom)
            table_data = []
            for schedule in schedules:
                row = [
                    schedule['schedule_id'],
                    schedule['departure'],
                    schedule['destination'],
                    schedule['train_name'],
                    schedule['date'],
                    schedule['departure_time'],
                    schedule['arrival_time'],
                    f"{schedule['price']:.2f}",
                    schedule['available_seats']
                ]
                table_data.append(row)
            
            # Header kolom tabel
            headers = [
    "🆔 ID", 
    "🏠 Keberangkatan", 
    "🎯 Tujuan", 
    "🚆 Kereta", 
    "📅 Tanggal", 
    "⏰ Jam Berangkat", 
    "🕒 Jam Tiba", 
    "💰 Harga", 
    "💺 Kursi"
]

            
            # Cetak tabel dengan tabulate, gunakan format 'fancy_grid' agar lebih jelas
            print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))        
        schedule_id = input("Masukkan ID jadwal yang akan diperbarui: ")
        
        # Cari jadwal dengan ID tersebut
        schedule = None
        for s in schedules:
            if s['schedule_id'] == schedule_id:
                schedule = s
                break
        
        if not schedule:
            print("\nJadwal tidak ditemukan!")
            pause()
            return
        
        print("\nSilakan masukkan data baru (kosongkan jika tidak ingin mengubah):")
        departure = input(f"Stasiun Keberangkatan [{schedule['departure']}]: ") or schedule['departure']
        destination = input(f"Stasiun Tujuan [{schedule['destination']}]: ") or schedule['destination']
        train_name = input(f"Nama Kereta [{schedule['train_name']}]: ") or schedule['train_name']
        departure_time = input(f"Waktu Keberangkatan [{schedule['departure_time']}]: ") or schedule['departure_time']
        arrival_time = input(f"Waktu Kedatangan [{schedule['arrival_time']}]: ") or schedule['arrival_time']
        
        try:
            price_input = input(f"Harga Tiket [{schedule['price']}]: ")
            price = float(price_input) if price_input else schedule['price']
            
            seats_input = input(f"Jumlah Kursi Tersedia [{schedule['available_seats']}]: ")
            available_seats = int(seats_input) if seats_input else schedule['available_seats']
        except ValueError:
            print("\nInput harga atau jumlah kursi tidak valid!")
            pause()
            return
        
        updated_data = {
            "departure": departure,
            "destination": destination,
            "train_name": train_name,
            "departure_time": departure_time,
            "arrival_time": arrival_time,
            "price": price,
            "available_seats": available_seats
        }
        
        if self.system.update_schedule(schedule_id, updated_data):
            print("\nJadwal berhasil diperbarui!")
        else:
            print("\nGagal memperbarui jadwal!")
        
        pause()
    
    def admin_delete_schedule(self):
        clear_screen()
        print_header("HAPUS JADWAL KERETA")
        
        schedules = self.system.get_all_schedules()
        if not schedules:
            print("Belum ada jadwal tersedia.")
            pause()
            return
        else:
            # Siapkan data dalam format list of list (baris dan kolom)
            table_data = []
            for schedule in schedules:
                row = [
                    schedule['schedule_id'],
                    schedule['departure'],
                    schedule['destination'],
                    schedule['train_name'],
                    schedule['date'],
                    schedule['departure_time'],
                    schedule['arrival_time'],
                    f"{schedule['price']:.2f}",
                    schedule['available_seats']
                ]
                table_data.append(row)
            
            # Header kolom tabel
            headers = [
    "🆔 ID", 
    "🏠 Keberangkatan", 
    "🎯 Tujuan", 
    "🚆 Kereta", 
    "📅 Tanggal", 
    "⏰ Jam Berangkat", 
    "🕒 Jam Tiba", 
    "💰 Harga", 
    "💺 Kursi"
]        
        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
        schedule_id = input("Masukkan ID jadwal yang akan dihapus: ")
        
        confirm = input(f"Anda yakin akan menghapus jadwal {schedule_id}? (y/n): ")
        if confirm.lower() != 'y':
            print("\nPenghapusan dibatalkan.")
            pause()
            return
        
        if self.system.delete_schedule(schedule_id):
            print("\nJadwal berhasil dihapus!")
        else:
            print("\nGagal menghapus jadwal!")
        
        pause()
    
    def admin_view_user_plans(self):
        clear_screen()
        print_header("LAPORAN PENGGUNA YANG MEMBUAT RENCANA")

        user_plans = self.system.get_users_plan_count()  # Dict[schedule_id: count]
        schedules = self.system.get_all_schedules()      # List[Dict]

        table_data = []
        for schedule in schedules:
            schedule_id = schedule['schedule_id']
            count = user_plans.get(schedule_id, 0)  # Ambil jumlah user yang membuat rencana

            row = [
                    schedule_id,
                    schedule['departure'],
                    schedule['destination'],
                    schedule['train_name'],
                    schedule['date'],
                    schedule['departure_time'],
                    schedule['arrival_time'],
                    schedule['available_seats'],
                    count  # Tambahkan kolom jumlah rencana
                ]
            table_data.append(row)

        headers = [
                "🆔 ID", 
                "🏠 Keberangkatan", 
                "🎯 Tujuan", 
                "🚆 Kereta", 
                "📅 Tanggal", 
                "⏰ Jam Berangkat", 
                "🕒 Jam Tiba", 
                "💺 Kursi",
                "📊 Jml Rencana"
            ]

        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

        pause()

            

    def show_user_menu(self):
        while self.system.current_user and not self.system.is_admin:
            clear_screen()
            print(r"""
 ______  ____    ____  ____  ____   _____ _____   ___   ____     ___  ____   _____
|      ||    \  /    ||    ||    \ / ___/|     | /   \ |    \   /  _]|    \ / ___/
|      ||  D  )|  o  | |  | |  _  (   \_ |   __||     ||  D  ) /  [_ |  _  (   \_ 
|_|  |_||    / |     | |  | |  |  |\__  ||  |_  |  O  ||    / |    _]|  |  |\__  |
  |  |  |    \ |  _  | |  | |  |  |/  \ ||   _] |     ||    \ |   [_ |  |  |/  \ |
  |  |  |  .  \|  |  | |  | |  |  |\    ||  |   |     ||  .  \|     ||  |  |\    |
  |__|  |__|\_||__|__||____||__|__| \___||__|    \___/ |__|\_||_____||__|__| \___|
                                                                                  
"""
)
            print_header(f"MENU PELANGGAN - {self.system.current_user}")
            print("1. 🚆 Lihat Jadwal Kereta")
            print("2. 🔍 Cari Jadwal")
            print("3. 📊 Urutkan Jadwal")
            print("4. 🗓️ Buat Rencana Perjalanan")
            print("5. 📁 Lihat Riwayat Rencana")
            print("0. 🔙 Logout")

            print_separator()
            
            choice = input("Pilih menu (0-5): ")
            
            if choice == "1":
                self.user_view_schedules()
            elif choice == "2":
                self.user_search_schedules()
            elif choice == "3":
                self.user_sort_schedules()
            elif choice == "4":
                self.user_create_plan()
            elif choice == "5":
                self.user_view_plan_history()
            elif choice == "0":
                self.system.logout()
                print("\nLogout berhasil!")
                pause()
            else:
                print("Input tidak valid!")
                pause()
    
    def user_view_schedules(self):
        clear_screen()
        print_header("JADWAL KERETA")
        
        schedules = self.system.get_all_schedules()
        
        if not schedules:
            print("Belum ada jadwal tersedia.")
        else:
            table_data = []
            now = datetime.datetime.now()
            for schedule in schedules:
            # Gabungkan tanggal dan jam keberangkatan menjadi datetime
                schedule_datetime_str = f"{schedule['date']} {schedule['departure_time']}"
                schedule_datetime = datetime.datetime.strptime(schedule_datetime_str, "%Y-%m-%d %H:%M")

                if schedule_datetime > now:
                        row = [
                            schedule['schedule_id'],
                            schedule['departure'],
                            schedule['destination'],
                            schedule['train_name'],
                            schedule['date'],
                            schedule['departure_time'],
                            schedule['arrival_time'],
                            f"{schedule['price']:.2f}",
                            schedule['available_seats']
                        ]
                        table_data.append(row)
                    
            headers = [
    "🆔 ID", 
    "🏠 Keberangkatan", 
    "🎯 Tujuan", 
    "🚆 Kereta", 
    "📅 Tanggal", 
    "⏰ Jam Berangkat", 
    "🕒 Jam Tiba", 
    "💰 Harga", 
    "💺 Kursi"
]

            print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
        
        pause()

    
    def user_search_schedules(self):
        clear_screen()
        print_header("CARI JADWAL KERETA")
        
        print("Kategori pencarian:")
        print("1. 🏠 Stasiun Keberangkatan")
        print("2. 🎯 Stasiun Tujuan")
        print("3. 🚆 Nama Kereta")
        print("0. 🔙 Kembali")

        print_separator()
        
        choice = input("Pilih kategori (1-3): ")
        
        category = ""
        if choice == "1":
            category = "departure"
            search_value = input("Masukkan Stasiun Keberangkatan: ")
        elif choice == "2":
            category = "destination"
            search_value = input("Masukkan Stasiun Tujuan: ")
        elif choice == "3":
            category = "train_name"
            search_value = input("Masukkan Nama Kereta: ")
        else:
            print("Kategori tidak valid!")
            pause()
            return
        
        results = self.system.search_schedules(category, search_value)
        
        clear_screen()
        print_header(f"HASIL PENCARIAN: {search_value}")
        
        if not results:
            print("Tidak ada jadwal yang sesuai dengan pencarian.")
        else:
            # Buat list data untuk tabulate
            table_data = []

            now = datetime.datetime.now()
            for schedule in results:
            # Gabungkan tanggal dan jam keberangkatan menjadi datetime
                schedule_datetime_str = f"{schedule['date']} {schedule['departure_time']}"
                schedule_datetime = datetime.datetime.strptime(schedule_datetime_str, "%Y-%m-%d %H:%M")

                if schedule_datetime > now:
                    row = [
                        schedule['schedule_id'],
                        schedule['departure'],
                        schedule['destination'],
                        schedule['train_name'],
                        schedule['date'],
                        schedule['departure_time'],
                        schedule['arrival_time'],
                        f"{schedule['price']:.2f}",
                        schedule['available_seats']
                    ]
                    table_data.append(row)
            
            headers = [
    "🆔 ID", 
    "🏠 Keberangkatan", 
    "🎯 Tujuan", 
    "🚆 Kereta", 
    "📅 Tanggal", 
    "⏰ Jam Berangkat", 
    "🕒 Jam Tiba", 
    "💰 Harga", 
    "💺 Kursi"
]

            print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))
        
        pause()

    def user_sort_schedules(self):
        clear_screen()
        print_header("URUTKAN JADWAL KERETA")
        
        print("Kategori pencarian:")
        print("1. 🏠 Stasiun Keberangkatan")
        print("2. 🎯 Stasiun Tujuan")
        print("3. 🚆 Nama Kereta")
        print("0. 🔙 Kembali")

        print_separator()
        
        choice = input("Pilih kategori (1-3): ")
        
        category = ""
        if choice == "1":
            category = "departure"
        elif choice == "2":
            category = "destination"
        elif choice == "3":
            category = "train_name"
        elif choice == "0":
            return
        else:
            print("Kategori tidak valid!")
            pause()
            return
        
        schedules = self.system.sort_schedules(category)
        clear_screen()
        print_header(f"HASIL SORTIR BERDASARKAN: {category}")
        
        if not schedules:
            print("Tidak ada jadwal yang tersedia.")
        else:
            table_data = []
            now = datetime.datetime.now()

            for schedule in schedules:
            # Gabungkan tanggal dan jam keberangkatan menjadi datetime
                schedule_datetime_str = f"{schedule['date']} {schedule['departure_time']}"
                schedule_datetime = datetime.datetime.strptime(schedule_datetime_str, "%Y-%m-%d %H:%M")

                if schedule_datetime > now:    

                    row = [
                    schedule['schedule_id'],
                    schedule['departure'],
                    schedule['destination'],
                    schedule['train_name'],
                    schedule['date'],
                    schedule['departure_time'],
                    schedule['arrival_time'],
                    f"{schedule['price']:.2f}",
                    schedule['available_seats']
                ]
                    table_data.append(row)
            
            headers = [
    "🆔 ID", 
    "🏠 Keberangkatan", 
    "🎯 Tujuan", 
    "🚆 Kereta", 
    "📅 Tanggal", 
    "⏰ Jam Berangkat", 
    "🕒 Jam Tiba", 
    "💰 Harga", 
    "💺 Kursi"
]
            print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))       
        pause()


    def user_create_plan(self):
        clear_screen()
        print_header("BUAT JADWAL RENCANA KEBERANGKATAN")

        departure = input("Masukkan Stasiun Keberangkatan: ").strip().lower()
        destination = input("Masukkan Stasiun Tujuan: ").strip().lower()
        date = input("Masukkan Tanggal Keberangkatan (format: YYYY-MM-DD): ").strip()

        # Validasi Format Tanggal
        try:
            tanggal_input = datetime.datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            print("Format tanggal tidak valid")
            pause()
            return

        now = datetime.datetime.now()
        if tanggal_input.date() < now.date():
            print("Tanggal keberangkatan sudah lewat!")
            pause()
            return

        # Ambil Semua Jadwal
        all_schedules = self.system.get_all_schedules()

        # Filter jadwal sesuai input dan BELUM berangkat
        matching = []
        for s in all_schedules:
            if (
                s["departure"].lower() == departure
                and s["destination"].lower() == destination
                and s["date"] == date
            ):
                jadwal_datetime_str = f"{s['date']} {s['departure_time']}"
                jadwal_datetime = datetime.datetime.strptime(jadwal_datetime_str, "%Y-%m-%d %H:%M")

                if jadwal_datetime > now:
                    matching.append(s)

        if not matching:
            print("\nTidak ada jadwal yang tersedia atau semua jadwal sudah lewat.")
            pause()
            return

        # Tampilkan jadwal
        print("\nJadwal yang tersedia:")
        table_data = []
        for s in matching:
            row = [
                s['schedule_id'],
                s['departure'],
                s['destination'],
                s['train_name'],
                s['date'],
                s['departure_time'],
                s['arrival_time'],
                f"{s['price']:.2f}",
                s['available_seats']
            ]
            table_data.append(row)

        headers = [
            "🆔 ID", 
            "🏠 Keberangkatan", 
            "🎯 Tujuan", 
            "🚆 Kereta", 
            "📅 Tanggal", 
            "⏰ Jam Berangkat", 
            "🕒 Jam Tiba", 
            "💰 Harga", 
            "💺 Kursi"
        ]

        print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

        # Input ID dan validasi
        schedule_id = input("\nMasukkan ID jadwal yang ingin dipilih: ")
        selected_schedule = next((s for s in matching if s['schedule_id'] == schedule_id), None)

        if not selected_schedule:
            print("ID jadwal tidak tersedia")
            pause()
            return

        # Validasi ulang waktu
        jadwal_datetime_str = f"{selected_schedule['date']} {selected_schedule['departure_time']}"
        jadwal_datetime = datetime.datetime.strptime(jadwal_datetime_str, "%Y-%m-%d %H:%M")

        if jadwal_datetime <= now:
            print("Tidak bisa membuat rencana. Jadwal keberangkatan sudah lewat!")
            pause()
            return

        # Simpan rencana
        if self.system.create_plan(schedule_id, date):
            print("Berhasil membuat rencana perjalanan!")
        else:
            print("Gagal membuat rencana perjalanan")
        pause()

    
    def user_view_plan_history(self):
        clear_screen()
        print_header("LIHAT RENCANA PERJALANAN")
        
        # Refresh data dari file (kalau ada prosesnya, tambahkan di sini)
        
        if self.system.current_user not in self.system.user_plan_history:
            print("Anda belum memiliki rencana perjalanan.")
            pause()
            return

        plan_stack = self.system.user_plan_history[self.system.current_user].get_all()

        if not plan_stack:
            print("Anda belum memiliki rencana perjalanan.")
            pause()
            return

        print("Filter riwayat berdasarkan:")
        print("1. 📜 Semua riwayat")
        print("2. 📅 Berdasarkan tanggal")
        print("3. 🚉 Berdasarkan stasiun keberangkatan")
        print("4. 🎯 Berdasarkan stasiun tujuan")
        print("0. 🔙 Kembali")

        print_separator()

        choice = input("Pilih menu (0-4): ")

        if choice == "0":
            return

        elif choice == "1":
            filtered = plan_stack

        elif choice == "2":
            search_date = input("Masukkan tanggal perjalanan (YYYY-MM-DD): ")
            filtered = [plan for plan in plan_stack if plan["date"] == search_date]

        elif choice == "3":
            station = input("Masukkan stasiun keberangkatan: ").lower()
            filtered = [plan for plan in plan_stack if plan["schedule"]["departure"].lower() == station]

        elif choice == "4":
            station = input("Masukkan stasiun tujuan: ").lower()
            filtered = [plan for plan in plan_stack if plan["schedule"]["destination"].lower() == station]

        else:
            print("Pilihan tidak valid!")
            pause()
            return

        clear_screen()
        print_header("HASIL RIWAYAT RENCANA")

        if not filtered:
            print("Tidak ada rencana yang sesuai dengan pencarian.")
        else:
            table_data = []
            for plan in filtered:
                row = [
                    plan['plan_id'],
                    plan['schedule']['departure'],
                    plan['schedule']['destination'],
                    plan['schedule']['train_name'],
                    plan['date']
                ]
                table_data.append(row)

            headers = [
    "🆔 ID", 
    "🏠 Keberangkatan", 
    "🎯 Tujuan", 
    "🚆 Kereta", 
    "📅 Tanggal", 
    "⏰ Jam Berangkat", 
    "🕒 Jam Tiba", 
    "💰 Harga", 
    "💺 Kursi"
]

            print(tabulate(table_data, headers=headers, tablefmt="fancy_grid"))

            self.user_plan_option()

        pause()


    def user_plan_option(self):
        print_separator("-", 100)
        print("1. ❌ Bersihkan Riwayat")
        print("0. 🔙 Kembali")


        choice = input("\nPilih Opsi: ")

        if choice == "1":
            if self.system.current_user in self.system.user_plan_history:
                with open('data/user_plan_history.json', 'r') as file:
                    data = json.load(file)
                    current_session = self.system.current_user
                    data[current_session] = []

                with open('data/user_plan_history.json', 'w') as file:
                    json.dump(data, file, indent = 4)
                
                current_user = self.system.current_user

                self.system.clear_user_plan_history(current_user)
                clear_screen()
                print("Berhasil membersihkan riwayat")
            else:
                return
            pause()

        pass

    def run(self):  
        clear_screen()
        print_header("SISTEM PEMESANAN TIKET KERETA ANTARKOTA")
        self.start()
        print("\nTerima kasih telah menggunakan sistem ini.")
        pause()
        exit(0)