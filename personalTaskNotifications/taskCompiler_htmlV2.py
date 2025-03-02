# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 16:04:19 2025

@author: Pete
@purpose: script is meant to grab tasks from notion for pete's personal
    list, organize them in a specific way and send an email with the tasks 
    to be completed 
"""

# ==========================================================================================
# ==========================================================================================
# everything that does not involve sending a failure email should exist in the try [beginning]
# ==========================================================================================
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
fm = 'C:\\Users\\Pete'
pwdPath = fm + '\\Documents\\systemScripts\\secrets.json'
pwdDf = pd.read_json(pwdPath)
emailUser = pwdDf[['personalGmail']].filter(like = 'user', axis = 0).to_string(index=False, header= False).strip()
emailPw = pwdDf[['personalGmail']].filter(like = 'password', axis = 0).to_string(index=False, header= False).strip()
emailRecipient = emailUser
# ==========================================================================================
# everything that does not involve sending a failure email should exist in the try [end]
# ==========================================================================================
# ==========================================================================================

try:
    # import the additional modules 
    import requests
    import numpy as np 
    pd.set_option('display.max_colwidth', -1)
    # email
    from email.mime.base import MIMEBase 
    from email import encoders 
    from datetime import datetime, timedelta, timezone
    
    # define a few variables 
    currTime = datetime.now()
    time_formalTime = currTime.strftime("%A in %B [%Y%m%d]")
    
    # ==========================================================================================
    # notion sweep [beginning]
    # ==========================================================================================
    # ==========================================================================================
    # first find the page that the database is on 
    # must share the page with "Pete's First Integration" in the "Connections" menu
    # ==========================================================================================
    apiToken = pwdDf[['notion']].filter(like = 'apiToken', axis = 0).to_string(index=False, header= False).strip()
    pageId = "19bb089c8ffd81c1a9d0d8c040d64ed2"
    url = f"https://api.notion.com/v1/databases/{pageId}"
    headers = {
        "Authorization": "Bearer " + apiToken,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }
    
    response = requests.get(url, headers=headers)
    print(response.json())
    resDetails = response.json()
    
    # then grab the tickets i care about 
    # ==========================================================================================
    url = f"https://api.notion.com/v1/databases/{pageId}/query"
    headers = {
        "Authorization": "Bearer " + apiToken,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    response = requests.post(url, headers=headers)
    print(response.json())
    resDetails = response.json()    

    # see how many results came back! 
    print(str(len(resDetails['results'])) + ' tasks & sub-tasks were found!')
    taskDf1 = pd.DataFrame(columns = ['taskName', 'status', 'parentId', 'id', 'otherTags', 'assignee', 'priority', 'url'])
    subTaskMappingDf = pd.DataFrame(columns = ['parentId', 'id'])
    
    # iterate through the objects and print details about them
    for i in range(0, len(resDetails['results'])):
        print('Block #' + str(i))
        # print(resDetails['results'][i]['properties']['Status']['status']['name'])
        # grab name 
        # grab priority level 
        if len(resDetails['results'][i]['properties']['Name']['title']) == 0:
            string_name = ''
        else: 
            string_name = resDetails['results'][i]['properties']['Name']['title'][0]['text']['content']
        print(string_name)
        # grab status 
        temp_status = resDetails['results'][i]['properties']['Status']['status']['name']
        # print(temp_status)
        # grab id 
        temp_id = resDetails['results'][i]['id']
        # grab parent id 
        temp_parent_id = resDetails['results'][i]['properties']['Parent item']['id']
        # grab other tags 
        temp_other_tags = resDetails['results'][i]['properties']['Tags']['multi_select'] # need to loop over to comma seperate or somethin' 
        # grab the url
        temp_url = resDetails['results'][i]['url']
        # print(len(temp_other_tags))
        # print(temp_other_tags)
        # create a comma seperated string with all the tags 
        string_oTag = ''
        if len(temp_other_tags) > 0:
            # print('lets try sumthin ')
            for oTag in temp_other_tags:
                # print(oTag)
                var_oTag = oTag['name']
                string_oTag = string_oTag + var_oTag + ', '
                # print(string_oTag)
                # print(oTag['name'])
            # reg ex to remove the last 2 characters 
            string_oTag = string_oTag[:-2]
        # print('my o tag is ..' + string_oTag)
        # grab assignee 
        temp_assignee = resDetails['results'][i]['properties']['Assign']['multi_select'] # need to loop over to comma seperate or somethin' 
        print(temp_assignee)
        # create a comma seperated string with all the tags 
        string_assignee = ''
        if len(temp_assignee) > 0:
            # print('lets try sumthin ')
            for assignee in temp_assignee:
                # print(oTag)
                var_assignee= assignee['name']
                string_assignee = string_assignee + var_assignee + ', '
                # print(string_oTag)
                # print(oTag['name'])
            # reg ex to remove the last 2 characters 
            string_assignee = string_assignee[:-2]
        print('my assignee is ..' + string_assignee)
        # grab priority level 
        string_priority = 99  # not actually a string 
        temp_priority = resDetails['results'][i]['properties']['Priority Level']['number']
        if temp_priority is not None:
            string_priority = temp_priority
        print(string_priority)
        print(resDetails['results'][i]['properties']['Parent item']['id'])
        temp_df = pd.DataFrame(data = [[string_name, temp_status, temp_parent_id, temp_id, string_oTag, string_assignee, string_priority, temp_url]], columns = ['taskName', 'status', 'parentId', 'id', 'otherTags', 'assignee', 'priority', 'url'])
        taskDf1 = taskDf1.append(temp_df)
        # print(len(resDetails['results'][i]['properties']['Sub-item']['relation']))
        temp_child = ''
        if len(resDetails['results'][i]['properties']['Sub-item']['relation']) > 0:
            for j in range(0, len(resDetails['results'][i]['properties']['Sub-item']['relation'])):
                # print(j)
                # print(resDetails['results'][i]['properties']['Sub-item']['relation'][j]['id'])
                temp_child = resDetails['results'][i]['properties']['Sub-item']['relation'][j]['id']
                temp_child_df = pd.DataFrame(data = [[temp_id, temp_child]], columns = ['parentId', 'id'])
                subTaskMappingDf = subTaskMappingDf.append(temp_child_df)
    
    # omit "done" items 
    taskDf1 = taskDf1[(taskDf1['status'] != 'Done') ]
    # create a "numeric status" column for sorting statuses 
    statusSortDf = pd.DataFrame({
        "status": ["Not started", "In progress", "Backlog", "Pinned"], 
        "rank": [2, 1, 3, 4]
        })
    taskDf1 = taskDf1.merge(statusSortDf, how = 'left', on = 'status')
    
    # do some sorting 
    # ==========================================================================================
    taskDf1 = taskDf1.sort_values(by = ['rank', 'priority', 'otherTags', 'assignee', 'taskName'])

    # associate parents to children
    # ==========================================================================================
    # create a flag for a "header task" 
    # find distinct childrens 
    childDf1 = pd.DataFrame(subTaskMappingDf['id'].drop_duplicates())
    childDf1 = childDf1.rename(columns={"id": "childId"})
    # filter out any parent's that are also in the children 
    taskDf2 = taskDf1.merge(childDf1, how = 'left', left_on = 'id', right_on = 'childId')
    taskDf2['headerTaskFlag'] = 0
    taskDf2.loc[taskDf2['childId'].isnull(), 'headerTaskFlag'] = 1
    # drop the child id column
    taskDf2 = taskDf2.drop(columns = 'childId')
    taskDf2 = taskDf2.drop(columns = 'parentId')
    # bring in the real parent id 
    taskDf3 = taskDf2.merge(subTaskMappingDf, how = 'left', left_on = 'id', right_on = 'id')

    # filter to header tasks 
    # ==========================================================================================
    headerTaskDf1 = taskDf3[(taskDf3['headerTaskFlag'] == 1) ]

    # ==========================================================================================
    # notion sweep [end]
    # ==========================================================================================    


    # ==========================================================================================
    # construct & send email [beginning]
    # ==========================================================================================    
    
    # start the html string 
    bodyStr = str('<html><body>')
    # iterate over status 
    # ==========================================================================================
    for i in headerTaskDf1['status'].unique():
        print(i)
        fontColorVar = "#66ff33" # 404041 .. but auto updates to a lighter text due to dark mode ... change to a color gradient and this should resolve itself
        if i == 'Not started':
            fontColorVar = "#7e7e81"
        elif i == 'Backlog':
            fontColorVar = "#bfbfc0"
        elif i == 'Pinned':
            fontColorVar = "#d8d8d9"
        headerFontColorVar = "#4e148c"
        if i == 'Not started':
            headerFontColorVar = "#701dc9"
        elif i == 'Backlog':
            headerFontColorVar = "#964de6"
        elif i == 'Pinned':
            headerFontColorVar = "#be8fef" 
        
        listItemStr = '<p><font color = "' + headerFontColorVar + '"><b><font size = 3>' + i + "</font></b></font></p>"
        bodyStr = bodyStr + listItemStr
        listItemStr = "<ul>" + '<font color = "' + fontColorVar + '">' +  '<font size = 2>'
        bodyStr = bodyStr + listItemStr        
        # loop over the actual tasks 
        # ==========================================================================================
        for j in headerTaskDf1[(headerTaskDf1['status'] == i)]['id']:
            print(j)
            stageDf = headerTaskDf1[(headerTaskDf1['id'] == j) ]
            taskName = headerTaskDf1[(headerTaskDf1['id'] == j)]['taskName'].to_string(index=False, header= False).strip()
            taskUrl = headerTaskDf1[(headerTaskDf1['id'] == j)]['url'].to_string(index=False, header= False).strip()
            print(taskName)
            print(taskUrl)
            # add the task name 
            # ==========================================================================================            
            # taskStr = "<li>" + taskName + " ~~ " + taskUrl + "</li>"
            taskStr = "<li>" + taskName  + ' <a href="' + taskUrl + '" style="text-decoration:none;">' + '&#128267;' + '</a>' + "</li>"
            bodyStr = bodyStr + taskStr         
            # add the tags & subitems 
            # ==========================================================================================            
            if (headerTaskDf1[(headerTaskDf1['id'] == j)]['otherTags'].to_string(index=False, header= False).strip() == '') & (headerTaskDf1[(headerTaskDf1['id'] == j)]['otherTags'].to_string(index=False, header= False).strip() == ''):
                print('no tags or subitems!')
            else:
                print('found something!')
                listItemStr = "<ul>"
                bodyStr = bodyStr + listItemStr           
                # add any tags 
                # ==========================================================================================            
                if headerTaskDf1[(headerTaskDf1['id'] == j)]['otherTags'].to_string(index=False, header= False).strip() != '':
                    taskTags = headerTaskDf1[(headerTaskDf1['id'] == j)]['otherTags'].to_string(index=False, header= False).strip()
                    taskStr = "<li>" + "<font size = 1>Tags: <i>" + taskTags + "</i></font></li>"
                    bodyStr = bodyStr + taskStr          
                else: 
                    print('do nothing ... no tags')
                # end of tags
                # ==========================================================================================            
                # add any sub-times 
                if len(taskDf3[(taskDf3['parentId'] == j) ]['id']) == 0:
                    # no subtasks 
                    textVar2 = 'no subtasks for this group'
                    print(textVar2)
                else: 
                    for k in taskDf3[(taskDf3['parentId'] == j) ]['id']:
                        print(k)
                        stageSubtaskDf = taskDf3[(taskDf3['id'] == k)]
                        subtaskTaskName = stageSubtaskDf['taskName'].to_string(index=False, header= False).strip() 
                        subtaskUrl = stageSubtaskDf['url'].to_string(index=False, header= False).strip() 
                        subtaskStatus =  stageSubtaskDf['status'].to_string(index=False, header= False).strip()
                        textVar2 = subtaskTaskName + ' (' + subtaskStatus + ') ' +  '<a href="' + subtaskUrl + '" style="text-decoration:none;">' + '&#128267;' + '</a>'
                        print(textVar2)
                        listItemStr = "<li>" + "<font size = 1>" + textVar2 + "</font>" + "</li>"
                        bodyStr = bodyStr + listItemStr
                # end of sub-items
        
                listItemStr = "</ul>"
                bodyStr = bodyStr + listItemStr       
        
        listItemStr = "</ul>" + "</font>" + "</font>"
        bodyStr = bodyStr + listItemStr
                

            
            
    bodyStr = bodyStr + "</body></html>"
    
    # send the mail 
    msg = MIMEMultipart("alternative")
    msg["Subject"] = '=?utf-8?Q?=F0=9F=A4=B9?=' + " Personal To Do's for a " + time_formalTime
    msg["From"] = "Some Personal To Do's <" + emailUser + ">"
    msg["To"] = "Human Peter <" + emailRecipient + ">"
    bodyMime = MIMEText(bodyStr, "html")
    msg.attach(bodyMime)
    
    # send the actual note
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        # server.login(emailUser, emailPw)
        server.login(emailUser, emailPw)
        server.sendmail(emailUser, emailRecipient, msg.as_string())
        # ...send emails
    except:
        print('Something went wrong...')
        
        

        
    # ==========================================================================================
    # construct & send email [end]
    # ==========================================================================================    


    
    # ==========================================================================================
    # grab some 
    # sample error below 
    # aa = bb

except Exception as e:
    # print(e)
    errorText = str(e)
    # emailText = '<html><font color = "#404041"><font face = "monospace">Something went wrong with the Phrase Mapping Load process. Please review and try again. The script lives here "C:\\Users\\peter.standbridge\\Documents\\reportingAndAnalyticsTeam\\peteSandbox\\adHoc\\202501_addressLatLong"</font>' + str(e)
    # string the email text together 
    emailText = '<html><font color = "#404041"><font face = "monospace">' 
    emailText = emailText + '<p>Something went wrong with the Personal Task Notification process. Please see the error message below:<p/>'
    emailText = emailText + '<p><bold><font color = "#e65c00">' + errorText + '</font></bold></p>'
    emailText = emailText + '<p>Please review the script here: "C:\\Users\\Pete\\Documents\\GitHub\\percySandbox\\personalTaskNotifications"<p/>'
    emailText = emailText + '</font></font>'
    # end of the string 
    subjectTxt = '=?utf-8?Q?=F0=9F=8E=BA?='  + " Something's wrong with the Personal Task Notification process"
    #F0 9F 8E BA
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subjectTxt
    msg["From"] = "Automated Notification <" + emailUser + ">"
    msg["To"] = "Automated Recipients <" + emailRecipient + ">"
    bodyMime = MIMEText(emailText, "html")
    msg.attach(bodyMime)
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(emailUser, emailPw)
    server.sendmail(emailUser, emailRecipient, msg.as_string())

