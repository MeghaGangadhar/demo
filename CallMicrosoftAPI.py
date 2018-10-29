import http.client, urllib.request, urllib.parse, urllib.error, base64, requests, json
import requests
from io import BytesIO
from PIL import Image, ImageDraw

###############################################
#### Update or verify the following values. ###
###############################################

# Replace the subscription_key string value with your valid subscription key.
subscription_key = '17dbdd001e1f462e94d3969c2f0b85b7'

# Replace or verify the region.
#
# You must use the same region in your REST API call as you used to obtain your subscription keys.
# For example, if you obtained your subscription keys from the westus region, replace 
# "westcentralus" in the URI below with "westus".
#
# NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
# a free trial subscription key, you should not need to change this region.
uri_base = 'https://westcentralus.api.cognitive.microsoft.com'

# Request headers.
headers = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
}

# Request parameters.
params = {
    'returnFaceId': 'true',
    'returnFaceLandmarks': 'false',
    'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise',
}

def call_mico_api(path):
    
    image=open(path,'rb').read()
    try:
        # Execute the REST API call and get the response.
        response = requests.request('POST', uri_base + '/face/v1.0/detect', data=image, headers=headers, params=params)
    
        print ('Response:')
        parsed = json.loads(response.text)
        age=parsed[0]['faceAttributes']['age']
        gender=parsed[0]['faceAttributes']['gender']

        facialHair_beard=parsed[0]['faceAttributes']['facialHair']['beard']
        facialHair_moustache=parsed[0]['faceAttributes']['facialHair']['moustache']
        facialHair_sideburns=parsed[0]['faceAttributes']['facialHair']['sideburns']


        makeup_eyeMakeup=parsed[0]['faceAttributes']['makeup']['eyeMakeup']
        makeup_lipMakeup=parsed[0]['faceAttributes']['makeup']['lipMakeup']
        return age,gender,facialHair_beard,facialHair_moustache,facialHair_sideburns,makeup_eyeMakeup,makeup_lipMakeup

        #print (json.dumps(parsed, sort_keys=True, indent=2))
    
    except Exception as e:
        print('Error:')
        print(e)
#call_mico_api("C:/Users/vmestha/Documents/My Received Files/roi.png")
####################################
