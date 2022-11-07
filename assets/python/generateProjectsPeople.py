import pandas as pd
import shutil
import os

rootOut = "/home/runner/work/geolabWeb/geolabWeb/geolabWeb/"

#Remove older files
try:
    shutil.rmtree(rootOut + "_people/")
    shutil.rmtree(rootOut + "_posts/projects")
except:
    print("Nothing to remove.")
os.mkdir(rootOut + "_people/")
os.mkdir(rootOut + "_posts/projects")

#Grab the CSVs
ssID = "1g8L6cfelu4E4d8dAU8G8NgDER418alHFid69LP_axm0"

peopleCSV = "https://docs.google.com/spreadsheets/d/" + ssID + "/gviz/tq?tqx=out:csv&sheet=" + "People"
projectCSV = "https://docs.google.com/spreadsheets/d/" + ssID + "/gviz/tq?tqx=out:csv&sheet=" + "Projects"
linkCSV = "https://docs.google.com/spreadsheets/d/" + ssID + "/gviz/tq?tqx=out:csv&sheet=" + "CensusDefinitions"

people = pd.read_csv(peopleCSV)
projects = pd.read_csv(projectCSV)
linkData = pd.read_csv(linkCSV)

for _, row in projects.iterrows():
    print(row['Project Name*'])

    outStr = "---\n"
    outStr = outStr + 'title: "' + row['Project Name*'] + '"\n'
    outstr = outStr + 'excerpt: "' + row['Excerpt*'] + '"\n'
    
    #funders
    if(isinstance(row['Funded By'], str)):
        funders = row['Funded By'].split(',')
        fundStr = "funders: "
        for i in funders:
            fundURL = linkData[linkData["Funders"]==i]["Funder Links"].values[0]
            fundStr = fundStr + "<a href='" + fundURL + "'>" + i + "</a>" + "<br />"
        
        outStr = outStr + fundStr + '\n'

    #header:
    if(isinstance(row["Image (350 x 250)*"] , str)):
        outStr = outStr + "header:" + "\n"
        outStr = outStr + "  teaser: " + "/assets/images/projectImages/" + row["Image (350 x 250)*"] + '\n'
    outStr = outStr + "categories: " + row['Theme(s)'] + '\n'
    outStr = outStr + "entryType: project" + '\n'
    outStr = outStr + "layout: singleProjects" + '\n'
    outStr = outStr + "permalink: /projects/" + row["Project Tag"] + "/" + "\n" 
    outStr = outStr + "tags: " + row['Descriptive Tags (space delimited)'] + '\n'
    outStr = outStr + "sidebar:\n"
    outStr = outStr + '  - title: "' + row['Project Name*'] + '"' + '\n'
    if(isinstance(row["Image (350 x 250)*"] , str)):
        outStr = outStr + '    image: /assets/images/projectImages/' + row["Image (350 x 250)*"] + '\n'
        outStr = outStr + '    image_alt: logo\n'
    
    text = '    text: "<b>Description</b><br />' + row['Excerpt*'] 
    text = text + "<br /><b>Timeline:</b><br />" + row["Start Semester"] + " to " + row["End Semester"] + "<br />"
    
    #Add people to the text

    text = text + "<b>People:</b><br />"
    for people_, peopleRow in people.iterrows():
        if(isinstance(peopleRow["Projects"], str)):
            allProjects = peopleRow["Projects"].split(',')
            for b in allProjects:
                if(b in row["Project Tag"]):
                    text = text + "<a href='/people/" + peopleRow["permalink"] + ".html'>" + peopleRow["Name"] + "</a>, "
    
    #Remove the last trailing comma
    text = text[:-2]
    
    text = text + '"\n---\n'

    text = text + row["Full Description (Can add links using HTML)*"]

    outStr = outStr + text

    startDate = row["Start Semester"].split(" ")[1] + "-01-01-"

    with open(rootOut + "_posts/projects/" + startDate + row["Project Tag"] + ".md", "w") as f:
        f.write(outStr)
        

#People
for _, row in people.iterrows():
    if(isinstance(row["Name"], str)):
        print(row["Name"])
        outStr = "---\n"
        outStr = outStr + "layout: author\n"
        outStr = outStr + "name: " + row["Name"] + "\n"
        if(isinstance(row["shortBio"], str)):
            outStr = outStr + "bio: " + row["shortBio"] + "\n"
        outStr = outStr + "type: " + row["WebType"] + "\n"
        outStr = outStr + "webOrder: " + str(row["WebOrder"]) + "\n"
        if(isinstance(row["imagePath"], str)):
            outStr = outStr + "avatar: /assets/images/peopleImages/" + row["imagePath"] + "\n"
            outStr = outStr + "imageMask: " + str(row["imageMask"]) + "\n"
        if(isinstance(row["Title"], str)):
            outStr = outStr + "profTitle: " + row["Title"] + "\n"
        outStr = outStr + "permalink: /people/" + row["permalink"] + ".html \n"
        outStr = outStr + "links:\n"
        if(isinstance(row["email"], str)):
            outStr = outStr + "  - label: 'Email'\n"
            outStr = outStr + "    icon: 'fas fa-fw fa-envelope square'\n"
            outStr = outStr + "    url: mailto:" + row["email"] + "\n"
        if(isinstance(row["twitter"], str)):
            outStr = outStr + "  - label: 'Twitter'\n"
            outStr = outStr + "    icon: 'fab fa-fw fa-twitter-square'\n"
            outStr = outStr + "    url: 'https://www.twitter.com/@" + row["twitter"] + "'\n"
        if(isinstance(row["otherWeb"], str)):
            outStr = outStr + "  - label: 'Website'\n"
            outStr = outStr + "    icon: 'fas fa-fw fa-link'\n"
            outStr = outStr + "    url: " + row["otherWeb"] + "\n"

        #Projects
        if(isinstance(row["Projects"], str)):
            outStr = outStr + "projects:\n"
            projectString = row["Projects"].split(',')
            for i in projectString:
                projFullName = projects[projects["Project Tag"]==i]["Project Name*"].values[0]
                outStr = outStr + '  - name: "' + projFullName + '"\n'
                outStr = outStr + "    link: /projects/" + i +"/\n"

        outStr = outStr + "---\n"
        if(isinstance(row["longBio"], str)):
            outStr = outStr + row["longBio"] 

        with open(rootOut + "_people/" + row["permalink"] + ".md", "w") as f:
            f.write(outStr)
