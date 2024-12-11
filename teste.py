import cv2
import speech_recognition as sr
from googletrans import Translator


recognizer = sr.Recognizer()
translator = Translator()

# Configurar a captura de vídeo
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  


while True:
    
    ret, frame = cap.read()
    if not ret:
        break

   
    with sr.Microphone() as source:
        print("Fale algo em inglês...")
        try:
            audio = recognizer.listen(source, timeout=5)  
            english_text = recognizer.recognize_google(audio, language='en-US')
            print(f"Texto reconhecido: {english_text}")

            
            translated_text = translator.translate(english_text, src='en', dest='pt').text
            print(f"Tradução: {translated_text}")

            
            cv2.putText(frame, translated_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, (255, 255, 255), 2, cv2.LINE_AA)

        except sr.UnknownValueError:
            print("Não foi possível reconhecer a fala.")
        except sr.RequestError:
            print("Erro na API de reconhecimento de fala.")

    # Mostrar o vídeo com a legenda
    cv2.imshow('Tradutor em Tempo Real', frame)

    # Pressione 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Finalizar captura de vídeo
cap.release()
cv2.destroyAllWindows()
