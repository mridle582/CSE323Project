import math
import os

working_dir = os.path.dirname(__file__)

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
with open(os.path.join(working_dir, "poses.txt"), 'r') as input:
    
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
        pose.rightAnkle = line.split()
        poseref.append(pose)
        poses.append(poseref)
def closeness_of_pose(ref, mannequin):
    #let mannequin also be a pose
    closeness=0
    #measure how close each individual part is to the mannequin
    #distance formula -> d = sqrt((refheadx-mannequinheadx)^2 + (refheady-mannequinheady)^2)
    headdist = math.sqrt((float(ref.head[0])-mannequin.head[0])**2 + (float(ref.head[1])-mannequin.head[1])**2)
    leftShoulderdist = math.sqrt((float(ref.leftShoulder[0])-mannequin.leftShoulder[0])**2 + (float(ref.leftShoulder[1])-mannequin.leftShoulder[1])**2)
    rightShoulderdist = math.sqrt((float(ref.rightShoulder[0])-mannequin.rightShoulder[0])**2 + (float(ref.rightShoulder[1])-mannequin.rightShoulder[1])**2)
    leftElbowdist = math.sqrt((float(ref.leftElbow[0])-mannequin.leftElbow[0])**2 + (float(ref.leftElbow[1])-mannequin.leftElbow[1])**2)
    rightElbowdist = math.sqrt((float(ref.rightElbow[0])-mannequin.rightElbow[0])**2 + (float(ref.rightElbow[1])-mannequin.rightElbow[1])**2)
    leftWristdist = math.sqrt((float(ref.leftWrist[0])-mannequin.leftWrist[0])**2 + (float(ref.leftWrist[1])-mannequin.leftWrist[1])**2)
    rightWristdist = math.sqrt((float(ref.rightWrist[0])-mannequin.rightWrist[0])**2 + (float(ref.rightWrist[1])-mannequin.rightWrist[1])**2)
    leftHipdist = math.sqrt((float(ref.leftHip[0])-mannequin.leftHip[0])**2 + (float(ref.leftHip[1])-mannequin.leftHip[1])**2)
    rightHipdist = math.sqrt((float(ref.rightHip[0])-mannequin.rightHip[0])**2 + (float(ref.rightHip[1])-mannequin.rightHip[1])**2)
    leftKneedist = math.sqrt((float(ref.leftKnee[0])-mannequin.leftKnee[0])**2 + (float(ref.leftKnee[1])-mannequin.leftKnee[1])**2)
    rightKneedist = math.sqrt((float(ref.rightKnee[0])-mannequin.rightKnee[0])**2 + (float(ref.rightKnee[1])-mannequin.rightKnee[1])**2)
    leftAnkledist = math.sqrt((float(ref.leftAnkle[0])-mannequin.leftAnkle[0])**2 + (float(ref.leftAnkle[1])-mannequin.leftAnkle[1])**2)
    rightAnkledist = math.sqrt((float(ref.rightAnkle[0])-mannequin.rightAnkle[0])**2 + (float(ref.rightAnkle[1])-mannequin.rightAnkle[1])**2)
    closeness = (headdist+leftShoulderdist+rightShoulderdist+leftElbowdist+rightElbowdist+leftWristdist+rightWristdist+leftHipdist+rightHipdist+leftKneedist+rightKneedist+leftAnkledist+rightAnkledist)/13
    #might make it weighted average if people want to have a preference for like, arm positions or leg positions or something, we can tweak it
    return closeness

def get_closestpose(mannequin):
    #let mannequin also be a pose 
    chosen = 0
    closeratings = []
    for pose in poses:
        closeratings.append(closeness_of_pose(pose[1],mannequin))
    #find best closeness out of closeratings and set that index to be chosen (lowest number is the best)
    chosen = closeratings.index(min(closeratings))
    return poses[chosen][0]
