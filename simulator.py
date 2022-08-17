# SGLSim_Basic/worker.py
import sys, os, ssl
import email, smtplib
import json, redis
import xlwt
import shutil
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

pathnameto_eppy = '../'
sys.path.append(pathnameto_eppy)

from eppy import modeleditor
from eppy.modeleditor import IDF
from eppy.results import readhtml
from xlwt import Workbook

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from zipfile import ZipFile
from os.path import basename

r = redis.Redis()
iddfile = "/usr/local/EnergyPlus-9-2-0/Energy+.idd"
IDF.setiddname(iddfile)

def zipResults():
    with ZipFile('answers.zip','w') as zipObj:
        dirName = '/home/shinigami/SGLSim/results/'
        for foldername, subfolfers, filenames in os.walk(dirName):
            for filename in filenames:
                filepath = os.path.join(foldername, filename)
                zipObj.write(filepath, basename(filepath))


def sendMail(email):
    subject = "Simulation Results"
    body = "This is an email with attachment sent from eSimApp"
    sender_email = os.environ.get('EMAIL_USER')
    receiver_email = email
    password = os.environ.get('EMAIL_PASS')
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    filename = "answers.zip"
    with open(filename, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())


    encoders.encode_base64(part)
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    message.attach(part)
    text = message.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)
    print(f"Result Mailed to the user {email}")

# def idf_simulator(city, n_axis, wwr, w_prop, hvac, email, floor_area):
def idf_simulator(city, n_axis, wwr, w_prop, hvac, floor_area):
    netenergy_list = []
    ########################## IDF File List Creation ###########################
    dir = "/home/shinigami/SGLSim/SF/"
    files = os.listdir(dir)
    file_list = []
    for i in files:
        if i.endswith(".idf"):
            file_list.append(i)

    file_list.sort(key=lambda x : int(x.split(".")[0]))

    for filename in file_list:
        if filename.endswith(".idf"):
            ###################### Setting up Simulation Location #######################
            epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Hyderabad_ISHRAE.epw"
            if city == 'Ahmedabad':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Ahmedabad_ISHRAE.epw"
            elif city == 'Akola':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Akola_ISHRAE.epw"
            elif city == 'Allahabad':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Allahabad_ISHRAE.epw"
            elif city == 'Amritsar':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Amritsar_ISHRAE.epw"
            elif city == 'Aurangabad':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Aurangabad_ISHRAE.epw"
            elif city == 'Bangalore':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Bangalore_ISHRAE.epw"
            elif city == 'Barmer':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Barmer_ISHRAE.epw"
            elif city == 'Belgaum':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Belgaum_ISHRAE.epw"
            elif city == 'Bhagalpur':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Bhagalpur_ISHRAE.epw"
            elif city == 'Bhopal':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Bhopal_ISHRAE.epw"
            elif city == 'Bhubneshwar':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Bhubneshwar_ISHRAE.epw"
            elif city == 'Bikaner':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Bikaner_ISHRAE.epw"
            elif city == 'Chennai':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Chennai_ISHRAE.epw"
            elif city == 'Chirtadurg':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Chirtadurg_ISHRAE.epw"
            elif city == 'Dehradun':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Dehradun_ISHRAE.epw"
            elif city == 'Dibrugarh':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Dibrugarh_ISHRAE.epw"
            elif city == 'Gorakhpur':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Gorakhpur_ISHRAE.epw"
            elif city == 'Guwahati':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Guwahati_ISHRAE.epw"
            elif city == 'Gwalior':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Gwalior_ISHRAE.epw"
            elif city == 'Hissar':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Hissar_ISHRAE.epw"
            elif city == 'Hyderabad':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Hyderabad_ISHRAE.epw"
            elif city == 'Imphal':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Imphal_ISHRAE.epw"
            elif city == 'Indore':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Indore_ISHRAE.epw"
            elif city == 'Jabalpur':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Jabalpur_ISHRAE.epw"
            elif city == 'Jagdelpur':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Jagdelpur_ISHRAE.epw"
            elif city == 'Jaipur':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Jaipur_ISHRAE.epw"
            elif city == 'Jaisalmer':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Jaisalmer_ISHRAE.epw"
            elif city == 'Jamnagar':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Jamnagar_ISHRAE.epw"
            elif city == 'Jodhpur':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Jodhpur_ISHRAE.epw"
            elif city == 'Jorhat':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Jorhat_ISHRAE.epw"
            elif city == 'Kolkata':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Kolkata_ISHRAE.epw"
            elif city == 'Kota':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Kota_ISHRAE.epw"
            elif city == 'Kurnool':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Kurnool_ISHRAE.epw"
            elif city == 'Lucknow':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Lucknow_ISHRAE.epw"
            elif city == 'Mangalore':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Mangalore_ISHRAE.epw"
            elif city == 'Nagpur':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Nagpur_ISHRAE.epw"
            elif city == 'Nellore':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Nellore_ISHRAE.epw"
            elif city == 'NewDelhi':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_NewDelhi_ISHRAE.epw"
            elif city == 'Panjim':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Panjim_ISHRAE.epw"
            elif city == 'Patna':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Patna_ISHRAE.epw"
            elif city == 'Pune':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Pune_ISHRAE.epw"
            elif city == 'Raipur':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Raipur_ISHRAE.epw"
            elif city == 'Rajkot':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Rajkot_ISHRAE.epw"
            elif city == 'Ramagundam':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Ramagundam_ISHRAE.epw"
            elif city == 'Ranchi':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Ranchi_ISHRAE.epw"
            elif city == 'Ratnagiri':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Ratnagiri_ISHRAE.epw"
            elif city == 'Raxaul':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Raxaul_ISHRAE.epw"
            elif city == 'Saharanpur':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Saharanpur_ISHRAE.epw"
            elif city == 'Shillong':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Shillong_ISHRAE.epw"
            elif city == 'Sholapur':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Sholapur_ISHRAE.epw"
            elif city == 'Sundernagar':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Sundernagar_ISHRAE.epw"
            elif city == 'Surat':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Surat_ISHRAE.epw"
            elif city == 'Tezpur':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Tezpur_ISHRAE.epw"
            elif city == 'Tiruchirapalli':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Tiruchirapalli_ISHRAE.epw"
            elif city == 'Trivandram':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Trivandram_ISHRAE.epw"
            elif city == 'Veraval':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Veraval_ISHRAE.epw"
            elif city == 'Vishakhapatnam':
                epwwfile = "/home/shinigami/SGLSim/epwFiles/IND_Vishakhapatnam_ISHRAE.epw"
            #########################  Doing Simulation  ########################
            print(filename)
            path= os.path.join(dir,filename)
            idf1 = IDF(path)
            idf = IDF(path, epwwfile)
            idf.run()
            ##################### Reading Simulation Result #####################
            fname = "/home/shinigami/SGLSim/eplustbl.htm"
            fileOpener = open(fname, 'r').read()
            if int(hvac) == 2:
                HTMLTables = readhtml.titletable(fileOpener)
                EndUsesTable = HTMLTables[3]
                EndUseRowWise = EndUsesTable[1]

                DistrictCooling = EndUseRowWise[2][4]
                LightingLoad = EndUseRowWise[3][1]
                EquipmentLoad = EndUseRowWise[5][1]
                CoolingLoad = int(DistrictCooling) / 2.5

                endUseCol = HTMLTables[7]
                endUseTable = endUseCol[1]
                endUse = endUseTable[3]
                photovoltaicsGeneration = endUse[1]

                netSiteEnergy = (int(CoolingLoad) + int(LightingLoad) + int(EquipmentLoad) - int(photovoltaicsGeneration))/int(floor_area)
                netenergy_list.append(round(netSiteEnergy,2))
            else:
                htables = readhtml.titletable(fileOpener)
                firstitem = htables[0]
                firstitem_table = firstitem[1]
                thirdrow = firstitem_table[2]
                thirdrow_secondcolumn = thirdrow[1]
                netSiteEnergy = int(thirdrow_secondcolumn)/int(floor_area)
                netenergy_list.append(round(netSiteEnergy,2))

            ############### Storing the Simulation HTML Files ##################
            savingDirectory = "/home/shinigami/SGLSim/SF/HTML_Files/" + str(filename) + ".htm"
            shutil.copy2(fname, savingDirectory)
            ################## Deleting the Simulation Files ####################
            sim_dir = "/home/shinigami/SGLSim/"
            for fname in os.listdir(sim_dir):
                if fname.startswith("eplus"):
                    os.remove(os.path.join(sim_dir, fname))
                elif fname.startswith("sqlite"):
                    os.remove(os.path.join(sim_dir, fname))
                else:
                    continue
    print (netenergy_list)
    idf_result(n_axis, wwr, netenergy_list, w_prop)
    # idf_result(n_axis, wwr, netenergy_list, w_prop, email)

# def idf_result(n_axis, wwr, netenergy_list, w_prop, email):
def idf_result(n_axis, wwr, netenergy_list, w_prop):
    n = len(n_axis)
    m = len(wwr)
    p = len(w_prop)//3
    print("No of Orientation(n) is", n)
    print("wwr length(m) is", m)
    print("no of windows(p) are",p)
    orientation = []
    for direction in n_axis:
        a = int(direction)
        if ((a >= 0 and a < 45) or (a >=315 and a < 360)):
            b = "North" + "-" + str(a) + chr(176)
            orientation += [str(b)]
        elif (a >= 45 and a < 135):
            b = "East" + "-" + str(a) + chr(176)
            orientation += [str(b)]
        elif (a >= 135 and a < 225):
            b = "South" + "-" + str(a) + chr(176)
            orientation += [str(b)]
        elif (a >= 225 and a < 315):
            b = "West" + "-" + str(a) + chr(176)
            orientation += [str(b)]

    ################### Saving Simulation results in excel ######################
    netenergy_list = np.array(netenergy_list)
    netenergy_list = netenergy_list.reshape((n*p,m))
    wb = Workbook()
    sheet1 = wb.add_sheet('Net Site Energy')

    for i in range(netenergy_list.shape[0]):
        for j in range(netenergy_list.shape[1]):
            sheet1.write(j, i, str(netenergy_list[i,j]))
    wb.save('netSiteEnergy.xls')
    ########################## Plotting the Graphs ##############################
    df = pd.read_excel('netSiteEnergy.xls', header = None)
    cols = df.columns
    glass_list = []
    x = 1
    w = 0
    while p >= x:
        glass_list.append("U-Value~" + str(w_prop[w]) + " SHGC~" + str(w_prop[w+1])
                            + " VLT~" + str(w_prop[w+2]))
        x = x + 1
        w = w + 3
    i = 0
    k = 0
    while i < (len(cols)):
        mp = 0
        fig = go.Figure()
        while mp < p:
            fig.add_trace(go.Scatter(x=wwr, y=df[cols[mp]], mode='lines+markers',
                                        name=glass_list[mp % p]))
            mp = mp + 1
        fig.update_layout(title = orientation[k], xaxis_title = "Window to Wall Ratio",
                            yaxis_title = "Net Site Energy(kWh/sq m)",
                            legend_title='<b> Glass Type </b>', font = dict(
                            family="Courier New, monospace",
                            size = 18,
                            color = "RebeccaPurple"
                            ))
        fig.write_html("/home/shinigami/SGLSim/results/{}.html".format(i*100))
        fig.show()
        i = i + mp
        k = k + 1
        if (i == len(cols)):
            break
    # zipResults()
    # sendMail(email)


def idf_generator(**kw):
    fname1 = "/home/shinigami/SGLSim/1.idf"
    idf1 = IDF(fname1)
    ############################### Reading Inputs ##############################
    name = kw['name']
    city = kw['location']
    hvac = kw['hvac']
    daylight = int(kw['daylight_control'])
    building_type = str(kw['building_type'])
    blind_control = int(kw['blind_control'])
    dimen_sions = []
    dimen_sions.append(kw['length'])
    dimen_sions.append(kw['height'])
    orientation = kw['orientation']
    wwr = kw['wwr']
    pv = kw['pv']
    n_axis = orientation
    w_prop = []
    for (shgc,uval,vlt) in zip(kw['shgc'],kw['uvalue'],kw['vlt']):
        w_prop.append(uval)
        w_prop.append(shgc)
        w_prop.append(vlt)
    print(  f' Building Name is {name} and has HVAC {hvac}'
            f' Simulation location is {city} &'
            f' Orientation is {orientation}'
            f' Length, Height is as follows {dimen_sions[0]}, {dimen_sions[1]}'
            f' Daylighting Control is {daylight}'
            f' Building Type is {building_type}'
            f' Blind Control is {blind_control}'
            f' SHGC is {w_prop[0]}'
            f' UValue is {w_prop[1]}'
            f' VLT is {w_prop[2]}'
            f' PV is {pv}')
    ############################ Building Name ##################################

    building = idf1.idfobjects['BUILDING'][0]
    building.Name = str(name)

    ############################ Photovoltaic ###################################
    total_window = len(w_prop)//3
    pv_property = len(pv)
    print(pv_property)
    total_pv = pv_property/5
    Dec = []
    i=0
    while i <(total_window):
        Dec.append('No')
        i = i + 1
    i=0
    if total_pv != 0:
        while i < (total_pv):
            Dec[i] = str('Yes')
            i = i + 1
    print("No of Photovoltaic is", Dec)
    ################################### HVAC ####################################
    if int(hvac) == 3:
        PTAC = idf1.newidfobject('HVACTEMPLATE:ZONE:PTAC')
        PTAC.Zone_Name = str('Testzone')
        PTAC.Template_Thermostat_Name = str('Last thermo')
        print(" We are using PTAC")
    if int(hvac) == 1:
        PTHP = idf1.newidfobject('HVACTEMPLATE:ZONE:PTHP')
        PTHP.Zone_Name = str('Testzone')
        PTHP.Template_Thermostat_Name = str('Last thermo')
        print("We are using PTHP")
    if int(hvac) == 2:
        ILAS = idf1.newidfobject('HVACTEMPLATE:ZONE:IDEALLOADSAIRSYSTEM')
        ILAS.Zone_Name = str('Testzone')
        ILAS.Template_Thermostat_Name = str('Last thermo')
        print("We are using ILAS")

    ############################ Changing Dimensions ############################
    L= dimen_sions[0]
    H= dimen_sions[1]
    DL= daylight
    print(L,H,DL)

    dimN = idf1.idfobjects['WALL:EXTERIOR'][0]
    dimN.Starting_X_Coordinate = float(L)
    dimN.Starting_Y_Coordinate = float(L)
    dimN.Length = float(L)
    dimN.Height = float(H)

    dimE = idf1.idfobjects['WALL:EXTERIOR'][1]
    dimE.Starting_X_Coordinate = float(L)
    dimE.Length = float(L)
    dimE.Height = float(H)

    dimS = idf1.idfobjects['WALL:EXTERIOR'][2]
    dimS.Length = float(L)
    dimS.Height = float(H)

    dimW = idf1.idfobjects['WALL:EXTERIOR'][3]
    dimW.Starting_Y_Coordinate = float(L)
    dimW.Length = float(L)
    dimW.Height = float(H)

    roof =idf1.idfobjects['ROOF'][0]
    roof.Starting_X_Coordinate = float(L)
    roof.Starting_Y_Coordinate = float(L)
    roof.Starting_Z_Coordinate = float(H)#+ float(0.75)
    roof.Length = float(L)
    roof.Width = float(L)

    floor =idf1.idfobjects['FLOOR:ADIABATIC'][0]
    floor.Length = float(L)
    floor.Width = float(L)
    floor_area = float(L) * float(L)

    ######################## Daylight Control ##################################
    FR= idf1.idfobjects['LIGHTS'][0]
    FR.Fraction_Replaceable = float(DL)

    area = float(H)*float(L)
    adj = float(L)-float(0.100)
    p= float(round(adj, 3))

    ################# Dynamic Internal Blinds Configuration ###################
    # DIB = idf1.idfobjects['WINDOWSHADINGCONTROL'][0]
    # DIB.Shading_Control_Type = str('OnIfHighGlare')

    #################### Changing Window Properties wrt WWR #####################
    ii = 0
    for ii in range(len(n_axis)):
        building.North_Axis = n_axis[ii]
        print('The orientation is', n_axis[ii])
        k = 0
        for k in range(len(w_prop)):
            n = 0
            N = 3
            b = [w_prop[n:n + N] for n in range(0, len(w_prop), N)]
        z = 0
        k = 3
        i = 0
        for z in range(len(b)):
            n = k * z
            SGS = idf1.idfobjects['WINDOWMATERIAL:SIMPLEGLAZINGSYSTEM'][0]
            SGS.Name = z + 1
            SGS.UFactor = str(w_prop[n])
            SGS.Solar_Heat_Gain_Coefficient = str(w_prop[n + 1])
            SGS.Visible_Transmittance = str(w_prop[n + 2])
            cons = idf1.idfobjects['CONSTRUCTION'][2]
            cons.Outside_Layer = z + 1

            j = 0
            i = i + 1
            for j in range(len(wwr)):
                ratio = wwr[j]
                W = int(ratio)
                a_w = W * area / 100
                x = float(float(a_w) / float(p))
                R = float(round(x, 2))
                o = (float(R) * float(p))
                w = (float(o) / float(area)) * 100
                Xcor = float(((float(L) - float(p)) / 2))
                Zcor = float(((float(H) - float(R)) / 2))
                XCD = round(Xcor, 3)
                ZCD = round(Zcor, 3)
                ################## Modelling Window ##################
                Window = idf1.idfobjects['WINDOW'][0]
                Window.Starting_X_Coordinate = float(XCD)
                Window.Starting_Z_Coordinate = float(ZCD)
                Window.Length = float(p)
                Window.Height = float(R)
                idf1.saveas('/home/shinigami/SGLSim/SF/{}.idf'.format(
                    ii * 1000000 + z * 100000 + 1000 * j + i))
                print(ii * 1000000 + z * 100000 + 1000 * j + i)
    # idf_simulator(city, n_axis, wwr, w_prop, hvac, email, floor_area)
    idf_simulator(city, n_axis, wwr, w_prop, hvac, floor_area)

def removeFiles():
    idfDir = '/home/shinigami/SGLSim/SF/'
    resDir = '/home/shinigami/SGLSim/SF/HTML_Files/'
    simDir = '/home/shinigami/SGLSim/'
    print("Removing Idf Files")
    for fname in os.listdir(idfDir):
        if fname.endswith(".idf"):
            os.remove(os.path.join(idfDir, fname))
        else:
            continue
    print("Removing HTML Files")
    for fname in os.listdir(resDir):
        if fname.endswith(".htm"):
            os.remove(os.path.join(resDir, fname))
        else:
            continue
    for fname in os.listdir(simDir):
        if fname.startswith("eplus"):
            os.remove(os.path.join(simDir, fname))
        elif fname.startswith("sqlite"):
            os.remove(os.path.join(simDir, fname))
        else:
            continue

while True:
    _, d = r.blpop('queue')
    removeFiles()
    idf_generator(**json.loads(d))
    # removeFiles()
