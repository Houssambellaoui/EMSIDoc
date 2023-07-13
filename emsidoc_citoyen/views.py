from datetime import date
import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .forms import DocumentForm
from emsidoc_sharedmodel.models import Document
from emsidoc_admin.models import User
import PyPDF2
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import cv2
import numpy as np
import face_recognition
from django.contrib.auth import logout


def verify_identity(image_path):
    known_image = face_recognition.load_image_file(image_path)
    known_encoding = face_recognition.face_encodings(known_image)[0]

    cap = cv2.VideoCapture(0)
    match = False
    i=0
    while i!= 5:
        i=i+1
        _, img = cap.read()

        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(imgS)
        face_encodings = face_recognition.face_encodings(imgS, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces([known_encoding], face_encoding)
            face_distance = face_recognition.face_distance([known_encoding], face_encoding)
            print(face_distance)

            if matches[0]:
                match = True

            top, right, bottom, left = face_location
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            cv2.rectangle(img, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.rectangle(img, (left, bottom-35), (right, bottom), (0, 0, 255), cv2.FILLED)
            cv2.putText(img, "Match Found" if match else "Unknown", (left+6, bottom-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

        cv2.imshow('Face Recognition', img)
        key = cv2.waitKey(1)
        
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return match

# Create your views here.
def indexC(request):
    User = request.session['USER']
    user_type = User["type"]
    documents = Document.objects.filter(proprietaire=User['id'])
    
    context = {
        'documents': documents,
        'Usertype':user_type
        
    }
    return render(request, 'pages/indexCitoyen.html', context )


def delete(request, id):
    doc_delete = get_object_or_404(Document, Doc_id=id)
    if request.method == 'POST':
        doc_delete.delete()
        return redirect('/citoyen')
    return render(request, 'pages/deleteDoc.html')

def docform(request):
    type_choix = [
        "Attestation",
        "Aval",
        "certificat de preuve d identite",
        "certificat d enagement",
    ]
    user2 = request.session['USER']
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        print(form)
        user = request.session['USER']
        user_type = user["type"]
        print(user_type)
        known_image_path = user["img_user"]  # Replace with the path to your known image
        
        # Call the verify_identity function with the known image path
        match = verify_identity(known_image_path)
        print(f"Match: {match}")
        if(match):
                print("enter")
                print(form.is_valid())
                if form.is_valid():
                    print("enter2")
                    # Create a new Document instance from the form data
                    document = form.save(commit=False)
                    
                    # Set the document's proprietaire and date_enregistrement attributes
                    user_id = User.objects.get(id=user["id"])
                    document.proprietaire = user_id
                    document.date_enregistrement = date.today()
                    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                    filename = f"{timestamp}_{request.FILES['fichier'].name}"
                    print(document.fichier.name)
                    print(filename)
                    document.fichier.name = filename
                    print(document.fichier.name)
                    form.save()
                
                
                
                    if 'sign' in request.POST:
                    # Perform the PDF watermarking
                        inputfile = document.fichier.path
                        outputfile = document.fichier.path
                        watermark = user["signature"]
                        
                        with open(inputfile, 'rb') as inputefile:
                            pdf = PyPDF2.PdfReader(inputfile)

                        with open(watermark, 'rb') as watermarkfile:
                            watermarkpdf = PyPDF2.PdfReader(watermarkfile)
                            p = pdf.pages[0]
                            w = watermarkpdf.pages[0]

                            p.merge_page(w)
                            pdfwriter = PyPDF2.PdfWriter()
                            pdfwriter.add_page(p)

                            with open(outputfile, 'wb') as outputfilecontent:
                                pdfwriter.write(outputfilecontent)

                        # Update the Document instance with the modified file path
                        document.fichier = outputfile

                        # Save the Document instance to the database
                    # document.save()

                        return redirect('/citoyen')
                    else:
                     return redirect('/citoyen')
        else:
            return redirect('/citoyen')
       
    else:
        form = DocumentForm()
    return render(request, 'pages/DocumentForm.html', {'form': form, 'type_choix': type_choix } )
def logout_view(request):
    logout(request)
    return redirect('/')