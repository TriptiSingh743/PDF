from django.shortcuts import render
from django.http import JsonResponse
import pdfplumber  # Library for extracting text from PDF
from urllib.parse import unquote
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    return render(request, 'home.html')

@csrf_exempt
def upload_pdf(request):
    """
    Handles PDF upload from the web form and extracts text using pdfplumber.
    """
    if request.method == 'POST':
        uploaded_file = request.FILES.get('pdf')  # Get the uploaded file
        if uploaded_file:
            try:
                # Extract text from the PDF using pdfplumber
                with pdfplumber.open(uploaded_file) as pdf:
                    extracted_text = ""
                    for page_num, page in enumerate(pdf.pages, start=1):
                        page_text = page.extract_text()

                        # Check if text is found, else add a placeholder
                        if page_text:
                            extracted_text += f"\n\n--- Page {page_num} ---\n\n{page_text}"
                        else:
                            extracted_text += f"\n\n--- Page {page_num} (No text extracted) ---\n\n"

                # Clean the extracted text
                extracted_text = extracted_text.strip()

                # Return the extracted text in a nicely formatted JSON response
                return JsonResponse({
                    'message': 'PDF uploaded and processed successfully!',
                    'extracted_text': extracted_text
                })

            except Exception as e:
                return JsonResponse({'error': f"Error processing PDF: {str(e)}"}, status=500)
        else:
            return JsonResponse({'error': 'No file uploaded'}, status=400)
    else:
        return render(request, 'upload_pdf.html')


@csrf_exempt
def extract_pdf_text_api(request):
    """
    API endpoint to extract text from a PDF file.
    Accepts a POST request with a PDF file.
    """
    if request.method == 'POST':
        uploaded_file = request.FILES.get('pdf')  # Get the uploaded file
        if uploaded_file:
            try:
                # Extract text from the PDF using pdfplumber
                with pdfplumber.open(uploaded_file) as pdf:
                    extracted_text = ""
                    for page_num, page in enumerate(pdf.pages, start=1):
                        page_text = page.extract_text()

                        if page_text:
                            extracted_text += f"\n\n--- Page {page_num} ---\n\n{page_text}"
                        else:
                            extracted_text += f"\n\n--- Page {page_num} (No text extracted) ---\n\n"

                extracted_text = extracted_text.strip()

                # Return JSON response for API
                return JsonResponse({
                    'status': 'success',
                    'extracted_text': extracted_text
                }, status=200)

            except Exception as e:
                return JsonResponse({'status': 'error', 'message': f"Error processing PDF: {str(e)}"}, status=500)
        else:
            return JsonResponse({'status': 'error', 'message': 'No file uploaded'}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

def display_extracted_text(request):
    extracted_text = request.GET.get('text', '')
    return render(request, 'display_extracted_text.html', {'extracted_text': unquote(extracted_text)})
