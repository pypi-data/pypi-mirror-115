import socket
import threading

# Функция для ожидания и приема новоых сообщений
def threaded_accept(connection):
	t = threading.currentThread()
	while getattr(t, "do_run", True):
		try:
			data = connection.recv(2048).decode('utf-8')
			print(data)
			if not data:
				break
		except:
			pass

# Функция с основной логикой клиента
def start_client(host='127.0.0.1', port=1234):
	# Создание сокета и попытка подключиться к серверу
	ClientSocket = socket.socket()
	try:
	    ClientSocket.connect((host, port))
	    ClientSocket.settimeout(1)
	except socket.error as e:
	    print(str(e))

	# Логин под псевдонимом
	alias = ''
	while True:
		alias = input(' Enter a nickname: ')
		ClientSocket.send(str.encode(alias))
		status = ClientSocket.recv(2048).decode('utf-8')
		if status == 'OK':
			break
		else:
			print(' Name is already taken or empty')

	# Приветственное сообщение
	print('-------------------------------------------------------------------------------')
	print(' This is console client-server chat ')
	print(' Type a message to send it to all of the members ')
	print(' Type a message starting with "/to <nickname>" to send it to particular member ')
	print(' Your name is {} '.format(alias))
	print('-------------------------------------------------------------------------------')

	# Запуск нового потока, ожидающего и принимающего новые сообщения
	new_thread = threading.Thread(target=threaded_accept, args=(ClientSocket,))
	new_thread.start()

	# Ввод и отправка введенного сообщения
	while True:
	    message = input()
	    if message:
	    	ClientSocket.send(str.encode(message))
	    else:
	    	print(' Exiting...')
	    	break

	# Уничтожение потока и сокета
	new_thread.do_run = False
	new_thread.join()
	ClientSocket.close()

if __name__=='__main__':
	start_client()