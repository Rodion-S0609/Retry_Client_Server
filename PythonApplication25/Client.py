import socket
import threading
import sys

class ChatClient:
    def __init__(self, host='127.0.0.1', port=1234):
        self.address = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_running = True

    def establish_connection(self):
        print(f"[*] Подключение к {self.address[0]}:{self.address[1]}...")
        while True:
            try:
                self.sock.connect(self.address)
                print("[+] Соединение установлено. Для выхода введите 'exit'.")
                break
            except ConnectionRefusedError:
                print("[-] Сервер не отвечает, повтор через 2 сек...")
                import time
                time.sleep(2)

    def _listen_to_server(self):
        while self.is_running:
            try:
                payload = self.sock.recv(1024)
                if not payload:
                    break
                
                message = payload.decode('utf-8')
                if message.lower() == "exit":
                    print("\n[!] Сервер разорвал соединение.")
                    break
                
                print(f"\rСервер: {message}\nВы: ", end="")
            except Exception:
                break
        
        self.is_running = False
        print("\n[*] Нажмите Enter, чтобы завершить работу.")

    def run(self):
        self.establish_connection()
        
        listener = threading.Thread(target=self._listen_to_server, daemon=True)
        listener.start()

        try:
            while self.is_running:
                user_input = input("Вы: ")
                if not self.is_running: break
                
                self.sock.send(user_input.encode('utf-8'))
                
                if user_input.lower() == "exit":
                    self.is_running = False
        except KeyboardInterrupt:
            pass
        finally:
            self.sock.close()
            print("\nСеанс завершен.")

if __name__ == "__main__":
    client = ChatClient()
    client.run()
