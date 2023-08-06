import mock
from flask import Flask, request
from google.cloud import ndb
from google.cloud.ndb import metadata

import google.auth.credentials

import os
from ndbmodlesfile import *
from main import app

try:
    from htmlFile import *
except:
    pass

os.environ["DATASTORE_DATASET"] = "test"
os.environ["DATASTORE_EMULATOR_HOST"] = "127.0.0.1:8001"
os.environ["DATASTORE_HOST"] = "http://127.0.0.1:8001"
os.environ["DATASTORE_PROJECT_ID"] = "test"



credentials = mock.Mock(spec=google.auth.credentials.Credentials)
try:
    if html1:
        pass
except:
    html1="""
    <!DOCTYPE html>
    <html>
        <head></head>
        <body>
    """
try:
    if html2:
        pass
except:
    html2="""
 </body>
</html>
"""

@app.route('/ndbviewer',methods=['GET','POST'])
def ndbviewerdef():
    if request.method == 'GET':
        client = ndb.Client(project="test", credentials=credentials)
        with client.context():
            toprint=""

            toprint+=html1
            daKinds=metadata.get_kinds()
            toprint+="""
            Please choose the kind that you would like to view
            <form method="post" action="/ndbviewer">
            <input type="hidden" name="dadelete" value="no">
            <input type="hidden" name="fromget" value="yes">
                <select name="Kind">
            """
            for a in daKinds:
                toprint+="<option value='{a}'>{a}</option>".format(a=str(a))
            toprint+="""
            </select>
            <input type="submit">
            </form>
            """
            toprint+=html2

            return toprint
    if request.method == 'POST':
        client = ndb.Client(project="test", credentials=credentials)
        with client.context():
            
            disKind=request.form["Kind"]
            fromget=request.form["fromget"]

            toprint=""

            toprint+=html1
            checkdel=request.values
            daKinds=metadata.get_kinds()
            daprops=metadata.get_properties_of_kind(disKind)
            toprint+="""
            <style>
            table, th, td {
  border: 1px solid black;
}
            </style>
            Please choose the kind that you would like to view
            <form method="post" action="/ndbviewer">
            <input type="hidden" name="dadelete" value="no">
            <input type="hidden" name="fromget" value="no">
                <select name="Kind">
            """
            for a in daKinds:
                toprint+="<option value='{a}'>{a}</option>".format(a=a)
            toprint+="</select><br>where <select name='props'><option value='NA'>NA</option>"
            for d in daprops:
                toprint+=("""<option value="{d}">{d}</option>""".format(d=str(d)))
            toprint+="</select> equals <input type='text' name='propsearch'>"
            toprint+="""
            
            <input type="submit">
            </form>
            """
            
            
            toprint+="""
            <form method="post" action="/ndbviewer">
            <input type="hidden" name="dadelete" value="yes">
            <input type="hidden" name="fromget" value="no">
            <input type="hidden" name="props" value="NA">
            <input type="hidden" name="Kind" value="{disKind}">
            <table><tr>
            """.format(disKind=disKind)
            toprint+=("<th>"+"Select Entity"+"</th>")
            toprint+=("<th>"+"URLSafe Key"+"</th>")
            for c in daprops:
                toprint+=("<th>"+str(c)+"</th>")
            toprint+=("""
            </tr>
            """)
            addsearch=""
            if fromget=="no":
                props=request.form["props"]
                if props!="NA":
                    propsearch=request.form["propsearch"]
                    addsearch=" where {props} = '{propsearch}'".format(propsearch=propsearch,props=props)
                
            BasicSearch=ndb.gql("Select * from {disKind}{addsearch}".format(disKind=disKind,addsearch=addsearch))
            for b in BasicSearch:

                gotdeleted=False
                dakey=b.key.urlsafe().decode("utf-8")
                
                dadelete=request.form["dadelete"]
                if dadelete=="yes":
                    
                    if dakey in checkdel:
                        todel=ndb.Key(urlsafe=dakey).get()
                        todel.key.delete()
                        gotdeleted=True
                
            
                if gotdeleted==False:
                    toprint+=("""
                    <tr>
                    """)
                    toprint+=("""<td><input type="checkbox" name="{dakey}" value="{dakey}"> </td>""".format(dakey=dakey))
                    toprint+=("<td>"+str(dakey)+"</td>")
                    for c in daprops:
                        davar=getattr(b,c)
                        toprint+=("<td>"+str(davar)+"</td>")
                toprint+=("""
                 </tr>
                """)
            toprint+=("</table> <input type='submit' value='delete selected'></form>")

            toprint+=(html2)

            return toprint


