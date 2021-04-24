class Pose:
    head = []
    leftShoulder = []
    rightShoulder = []
    leftElbow = []
    rightElbow = []
    leftWrist = []
    rightWrist = []
    leftHip = []
    rightHip = []
    leftKnee = []
    rightKnee = []
    leftAnkle = []
    rightAnkle = []

#Read pose data from file
poses = []
with open('BackEnd\poses.txt', 'r') as input:
    
    while True:
        line = input.readline()
        if not line:
            break
        poseref = []
        pose = Pose()
        poseref.append(line) #first line is the image url
        line = input.readline() #second line is headx and heady
        pose.head = line.split()
        line = input.readline() #third line is left shoulder
        pose.leftShoulder = line.split()
        line = input.readline() #fourth line is right shoulder
        pose.rightShoulder = line.split()
        line = input.readline() #fifth line is left elbow
        pose.leftElbow = line.split()
        line = input.readline() #sixth line is right elbow
        pose.rightElbow = line.split()
        line = input.readline() #seventh line is left wrist
        pose.leftWrist = line.split()
        line = input.readline() #eigth line is right wrist
        pose.rightWrist = line.split()
        line = input.readline() #ninth line is left Hip
        pose.leftHip = line.split()
        line = input.readline() #tenth line is right Hip
        pose.rightHip = line.split()
        line = input.readline() #eleventh line is left knee
        pose.leftKnee = line.split()
        line = input.readline() #twelfth line is right knee
        pose.rightKnee = line.split()
        line = input.readline() #thirteenth line is left ankle
        pose.leftAnkle = line.split()
        line = input.readline() #fourteenth line is right ankle
        pose.rightHip = line.split()
        poseref.append(pose)
        poses.append(poseref)
def closeness_of_pose(ref, mannequin):
    #let mannequin also be a pose
    closeness=0
    #measure how close each individual part is to the mannequin, how do we determine closeness anyhow?
    return closeness

def get_closestpose(mannequin):
    #let mannequin also be a pose 
    chosen = 0
    closeratings = []
    for pose in poses:
        closeratings.append(closeness_of_pose(pose,mannequin))
    #find best closeness out of closeratings and set that index to be chosen
    return poses[chosen][0]