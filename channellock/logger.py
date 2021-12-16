import datetime

first = True


def clear_logs():
	file = open('logs.txt', 'w')
	file.write('# logs.txt file\n# Used to log errors & dev messages\n\nCurrent Date     | Current Time   | Log message\n\n')


def log(text):
	global first

	dt = datetime.datetime.now()
	dt_string = dt.strftime("Date: %d/%m/%Y | Time: %H:%M:%S")
	file = open('logs.txt', 'r')
	c_text = file.read()
	file.close()

	file = open('logs.txt', 'w')

	if not first:
		file.write(c_text + f'{dt_string} | {text}\n')
	else:
		clear_logs()
		first = False

	file.close()
