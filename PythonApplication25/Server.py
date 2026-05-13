import socket
import threading
import sys

class SimpleTcpServer:
    def __init__(self, host='127.0.0.1', port=4000):
        self.addr = (host, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.client_conn = None
        self.is_active = True

    def _incoming_handler(self):
        """Обработка входящих данных в отдельном потоке."""
        while self.is_active:
            try:
                raw_data = self.client_conn.recv(1024)
                if not raw_data:
                    break

                message = raw_data.decode('utf-8')
                if message.lower() == "exit":
                    print("\n[!] Клиент инициировал выход.")
                    break

                # Красивый вывод, чтобы не перекрывать строку ввода
                sys.stdout.write(f"\rКлиент: {message}\nВы: ")
                sys.stdout.flush()
            except Exception:
                break
        
        self.is_active = False
        print("\n[*] Сессия завершена. Нажмите Enter для выхода.")

    def start(self):
        try:
            self.server_socket.bind(self.addr)
            self.server_socket.listen(1)
            print(f"[#] Сервер запущен на {self.addr[0]}:{self.addr[1]}")
            print("[#] Ожидание подключения...")

            self.client_conn, client_addr = self.server_socket.accept()
            print(f"[+] Установлена связь с: {client_addr[0]}:{client_addr[1]}")

            # Запуск потока прослушивания
            threading.Thread(target=self._incoming_handler, daemon=True).start()

            # Основной цикл отправки
            while self.is_active:
                out_msg = input("Вы: ")
                if not self.is_active: 
                    break
                
                self.client_conn.send(out_msg.encode('utf-8'))
                
                if out_msg.lower() == "exit":
                    self.is_active = False

        except KeyboardInterrupt:
            print("\n[!] Сервер остановлен вручную.")
        finally:
            if self.client_conn:
                self.client_conn.close()
            self.server_socket.close()
            print("[*] Ресурсы очищены. Пока!")

if __name__ == "__main__":
    srv = SimpleTcpServer()
    srv.start()