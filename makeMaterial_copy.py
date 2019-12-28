import maya.cmds as mc

def applyMaterial():
    list = mc.ls(sl=1)
        
    for node in list:
               
        if node:
            shd = mc.shadingNode('lambert', name ='%s_lambert'%node, asShader=True)
            shdSG = mc.sets(n='%sSG'%shd, empty=True, renderable=True, noSurfaceShader=True)
            mc.connectAttr('%s.outColor' % shd, '%s.surfaceShader' % shdSG)
            mc.sets(node, e=True, forceElement=shdSG)


applyMaterial()