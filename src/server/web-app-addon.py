## NOTE: web-app to manage NYU mobile testbed
## Author: Matteo Varvello (matteo.varvello@nokia.com)
## Date: 11/1/2021
## POST API
## curl -H "Content-Type: application/json" --data '{"data":"testing data"}' https://mobile.batterylab.dev:8082/status
## GET API 
## curl https://mobile.batterylab.dev:8082/action?id=1234
## POST API (via APP)
## curl -H "Content-Type: application/json" --data '{"uid":"c95ad2777d56", "timestamp":"1635973511", "command_id":"1234", "command":"recharge"}' https://mobile.batterylab.dev:8082/appstatus

#!/usr/bin/python
#import random
import string
import json
import cherrypy
import os
from threading import Thread
import threading
import signal
import sys
import time 
import argparse
import simplejson
import subprocess
import psycopg2
import db_manager
from db_manager import run_query, insert_data, insert_command, connect_to_database_pool, insert_data_pool
import random 

# run a generic query on the database (pool)
def run_query_pool(query, postgreSQL_pool):
	info = None
	msg = ''

	# Use getconn() to Get Connection from connection pool
	ps_connection = postgreSQL_pool.getconn()
	if (ps_connection):
		try:
			ps_cursor = ps_connection.cursor()
			ps_cursor.execute(query)
			if 'select' in query or 'SELECT' in query:
				info = ps_cursor.fetchall()
			else: 
				ps_connection.commit()
			msg = 'OK'
		# handle exception 
		except Exception as e:
			msg = 'Exception: %s' % e    
		# finally close things 
		finally:
			ps_cursor.close()
			postgreSQL_pool.putconn(ps_connection)	
	# all good 
	return info, msg 

# simple function to read json from a POST message 
def read_json(req): 
	cl = req.headers['Content-Length']
	rawbody = req.body.read(int(cl))
	#body = simplejson.load(rawbody)
	body = simplejson.loads(rawbody)	
	return body 

# global parameters
port    = 8084                    # default listening port 
THREADS = []                      # list of threads 
ACL     = False                   # control whether application ACL rules should be used 
allowedips      = {               # ACL rules 
    '127.0.0.1':'-1',                     
}
session_id = ""
session_data = {}
supportedIDs = ['c95ad2777d56']   # list of client IDs supported 
id_control  = False               # flag for client ID control 
postgreSQL_pool = None            # pool of connection to DB
letters = string.ascii_lowercase  # collection of lowercase letter used to compute unique identifier

# function to run a bash command
def run_bash(bashCommand, verbose = True):
	process = subprocess.Popen(bashCommand.split(), stdout = subprocess.PIPE, stdin =subprocess.PIPE, shell = False)
	output, error = process.communicate()
	
	#if verbose: 
	print("Command: " + bashCommand + " Output: " + str(output) + " Error: " + str(error))

	# all good (add a check?)
	return str(output.decode('utf-8'))

# pre-flight request 
# see http://www.w3.org/TR/cors/#cross-origin-request-with-preflight-0    
def cors():
  # logging 
  if cherrypy.request.method == 'OPTIONS':
    cherrypy.response.headers['Access-Control-Allow-Methods'] = 'POST'
    cherrypy.response.headers['Access-Control-Allow-Headers'] = 'content-type'
    cherrypy.response.headers['Access-Control-Allow-Origin']  = '*'
    # tell CherryPy no avoid normal handler
    return True
  else:
    cherrypy.response.headers['Access-Control-Allow-Origin'] = '*'


# thread to control client-server communication
def web_app():
    # configuration 
    conf = {
        '/': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.sessions.on': True,
            'tools.response_headers.on': True,
        }
    }

    cherrypy.tools.cors = cherrypy._cptools.HandlerTool(cors)
    server_config={
        'server.socket_host': '0.0.0.0',
        'server.socket_port': port, 
        'server.ssl_module':'builtin',
        'server.ssl_certificate':'certificate.pem',
        'server.thread_pool': 50,
    }
    cherrypy.config.update(server_config)

    # GET - ADD/REMOVE-ACL-RULE (localhost only)
    cherrypy.tree.mount(StringGeneratorWebService(), '/addACLRule', conf)
    cherrypy.tree.mount(StringGeneratorWebService(), '/removeACLRule', conf)
    cherrypy.tree.mount(StringGeneratorWebService(), '/action', conf)         # for now query each rand(30) seconds
    cherrypy.tree.mount(StringGeneratorWebService(), '/commandDone', conf)    # allow marking a command as done
    cherrypy.tree.mount(StringGeneratorWebService(), '/code', conf)

    # POST/REPORT-MEASUREMENTS 
    cherrypy.tree.mount(StringGeneratorWebService(), '/addonstatus', conf)
    cherrypy.tree.mount(StringGeneratorWebService(), '/addontest', conf)     # report addontest 

    # start cherrypy engine 
    cherrypy.engine.start()
    cherrypy.engine.block()

# catch ctrl-c
def signal_handler(signal, frame):

	# logging 
	print('You pressed Ctrl+C!')

	# kill throughput thread 
	print("stopping main thread")
	THREADS[0].do_run = False
	THREADS[0].join()
	
	# kill cherrypy
	print("stopping cherrypy webapp")
	cherrypy.engine.exit()

	# exiting from main process
	sys.exit(0)


@cherrypy.expose
class StringGeneratorWebService(object):

	@cherrypy.tools.accept(media='text/plain')
	def GET(self, var=None, **params):
		
		# log last IP that contacted the server
		src_ip = cherrypy.request.headers['Remote-Addr']
		
		# get user id 
		print(cherrypy.request.params)
		if 'code' in cherrypy.url():
			if 'code' in cherrypy.request.params: 
				# logging 
				print("received request to check code:", src_ip, cherrypy.request.params['code'])
				
				# query the db for a code for this user -- which needs to match what reported
				query = "select code from crowdsourcing where tester_ip = " + src_ip " and to_timestamp(timestamp) > now() - interval '10 mins' order by timestamp desc"
				info, msg  = run_query_pool(query, postgreSQL_pool)							
				print(info, msg)				

				# prepare response to send back 				
				ans = {}				
				ans['msg']="ERROR"				
				if info is None:
					cherrypy.response.status = 202
					return "myCallBackMethod(" + json.dumps(ans) + ")"
				local_code = info[0][0] 				
				cherrypy.response.status = 200				
				if local_code == cherrypy.request.params['code']:
					ans['msg'] = "ok"
				return "myCallBackMethod(" + json.dumps(ans) + ")"
			else: 
				# logging 
				print("received a request to generate a code") 
				
				# compute unique code to be returned
				ans = {}
				code_to_return = print ( ''.join(random.choice(letters) for i in range(12)) )
				ans['code'] = code_to_return
				
				# insert code in the database 
				insert_code(src_ip, time.time(), code_to_return, postgreSQL_pool):
				
				# send out the response 
				print(src_ip, code_to_return)
				cherrypy.response.status = 200				
				return "myCallBackMethod(" + json.dumps(ans) + ")"
				
		if 'uid' not in cherrypy.request.params: 
			cherrypy.response.status = 400
			print("Malformed URL")
			return "Error: Malformed URL" 
		user_id = cherrypy.request.params['uid']
		if user_id not in supportedIDs and id_control:  
			cherrypy.response.status = 400
			print("User %s is not supported" %(user_id))
			return "Error: User is not supported"
	
		# see if there is a command
		if 'action' in cherrypy.url():
			if 'prev_command' not in cherrypy.request.params: 
				cherrypy.response.status = 400
				print("Malformed URL")
				return "Error: Malformed URL" 
			prev_command = cherrypy.request.params['prev_command']
			
			# look for a potential action to be performed
			query = "select * from commands where ('" + user_id + "' = ANY (tester_id_list) or '*' = ANY (tester_id_list)) and command_id != '" + prev_command + "';"
			print(query)
			#info, msg  = run_query(query)
			info, msg  = run_query_pool(query, postgreSQL_pool)
			print(info, msg)	
			#print(info, msg)
			if info is None or len(info) == 0:
				cherrypy.response.status = 202 # 202 triggers an error 
				return "No command matching the query found"
			max_timestamp = 0
			unique_id = user_id
			for entry in info:
				timestamp = entry[5]
				user_target_list = entry[1]
				status = entry[6]
				if unique_id in status:  # it means this user already completed this job
					continue
				if timestamp > max_timestamp: 
					max_timestamp = timestamp 
					command = entry[2]
					comm_id = entry[0]
					duration = entry[3]
					isBackground = entry[4]
			
			# all good 
			if max_timestamp == 0:
				return "No command matching the query found"
			ans = command + ';' + str(max_timestamp) + ';' + comm_id + ';' + str(duration) + ';' + isBackground + '\n'
			cherrypy.response.status = 200
			return ans 

		# mark command as done
		elif 'commandDone' in cherrypy.url():
			if 'command_id' not in cherrypy.request.params: 
				cherrypy.response.status = 400
				print("Malformed URL")
				return "Error: Malformed URL" 
			command_id = cherrypy.request.params['command_id']
			comm_status = cherrypy.request.params['status'] #FIXME: potentially use this 

			# look for a potential action to be performed
			status = termux_id + ';' + user_id
			query = "update commands set status = array_append(status, '" + status + "') where command_id = '" + command_id + "';"
			#info, msg  = run_query(query)
			info, msg  = run_query_pool(query, postgreSQL_pool)			
			print(info, msg)
	
			# all good 
			cherrypy.response.status = 200
			return msg

	# handle POST requests 
	def POST(self, name="test"):
	
		# parameters 
		ret_code = 202	   # default return code 
		result = []        # result to be returned when needed 
		ans = ''           # placeholder for response 

		# extract incoming IP address 
		src_ip = cherrypy.request.headers['Remote-Addr']

		# ACL control 
		if ACL: 
			if not src_ip in allowedips:
				cherrypy.response.status = 403
				print("Requesting ip address (%s) is not allowed" %(src_ip))
				return "Error: Forbidden" 

		# status update reporting 
		url = cherrypy.url()
		if 'addonstatus' in url or 'addontest' in url:
			data_json = read_json(cherrypy.request)
			data_json['ip'] = src_ip
			user_id = data_json['uid']
			if 'status' in cherrypy.url():
				post_type = "addonstatus"
			elif 'addontest' in cherrypy.url():
				post_type = "addontest"
			timestamp = data_json['timestamp']			
			msg = insert_data_pool(user_id, post_type, timestamp, data_json, postgreSQL_pool)	
		
		# respond all good 
		cherrypy.response.headers['Content-Type'] = 'application/json'
		cherrypy.response.headers['Access-Control-Allow-Origin']  = '*'
		cherrypy.response.status = ret_code
		if ans == '':
			ans = 'OK\n'

		# all good, send response back 
		return ans.encode('utf8')

	# preflight request 
	# see http://www.w3.org/TR/cors/#cross-origin-request-with-preflight-0	
	def OPTIONS(self, name="test"): 
		cherrypy.response.headers['Access-Control-Allow-Methods'] = 'POST'
		cherrypy.response.headers['Access-Control-Allow-Headers'] = 'content-type'
		cherrypy.response.headers['Access-Control-Allow-Origin']  = '*'

	def PUT(self, another_string):
		cherrypy.session['mystring'] = another_string

	def DELETE(self):
		cherrypy.session.pop('mystring', None)

# main goes here 
if __name__ == '__main__':

	# create connection pool to the database 
	connected, postgreSQL_pool = connect_to_database_pool()
	if not connected: 
		print("Issue creating the connection pool")
		sys.exit(-1)

	# start a thread which handle client-server communication 
	THREADS.append(Thread(target = web_app()))
	THREADS[-1].start()
	
	# listen to Ctrl+C
	signal.signal(signal.SIGINT, signal_handler)
