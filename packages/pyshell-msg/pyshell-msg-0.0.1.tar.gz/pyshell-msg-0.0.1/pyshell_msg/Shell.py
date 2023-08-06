def ShellMessage(base, message, value): #pyshell_msg
	'''
		log/print your status and messages for python application on terminal in a
		standard but customizable format.
	'''
	'''
		base is string to indicate application name
		message is the display message or status message
		
		  --<base> $ message > value

		  exapmle:

		  --<yt> $ url status      > 200
	'''


	base = '--<{}> $ '.format(base)
	end = '> '
	if type(message) != str:
		raise ValueError("message must be a string")
	elif type(base) != str:
		raise ValueError("base must be a string")
	else:
		shell_str = base + message
		if len(shell_str) < 30:
			white_sp = ' ' * (30-len(shell_str))
		else:
			white_sp = ' '

		shell_str += white_sp + end + str(value)
		print(shell_str)