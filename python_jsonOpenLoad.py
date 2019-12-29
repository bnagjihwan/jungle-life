try:
    import json
    import os
    import maya.cmds as mc
    import glob
    import pymel.core
#   from see import see
    from pymel.core import Path
    

    
except:
    print "Error"
    
def TransformExport_Import(imp=1):
    if imp:
        sel=mc.ls(sl=1, type='transform')
        if sel:
            for obj in sel:
                sceneName=mc.file(q=True, l=True)
                #print sceneName
                if sceneName:
                    fileName,extName = os.path.splitext(sceneName[0])
                    jsonFile='%s_%s.json'%(fileName,obj)
                    
                    startF=mc.playbackOptions(q=1, min=1)
                    endF=mc.playbackOptions(q=1, max=1)
                    
                    outDIC = {"Name":obj,
                              "frameStart":startF,
                              "frameEnd":endF,
                              "frames":{"matrix_world":{}}
                              }
                    for x in range(int(startF), int(endF)+1):
                        mc.currentTime(x)
                        outDIC["frames"]["matrix_world"][str(x)]=mc.xform(obj, q=1, matrix=1, ws=1)
                        
                    outFile=open(jsonFile,'w')
                    json.dump(outDIC, outFile, indent=2)
                    outFile.close()
                    
    else:        
        sceneName=mc.file(q=True, l=True)
        fileName,extname=os.path.splitext(sceneName[0])
        jsonFile=Path('%s/'%(fileName.rsplit('/',1)[0]))
        poseJsons=[p for p in jsonFile.glob("*.json") if "001" in p]
        for jsonF in poseJsons:
            print jsonF
            poseData=json.load(open(jsonF))
            obj=poseData['Name']
            startF=poseData['frameStart']
            endF=poseData['frameEnd']
            print poseData
            mc.playbackOptions(min=int(startF), max=int(endF))
            
            if mc.ls(obj, type='transform'):
                for c,vals in poseData["frames"]["matrix_world"].iteritems():
                    mc.currentTime(int(c))
                    mc.xform(obj,matrix=vals)
                    for x in ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']:
                        mc.setKeyframe('%s.%s'%(obj,x));

TransformExport_Import(0)