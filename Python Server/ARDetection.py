from variables import *

def SLUGDetections(detections, image):
    h,w,_ = image.shape
    
    centerY = h/2
    centerX = w/2

    distanceOld = 1000
    index_token = 0

    for i in range(len(detections)):
        det = detections[i]
        distance = ((centerX - det[0])**2 + (centerY - det[1])**2)**0.5
        if distance < distanceOld:
            distanceOld = distance
            index_token = i
            print(index_token)
    
    id_token = int(detections[int(index_token)][3])
    print(id_token)
    slug_token = str(labels[id_token])
    reliability = str(detections[index_token][2])

    for token in phase_tokens:
        # print(token["name"].lower())
        if token["name"].lower() == slug_token:
            token_type = "phases"
    for token in activity_tokens:
        if token["name"].lower() == slug_token:
            token_type = "activities"


    response = '[{"id":'+str(id_token)+',"slug":"'+slug_token+'","reliability":'+reliability+',"type":"'+token_type +'"}]'

    return response
