import PyPDF2
from django.shortcuts import render, redirect, get_object_or_404
from emsidoc_citoyen.forms import DocumentForm
from emsidoc_citoyen.views import verify_identity
import PyPDF2
from reportlab.lib.units import inch 
from  datetime import date
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
import datetime
import os
from django.contrib.auth import logout

from emsidoc_sharedmodel.models import Document
def add_signature_and_date(c, signature_path):
    # Load the image of the signature
    signature_image = signature_path
    signature_width = 2 * inch  # Adjust the width of the signature image as desired
    signature_height = 1 * inch  # Adjust the height of the signature image as desired

    # Set the font and size for the date
    c.setFont("Helvetica", 12)  # Adjust the font and size as desired

    # Add the current date above the image
    current_date = date.today().strftime('%B %d, %Y')  # Format the current date as desired
    c.drawCentredString(letter[0] / 2, inch, current_date)  # Adjust the y-coordinate as desired

    # Add the signature image at the right bottom
    c.drawImage(signature_image, letter[0] - signature_width, 0, width=signature_width, height=signature_height)

    return c
# Create your views here.
def index2(request):
    documents = Document.objects.filter()
    User = request.session['USER']
    user_type = User["type"]
    context = {
        'documents': documents,
        'Usertype':user_type
        
    }
    return render(request, 'pages/indexFonctionnaire.html', context)

def files(request):
    return render(request, 'pages/Files.html')
def delete(request, id):
    doc_delete = get_object_or_404(Document, Doc_id=id)
    if request.method == 'POST':
        doc_delete.delete()
        return redirect('/fonctionnaire')
    return render(request, 'pages/deleteDoc.html')


def document_detail(request, id):
    document = get_object_or_404(Document, Doc_id=id)
    # Ajoutez ici toute logique supplémentaire ou données contextuelles nécessaires pour la vue de détail
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        user = request.session['USER']
        known_image_path = user["img_user"]  # Replace with the path to your known image
        
        # Call the verify_identity function with the known image path
        match = verify_identity(known_image_path)
        print(f"Match: {match}")
        
        if match:
            if 'sign' in request.POST:
                # Perform the PDF watermarking
                print('Signing the document')
                document.status = 'Signed'

                inputfile = document.fichier.path
                outputfile = document.fichier.path
                watermark = user["signature"]
                file_n2 = "teeest.pdf"
                timestamp2 = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
                temp_med="./tempmedia/"
                filename2 = f"{timestamp2}_{file_n2}"
                # import the template
                c = canvas.Canvas(filename2, pagesize=letter)
                #c=my_temp(c) # run the template
                # Add the signature and date
                c = add_signature_and_date(c, watermark )

                c.showPage()        
                c.save()
                
                with open(inputfile, 'rb') as inputefile:
                    pdf = PyPDF2.PdfReader(inputfile)
                with open(filename2, 'rb') as inputefile2:
                    pdf2 = PyPDF2.PdfReader(filename2)
                    p = pdf.pages[0]
                    p2 = pdf2.pages[0]
                    #w = watermarkpdf.pages[0]

                    p.merge_page(p2)
                    #p.merge_page(w)
                    pdfwriter = PyPDF2.PdfWriter()
                    pdfwriter.add_page(p)

                    with open(outputfile, 'wb') as outputfilecontent:
                        pdfwriter.write(outputfilecontent)
                os.remove(filename2)
               

                # Update the Document instance with the modified file path
                document.fichier = outputfile

                # Save the Document instance to the database
                document.save()

                return redirect('/fonctionnaire')
            
            elif 'reject' in request.POST:
                print('Rejecting the document')
                document.status = 'Rejected'
                
                # Save the Document instance to the database
                document.save()

                return redirect('/fonctionnaire')
        else:
            return redirect('/fonctionnaire')
       
    else:
        form = DocumentForm()
    
    return render(request, 'pages/Files.html', {'Document': document})



def logout_view(request):
    logout(request)
    return redirect('/')
