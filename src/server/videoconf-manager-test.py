#!/usr/bin/env python
import psutil
import time, datetime
import sys
import psycopg2
from psycopg2 import pool

# connect to databse (with a pool)
def connect_to_database_pool(): 
	postgreSQL_pool = None
	try:
		print("connecting to database with a pool")
		postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user="nyu",
					password="pa0l1n0",
					host="127.0.0.1",
					port="5432",
					database="mobile_testbed")
		if (postgreSQL_pool):
			print("Connection pool created successfully")
			status = True
		else: 
			print("Something is wrong")
			status = False 
	except (Exception, psycopg2.DatabaseError) as error:
		print("Error while connecting to PostgreSQL", error)
		status = False 
	
	# all good 
	return status, postgreSQL_pool

# insert command for pi
def insert_command(command_id, tester_id_list, timestamp, action, duration, isBackground):	
	info = None
	msg = ""
	ps_connection = postgreSQL_pool.getconn()
	if (ps_connection):
		try:
			ps_cursor = ps_connection.cursor()	
			insert_sql = "insert into commands(command_id, tester_id_list, command, duration, background, timestamp, status) values(%s, %s, %s, %s, %s, %s, %s);"	
			data = (command_id, tester_id_list, action, duration, isBackground, timestamp, "{active}")
			ps_cursor.execute(insert_sql, data)
			msg = "action_update:all good" 				
			conn.commit()
		# handle exception 
		except Exception as e:
			msg = 'Exception: %s' % e    
		# finally close things 
		finally:
			ps_cursor.close()
			postgreSQL_pool.putconn(ps_connection)	
	# all good 
	return info, msg 

# run a generic query on the database
def run_query(query):
	info = None
	msg = ''

	# Use getconn() to Get Connection from connection pool
	ps_connection = postgreSQL_pool.getconn()
	if (ps_connection):
		try:
			ps_cursor = ps_connection.cursor()
			ps_cursor.execute(query)
			info = ps_cursor.fetchall()
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

# parameters 
VIDEOCONF_SIZE = 4          # 1 host + 3 phones
candidate_testers = []		# list of candidate testers 
VIDEOCONF_DUR = 180         # duration of a videoconference          
SAFE_TIME = 60              # safe time post a conference 
app = "zoom"                # videoconference app under test 
start_host = False          # flag to control if to start a host or not 
list_meeting_ids = {}       # dictionaire of meeting IDs

# start the host in the cloud (maybe manua)
if start_host: 
	print("Add code to start a VM for app: " + app) 
	# TODO 

# populate meeting IDs and passwords
list_meeting_ids["zoom"]="4170438763"  #6893560343
zoom_password="6m2jmA"                 #m06Yb9
list_meeting_ids["meet"]="nfk-ttfy-bzi"
list_meeting_ids["webex"]="1828625842"

# command in common across apps and tests
meeting_id = list_meeting_ids[app]
basic_command = "./videoconf-tester.sh -a " + app + " -m " + meeting_id + " --dur " + str(VIDEOCONF_DUR) + " --pcap --clear" ## " --view --video"

# add password for zoom
if app == "zoom": 
	basic_command += " -p " + zoom_password + " --big 400"
elif app == "webex": 
	basic_command += " --big 400" 
elif app == "meet":
	basic_command += " --big 500" 

# main goes here 
if __name__ == '__main__':
	# create connection pool to the database 
	connected, postgreSQL_pool = connect_to_database_pool()
	if not connected: 
		print("Issue creating the connection pool")
		
	# find devices currently available, along with networking info 
	query = "select distinct(tester_id) from status_update WHERE type = 'status' and  data->>'vrs_num' is not NULL and to_timestamp(timestamp) > now() - interval '1 hrs';"
	active_testers, msg  = run_query(query)

	# iterate on testers until three are found who match
	for entry in active_testers: 
		tester_id = entry[0]
		query = "select tester_id, timestamp, data->>'wifi_ip', data->>'wifi_iface', data->>'mobile_ip', data->>'mobile_iface', data->>'battery_level', data->>'net_testing_proc' from status_update WHERE type = 'status' and  data->>'vrs_num' is not NULL and to_timestamp(timestamp) > now() - interval '15 min' and tester_id = '" + tester_id + "';"
		info, msg  = run_query(query)
		if len(info) == 0: 
			print("No info available for user %s in the last 15 minutes" %(tester_id))
			continue
		try: 
			user_data = info[-1]
			timestamp = user_data[1]
			wifi_ip = user_data[2] 
			wifi_iface = user_data[3]
			mobile_ip = user_data[4]
			mobile_iface = user_data[5]
			battery_level = int(user_data[6].strip())
			is_net_testing = int(user_data[7])
			print(timestamp, wifi_ip, wifi_iface, mobile_ip, mobile_iface, battery_level, is_net_testing)
		except AttributeError as e:
			print("WARNING -- AttributeError")
			continue

		# make sure at least one connection is working
		if wifi_ip == "none" and mobile_ip == "none":
			print("Something seems wrong for user %s. Both wifi and mobile IPs are missing" %(tester_id))
			continue	
		# make sure no net testing and enough battery 
		if(is_net_testing != 0 or battery_level < 20): 
			print("Low battery (%d) or net-testing (%d) detected. Skipping %s" %(battery_level, is_net_testing, tester_id))
			continue	
		
		# geolocate IPs -- TODO 

		# if we reach here, user is good
		tester_info = (tester_id, wifi_ip, wifi_iface, mobile_ip, mobile_iface)
		candidate_testers.append(tester_info)
		print("potentially candidate found. Added to list. New size: " + str(len(candidate_testers)))

		# check if we have a list ready for testing
		curr_time = int(time.time()) 				
		if len(candidate_testers) == VIDEOCONF_SIZE - 1: 
			print("ready to start the conference with: ")
			today = datetime.date.today()
			suffix = str(today.day) + '-' + str(today.month) + '-' + str(today.year)
			curr_id = int(time.time())
			
			# add common options: sync time, suffix, and test identifier
			sync_time = curr_id + 180 
			command = basic_command + " --id " + str(curr_id) + " --sync " + str(sync_time) + " --suffix " + suffix

			# compute duration 
			t_sleep = (sync_time - curr_time) + VIDEOCONF_DUR + SAFE_TIME 

			# add user specific options 
			for tester_info in candidate_testers: 
				uid_list = []			
				uid = tester_info[0]
				wifi_ip = tester_info[1]
				wifi_iface   = tester_info[2]
				mobile_ip    = tester_info[3]
				mobile_iface = tester_info[4]
				if wifi_ip != "none":
					command = basic_command + " --iface " + wifi_iface
				elif mobile_ip != "none":
					command = basic_command + " --iface " + mobile_iface 
				print(command)
				command_id = "root-" + str(curr_time)
 				uid_list.append(uid)
				print("insert_command " + command_id + ',' + uid_list + ',' + str(time.time()) + ',' + command + ',' + str(t_sleep) + ", false)")
				#info = insert_command(command_id, uid_list, time.time(), command, str(t_sleep), "false")

			# wait for experiment to be done 
			print("Sleeping for: " + str(t_sleep))
			#time.sleep(t_sleep)

			# add entry to the db (can we confirm all good?) -- TODO
			# clean list 
			candidate_testers.clear()
		
			print("Verify new size: " + str(len(candidate_testers)))
			break 

	# close connection to database 
	if postgreSQL_pool:
		postgreSQL_pool.closeall
		print("PostgreSQL connection pool is closed")
