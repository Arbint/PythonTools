import maya.cmds as mc
import math


#################################################################################
#                                  Utility Funcs                                #
#################################################################################

# vector class
class vector:
    def __init__(self, elements):
        self.x = elements[0]
        self.y = elements[1]
        self.z = elements[2]

    def __add__(self, rhs):
        return vector([self.x + rhs.x, self.y + rhs.y, self.z + rhs.z])

    def __str__(self):
        return f"<{self.x},{self.y},{self.z}>"

    def __sub__(self, rhs):
        return vector([self.x - rhs.x, self.y - rhs.y, self.z - rhs.z])

    def __mul__(self, coeficient):
        return vector([self.x * coeficient, self.y * coeficient, self.z * coeficient])

    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalized(self):
        return self * (1 / self.magnitude())


def setColor(obj, rgbColor):
    mc.setAttr(obj + ".overrideEnabled", 1)
    mc.setAttr(obj + ".overrideRGBColors", 1)
    mc.setAttr(obj + ".overrideColorR", rgbColor[0])
    mc.setAttr(obj + ".overrideColorG", rgbColor[1])
    mc.setAttr(obj + ".overrideColorB", rgbColor[2])


def setCircleRadius(c, radius):
    shape = mc.listRelatives(c, s=True)[0]
    makeCircleName = mc.listConnections(shape, s=True)[0]
    if makeCircleName:
        mc.setAttr(makeCircleName + ".radius", radius)


def setCurveThickness(crv, thickness):
    ShapeName = mc.listRelatives(crv, s=True)[0]
    mc.setAttr(ShapeName + ".lineWidth", thickness)


def crvInfoForCrv(crv):
    shape = mc.listRelatives(crv, s=True, ni=True)[0]
    name = "curveInfo_" + crv
    mc.createNode("curveInfo", n=name)
    mc.connectAttr(shape + ".worldSpace[0]", name + ".inputCurve")
    return name


def hidAllChannelBoxAttr(obj):
    attrs = mc.listAttr(obj, k=True)
    for attr in attrs:
        mc.setAttr(obj + "." + attr, lock=True, k=False, cb=False)


def CreateController(jointName, parentController, prefix, radius, replaceStr="jnt_drv_", offsetGrp=False, pc=False):
    # create circle, give it a name
    controllerName = prefix + jointName.replace(replaceStr, "")
    mc.circle(n=controllerName, nr=(1, 0, 0), r=radius)
    setCurveThickness(controllerName, GetUniversalCtrlThickness())
    # group circle
    controllerGrpName = controllerName + "_grp"
    mc.group(controllerName, n=controllerGrpName)

    if offsetGrp:
        offsetGrpName = controllerName + getOffsetGrpSubfix()
        mc.group(controllerName, n=offsetGrpName)

    # match group to joint
    mc.matchTransform(controllerGrpName, jointName)
    # do constraint
    if pc:
        mc.parentConstraint(controllerName, jointName, mo=True)
    else:
        mc.orientConstraint(controllerName, jointName)

    if parentController != "":
        mc.parent(controllerGrpName, parentController)
    return controllerName, controllerGrpName


def CreateCtrl(jntName, parentCtrl, offsetGrp=False, pc=False):
    return CreateController(jntName, parentCtrl, GetCtrlPrefix(), GetUniversalCtrlRadius(), getJntNameBase(), offsetGrp,
                            pc)


def createDup(jnts, prefix):
    outJnts = []
    dup = mc.duplicate(jnts, po=True, rc=True)
    for i in range(0, len(dup)):
        jntName = prefix + "_" + jnts[i]
        mc.rename(dup[i], jntName)
        outJnts.append(jntName)
    return outJnts


def createRpIKHandle(start, end):
    ikHandleName = "ikHandle_" + end
    mc.ikHandle(sj=start, ee=end, n=ikHandleName, solver="ikRPsolver")
    return ikHandleName


def getPos(obj):
    return vector(mc.xform(obj, t=True, ws=True, q=True))


def setPos(obj, pos):
    posToTuple = (pos.x, pos.y, pos.z)
    mc.xform(obj, t=posToTuple, ws=True)


def setLocalPos(obj, pos):
    mc.setAttr(obj + ".translateX", pos.x)
    mc.setAttr(obj + ".translateY", pos.y)
    mc.setAttr(obj + ".translateZ", pos.z)


###################################################################################
#                                       UI                                        #
###################################################################################
def GetWindowWidth():
    return 300


def GetDrvJntLable():
    return "drv_"


windowID = "JTControllerToolkit922022"

if mc.window(windowID, q=True, exists=True):
    mc.deleteUI(windowID)

mc.window(windowID, title="JT Controller Toolkit", w=GetWindowWidth())

# universal vars
masterLayout = mc.columnLayout()
UniversalSetUpLayout = mc.frameLayout(cll=True, l="Universal Setup", w=GetWindowWidth())
CtrlRadiusFF = mc.floatFieldGrp(l="controller Radius", v1=2)
mc.button(l="set controller radius", c="setControllerRadiusBtnCmd()")
CtrlLineWidthFF = mc.floatFieldGrp(l="controller line thickness", v1=2)
mc.button(l="set controller Thickness", c="setControllerThickness()")
ACPrefixTF = mc.textFieldGrp(l="Controller name prefix", tx="ac_")
JntNameToRemoveTF = mc.textFieldGrp(l="Joint name to remove", tx="jnt_")
rightPrefixTF = mc.textFieldGrp(l="right prefix", tx="_r_")
rightColorSG = mc.colorSliderGrp(l="right color", rgb=(0, 0, 1))
leftPrefixTF = mc.textFieldGrp(l="left prefix", tx="_l_")
leftColorSG = mc.colorSliderGrp(l="left color", rgb=(1, 0, 0))
CenterColorSG = mc.colorSliderGrp(l="center color", rgb=(1, 1, 0))

# three joint chain
mc.setParent(masterLayout)
ThreeJointChainLayout = mc.frameLayout(cll=True, l="Three Joint Chain System", w=GetWindowWidth())
mc.columnLayout()
mc.text("Select the root joint and:")
mc.button(l="build", w=GetWindowWidth(), c="CreateThreeJointChainCmd()")

# hand rig
mc.setParent(masterLayout)
HandLayout = mc.frameLayout(cll=True, l="Hand", w=GetWindowWidth())
mc.columnLayout()
mc.text("Select the wrist joint and:")
handNamePrefixTF = mc.textFieldGrp(l="hand top grp prefix:", tx="hand")
fingerNameBaseTF = mc.textFieldGrp(l="finger name base:", tx="finger")
mc.button(l="Rig Hand", c="RigHand()", w=GetWindowWidth())

# ik spline
mc.setParent(masterLayout)
IkSplineLayout = mc.frameLayout(cll=True, l="IK Spline", w=GetWindowWidth())
mc.text("Select all joints from root to end in order, and:")
IKSplineName = mc.textFieldGrp(l="name:", tx="spine")
mc.button(l="create IK Spline", c="CreateIKSplineBtnCmd()", w=GetWindowWidth())


# UI Utilities
def getFloatValueFromField(field):
    return mc.floatFieldGrp(field, q=True, v=True)[0]


def getStrFromField(field):
    return mc.textFieldGrp(field, q=True, tx=True)


def GetCdFrom(SG):
    return mc.colorSliderGrp(SG, q=True, rgb=True)


def GetUniversalCtrlRadius():
    return getFloatValueFromField(CtrlRadiusFF)


def GetUniversalCtrlThickness():
    return getFloatValueFromField(CtrlLineWidthFF)


def GetCtrlPrefix():
    return getStrFromField(ACPrefixTF)


def getJntNameBase():
    return getStrFromField(JntNameToRemoveTF)


def getLeftPrefix():
    return getStrFromField(leftPrefixTF)


def getRightPrefix():
    return getStrFromField(rightPrefixTF)


def getFingerNameBase():
    return getStrFromField(fingerNameBaseTF)


def getOffsetGrpSubfix():
    return "_offset_grp"


def getLeftCd():
    return GetCdFrom(leftColorSG)


def getRightCd():
    return GetCdFrom(rightColorSG)


def getCenterCd():
    return GetCdFrom(CenterColorSG)


def getColorFromSide(sideIdentifier):
    if getLeftPrefix() == sideIdentifier:
        return getLeftCd()
    else:
        return getRightCd()


mc.showWindow(windowID)


##################################################################################
#                                    Methods                                     #
##################################################################################

def setControllerRadiusBtnCmd():
    controllerRadius = GetUniversalCtrlRadius()
    ctrls = mc.ls(sl=True)
    for ctrl in ctrls:
        setCircleRadius(ctrl, controllerRadius)


def setControllerThickness():
    ctrls = mc.ls(sl=True)
    lineThickness = GetUniversalCtrlThickness()
    for ctrl in ctrls:
        setCurveThickness(ctrl, lineThickness)


def CreateThreeJointChainCmd():
    controllerRaidus = GetUniversalCtrlRadius()
    lineThickness = GetUniversalCtrlThickness()
    # collect joints
    root = mc.ls(sl=True)[0]
    middle = mc.listRelatives(root, c=True)[0]
    end = mc.listRelatives(middle, c=True)[0]
    AllJnts = [root, middle, end]

    # create ik fk drv joints
    fkPrefix = GetDrvJntLable() + "fk"
    ikPrefix = GetDrvJntLable() + "ik"
    fkJnts = createDup(AllJnts, fkPrefix)
    ikJnts = createDup(AllJnts, ikPrefix)

    # create fk controllers
    FkParent = ""
    FKGrps = []
    for fkJnt in fkJnts:
        FkParent, FkGrp = CreateCtrl(fkJnt, FkParent)
        FKGrps.append(FkGrp)
    FKTopGrp = FKGrps[0]

    # create ik controllers
    IkWristJnt = ikJnts[-1]
    IkWristCtrl, IKWristCtrlGrp = CreateCtrl(IkWristJnt, "")
    IkHandle = createRpIKHandle(ikJnts[0], ikJnts[-1])

    # pole vector controller
    ikPoleVectCtrl = GetCtrlPrefix() + ikJnts[1].replace(getJntNameBase(), "")
    mc.curve(d=1, n=ikPoleVectCtrl,
             p=[(-1, 0, -1), (-1, 0, -3), (-2, 0, -3), (0, 0, -5), (2, 0, -3), (1, 0, -3), (1, 0, -1), (3, 0, -1),
                (3, 0, -2), (5, 0, 0), (3, 0, 2), (3, 0, 1), (1, 0, 1), (1, 0, 3), (2, 0, 3), (0, 0, 5), (-2, 0, 3),
                (-1, 0, 3), (-1, 0, 1), (-3, 0, 1), (-3, 0, 2), (-5, 0, 0), (-3, 0, -2), (-3, 0, -1), (-1, 0, -1)])
    setCurveThickness(ikPoleVectCtrl, GetUniversalCtrlThickness())
    ikPoleVectCtrlGrp = ikPoleVectCtrl + "_grp"
    mc.group(ikPoleVectCtrl, n=ikPoleVectCtrlGrp)
    mc.matchTransform(ikPoleVectCtrlGrp, root)
    poleVectorVal = vector(mc.getAttr(IkHandle + ".poleVector")[0])
    grpPosition = getPos(ikPoleVectCtrlGrp)
    endPos = getPos(end)
    chainLength = (endPos - grpPosition).magnitude()
    endDir = (endPos - grpPosition).normalized()
    poleVectorCtrlPos = grpPosition + poleVectorVal.normalized() * (chainLength / 2) + endDir * (chainLength / 2)
    setLocalPos(ikPoleVectCtrlGrp, poleVectorCtrlPos)
    mc.poleVectorConstraint(ikPoleVectCtrl, IkHandle)

    # parent of the ik handle should happen after positioning ik pole vector controller
    mc.parent(IkHandle, IkWristCtrl)

    # create ikfk blend
    blendAttrName = "_ikfk_blend"
    ikfkBlendName = AllJnts[0].replace(getJntNameBase(), "") + blendAttrName
    ikfkBlendAttr = ikfkBlendName + "." + blendAttrName

    ikfkBlend = mc.curve(d=1,
                         p=[(-1, 0, 1), (-1, 0, 3), (1, 0, 3), (1, 0, 1), (3, 0, 1), (3, 0, -1), (1, 0, -1), (1, 0, -3),
                            (-1, 0, -3), (-1, 0, -1), (-3, 0, -1), (-3, 0, 1), (-1, 0, 1)],
                         k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], n=ikfkBlendName)
    hidAllChannelBoxAttr(ikfkBlendName)
    setCurveThickness(ikfkBlend, lineThickness)
    mc.addAttr(ikfkBlendName, ln=blendAttrName, at="double", min=0, max=1, dv=0, h=False, k=True)
    IKFKBlendReverseName = "reverse_" + ikfkBlendName;
    IKFKBlendReverse = mc.createNode("reverse", n=IKFKBlendReverseName)
    mc.connectAttr(ikfkBlendAttr, IKFKBlendReverse + ".inputX")
    for i in range(0, len(AllJnts)):
        jnt = AllJnts[i]
        fkJnt = fkJnts[i]
        ikJnt = ikJnts[i]
        blendColors = mc.createNode("blendColors")
        mc.connectAttr(ikfkBlendAttr, blendColors + ".blender")
        mc.connectAttr(fkJnt + ".rotate", blendColors + ".color2")
        mc.connectAttr(ikJnt + ".rotate", blendColors + ".color1")
        mc.connectAttr(blendColors + ".output", jnt + ".rotate")

    # visibilityControl
    mc.connectAttr(ikfkBlendAttr, IKWristCtrlGrp + ".v")
    mc.connectAttr(ikfkBlendAttr, ikPoleVectCtrlGrp + ".v")
    mc.connectAttr(IKFKBlendReverseName + ".outputX", FKTopGrp + ".v")
    mc.setAttr(fkJnts[0] + ".v", 0)
    mc.setAttr(ikJnts[0] + ".v", 0)
    mc.setAttr(IkHandle + ".v", 0)

    # position ikfk blend
    ikfkBlendGrpName = ikfkBlendName + "_grp"
    mc.group(ikfkBlendName, n=ikfkBlendGrpName)
    mc.matchTransform(ikfkBlendGrpName, root)
    rootPos = getPos(root)
    rootParentPos = getPos(mc.listRelatives(root, p=True)[0])

    ikfkBlendPos = rootPos + (rootPos - rootParentPos)
    setLocalPos(ikfkBlendGrpName, ikfkBlendPos)

    # organization
    drvJntGrp = root.replace("jnt_", "jnt_drv_") + "_grp"
    mc.group(fkJnts[0], ikJnts[0], n=drvJntGrp)
    rigGrp = root.replace("jnt_", "") + "_rig_grp"
    mc.group(ikfkBlendGrpName, IKWristCtrlGrp, ikPoleVectCtrlGrp, FKTopGrp, drvJntGrp, n=rigGrp)

    # follow higher hierachy
    rootParent = mc.listRelatives(root, p=True)
    mc.parentConstraint(rootParent, drvJntGrp, mo=True)
    mc.parentConstraint(rootParent, FKTopGrp, mo=True)

    # color
    side = getRightPrefix()
    if getLeftPrefix() in root:
        side = getLeftPrefix()

    setColor(rigGrp, getColorFromSide(side))


def createHandGlobalCtrl(name):
    mc.curve(d=1, n=name,
             p=[(-2, 0, 2), (-4, 0, 0), (-4, 0, -4), (-3, 0, -4), (-3, 0, -2), (-3, 0, -6), (-2, 0, -6), (-2, 0, -3),
                (-2, 0, -7), (-1, 0, -7), (-1, 0, -3), (-1, 0, -6), (0, 0, -6), (0, 0, -3), (0, 0, -5), (1, 0, -5),
                (1, 0, 0), (0, 0, 2), (-2, 0, 2)])
    grpName = name + "_grp"
    mc.group(name, n=grpName)
    hidAllChannelBoxAttr(name)
    setCurveThickness(name, GetUniversalCtrlThickness())
    return name, grpName


def createFingerAttr(ctrl, offsetGrp, fingerName):
    minAttr = fingerName + "_min"
    maxAttr = fingerName + "_max"
    mc.addAttr(ctrl, ln=fingerName, at="float", min=-10, max=10, k=True)
    mc.addAttr(ctrl, ln=minAttr, at="float", min=-120, max=120, dv=-50)
    mc.addAttr(ctrl, ln=maxAttr, at="float", min=-120, max=120, dv=50)

    exp = f"""
    if({ctrl}.{fingerName}>0)
    {{
    	    {offsetGrp}.rotateZ = {ctrl}.{fingerName} /10 * {ctrl}.{maxAttr};
    }}
    else
    {{
    	    {offsetGrp}.rotateZ = {ctrl}.{fingerName} /10 * {ctrl}.{maxAttr};
    }}"""
    mc.expression(s=exp)


def RigHand():
    wrist = mc.ls(sl=True)[0]
    # create hand top grp name
    grpNamePrefix = getStrFromField(handNamePrefixTF)
    side = getRightPrefix()
    if getLeftPrefix() in wrist:
        side = getLeftPrefix()

    handGrpName = grpNamePrefix + side + "rig_grp"
    # create global ctrl
    globalCtrl, globalCtrlGrp = createHandGlobalCtrl(GetCtrlPrefix() + handGrpName.replace("rig_grp", "global"))
    mc.matchTransform(globalCtrlGrp, wrist)
    mc.group(globalCtrlGrp, n=handGrpName)
    mc.parentConstraint(wrist, handGrpName, mo=True)

    # rig fingers
    roots = mc.listRelatives(wrist, typ="joint")
    topGrps = []

    dividerNum = 1
    for root in roots:
        offsetGrps = []
        hiearchy = mc.listRelatives(root, ad=True, c=True)
        hiearchy = hiearchy[1:]
        hiearchy.reverse()
        hiearchy.insert(0, root)

        p = ""
        for jnt in hiearchy:
            first = False
            if p == "":
                first = True

            p, pGrp = CreateCtrl(jnt, p, True)
            offsetGrp = mc.listRelatives(p, p=True)[0]
            offsetGrps.append(offsetGrp)
            if first:
                topGrp = mc.listRelatives(offsetGrp, p=True)[0]
                topGrps.append(topGrp)

        # add global ctrl attr
        mc.addAttr(globalCtrl, ln=getFingerNameBase() + "_" + str(dividerNum), at="enum", en="-----", k=True)
        dividerNum += 1
        for offset in offsetGrps:
            attrName = offset.replace(GetCtrlPrefix(), "").replace(getRightPrefix(), "").replace(getLeftPrefix(),
                                                                                                 "").replace(
                getOffsetGrpSubfix(), "").replace(getFingerNameBase(), "")
            createFingerAttr(globalCtrl, offset, attrName)

    # parent fingers to hand top grp
    mc.parent(topGrps, handGrpName)

    setColor(handGrpName, getColorFromSide(side))


def createIKSplineHandle(root, end, nameBase):
    name = "ikHandle_" + nameBase
    crvName = "curve_" + nameBase + "_ik_spline"
    ik, efctr, crv = mc.ikHandle(sol="ikSplineSolver", ccv=True, n=name, sj=root, ee=end, pcv=False)
    mc.rename(crv, crvName)
    return name, crvName


def CreateIKSplineBtnCmd():
    # gather info
    splineName = getStrFromField(IKSplineName)
    splineTopGrpName = splineName + "_rig_grp"
    jnts = mc.ls(sl=True)
    root = jnts[0]
    end = jnts[-1]

    # create driver joints
    dup = mc.duplicate(jnts, po=True, rc=True)
    drvJnts = []
    for i in range(0, len(dup)):
        jntNameBase = getJntNameBase()
        drvJntName = jnts[i].replace(jntNameBase, jntNameBase + GetDrvJntLable())
        mc.rename(dup[i], drvJntName)
        origRadius = mc.getAttr(drvJntName + ".radius")
        mc.setAttr(drvJntName + ".radius", origRadius * 4)
        drvJnts.append(drvJntName)

        if i > 0 and i < len(dup) - 1:
            mc.parentConstraint(drvJntName, jnts[i])

    drvTopGrpName = drvJnts[0] + "_grp"
    mc.group(drvJnts[0], n=drvTopGrpName)

    # create controllers
    hipCtrl, hipCtrlGrp = CreateCtrl(root, "", False, True)
    endCtrl, endCtrlGrp = CreateCtrl(end, "", False, True)

    # root
    rootCtrlName = GetCtrlPrefix() + splineName + "_root"
    rootCtrlGrpName = rootCtrlName + "_grp"
    dupCtrlGrp, dupCtrl = mc.duplicate(hipCtrlGrp, rc=True)
    mc.rename(dupCtrl, rootCtrlName)
    mc.rename(dupCtrlGrp, rootCtrlGrpName)
    setCurveThickness(rootCtrlName, GetUniversalCtrlThickness())
    mc.parentConstraint(rootCtrlName, drvTopGrpName, mo=True)

    # middle
    middleCtrlName = GetCtrlPrefix() + splineName + "_middle"
    middleCtrlGrpName = middleCtrlName + "_grp"
    dupCtrlGrp, dupCtrl = mc.duplicate(hipCtrlGrp, rc=True)
    mc.rename(dupCtrl, middleCtrlName)
    mc.rename(dupCtrlGrp, middleCtrlGrpName)
    setCurveThickness(middleCtrlName, GetUniversalCtrlThickness())

    # position middle
    rootPos = getPos(rootCtrlName)
    endPos = getPos(endCtrl)
    midPos = (rootPos + endPos) * 0.5
    setPos(middleCtrlGrpName, midPos)

    # controller hierachy
    mc.parent(endCtrlGrp, middleCtrlName)
    mc.parent(middleCtrlGrpName, rootCtrlName)
    mc.parent(hipCtrlGrp, rootCtrlName)
    setCircleRadius(hipCtrl, GetUniversalCtrlRadius() * 0.8)

    # create ik spline
    ikStuff = []
    ikHanlde, ikCrv = createIKSplineHandle(drvJnts[0], drvJnts[-1], splineName)
    ikCrvOrig = ikCrv + "_orig"
    mc.duplicate(ikCrv, n=ikCrvOrig)
    ikStuff.append(ikHanlde)
    ikStuff.append(ikCrv)
    ikStuff.append(ikCrvOrig)
    ikStuffTopGrp = splineName + "_ik_grp"
    mc.group(ikStuff, n=ikStuffTopGrp)
    mc.setAttr(ikCrv + ".inheritsTransform", 0)
    mc.setAttr(ikCrvOrig + ".inheritsTransform", 0)

    topClusterName = "cluster_" + splineName + "_upper"
    cs, ch = mc.cluster(ikCrv + ".cv[2:3]")
    mc.rename(ch, topClusterName)
    mc.setAttr(topClusterName + ".v", 0)

    btmClusterName = "cluster_" + splineName + "_lower"
    cs, ch = mc.cluster(ikCrv + ".cv[0:1]")
    mc.rename(ch, btmClusterName)
    mc.setAttr(btmClusterName + ".v", 0)

    mc.parent(btmClusterName, hipCtrl)
    mc.parent(topClusterName, endCtrl)

    # twist
    exp = f"""
    {ikHanlde}.twist = {middleCtrlName}.rx + {endCtrl}.rx - {hipCtrl}.rx;
    {ikHanlde}.roll = {hipCtrl}.rx;
    """
    mc.expression(s=exp)

    # stretch
    crvInfo = crvInfoForCrv(ikCrv)
    origCrvInfo = crvInfoForCrv(ikCrvOrig)
    for drvJnt in drvJnts:
        exp = f"""
        {drvJnt}.sx = {crvInfo}.arcLength / {origCrvInfo}.arcLength;
        """
        mc.expression(s=exp)

        # volume maintain
    VolumeMaintainAttrName = splineName + "VolumnMaintian"
    mc.addAttr(rootCtrlName, ln=VolumeMaintainAttrName, at="float", min=0, max=1, k=True, dv=1)

    for i in range(1, len(jnts) - 2):
        jnt = jnts[i]
        drvJnt = drvJnts[i]
        exp = f"""
        {jnt}.scaleY = {jnt}.scaleZ =  (1 / sqrt({drvJnt}.scaleX) - 1) * {rootCtrlName}.{VolumeMaintainAttrName} + 1;
        """
        mc.expression(s=exp)

    # final hierachy
    mc.group(rootCtrlGrpName, n=splineTopGrpName)
    mc.parent(drvTopGrpName, splineTopGrpName)
    mc.parent(ikStuffTopGrp, splineTopGrpName)
    mc.setAttr(drvTopGrpName + ".v", 0)
    mc.setAttr(ikStuffTopGrp + ".v", 0)
    setColor(splineTopGrpName, getCenterCd())













