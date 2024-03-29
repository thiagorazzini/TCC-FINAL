import cv2

detectorFace = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
reconhecedor = cv2.face.FisherFaceRecognizer_create()
reconhecedor.read("classificadorFisher.yml")
largura, altura = 220, 220
font = cv2.FONT_HERSHEY_COMPLEX_SMALL
ds_factor=0.6

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        conectado, imagem = self.video.read()
        imagemCinza=cv2.cvtColor(imagem,cv2.COLOR_BGR2GRAY)
        facesDetectadas = detectorFace.detectMultiScale(imagemCinza,scaleFactor=1.5, minSize=(30, 30))

        for(x, y, l, a) in facesDetectadas:
            imagemFace = cv2.resize(imagemCinza[y:y + a, x:x + l], (largura, altura))
            cv2.rectangle(imagem, (x, y), (x + l, y + a), (0,0,255), 2)
            id, confianca = reconhecedor.predict(imagemFace)
            nome = ""
            if id == 1:
                nome = 'Thiago'
            elif id == 2:
                nome = 'Augusto'
            cv2.putText(imagem, nome, (x,y +(a+30)), font, 2, (0,0,255))
            cv2.putText(imagem, str(confianca), (x,y + (a+50)), font, 1, (0,0,255))
        # cv2.imshow("Face", imagem)
        	
        ret, jpeg = cv2.imencode('.jpg', imagem)
        return jpeg.tobytes()
