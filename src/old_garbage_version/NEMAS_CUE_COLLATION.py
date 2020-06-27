"""Designed to open all output files of the ETEMP5 task (aiming to be flexibly available for all versions), and put those outputs into one file.
"""

#SHANNON -- 07/31/2018 This is the WORKING version of this task.

#SHANNON -- 06/19/2018 This task provides output, but still only for ETEMP_SMG (see the file path near the end of the script); however, certain correct/incorrect outputs are still not working properly, due to discrepancies in classy.py and the function calls in this script.
#SHANNON -- 06/19/2018 This task was copied, and additional alterations will be applied to the copy to preserve this (semi)working version.
#SHANNON -- find 'SMG' to see edits (other than 'race' edits)
import os,sys,copy,traceback,math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import traceback
import matplotlib
import pylab as p
from Classy import start,end
from scipy import stats
from psychopy import gui
import datetime #SMG -- added on 07/31/2018 in order to include the date to the output

class DataCollation():
    def __init__(self):
        return
    def Untrimmed(self):
        for ftype in ['Cue']:
            now = datetime.datetime.now() #SMG added on 07/31/2018
            date=now.strftime("%m-%d-%y") #SMG added on 07/31/2018
            filename=os.path.join(os.getcwd(),'NEMAS Probability %s_Collation_%s.csv' %(ftype,date)) #SMG changed on 07/31/208
#            filename=os.path.join(os.getcwd(),'Output %s_Phase.csv' %(ftype))
            output=open(filename,'w')
            output.write("Sub,")
            cues=[item+'_Cue' for item in ['Fearful','Neutral']]
            #races=['AA','Cau']
            stims=[item+'_Stim' for item in self.emos]
            if ftype=='Cue':
                for type in ['Acc','AvgRT']:
                    for cue in cues:
                        #for race in races:
                        for stim in stims:
                            output.write('%s_%s %s,' %(cue,stim,type))
                            #output.write('%s_%s_%s %s,' %(race,cue,stim,type))
                    for cue in cues:
                        output.write('%s %s,' %(cue,type))
                    #for cue in cues:
                        #for race in races:
                        #output.write('Prob %s %s,' %(cue,type))
                         #output.write('%s Prob %s %s,' %(race,cue,type))
            else:
                for stim in stims:
                    output.write('%s Threshold,' %(stim))
            if ftype!='Learning':
                for type in ['Acc','AvgRT']:
                    for stim in stims:
                        output.write('%s %s,' %(stim,type))
            if ftype=='Cue':
                for tert in ['Correct','Incorrect']:
                    for type in ['AvgRT']:
                        for cue in cues:
                            #for race in races:
                            for stim in stims:
                                output.write('%s %s_%s %s,' %(stim,tert,cue,type))
                                #output.write('%s %s_%s_%s %s,' %(tert,race,cue,stim,type))
                        for cue in cues:
                            output.write('%s %s %s,' %(tert,cue,type))
                    #for cue in cues:
                            #for race in races:
                             #output.write('%s %s %s %s,' %(tert,race,cue,type))
            if ftype!='Learning':
                for tert in ['Correct','Incorrect']:
                    for type in ['AvgRT']:
                        for stim in stims:
                            output.write('%s %s %s,' %(tert,stim,type))
            if ftype=='Cue':
                for type in ['HR','FAR','ZHR','ZFAR','dPrime']:
                    for cue in cues:
                    #for race in races:
                        #output.write('%s %s_%s,' %(type,race,cue))
                    #for cue in cues:
                        output.write('%s %s,' %(type,cue))
            output.write('\n')
            if ftype=='Threshold':
                data=self.datafilesT
            elif ftype=='Cue':
                data=self.datafiles
            prRem=[]
            checker=data[1].split('\\')[-1].split('ETEMP1_fMRI_v2.2 ')[1].split('_')[0]
            for num in range(len(data)):
                fname=data[num]
#                print fname
                panf=pd.io.parsers.read_csv(fname,na_values=['NR','None','Wrong button','Catch','-']) #SMG -- added 'Catch' and '-'
                headers=panf.columns.values.tolist()
                panf_val=panf.dropna(subset=['resp','rt']) #SMG -- Changed 'Correct?' to 'resp'
                number=fname.split('\\')[-1].split('ETEMP1_fMRI_v2.2 ')[1].split('_')[0] #SMG -- changed 'Task ' to 'NEMAS_v1.4 '(use find to see all)
                output.write('%s,' %(number))
                if ftype=='Threshold':
                    PD=end.PsychophysicsDictMaker(stims,['Incorrect','Correct'])
                else:
                    PD=end.PsychophysicsDictMaker(cues,stims,['Incorrect','Correct']) #SMG -- Not sure if this will work...
                    #PD=end.PsychophysicsDictMaker(cues,[str(item) for item in races],stims,['Incorrect','Correct']) #SMG -- Not sure how to change this one...?
                self.FirstCalcs={'Learning':'Average Threat Accuracy:','Threshold':'Fearful:','Cue':''}
                self.lengths={}
                if ftype!='Threshold':
                    try:
                        self.lengths[ftype]=len(list(panf['Trial']))-26 #SMG -- changed 'block' to 'Trial' (see NEMAS output) #SMG -- added "-26" on 7/26 (script was working and then stopped working!)
#                        print "Length of trial."
                    except:
                        self.lengths[ftype]=len(panf['rt'])-26 #SMG -- changed to -26
                        print 'Used rt to determine length of columns.'
                else:
                    try:
                        self.lengths[ftype]=list(panf['Trial']).index(self.FirstCalcs[ftype])
                    except:
                        self.lengths[ftype]=len(panf['rt'])-4
                for x in range(self.lengths[ftype]):
                    try:
                        resp=int(panf['resp'][x]) #SMG
                        rt=float(panf['rt'][x])
                        #if int(panf['Image'][x].split(panf['Stim'][x])[1].split('.')[0])<=8:
                        #    race='AA'
                        #else:
                        #    race='Cau'
                        PD[panf['Stim'][x]+'_Stim'+'Acc'].append(resp) #modified to panf['Stim'] rather than panf['Emotion'] 7/30/18 - teaching moment: why did I do that? -AS
                        PD[panf['Stim'][x]+'_Stim'+'AvgRT'].append(rt)
                        PD[panf['Stim'][x]+'_Stim'+['Incorrect','Correct'][resp]+'AvgRT'].append(rt)
                        PD[panf['Cue'][x]+'_Cue'+'Acc'].append(resp) #modified to panf['Cue'] rather than panf['Cue type'] 7/30/18 - teaching moment: why did I do that? -AS
                        PD[panf['Cue'][x]+'_Cue'+'AvgRT'].append(rt)
                        PD[['Incorrect','Correct'][resp]+panf['Cue'][x]+'_Cue'+'AvgRT'].append(rt)
                        PD[panf['Stim'][x]+'_Stim'+['Incorrect','Correct'][resp]+panf['Cue'][x]+'_Cue'+'AvgRT'].append(rt)
                        #PD[race+panf['Cue'][x]+'_Cue'+'Acc'].append(resp)
                        #PD[race+panf['Cue'][x]+'_Cue'+'AvgRT'].append(rt)
                        #PD[race+['Incorrect','Correct'][resp]+panf['Cue'][x]+'_Cue'+'AvgRT'].append(rt)
                        #PD[race+panf['Stim'][x]+'_Stim'+['Incorrect','Correct'][resp]+panf['Cue'][x]+'_Cue'+'AvgRT'].append(rt)
                        PD[panf['Stim'][x]+'_Stim'+panf['Cue'][x]+'_Cue'+'Acc'].append(resp)
                        PD[panf['Stim'][x]+'_Stim'+panf['Cue'][x]+'_Cue'+'AvgRT'].append(rt)
                        #PD[race+panf['Stim'][x]+'_Stim'+panf['Cue'][x]+'_Cue'+'Acc'].append(resp)
                        #PD[race+panf['Stim'][x]+'_Stim'+panf['Cue'][x]+'_Cue'+'AvgRT'].append(rt)
                        if panf['Stim'][x][0]==panf['Cue'][x][0]:
                            if resp==1:
                                PD['dResponses'+panf['Cue'][x]+'_Cue'].append('Hit')
                                #PD['dResponses'+race+panf['Cue'][x]+'_Cue'].append('Hit')
                            elif resp==0:
                                PD['dResponses'+panf['Cue'][x]+'_Cue'].append('Miss')
                                #PD['dResponses'+race+panf['Cue'][x]+'_Cue'].append('Miss')
                        elif panf['Stim'][x]!=panf['Cue'][x]:
                            if resp==1:
                                PD['dResponses'+panf['Cue'][x]+'_Cue'].append('Correct Rejection')
                                #PD['dResponses'+race+panf['Cue'][x]+'_Cue'].append('Correct Rejection')
                            elif resp==0:
                                PD['dResponses'+panf['Cue'][x]+'_Cue'].append('False Alarm')
                                #PD['dResponses'+race+panf['Cue'][x]+'_Cue'].append('False Alarm')
                    except Exception as e:
#                        print(traceback.format_exc()),number,ftype #used this to see that the column header being used previously was incorrect.  Uncomment to see what it does -AS
                        continue
                for type in ['Acc','AvgRT']:
                    for cue in cues:
                        #for race in races:
                        for stim in stims:
                            #output.write('%s,' %(end.Average(PD[race+stim+cue+type])))
                            #thing=PD[stim+cue+type]
                            #print thing
#                            print PD
                            #output.write('%s,' %(end.Average(PD(0,1,2)))) #SMG -- attempt to fix tuple error (unsuccessful). Still a TypeError
                            output.write('%s,' %(end.Average(PD[stim+cue+type]))) #SMG -- 'TypeError: tuple indices must be integers, not str'
                    for cue in cues:
                        output.write('%s,' %(end.Average(PD[cue+type])))
                #for cue in cues:
                        #for race in races:
                        #output.write('%s,' %(end.Average(PD[race+cue+type])))
                if ftype!='Learning':
                    for type in ['Acc','AvgRT']:
                        for stim in stims:
                            output.write('%s,' %(end.Average(PD[stim+type])))
                if ftype=='Cue':
                    for tert in ['Correct','Incorrect']:
                        for type in ['AvgRT']:
                            for cue in cues:
                                #for race in races:
                                for stim in stims:
                                    output.write('%s,' %(end.Average(PD[stim+tert+cue+type])))
                                    #output.write('%s,' %(end.Average(PD[race+stim+tert+cue+type])))
                            for cue in cues:
                                output.write('%s,' %(end.Average(PD[tert+cue+type])))
                        #for cue in cues:
                                #for race in races:
                                #output.write('%s,' %(end.Average(PD[race+tert+cue+type])))
                for tert in ['Correct','Incorrect']:
                    for type in ['AvgRT']:
                        for stim in stims:
                            if ftype=='Cue':
                                output.write('%s,' %(end.Average(PD[stim+tert+type])))
#                                output.write('%s,' %(end.Average(PD[tert+stim+type]))) #modified 7/30/18 - teaching moment: why is this incorrect? -AS
                            else:
                                output.write('%s,' %(end.Average(PD[stim+tert+type])))
                if ftype=='Cue':
                    Hits=[]
                    FAs=[]
                    ZHs=[]
                    ZFAs=[]
                    #for x in range(0,len(cues)):
                        #for r in range(len(races)):
                        #Hits.append(end.HitRate(PD['dResponses'+cues[x]]))
                        #Hits.append(end.HitRate(PD['dResponses'+races[r]+cues[x]]))
                        #output.write('%s,' %(end.HitRate(PD['dResponses'+cues[x]])))
                        #output.write('%s,' %(end.HitRate(PD['dResponses'+races[r]+cues[x]])))
                    for x in range(0,len(cues)):
                        Hits.append(end.HitRate(PD['dResponses'+cues[x]]))
                        output.write('%s,' %(end.HitRate(PD['dResponses'+cues[x]])))
                    #for x in range(0,len(cues)):
                        #for r in range(len(races)):
                        #FAs.append(end.FArate(PD['dResponses'+races[r]+cues[x]]))
                        #FAs.append(end.FArate(PD['dResponses'+cues[x]]))
                        #output.write('%s,' %(end.FArate(PD['dResponses'+races[r]+cues[x]])))
                        #output.write('%s,' %(end.FArate(PD['dResponses'+cues[x]])))
                    for x in range(0,len(cues)):
                        FAs.append(end.FArate(PD['dResponses'+cues[x]]))
                        output.write('%s,' %(end.FArate(PD['dResponses'+cues[x]])))
                    for x in range(len(Hits)):
                        ZHs.append(end.Zscore(Hits[x]))
                        output.write('%s,' %(end.Zscore(Hits[x],)))
                    for x in range(len(FAs)):
                        ZFAs.append(end.Zscore(FAs[x]))
                        output.write('%s,' %(end.Zscore(FAs[x])))
                    for x in range(len(ZHs)):
                        end.dPrime(ZHs[x],ZFAs[x])
                        output.write('%s,' %(end.dPrime(ZHs[x],ZFAs[x])))
#                    if number==checker:
#                        print len(Hits),len(FAs)
                output.write('\n')
        output.close()
        return
    def Begin(self):
        expInfo = {'Untrimmed?':'yes','Experiment':'ETEMP_SMG'} #dictionary to run GUI
        expInfo['Standard Deviations from mean']= 3 #this should be modified in __init__
        expInfo["You may need to manually modify Begin"]='I understand'
#        dlg = gui.DlgFromDict(expInfo, title='ETEMP1_Happy_Data_Collation',fixed=['Standard Deviations from mean','You may need to manually modify Begin']) #how the GUI appears
#        if dlg.OK: #you can cancel out of the dialogue
        self.SD=int(expInfo['Standard Deviations from mean'])
        try:
            os.chdir('C:\Users\MohantyLab\Desktop\NEMAS_ProbabilityTask_RecodedSub')
#            os.chdir('C:\Users\mohantylab\Experiments_and_Data\Projects\ETEMP_Shannon\data') #modified to be used on lab computer -AS
        except:
            pass
            print "passed"
        if expInfo['Experiment']=='ETEMP_SMG':
            self.ETEMP_SMG()
        else:
            print 'Add the necessary components for this experiments, or spell correctly'
            sys.exit()
        self.Untrimmed()
    def ETEMP_SMG(self):
        self.ExpName='ETEMP_SMG'
        self.Avoids=['Sub test','Sub test1','Sub type in subject ID here please','v1','v1x','Sub ETEMP5_test','Sub ETEMP5_testing','Sub KDPilot1',
            'Sub KDtest','Sub KRD pilot','Sub 31_test','Sub asdf','Sub ETEMP_testing']
        self.ends={'Phase':3,'version#':1,'versionLoc':1}
        self.emos=['Fearful','Neutral']
        self.numPlace=3
        self.HRs=18
        NRs_by_sub={}
        self.datafiles=[os.path.join(os.getcwd(),folder,file)
            for folder in os.listdir(os.getcwd()) if folder not in self.Avoids if folder[-1] not in ['v','x','s']
            for file in os.listdir(os.path.join(os.getcwd(),folder)) if file.split('_')[-1]!='fixed.csv' if file[-1]!='p' #SMG -- throwing an error:WindowsError: [Error 267] The directory name is invalid: 'C:\\Users\\MohantyLab\\Desktop\\7-Zip File Manager.lnk/*.*'
            if 'ETEMP1' in file #modified to work in lab
            if 'Thresholding' not in file if os.stat(os.path.join(os.getcwd(),folder,file)).st_size>10000]
        for fname in self.datafiles:
#            print fname #used to find which subject ID numbers were listed as "please type in subject ID here" -AS
            number=fname.split('\\')[-1].split('ETEMP1_fMRI_v2.2 ')[1].split('_')[0]
            for split in ['Cue']:
                for stim in ['Fearful','Neutral','Both']:
                    NRs_by_sub[number+split+'_'+stim+'Stim']=0
                    if split not in ['All','Threshold']:
                        for cue in ['N','F','All']:
                            NRs_by_sub[number+split+'_'+cue+'Cue_'+stim+'Stim']=0
        for fname in self.datafiles:
            file=open(fname,'r')
            lines=file.readlines()
            file.close()
            number=fname.split('\\')[-1].split('ETEMP1_fMRI_v2.2 ')[1].split('_')[0]
            phase='Cue'
            if phase=='Cue':
                try:
                    CLoc=lines[0].split(',').index('Cue')#CLoc=lines[0].split(',').index('Cue') ##SMG
                except:
                    continue
            if phase!='Learning':
                try:
                    ElLoc=lines[0].split(',').index('Stim')
                except:
                    continue
            try:
                ResLoc=lines[0].split(',').index('resp') #SMG
            except:
                continue
            for x in range(1,len(lines)):
                try:
                    if lines[x].split(',')[ResLoc] in ['NR','Wrong button','Catch']: #SMG -- added 'Catch'
                        NRs_by_sub[number+phase+'_'+lines[x].split(',')[ElLoc]+'Stim']+=1
                        if phase!='Threshold':
                            NRs_by_sub[number+phase+'_'+lines[x].split(',')[ClLoc]+'Cue'+'_'+lines[x].split(',')[ElLoc]+'Stim']+=1
                        NRs_by_sub[number+'_All_Both']+=1
                        NRs_by_sub[number+'All'+'_'+lines[x].split(',')[ElLoc]+'Stim']+=1
                        if phase!='Threshold':
                            NRs_by_sub[number+'All'+'_'+lines[x].split(',')[ClLoc]+'Cue'+'_'+lines[x].split(',')[ElLoc]+'Stim']+=1
                except:
#                    print traceback.format_exc()
                    continue
        now = datetime.datetime.now() #SMG added on 07/31/2018
        date=now.strftime("%m-%d-%y") #SMG added on 07/31/2018
        file=open(os.path.join(os.getcwd(),'NRs_by_phase_cue_stim_%s.csv'%(date)),'w')
#        file=open(os.path.join(os.getcwd(),'NRs_by_phase_cue_stim.csv'),'w')
        file.write('Sub,Phase,Cue,Emotion,Count\n')
        for fname in self.datafiles:
            number=fname.split('\\')[-1].split('ETEMP1_fMRI_v2.2 ')[1].split('_')[0]
            for split in ['Cue']:
                if split not in ['All','Threshold']:
                    for cue in ['F','N','All']:
                        for stim in ['Fearful','Neutral','Both']:
                            file.write('%s,%s,%s,%s,%s\n' %(number,split,cue,stim,NRs_by_sub[number+split+'_'+cue+'Cue_'+stim+'Stim']))
                for stim in ['Fearful','Neutral','Both']:
                    file.write('%s,%s,%s,%s,%s\n' %(number,split,cue,stim,NRs_by_sub[number+split+'_'+stim+'Stim']))
        file.close()
        print "Program Completed" #SMG -- This is unnecessary, but it will allow unfamiliar users to recognize that the program is finished, and that the program ran to completion.
        return
D=DataCollation()
D.Begin()