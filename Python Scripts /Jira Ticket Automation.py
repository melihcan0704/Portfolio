from jira import JIRA
import pandas as pd

api_token='HIDDEN'

username = 'user-id' #your actual user ID not user name.

jira_connection = JIRA(basic_auth=('name@domain.com', api_token),server="https://your-company-domain.atlassian.net")

df = pd.read_csv('my-csv-file',header=None)
df2 = df.fillna('')
df3 = df2.replace(r"\n"," ",regex=True)

high_priority = ["VPN"]
root_cause_RCA = {'Connectivity 3G/4G': 10721,'Software': 10719,'Other':10727}
grafana = "grafana-cloud-link-to-direct-server-status-dashboard"


def link(ticket_key): #Allows keys on the output to be a hyperlink.
	hyperlink = f"https://domain.atlassian.net/browse/{ticket_key}" 
					# OSC 8 ; params ; URI ST <name> OSC 8 ;; ST 
	escape_mask = f"\u001b]8;;{hyperlink}\u001b\\{ticket_key}\u001b]8;;\u001b\\"
	return escape_mask


try:
	for i in range(1,len(df3)):
		tail_id = df3.loc[i,2]
		airline = df3.loc[i,0]
		if airline in ["AVA","VIV","CAL","VOE"]:
			summary= "[{}] ".format(df3.loc[i,0]) + str(tail_id) +" ({})".format(df3.loc[i,9]) +" {}".format(df3.loc[i,7]) #adds server number if P100
		else:
			summary= "[{}] ".format(df3.loc[i,0]) + str(tail_id) + " {}".format(df3.loc[i,7])
		spn_number= df3.loc[i,1]
		last_release = df3.loc[i,6]
		last_flight_date = df3.loc[i,3]
		last_vpn_connection = df3.loc[i,4]
		last_tracks = df3.loc[i,5]
		additional_info = df3.loc[i,8]
		priority = "High" if any(keyword in summary for keyword in high_priority) else "Medium" # list comprehension determine if ticket is High is any of the values in high_priority list exists anywhere in "summary".Update the high_priority list for any other ticket that needs to be "High" priority.
		root_cause = root_cause_RCA['Connectivity 3G/4G'] if 'VPN' in df3.loc[i,7] else root_cause_RCA['Software'] #similar to above if VPN exists in summary its a 3g/4g problem else its a software problem.
		label = "VPN" if 'VPN' in summary else "" #VPN label if VPN ticket
		grafana = grafana+str(spn_number)

		issue_dict = {
			'project': {'key': 'OC'},
			'summary': '{}'.format(summary),
			'description': f"""This AC is installed with *{spn_number}* \n
			*Last Release Received:* {last_release} \n
			*The last flight date:* {last_flight_date}
			*The last VPN connection:* {last_vpn_connection}
			*The last tracks:* {last_tracks}
			\n {additional_info}
			\n [Grafana |{grafana}]""",
			'issuetype': {'name': 'Incident'},
			'priority' : {'name':f"{priority}"},
			'assignee': {'id':f'{username}'},
			'customfield_10048': [tail_id], #aircraft field
			'customfield_10047': [{'value':airline}], #airline field
			'customfield_10243': {'value':'Aircraft'},
		 	'customfield_10026': "oc/systemproblem", #RequestType.
		 	"customfield_10082": {"id":"10679"}, #all passengers on board
			'customfield_10120': [{"id":str(root_cause)}], #Root Cause RCA 
			'labels' : [label]
			}


		new_issue = jira_connection.create_issue(fields=issue_dict)
		print(summary+' has been created successfully on: '+ link(str(new_issue)))
		
		if label in ("VPN",""): #All tickets will be linked to opened ticket if there are any.
			jql = """PROJECT in (#Internal-project-names) AND issuetype in (Incident, "Service Request") AND Status not in (Closed, Done, Resolved, Canceled) AND "Aircraft[Labels]" = {}""".format(tail_id)
			open_tickets = []
			get_issues = jira_connection.search_issues(jql)
			for issue_key in get_issues:
				open_tickets.append(str(issue_key))
				if new_issue != issue_key:
					jira_connection.create_issue_link(type="Relates",inwardIssue=str(new_issue),outwardIssue=str(issue_key))
			
			for key in open_tickets:
				if key == str(new_issue):
					open_tickets.remove(key)
			
			if len(open_tickets) > 0:
				print("Above ticket "+link(str(new_issue))+" is linked with: ", open_tickets)		
		else:
			pass
		
except Exception as e:
	print('An error has been encountered. Error: '+ str(e))
	

#Please see read_me.txt for additional info.
#Author: Melihcan Sarı
