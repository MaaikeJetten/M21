from variables import *


def JSONDetections(detections):
    maxY = detections[0][1]
    vertrekpunt = False

    for index in range(len(detections)):
        det = detections[index]
        if det[3] == labels.index("vertrekpunt"):
            vertrekIndex = index
            vertrekpunt = True
            break
        else:
            if detections[index][1] > maxY:
                maxY = detections[index][1]
                vertrekIndex = index
    minDistance = 10000
    # array to make sure only next tokens are being looked at
    doneIndexes = []
    distances = []
    reliability_scores = []
    min_reliability = 0.5
    final_ids = []
    final_sign = False
    first_ids = []
    first_sign = False

    id_token = 0
    token_type = ""
    eindpunt = False
    oldLevel = False

    # start with 'VertrekPunt'
    doneIndexes.append(vertrekIndex)
    distances.append(0)
    newIndex = vertrekIndex
    # print(vertrekpunt)
    # go through all tokens and check which is closest
    for i in range(len(detections)):
        id_token = 0
        distance_level = 1
        # use the token that was closest to the token in the previous round
        detNew = detections[newIndex]
        for index in range(len(detections)):
            # check the token has not been used before and index not in skipIndexes:
            if index not in doneIndexes:
                det = detections[index]
                newDistance = ((detNew[0] - det[0])**2 + (detNew[1] - det[1])**2)**0.5
                #check if new distance is actually the smallest
                if newDistance < minDistance:
                    if newDistance < 10:
                        multipleDetections = True
                    else:
                        multipleDetections = False
                    closestIndex = index
                    minDistance = newDistance
                    # to not repeat final loop
                    new = 1
        if new == 1:
            doneIndexes.append(closestIndex)
            closestClass = detections[closestIndex][3]
            nameLabel = str(labels[int(detections[closestIndex][3])])
            reliability = str(detections[closestIndex][2])
            for token in phase_tokens:
                if token["name"].lower() == nameLabel:
                    id_token = token["id"]
                    token_type = "phases"
            for token in activity_tokens:
                if token["name"].lower() == nameLabel:
                    id_token = token["id"]
                    token_type = "activities"
            if(nameLabel == 'eindpunt'): eindpunt = True
            
            if multipleDetections and not oldLevel:
                first_ids.append(i)
            elif oldLevel and not multipleDetections:
                final_ids.append(i)
            distances.append(minDistance)
        if i == len(detections)-1:
            if oldLevel:
                final_ids.append(i)
        # start next loop with this found token
        oldLevel = multipleDetections
        newIndex = closestIndex
        minDistance = 10000
        new = 0

        
    # Printen van de JSON
    if vertrekpunt :
        json_tokens = '['
    else:
        json_tokens = '[{"id": 6,"slug":"vertrekpunt","reliability":1.1,"type":"phases"},'

    for i in range(len(doneIndexes)):
        id_token = 0
        nameLabel = str(labels[int(detections[doneIndexes[i]][3])])
        reliability = str(detections[doneIndexes[i]][2])
        for token in phase_tokens:
            # print(token["name"].lower())
            if token["name"].lower() == nameLabel:
                id_token = token["id"]
                token_type = "phases"
        for token in activity_tokens:
            if token["name"].lower() == nameLabel:
                id_token = token["id"]
                token_type = "activities"
        if(nameLabel == 'eindpunt'): eindpunt = True
        
        for final in final_ids:
            if i == final:
                final_sign = True
                break
            else:
                final_sign = False
        for first in first_ids:
            if i == first:
                first_sign = True
                break
            else:
                first_sign = False
        
        if first_sign:
            json_tokens += '{"id": 61,"slug":"onbekend","reliability":1.1,"type":"activities", "options": ['
        
        if (nameLabel == "literatuur-lezen"):
            nameLabel = "literatuur-inzetten"
        
        json_tokens += '{"id":'+str(id_token)+',"slug":"'+nameLabel+'","reliability":'+reliability+',"type":"'+token_type +'"}'
        
        if final_sign:
            json_tokens += ']}'
        
        if i != len(doneIndexes)-1: 
            json_tokens += ','
        
        # print(str(id_token) + " : " + nameLabel + " : " + str(detections[doneIndexes[i]][2]) + " : " + str(distances[i]))

    if eindpunt :
        json_tokens += ']'
    else:
        json_tokens += ',{"id": 7,"slug":"eindpunt","reliability":1.1,"type":"phases"}]'
    
    return json_tokens
