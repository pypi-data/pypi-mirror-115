import socket
import threading
import syslog
from datetime import datetime

# Функция, отвечающая за прием сообщения от конкретного клиента и отправку его адресату
def threaded_client(connection, current_clients):
	# Проверка корректности имени пользователя и добавление нового пользователя в список
	alias = ''
	while True:
		alias = connection.recv(2048).decode('utf-8')
		if (alias in current_clients) or alias.strip() == '':
			connection.sendall(str.encode('FAIL'))
		else:
			connection.sendall(str.encode('OK'))
			break
	print(alias, 'entered chat')
	current_clients[alias] = connection

	while True:
		data = connection.recv(2048).decode('utf-8')
		date = datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
		status = '(sent)'
		formatted = ''

		# Парсинг сообщения
		if data.startswith('/to '):
			dest = data.split(' ')[1]
			data  = data.replace('/to ' + dest + ' ', '')
			formatted = '{} "{}" to "{}": {}'.format(date, alias, dest, data)
			# Отправка сообщения адресату
			if dest in current_clients.keys():
				send_to_other_client(formatted, dest, current_clients)
			else:
				status = '(failed)'
		else:
			formatted = '{} "{}" to "{}": {}'.format(date, alias, 'all', data)
			if len(current_clients.keys()) == 1:
				status = '(failed)'
			# Отправка сообщения адресату	
			for dest in current_clients.keys():
				if alias == dest: continue
				send_to_other_client(formatted, dest, current_clients)

		# Логирование сообщения в syslog
		loggable = formatted + ' ' + status
		if data: syslog.syslog(loggable)

		# Формирование и отправка ответа о статусе сообщения отправителю
		reply = '{} {} {}'.format(date, data, status)
		if not data:
			break
		connection.sendall(str.encode(reply))
	# Отключение пользователя
	connection.close()
	current_clients.pop(alias)
	print(alias, 'left chat')

# Функция, отвечающая за отправку сообщения адресату
def send_to_other_client(formatted, dest, current_clients):
	if dest in current_clients.keys():
		current_clients[dest].sendall(str.encode(formatted))

# Функция с основной логикой сервера
def start_server(host='127.0.0.1', port=1234):
	# Создание сокета и привязка к конкретному адресу
	ServerSocket = socket.socket()
	current_clients = dict()
	try:
		ServerSocket.bind((host, port))
	except socket.error as e:
		print(str(e))

	print('Waitiing for a Connection...')
	ServerSocket.listen()

	# Принятие подключения от клиента и создание отдельного потока для него
	while True:
		Client, address = ServerSocket.accept()
		new_thread = threading.Thread(target=threaded_client, args=(Client, current_clients,))
		new_thread.start()

	# Отключение сокета сервера
	ServerSocket.close()

if __name__=='__main__':
	start_server()