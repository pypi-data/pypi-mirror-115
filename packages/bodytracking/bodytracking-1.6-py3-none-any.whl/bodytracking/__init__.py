import cv2,mediapipe,time,keyboard,numpy
class Hand:
    def __init__(self,n_hand:int,lm:list,handLms):
        self.hand_n             = n_hand
        self.sol                = mediapipe.solutions
        self.lm_list            = lm
        self.hand_lms           = handLms
        self.mpHands            = self.sol.hands
        self.WRIST              = self.lm_list[0]
        self.THUMB_CMC          = self.lm_list[1]
        self.THUMB_MCP          = self.lm_list[2]
        self.THUMB_IP           = self.lm_list[3]
        self.THUMB_TIP          = self.lm_list[4]
        self.INDEX_FINGER_MCP   = self.lm_list[5]
        self.INDEX_FINGER_PIP   = self.lm_list[6]
        self.INDEX_FINGER_DIP   = self.lm_list[7]
        self.INDEX_FINGER_TIP   = self.lm_list[8]
        self.MIDDLE_FINGER_MCP  = self.lm_list[9]
        self.MIDDLE_FINGER_PIP  = self.lm_list[10]
        self.MIDDLE_FINGER_DIP  = self.lm_list[11]
        self.MIDDLE_FINGER_TIP  = self.lm_list[12]
        self.RING_FINGER_MCP    = self.lm_list[13]
        self.RING_FINGER_PIP    = self.lm_list[14]
        self.RING_FINGER_DIP    = self.lm_list[15]
        self.RING_FINGER_TIP    = self.lm_list[16]
        self.PINKY_MCP          = self.lm_list[17]
        self.PINKY_PIP          = self.lm_list[18]
        self.PINKY_DIP          = self.lm_list[19]
        self.PINKY_TIP          = self.lm_list[20]
        self.THUMB              = [self.THUMB_CMC,self.THUMB_MCP,self.THUMB_IP,self.THUMB_TIP]
        self.INDEX              = [self.INDEX_FINGER_MCP,self.INDEX_FINGER_PIP,self.INDEX_FINGER_DIP,self.INDEX_FINGER_TIP]
        self.MIDDLE             = [self.MIDDLE_FINGER_MCP,self.MIDDLE_FINGER_PIP,self.MIDDLE_FINGER_DIP,self.MIDDLE_FINGER_TIP]
        self.RING               = [self.RING_FINGER_MCP,self.RING_FINGER_PIP,self.RING_FINGER_DIP,self.RING_FINGER_TIP]
        self.PINKY              = [self.PINKY_MCP,self.PINKY_PIP,self.PINKY_DIP,self.PINKY_TIP]
class Pose:
    def __init__(self,lm_list:list,res):
        self.lm_list          = lm_list
        self.results          = res
        self.nose             = lm_list[0]
        self.left_eye_inner   = lm_list[1]
        self.left_eye         = lm_list[2]
        self.left_eye_outer   = lm_list[3]
        self.right_eye_inner  = lm_list[4]
        self.right_eye        = lm_list[5]
        self.right_eye_outer  = lm_list[6]
        self.left_ear         = lm_list[7]
        self.right_ear        = lm_list[8]
        self.mouth_left       = lm_list[9]
        self.mouth_right      = lm_list[10]
        self.left_shoulder    = lm_list[11]
        self.right_shoulder   = lm_list[12]
        self.left_elbow       = lm_list[13]
        self.right_elbow      = lm_list[14]
        self.left_wrist       = lm_list[15]
        self.right_wrist      = lm_list[16]
        self.left_pinky       = lm_list[17]
        self.right_pinky      = lm_list[18]
        self.left_index       = lm_list[19]
        self.right_index      = lm_list[20]
        self.left_thumb       = lm_list[21]
        self.right_thumb      = lm_list[22]
        self.left_hip         = lm_list[23]
        self.right_hip        = lm_list[24]
        self.left_knee        = lm_list[25]
        self.right_knee       = lm_list[26]
        self.left_ankle       = lm_list[27]
        self.right_ankle      = lm_list[28]
        self.left_heel        = lm_list[29]
        self.right_heel       = lm_list[30]
        self.left_foot_index  = lm_list[31]
        self.right_foot_index = lm_list[32]
class FaceMesh:
    def __init__(self,lm_list:list,faceLms):
        # There is no landmark index on mediapipe.dev
        List = []
        for l in lm_list:
            List.append((l[0]))
        self.lms = List
        self.lms_ext = lm_list
        self.fLms = faceLms
class Face:
    def __init__(self,lm_list:list,res,score:int,bbox):
        # There is no landmark index on mediapipe.dev
        List = []
        for l in lm_list:
            List.append((l[0]))
        self.lms = List
        self.results = res
        self.conf_score = score
        self.bbox = bbox
        self.ext_lms = lm_list
class Utils:
    def absa(c1:tuple,c2:tuple,t:int):
        """
        Gets two tuples and looks if the (1) values is
        about the same, by subtracting the smaller one from
        the bigger one and looking if the bigger one is bigger
        than t.
        """
        thresh = t
        C1,C2 = c1[1],c2[1]
        if C1 > C2:
            F1 = C1 - C2
            if F1 < thresh:return True
            else:return False
        else:
            F1 = C2 - C1
            if F1 < thresh: return True
            else:return False
class HandDetector:
    def __init__(self,mode=False,maxHands=2,detectionConfidence=0.5,trackConfidence=0.5):
        """
        Sets all the values for mediapipe and the other HandDetector functions.
        """
        self.mode = mode
        self.maxHands = maxHands
        self.detectConf = detectionConfidence
        self.trackConf = trackConfidence
        self.sol = mediapipe.solutions
        self.mpHands = self.sol.hands
        self.hands = self.mpHands.Hands(self.mode,self.maxHands,self.detectConf,self.trackConf)
        self.mpDraw = self.sol.drawing_utils
        self.nt_list = [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0),(0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
    def get_Hands(self,img):
        """
        Finds the hands img the given img, needs RGB img
        to find the hands, so it first converts them.
        Returns the Hand object with all the landmarks for each hand.
        !!! ONLY INITIALIZE THIS ONCE!!!
        """
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        res = self.hands.process(imgRGB)
        HAND = 0
        if res.multi_hand_landmarks:
            for handLms in res.multi_hand_landmarks:
                HAND = HAND + 1
                List = []
                for id, lm in enumerate(handLms.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    List.append((cx,cy))
                yield Hand(HAND,List,handLms)
        else:
            return Hand(1,self.nt_list,[])
    def draw_hand(self,img,hand:Hand):
        """
        Draws the Landmarks and connections on the image.
        """
        self.mpDraw.draw_landmarks(img,hand.hand_lms ,self.mpHands.HAND_CONNECTIONS)
        return True
class PoseDetector:
    def __init__(self,static_image_mode=False,model_complexity=1,smooth_landmarks=True,min_detection_confidence=0.5,min_tracking_confidence=0.5):
        """
        Sets all the values for mediapipe and the other PoseDetector functions.
        !!! ONLY INITIALIZE THIS ONCE!!!
        """
        self.static_image_mode = static_image_mode
        self.model_complexity = model_complexity
        self.smooth_landmarks = smooth_landmarks
        self.min_detection_conf = min_detection_confidence
        self.min_tracking_conf = min_tracking_confidence
        self.sol = mediapipe.solutions
        self.mpPose = self.sol.pose
        self.pose = self.mpPose.Pose(self.static_image_mode, model_complexity, smooth_landmarks, min_detection_confidence, min_tracking_confidence)
        self.nt_list = [(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),(0,0),]
        self.mpDraw = self.sol.drawing_utils
    def get_Pose(self,img,wd=True):
        """
        Transforms the img to RGB and then builds the Pose object
        based off all the landmarks on the frame.
        Returns the Pose object with the complete list of landmarks.
        """
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        res = self.pose.process(imgRGB).pose_landmarks
        if res:
            List = []
            if wd:
                for id, lm in enumerate(res.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)        # I have not tested the two person option, bcuz i have no friends
                    List.append((cx,cy))
                try:
                    yield Pose(List, res)
                except IndexError:
                    return Pose(self.nt_list, [])
            else:
                yield Pose(self.nt_list, res)
        else:
            return Pose(self.nt_list,[])
    def draw_pose(self,img,pose:Pose):
        """
        Draws the Landmarks and connections on the image.
        """
        self.mpDraw.draw_landmarks(img,pose.results,self.mpPose.POSE_CONNECTIONS)
        return True
class FaceMeshDetector:
    def __init__(self,static_image_mode=False,max_num_faces=1,min_detection_confidence=0.5,min_tracking_confidence=0.5):
        """
        Sets all the values for mediapipe and the other PoseDetector functions.
        !!! ONLY INITIALIZE THIS ONCE!!!
        """
        self.static_image_mode = static_image_mode
        self.max_num_faces = max_num_faces
        self.min_detection_conf = min_detection_confidence
        self.min_tracking_conf = min_tracking_confidence
        self.sol = mediapipe.solutions
        self.mpDraw = self.sol.drawing_utils
        self.mpFaceMesh = self.sol.face_mesh
        self.face_mesh = self.mpFaceMesh.FaceMesh()
        self.drawSpec = self.mpDraw.DrawingSpec(thickness=1, circle_radius=2)
    def get_faces(self,img):
        """
        Transforms the img to RGB and then builds the FaceMesh object
        based off all the landmarks on the frame.
        Returns the FaceMesh object with the complete list of landmarks.
        """
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res = self.face_mesh.process(imgRGB)
        if res.multi_face_landmarks:
            for faceLms in res.multi_face_landmarks:
                List = []
                c = -1
                for lm in faceLms.landmark:
                    c = c + 1
                    ih, iw, ic = img.shape
                    cx, cy = int(lm.x * iw), int(lm.y * ih)
                    List.append(((cx,cy),c))
                yield FaceMesh(List,faceLms)
    def draw_mesh(self,img,face_mesh:FaceMesh):
        """
        Draws the Landmarks and connections on the image.
        """
        self.mpDraw.draw_landmarks(img,face_mesh.fLms,self.mpFaceMesh.FACE_CONNECTIONS,self.drawSpec,self.drawSpec)
        return True
class FaceDetection:
    def __init__(self,min_detection_confidence=0.5, model_selection=1):
        self.sol = mediapipe.solutions
        self.mpFaceDetection = self.sol.face_detection
        self.mpDraw = self.sol.drawing_utils
        self.min_detection_conf = min_detection_confidence
        self.model_selection = model_selection
        self.FaceDetection = self.mpFaceDetection.FaceDetection(self.min_detection_conf,self.model_selection)
    def get_faces(self,img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res = self.FaceDetection.process(imgRGB)
        if res.detections:
            for id, detections in enumerate(res.detections):
                iw, ih, ic = img.shape
                score = int(float(detections.score[0]) * 100)
                ld = detections.location_data
                rbb = ld.relative_bounding_box
                bbox = int(rbb.xmin * iw)+55, int(rbb.ymin * ih)-70, int(rbb.width * iw)+50, int(rbb.height * ih)-20
                List = []
                c = 0
                for kp in ld.relative_keypoints:
                    c = c + 1
                    cx, cy = int(kp.x * iw)+85, int(kp.y * ih)-50
                    cent = (cx, cy)
                    List.append((cent,c))
                yield Face(List,res,score,bbox)
    def draw_face(self,img,face:Face):
        cv2.rectangle(img,face.bbox,color=(0,0,255),thickness=3)
        for lm in face.lms:
            cv2.circle(img,(lm[0],lm[1]),1,(0,0,255),1)
        cv2.putText(img,f'{face.conf_score}%',(face.bbox[0],face.bbox[1]),cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
class Gestures:
    """
    Looks at the bottom of the finger and on the tip, if
    the tip is higher, it returns true. Ont the thumb it looks
    at the bottom and the point above, if both are about the same
    it returns true.

    The locked gestures (ROCK,SCISSOR,PAPER) look at the fingers up and
    returns true if the right fingers are up/down.
    """
    def INDEX_finger_up(hand:Hand):
        L1 = hand.INDEX
        if L1[0][1] > L1[3][1]:return True
        else:return False
    def THUMB_finger_up(hand:Hand):
        L1 = hand.THUMB
        if L1[0][1] > L1[3][1] and not Utils.absa(L1[0],L1[1],22):
            return True
        else:
            return False
    def PINKY_finger_up(hand:Hand):
        L1 = hand.PINKY
        if L1[0][1] > L1[3][1]:return True
        else:return False
    def RING_finger_up(hand:Hand):
        L1 = hand.RING
        if L1[0][1] > L1[3][1]:return True
        else:return False
    def MIDDLE_finger_up(hand:Hand):
        L1 = hand.MIDDLE
        if L1[0][1] > L1[3][1]:return True
        else:return False
    def paper(hand:Hand):
        if Gestures.INDEX_finger_up(hand) and Gestures.RING_finger_up(hand) and Gestures.PINKY_finger_up(hand) and Gestures.MIDDLE_finger_up(hand):
            return True
        else:
            return False
    def rock(hand:Hand):
        if Gestures.INDEX_finger_up(hand) or Gestures.RING_finger_up(hand) or Gestures.PINKY_finger_up(hand) or Gestures.MIDDLE_finger_up(hand):
            return False
        else:
            return True
    def scissor(hand:Hand):
        if Gestures.INDEX_finger_up(hand) and Gestures.MIDDLE_finger_up(hand) and not Gestures.RING_finger_up(hand) and not Gestures.PINKY_finger_up(hand):
            return True
        else:
            return False
class Segmentation:
    def __init__(self,rep_img:str,rem_perc:float,bod=False):
        """
        rep_img is the replacement for the background.
        rem_perc is the percentage of the background that gets deleted (0.85 is good)
        bod is if the foreground or the background should be replaced
        """
        self.rem = rem_perc
        self.body = bod
        self.replace_img = rep_img
        self.mp_selfie_segmentation = mediapipe.solutions.selfie_segmentation
        self.model = self.mp_selfie_segmentation.SelfieSegmentation()
    def segment(self,img):
        """
        The given background Image must be the same size as the normal Image
        """
        img.flags.writeable = False
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        res = self.model.process(imgRGB)
        img.flags.writeable = True
        background = cv2.imread(self.replace_img)
        if self.body:
            mask = numpy.stack((res.segmentation_mask,) * 3, axis=-1) < self.rem
        else:
            mask = numpy.stack((res.segmentation_mask,) * 3, axis=-1) > self.rem
        segmented_image = numpy.where(mask, imgRGB, background)
        got_image = cv2.cvtColor(segmented_image, cv2.COLOR_RGB2BGR)
        return got_image
class Examples:
    def SPS(input=1,quit_key='esc'):
        """
        Simple scissor paper rock game. Input is for 'cv2.VideoCapture(input)'
        """
        global a_time,erg
        erg = 0
        class hand_init:
            def zei(hand: Hand):
                g1, g2, g3 = Gestures.paper(hand), Gestures.rock(hand), Gestures.scissor(hand)
                if g1:
                    cv2.putText(img, f'PAPER', (10, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
                    return 1
                elif g2:
                    cv2.putText(img, f'ROCK', (10, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
                    return 2
                elif g3:
                    cv2.putText(img, f'SCISSOR', (10, 50), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255), 1)
                    return 3
                else:return 4
            def pst(a1: int, a2: int):
                global erg
                if a1 == 4 or a2 == 4:
                    erg = 3
                    return
                if a1 == 1:
                    if a2 == 1:
                        erg = 4
                        return
                    elif a2 == 2:
                        erg = 1
                        return
                    elif a2 == 3:
                        erg = 2
                        return
                elif a1 == 2:
                    if a2 == 2:
                        erg = 4
                        return
                    elif a2 == 3:
                        erg = 1
                        return
                    elif a2 == 1:
                        erg = 2
                        return
                elif a1 == 3:
                    if a2 == 1:
                        erg = 1
                        return
                    elif a2 == 2:
                        erg = 2
                        return
                    elif a2 == 3:
                        erg = 4
                        return
        vid = cv2.VideoCapture(input)
        detector = HandDetector(detectionConfidence=0.75, trackConfidence=0.75)
        a_time = time.time() + 5
        while True:
            _, img = vid.read()
            hands = detector.get_Hands(img)
            c_time = time.time()
            for hand in hands:
                if not erg == 0:
                    if erg == 1:cv2.putText(img, 'PLAYER1 WON SHOW ONLY INDEX FINGER TO RESTART', (20, 50),cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                    elif erg == 2:cv2.putText(img, 'PLAYER2 WON SHOW ONLY INDEX FINGER TO RESTART', (20, 50),cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                    elif erg == 3:cv2.putText(img, 'WRONG GESTURE SHOW ONLY INDEX FINGER TO RESTART', (20, 50),cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                    elif erg == 4:cv2.putText(img, 'NOT SURE SHOW ONLY INDEX FINGER TO RESTART', (20, 50), cv2.FONT_HERSHEY_PLAIN,2, (255, 255, 255), 2)
                    if Gestures.INDEX_finger_up(hand) and not Gestures.RING_finger_up(hand) and not Gestures.PINKY_finger_up(hand) and not Gestures.MIDDLE_finger_up(hand) and not Gestures.THUMB_finger_up(hand):
                        cv2.putText(img, 'RESTARTING', (50, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)
                        a_time = time.time() + 5
                        erg = 0
                        continue
                elif Utils.absa((0, c_time), (0, a_time), 0.1):
                    if hand.hand_n == 1:
                        global a1
                        a1 = hand_init.zei(hand)
                    elif hand.hand_n == 2:a2 = hand_init.zei(hand)
                elif erg == 0:cv2.putText(img, f'STARTING IN : {str(a_time - c_time)}', (20, 50), cv2.FONT_HERSHEY_PLAIN, 2,(255, 255, 255), 2)
                cv2.putText(img, str(hand.hand_n), hand.WRIST, cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
            if Utils.absa((0, c_time), (0, a_time), 0.1):
                try:hand_init.pst(a1, a2)
                except NameError:erg = 0
            cv2.imshow("Image", img)
            if keyboard.is_pressed(quit_key):return
            cv2.waitKey(1)
    def face_detection(input=1,quit_key='esc'):
        cap = cv2.VideoCapture(input)
        pTime = time.time()
        detector = FaceDetection()
        while True:
            _, img = cap.read()
            faces = detector.get_faces(img)
            for face in faces:
                for lm in face.lms:
                    cv2.putText(img,f'{str(face.ext_lms[1][1])}',lm,cv2.FONT_HERSHEY_PLAIN,2,(0,0,255),2)
                detector.draw_face(img, face)
            cTime = time.time()
            fps = 1 / (cTime - pTime)
            cv2.putText(img, f'FPS : {str(int(fps))}', (10, 50), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            pTime = cTime
            cv2.imshow("Image", img)
            if keyboard.is_pressed(quit_key):
                return
            cv2.waitKey(1)
    def bg_removal(rep_img:str,rep_perc:float,input=1,quit_key='esc'):
        cap = cv2.VideoCapture(1)
        seg = Segmentation(rep_img,rep_perc)
        while True:
            _, img = cap.read()
            ref_img = seg.segment(img)
            cv2.imshow("Image", ref_img)
            cv2.waitKey(1)