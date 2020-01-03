import numpy as np
import os
import csv

class point:
    def __init__(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z


#----------------------------------------------------------------------------
#空间距离特征
def calDistance(point1,point2):
    distance = np.sqrt((point1.x-point2.x)**2 + (point1.y-point2.y)**2 + (point1.z-point2.z)**2)
    return distance

#计算脖子与脚的y轴距离
def neckHeight(neck,leftFeet,rightFeet):
    return neck.y - (leftFeet.y + rightFeet.y)/2


#计算三角形面积
def calArea(point1, point2, point3):
    side1 = calDistance(point1, point2)
    side2 = calDistance(point1, point3)
    side3 = calDistance(point2, point3)

    s = (side1 + side2 + side3)/2
    area = (s * (s - side1) * (s - side2) * (s - side3)) ** 0.5
    return area



#----------------------------------------------------------------------------
#方向特征

#头部方向，返回一个三维的单位方向向量
def headOrientation(head, leafEar, rightEar):
    centerX = (leafEar.x + rightEar.x) / 2
    centerY = (leafEar.y + rightEar.y) / 2
    centerZ = (leafEar.z + rightEar.z) / 2

    orientationX = head.x - centerX
    orientationY = head.y - centerY
    orientationZ = head.z - centerZ

    MO = (orientationX**2 + orientationY**2 + orientationZ**2)**0.5
    return orientationX/MO, orientationY/MO, orientationZ/MO


#身体方向，两个肩膀和盆骨构成平面的法向量
def bodyOrientation(v1, v2, v3):
    na = (v2.y - v1.y)*(v3.z - v1.z) - (v2.z - v1.z)*(v3.y - v1.y)
    nb = (v2.z - v1.z)*(v3.x - v1.x) - (v2.x - v1.x)*(v3.z - v1.z)
    nc = (v2.x - v1.x)*(v3.y - v1.y) - (v2.y - v1.y)*(v3.x - v1.x)

    MO = (na ** 2 + nb ** 2 + nc ** 2) ** 0.5
    return na/MO, nb/MO, nc/MO





#----------------------------------------------------------------------------
#动态特征

#这里计算速度，返回每一个方向的分速度，之后记得加和
def calSpeed(point1, point2, time):
    vx = (point1.x - point2.x)/time
    vy = (point1.y - point2.y)/time
    vz = (point1.z - point2.z)/time

    return vx, vy, vz
    #return (vx**2 + vy**2 + vz**2)**0.5


#这里计算加速度，输入为两个速度数据list，返回依旧为分方向加速度
def calAcceleration(v1, v2, time):
    ax = (v1[0] - v2[0])/time
    ay = (v1[1] - v2[1])/time
    az = (v1[2] - v2[2])/time

    return ax, ay, az




#----------------------------------------------------------------------------
#特殊特征
#计算动能,默认质量都为1,输入为速度的标量
def calEnergy_two(v1, v2):
    return 0.5*(v1**2) + 0.5*(v2**2)

def calEnergy_three(v1, v2, v3):
    return 0.5*(v1**2) + 0.5*(v2**2) + 0.5*(v3**2)

def calEnergy_five(v1, v2, v3, v4, v5):
    return 0.5*(v1**2) + 0.5*(v2**2) + 0.5*(v3**2)+ 0.5*(v4**2)+ 0.5*(v5**2)


#计算平滑度,输入为当前这个点的速度与加速度的list
def calSmooth(v,a):
    x1, y1, z1 = v[0], v[1], v[2]
    x2, y2, z2 = a[0], a[1], a[2]
    if (np.sqrt(x1 ** 2 + y1 ** 2 + z1 ** 2)) ** 3 == 0:
        return 0
    K = np.sqrt((y1 * z2 - z1 * y2) ** 2 + (z1 * x2 - x1 * z2) ** 2 + (x1 * y2 - x2 * y1) ** 2) / (
                (np.sqrt(x1 ** 2 + y1 ** 2 + z1 ** 2)) ** 3)
    if K == 0:
        return 10000000000
    return 1/K


#计算对称性,返回值为三维不对称度
def symmetry(neck,lefHand,rightHand):
    print(neck.x,lefHand.x, rightHand.x)
    Sx = abs(abs(neck.x - lefHand.x) - abs(neck.x - rightHand.x)) / abs(lefHand.x - rightHand.x)
    Sy = abs(abs(neck.y - lefHand.y) - abs(neck.y - rightHand.y)) / abs(lefHand.y - rightHand.y)
    Sz = abs(abs(neck.z - lefHand.z) - abs(neck.z - rightHand.z)) / abs(lefHand.z - rightHand.z)

    return Sx, Sy, Sz

#前后倾，直接用算好的速度z值






#----------------------------------------------------------------------------
#加载数据
def loadData():
    path = "skel"  # 文件夹目录
    files = os.listdir(path)  # 得到文件夹下的所有文件名称
    txts = dict()
    for file in files:  # 遍历文件夹
        position = path + '/' + file
        with open(position, "r", encoding='utf-8') as f:  # 打开文件
            data = f.read()  # 读取文件
            txts[file.split('.')[0]] = data
    return txts





def carreSum(arr):
    distance = np.sqrt(arr[0]**2 + arr[1]**2 + arr[2]**2)
    return distance






if __name__ == "__main__":
    data = loadData()
    featureList = [
        '盆骨',
        '脖子',
        '左屁股',
        '右屁股',
        '头',
        '左肩',
        '右肩',
        '左膝',
        '右膝',
        '左耳',
        '右耳',
        '左肘',
        '右肘',
        '左脚踝',
        '右脚踝',
        '左手',
        '右手',
        '右脚尖',
        '左脚尖']

    featureDict = {
        '盆骨': 1,
        '脖子': 2,
        '左屁股': 3,
        '右屁股': 4,
        '头': 5,
        '左肩': 6,
        '右肩': 7,
        '左膝': 8,
        '右膝': 9,
        '左耳': 10,
        '右耳': 11,
        '左肘': 12,
        '右肘': 13,
        '左脚踝': 14,
        '右脚踝': 15,
        '左手': 16,
        '右手': 17,
        '右脚尖': 18,
        '左脚尖': 19,
    }


    f = open('data.csv', 'w', encoding='utf-8',newline='')
    csv_writer = csv.writer(f)
    csv_writer.writerow(["LeftFoot-pelvic-distance",
                         "RightFoot-pelvic-distance",
                         "LeftHand-leftShoulder-distance",
                         "RightHand-rightShoulder-distance",
                         "LeftHand-rightHand-distance",
                         "LeftHand-Head-distance",
                         "RightHand-Head-distance",

                         "Neck-height",

                         "LeftToe-leftAnkle-distance",
                         "RightToe-rightAnkle-distance",
                         "LeftAnkle-rightAnkle-distance",
                         "LeftElbow-rightElbow-distance",
                         "LeftElbow-neck-distance",
                         "RightElbow-neck-distance",
                         "LeftKnee-rightKnee-distance",
                         "LeftEar-leftShoulder-distance",
                         "RightEar-rightShoulder-distance",

                         "UpperBody-area",
                         "LowerBody-area",

                         "HeadFacingX-coordinate",
                         "HeadFacingY-coordinate",
                         "HeadFacingZ-coordinate",

                         "UpperBodyX coordinate",
                         "UpperBodyY coordinate",
                         "UpperBodyZ coordinate",


                        "Head-speed",
                        "Head-acceleration",
                        "LeftEar-speed",
                        "LeftEar-acceleration",
                        "RightEar-speed",
                        "RightEar-acceleration",
                        "Neck-speed",
                        "Neck-acceleration",
                        "LeftShoulder-speed",
                        "LeftShoulder-acceleration",
                        "RightShoulder-speed",
                        "RightShoulder-acceleration",
                        "LeftElbow-speed",
                        "LeftElbow-acceleration",
                        "RightElbow-speed",
                        "RightElbow-acceleration",
                        "LeftHand-speed",
                        "LeftHand-acceleration",
                        "RightHand-speed",
                        "RightHand-acceleration",
                        "Pelvic-speed",
                        "Pelvic-acceleration",
                        "LeftButt-speed",
                        "LeftButt-acceleration",
                        "RightButt-speed",
                        "RightButt-acceleration",
                        "LeftKnee-speed",
                        "LeftKnee-acceleration",
                        "RightKnee-speed",
                        "RightKnee-acceleration",
                        "LeftAnkle-speed",
                        "LeftFoot-acceleration",
                        "RightAnkle-speed",
                        "RightFoot-acceleration",
                        "LeftToe-speed",
                        "LeftFoot-acceleration",
                        "RightToe-speed",
                        "RightFoot-acceleration",




                        "Head-energy",
                        "LeftHand-energy",
                        "RightHand-energy",
                        "Body-energy",
                        "leftLeg-energy",
                        "rightLeg-energy",


                        "Head-smoothness",
                        "LeftHand-smoothness",
                        "RightHand-smoothness",
                        "Body-smoothness",
                        "LeftLeg-smoothness",
                        "RightLeg-smoothness",


                        "UpperBody-symmetryX",
                        "UpperBody-symmetryY",
                        "UpperBody-symmetryZ",


                        "Head-speedZ",
                        "Neck-speedZ"])




    i = 2
    while i <=  59:
        result = []
        last_data =  data[str(i-1)]
        lastPoint = dict()
        for feature in featureList:
            target = last_data.split('\n')[featureDict[feature]]
            target = ' '.join(target.split())

            X = float(target.split(' ')[1])
            Y = float(target.split(' ')[2])
            Z = float(target.split(' ')[0])

            lastPoint[feature] = point(X,Y,Z)

        now_data =  data[str(i)]
        nowPoint = dict()
        for feature in featureList:
            target = now_data.split('\n')[featureDict[feature]]
            target = ' '.join(target.split())

            X = float(target.split(' ')[1])
            Y = float(target.split(' ')[2])
            Z = float(target.split(' ')[0])

            nowPoint[feature] = point(X,Y,Z)

        last_last_data = data[str(i-2)]
        last_lastPoint = dict()
        for feature in featureList:
            target = last_last_data.split('\n')[featureDict[feature]]
            target = ' '.join(target.split())

            X = float(target.split(' ')[1])
            Y = float(target.split(' ')[2])
            Z = float(target.split(' ')[0])

            last_lastPoint[feature] = point(X,Y,Z)


        # 左脚 - 盆骨距离
        result.append(calDistance(nowPoint['左脚尖'],nowPoint['盆骨']))
        # 右脚 - 盆骨距离
        result.append(calDistance(nowPoint['右脚尖'], nowPoint['盆骨']))
        # 左手 - 左肩距离
        result.append(calDistance(nowPoint['左手'], nowPoint['左肩']))
        # 右手 - 右肩距离
        result.append(calDistance(nowPoint['右手'], nowPoint['右肩']))
        # 左手 - 右手距离
        result.append(calDistance(nowPoint['左手'], nowPoint['右手']))
        # 左手 - 头距离
        result.append(calDistance(nowPoint['左手'], nowPoint['头']))
        # 右手 - 头距离
        result.append(calDistance(nowPoint['右手'], nowPoint['头']))
        # 脖子的高度
        result.append(neckHeight(nowPoint['脖子'],nowPoint['左脚尖'],nowPoint['右脚尖']))
        # 左脚尖 - 左脚踝距离
        result.append(calDistance(nowPoint['左脚尖'], nowPoint['左脚踝']))
        # 右脚尖 - 右脚踝距离
        result.append(calDistance(nowPoint['右脚尖'], nowPoint['右脚踝']))
        # 左脚踝 - 右脚踝距离
        result.append(calDistance(nowPoint['左脚踝'], nowPoint['右脚踝']))
        # 左手肘 - 右手肘距离
        result.append(calDistance(nowPoint['左肘'], nowPoint['右肘']))
        # 左手肘 - 脖子距离
        result.append(calDistance(nowPoint['左肘'], nowPoint['脖子']))
        # 右手肘 - 脖子距离
        result.append(calDistance(nowPoint['右肘'], nowPoint['脖子']))
        # 左膝 - 右膝距离
        result.append(calDistance(nowPoint['左膝'], nowPoint['右膝']))
        # 左耳 - 左肩膀距离
        result.append(calDistance(nowPoint['左耳'], nowPoint['左肩']))
        # 右耳 - 右肩膀距离
        result.append(calDistance(nowPoint['右耳'], nowPoint['右肩']))

        # 上半身面积(左右两肩与盆骨构成的三角形面积)
        result.append(calArea(nowPoint['左肩'],nowPoint['右肩'],nowPoint['盆骨']))
        # 下半身面积(左右两脚踝与盆骨构成的三角形面积)
        result.append(calArea(nowPoint['左脚踝'],nowPoint['右脚踝'],nowPoint['盆骨']))

        # 头部朝向：x坐标，y坐标，z坐标
        orientationX, orientationY, orientationZ = headOrientation(nowPoint['头'], nowPoint['左耳'], nowPoint['右耳'])
        result.append(orientationX)
        result.append(orientationY)
        result.append(orientationZ)
        # 上半身朝向: x坐标，y坐标，z坐标
        orientationX, orientationY, orientationZ = bodyOrientation(nowPoint['左肩'],nowPoint['右肩'],nowPoint['盆骨'])
        result.append(orientationX)
        result.append(orientationY)
        result.append(orientationZ)


        # 头部速度、加速度
        speed_now = list(calSpeed(nowPoint['头'], lastPoint['头'], 1/24))
        result.append(carreSum(speed_now))

        speed_last = list(calSpeed(lastPoint['头'], last_lastPoint['头'], 1/24))
        acceleration = calAcceleration(speed_now, speed_last, 1/24)
        result.append(carreSum(acceleration))

        # 左耳速度、加速度
        speed_now = list(calSpeed(nowPoint['左耳'], lastPoint['左耳'], 1/24))
        result.append(carreSum(speed_now))

        speed_last = list(calSpeed(lastPoint['左耳'], last_lastPoint['左耳'], 1/24))
        acceleration = calAcceleration(speed_now, speed_last, 1/24)
        result.append(carreSum(acceleration))
        # 右耳速度、加速度
        speed_now = list(calSpeed(nowPoint['右耳'], lastPoint['右耳'], 1/24))
        result.append(carreSum(speed_now))

        speed_last = list(calSpeed(lastPoint['右耳'], last_lastPoint['右耳'], 1/24))
        acceleration = calAcceleration(speed_now, speed_last, 1/24)
        result.append(carreSum(acceleration))
        # 脖子速度、加速度
        speed_now = list(calSpeed(nowPoint['脖子'], lastPoint['脖子'], 1/24))
        result.append(carreSum(speed_now))

        speed_last = list(calSpeed(lastPoint['脖子'], last_lastPoint['脖子'], 1/24))
        acceleration = calAcceleration(speed_now, speed_last, 1/24)
        result.append(carreSum(acceleration))
        # 左肩速度、加速度
        speed_now = list(calSpeed(nowPoint['左肩'], lastPoint['左肩'], 1/24))
        result.append(carreSum(speed_now))

        speed_last = list(calSpeed(lastPoint['左肩'], last_lastPoint['左肩'], 1/24))
        acceleration = calAcceleration(speed_now, speed_last, 1/24)
        result.append(carreSum(acceleration))
        # 右肩速度、加速度
        speed_now = list(calSpeed(nowPoint['右肩'], lastPoint['右肩'], 1/24))
        result.append(carreSum(speed_now))

        speed_last = list(calSpeed(lastPoint['右肩'], last_lastPoint['右肩'], 1/24))
        acceleration = calAcceleration(speed_now, speed_last, 1/24)
        result.append(carreSum(acceleration))
        # 左肘速度、加速度
        speed_now = list(calSpeed(nowPoint['左肘'], lastPoint['左肘'], 1/24))
        result.append(carreSum(speed_now))

        speed_last = list(calSpeed(lastPoint['左肘'], last_lastPoint['左肘'], 1/24))
        acceleration = calAcceleration(speed_now, speed_last, 1/24)
        result.append(carreSum(acceleration))
        # 右肘速度、加速度
        speed_now = list(calSpeed(nowPoint['右肘'], lastPoint['右肘'], 1/24))
        result.append(carreSum(speed_now))

        speed_last = list(calSpeed(lastPoint['右肘'], last_lastPoint['右肘'], 1/24))
        acceleration = calAcceleration(speed_now, speed_last, 1/24)
        result.append(carreSum(acceleration))
        # 左手速度、加速度
        speed_now = list(calSpeed(nowPoint['左手'], lastPoint['左手'], 1/24))
        result.append(carreSum(speed_now))

        speed_last = list(calSpeed(lastPoint['左手'], last_lastPoint['左手'], 1/24))
        acceleration = calAcceleration(speed_now, speed_last, 1/24)
        result.append(carreSum(acceleration))
        # 右手速度、加速度
        speed_now = list(calSpeed(nowPoint['右手'], lastPoint['右手'], 1/24))
        result.append(carreSum(speed_now))

        speed_last = list(calSpeed(lastPoint['右手'], last_lastPoint['右手'], 1/24))
        acceleration = calAcceleration(speed_now, speed_last, 1/24)
        result.append(carreSum(acceleration))
        # 盆骨速度、加速度
        speed_now = list(calSpeed(nowPoint['盆骨'], lastPoint['盆骨'], 1/24))
        result.append(carreSum(speed_now))

        speed_last = list(calSpeed(lastPoint['盆骨'], last_lastPoint['盆骨'], 1/24))
        acceleration = calAcceleration(speed_now, speed_last, 1/24)
        result.append(carreSum(acceleration))
        # 左屁股速度、加速度
        speed_now = list(calSpeed(nowPoint['左屁股'], lastPoint['左屁股'], 1/24))
        result.append(carreSum(speed_now))

        speed_last = list(calSpeed(lastPoint['左屁股'], last_lastPoint['左屁股'], 1/24))
        acceleration = calAcceleration(speed_now, speed_last, 1/24)
        result.append(carreSum(acceleration))
        # 右屁股速度、加速度
        speed_now = list(calSpeed(nowPoint['右屁股'], lastPoint['右屁股'], 1/24))
        result.append(carreSum(speed_now))

        speed_last = list(calSpeed(lastPoint['右屁股'], last_lastPoint['右屁股'], 1/24))
        acceleration = calAcceleration(speed_now, speed_last, 1/24)
        result.append(carreSum(acceleration))
        # 左膝盖速度、加速度
        speed_now = list(calSpeed(nowPoint['左膝'], lastPoint['左膝'], 1/24))
        result.append(carreSum(speed_now))

        speed_last = list(calSpeed(lastPoint['左膝'], last_lastPoint['左膝'], 1/24))
        acceleration = calAcceleration(speed_now, speed_last, 1/24)
        result.append(carreSum(acceleration))
        # 右膝盖速度、加速度
        speed_now = list(calSpeed(nowPoint['右膝'], lastPoint['右膝'], 1/24))
        result.append(carreSum(speed_now))

        speed_last = list(calSpeed(lastPoint['右膝'], last_lastPoint['右膝'], 1/24))
        acceleration = calAcceleration(speed_now, speed_last, 1/24)
        result.append(carreSum(acceleration))
        # 左脚踝速度、加速度
        speed_now = list(calSpeed(nowPoint['左脚踝'], lastPoint['左脚踝'], 1/24))
        result.append(carreSum(speed_now))

        speed_last = list(calSpeed(lastPoint['左脚踝'], last_lastPoint['左脚踝'], 1/24))
        acceleration = calAcceleration(speed_now, speed_last, 1/24)
        result.append(carreSum(acceleration))
        # 右脚踝速度、加速度
        speed_now = list(calSpeed(nowPoint['右脚踝'], lastPoint['右脚踝'], 1/24))
        result.append(carreSum(speed_now))

        speed_last = list(calSpeed(lastPoint['右脚踝'], last_lastPoint['右脚踝'], 1/24))
        acceleration = calAcceleration(speed_now, speed_last, 1/24)
        result.append(carreSum(acceleration))
        # 左脚尖速度、加速度
        speed_now = list(calSpeed(nowPoint['左脚尖'], lastPoint['左脚尖'], 1/24))
        result.append(carreSum(speed_now))

        speed_last = list(calSpeed(lastPoint['左脚尖'], last_lastPoint['左脚尖'], 1/24))
        acceleration = calAcceleration(speed_now, speed_last, 1/24)
        result.append(carreSum(acceleration))
        # 右脚尖速度、加速度
        speed_now = list(calSpeed(nowPoint['右脚尖'], lastPoint['右脚尖'], 1/24))
        result.append(carreSum(speed_now))

        speed_last = list(calSpeed(lastPoint['右脚尖'], last_lastPoint['右脚尖'], 1/24))
        acceleration = calAcceleration(speed_now, speed_last, 1/24)
        result.append(carreSum(acceleration))


        # 头部动能(头部 + 两只耳朵）
        speed_Head = carreSum(list(calSpeed(nowPoint['头'], lastPoint['头'], 1 / 24)))
        speed_LEar = carreSum(list(calSpeed(nowPoint['左耳'], lastPoint['左耳'], 1 / 24)))
        speed_REar = carreSum(list(calSpeed(nowPoint['右耳'], lastPoint['右耳'], 1 / 24)))
        result.append(calEnergy_three(speed_Head, speed_LEar, speed_REar))

        # 左手动能 （手 + 肘）
        speed_LHand = carreSum(list(calSpeed(nowPoint['左手'], lastPoint['左手'], 1 / 24)))
        speed_LElbow = carreSum(list(calSpeed(nowPoint['左肘'], lastPoint['左肘'], 1 / 24)))
        result.append(calEnergy_two(speed_LHand, speed_LElbow))

        # 右手动能
        speed_RHand = carreSum(list(calSpeed(nowPoint['右手'], lastPoint['右手'], 1 / 24)))
        speed_RElbow = carreSum(list(calSpeed(nowPoint['右肘'], lastPoint['右肘'], 1 / 24)))
        result.append(calEnergy_two(speed_RHand, speed_RElbow))

        # 身体动能（肩膀 + 盆骨 + 屁股）
        speed_P = carreSum(list(calSpeed(nowPoint['盆骨'], lastPoint['盆骨'], 1 / 24)))
        speed_LShoulder = carreSum(list(calSpeed(nowPoint['左肩'], lastPoint['左肩'], 1 / 24)))
        speed_RShoulder = carreSum(list(calSpeed(nowPoint['右肩'], lastPoint['右肩'], 1 / 24)))
        speed_LHip = carreSum(list(calSpeed(nowPoint['左屁股'], lastPoint['左屁股'], 1 / 24)))
        speed_RHip = carreSum(list(calSpeed(nowPoint['右屁股'], lastPoint['右屁股'], 1 / 24)))
        result.append(calEnergy_five(speed_P, speed_LShoulder, speed_RShoulder, speed_LHip, speed_RHip))

        # 左腿动能（脚尖 + 脚踝 + 膝盖）
        speed_LFeet = carreSum(list(calSpeed(nowPoint['左脚尖'], lastPoint['左脚尖'], 1 / 24)))
        speed_LAnkle = carreSum(list(calSpeed(nowPoint['左脚踝'], lastPoint['左脚踝'], 1 / 24)))
        speed_LKnee = carreSum(list(calSpeed(nowPoint['左膝'], lastPoint['左膝'], 1 / 24)))
        result.append(calEnergy_three(speed_LFeet, speed_LAnkle, speed_LKnee))

        # 右腿动能
        speed_RFeet = carreSum(list(calSpeed(nowPoint['右脚尖'], lastPoint['右脚尖'], 1 / 24)))
        speed_RAnkle = carreSum(list(calSpeed(nowPoint['右脚踝'], lastPoint['右脚踝'], 1 / 24)))
        speed_RKnee = carreSum(list(calSpeed(nowPoint['右膝'], lastPoint['右膝'], 1 / 24)))
        result.append(calEnergy_three(speed_RFeet, speed_RAnkle, speed_RKnee))



        # 头部平滑度(头部 + 两只耳朵）
        speed_now = list(calSpeed(nowPoint['头'], lastPoint['头'], 1/24))
        speed_last = list(calSpeed(lastPoint['头'], last_lastPoint['头'], 1/24))
        acceleration_now = calAcceleration(speed_now, speed_last, 1/24)
        smoothHead = calSmooth(speed_now, acceleration_now)

        speed_now = list(calSpeed(nowPoint['左耳'], lastPoint['左耳'], 1/24))
        speed_last = list(calSpeed(lastPoint['左耳'], last_lastPoint['左耳'], 1/24))
        acceleration_now = calAcceleration(speed_now, speed_last, 1/24)
        smoothLEar = calSmooth(speed_now, acceleration_now)

        speed_now = list(calSpeed(nowPoint['右耳'], lastPoint['右耳'], 1/24))
        speed_last = list(calSpeed(lastPoint['右耳'], last_lastPoint['右耳'], 1/24))
        acceleration_now = calAcceleration(speed_now, speed_last, 1/24)
        smoothREar = calSmooth(speed_now, acceleration_now)

        result.append(smoothHead+smoothLEar+smoothREar)

        # 左手平滑度 （手 + 肘）
        speed_now = list(calSpeed(nowPoint['左手'], lastPoint['左手'], 1/24))
        speed_last = list(calSpeed(lastPoint['左手'], last_lastPoint['左手'], 1/24))
        acceleration_now = calAcceleration(speed_now, speed_last, 1/24)
        smoothLHand = calSmooth(speed_now, acceleration_now)

        speed_now = list(calSpeed(nowPoint['左肘'], lastPoint['左肘'], 1/24))
        speed_last = list(calSpeed(lastPoint['左肘'], last_lastPoint['左肘'], 1/24))
        acceleration_now = calAcceleration(speed_now, speed_last, 1/24)
        smoothLElbow = calSmooth(speed_now, acceleration_now)

        result.append(smoothLHand+smoothLElbow)

        # 右手平滑度
        speed_now = list(calSpeed(nowPoint['右手'], lastPoint['右手'], 1/24))
        speed_last = list(calSpeed(lastPoint['右手'], last_lastPoint['右手'], 1/24))
        acceleration_now = calAcceleration(speed_now, speed_last, 1/24)
        smoothRHand = calSmooth(speed_now, acceleration_now)

        speed_now = list(calSpeed(nowPoint['右肘'], lastPoint['右肘'], 1/24))
        speed_last = list(calSpeed(lastPoint['右肘'], last_lastPoint['右肘'], 1/24))
        acceleration_now = calAcceleration(speed_now, speed_last, 1/24)
        smoothRElbow = calSmooth(speed_now, acceleration_now)

        result.append(smoothRHand+smoothRElbow)

        # 身体平滑度（肩膀 + 盆骨 + 屁股）
        speed_now = list(calSpeed(nowPoint['盆骨'], lastPoint['盆骨'], 1/24))
        speed_last = list(calSpeed(lastPoint['盆骨'], last_lastPoint['盆骨'], 1/24))
        acceleration_now = calAcceleration(speed_now, speed_last, 1/24)
        smoothP = calSmooth(speed_now, acceleration_now)

        speed_now = list(calSpeed(nowPoint['左肩'], lastPoint['左肩'], 1/24))
        speed_last = list(calSpeed(lastPoint['左肩'], last_lastPoint['左肩'], 1/24))
        acceleration_now = calAcceleration(speed_now, speed_last, 1/24)
        smoothLShoulder = calSmooth(speed_now, acceleration_now)

        speed_now = list(calSpeed(nowPoint['右肩'], lastPoint['右肩'], 1/24))
        speed_last = list(calSpeed(lastPoint['右肩'], last_lastPoint['右肩'], 1/24))
        acceleration_now = calAcceleration(speed_now, speed_last, 1/24)
        smoothRShoulder = calSmooth(speed_now, acceleration_now)

        speed_now = list(calSpeed(nowPoint['左屁股'], lastPoint['左屁股'], 1/24))
        speed_last = list(calSpeed(lastPoint['左屁股'], last_lastPoint['左屁股'], 1/24))
        acceleration_now = calAcceleration(speed_now, speed_last, 1/24)
        smoothLHip = calSmooth(speed_now, acceleration_now)

        speed_now = list(calSpeed(nowPoint['右屁股'], lastPoint['右屁股'], 1/24))
        speed_last = list(calSpeed(lastPoint['右屁股'], last_lastPoint['右屁股'], 1/24))
        acceleration_now = calAcceleration(speed_now, speed_last, 1/24)
        smoothRHip = calSmooth(speed_now, acceleration_now)

        result.append(smoothP+smoothLShoulder+smoothRShoulder+smoothLHip+smoothRHip)

        # 左腿平滑度（脚尖 + 脚踝 + 膝盖)
        speed_now = list(calSpeed(nowPoint['左脚尖'], lastPoint['左脚尖'], 1/24))
        speed_last = list(calSpeed(lastPoint['左脚尖'], last_lastPoint['左脚尖'], 1/24))
        acceleration_now = calAcceleration(speed_now, speed_last, 1/24)
        smoothLFeet = calSmooth(speed_now, acceleration_now)

        speed_now = list(calSpeed(nowPoint['左脚踝'], lastPoint['左脚踝'], 1/24))
        speed_last = list(calSpeed(lastPoint['左脚踝'], last_lastPoint['左脚踝'], 1/24))
        acceleration_now = calAcceleration(speed_now, speed_last, 1/24)
        smoothLAnkle = calSmooth(speed_now, acceleration_now)

        speed_now = list(calSpeed(nowPoint['左膝'], lastPoint['左膝'], 1/24))
        speed_last = list(calSpeed(lastPoint['左膝'], last_lastPoint['左膝'], 1/24))
        acceleration_now = calAcceleration(speed_now, speed_last, 1/24)
        smoothLKnee = calSmooth(speed_now, acceleration_now)

        result.append(smoothLFeet+smoothLAnkle+smoothLKnee)
        # 右腿平滑度
        speed_now = list(calSpeed(nowPoint['右脚尖'], lastPoint['右脚尖'], 1/24))
        speed_last = list(calSpeed(lastPoint['右脚尖'], last_lastPoint['右脚尖'], 1/24))
        acceleration_now = calAcceleration(speed_now, speed_last, 1/24)
        smoothRFeet = calSmooth(speed_now, acceleration_now)

        speed_now = list(calSpeed(nowPoint['右脚踝'], lastPoint['右脚踝'], 1/24))
        speed_last = list(calSpeed(lastPoint['右脚踝'], last_lastPoint['右脚踝'], 1/24))
        acceleration_now = calAcceleration(speed_now, speed_last, 1/24)
        smoothRAnkle = calSmooth(speed_now, acceleration_now)

        speed_now = list(calSpeed(nowPoint['右膝'], lastPoint['右膝'], 1/24))
        speed_last = list(calSpeed(lastPoint['右膝'], last_lastPoint['右膝'], 1/24))
        acceleration_now = calAcceleration(speed_now, speed_last, 1/24)
        smoothRKnee = calSmooth(speed_now, acceleration_now)

        result.append(smoothRFeet+smoothRAnkle+smoothRKnee)

        # 上半身对称性(左手到脖子，右手到脖子)
        Sx, Sy, Sz = symmetry(nowPoint['脖子'], nowPoint['左手'], nowPoint['右手'])
        result.append(Sx)
        result.append(Sy)
        result.append(Sz)

        # 头部前倾: 头部的速度z值
        speedHead = list(calSpeed(nowPoint['头'], lastPoint['头'], 1 / 24))
        result.append(speedHead[2])
        # 身体前倾：脖子的速度z值
        speedNeck = list(calSpeed(nowPoint['脖子'], lastPoint['脖子'], 1 / 24))
        result.append(speedNeck[2])

        csv_writer.writerow(result)
        i += 1
    # 5. 关闭文件
    f.close()

