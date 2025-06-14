from django.shortcuts import render, redirect
import regex as re
from .models import OCRRecord
from PIL import Image, ImageEnhance
import google.generativeai as genai
import json
import fitz
import io
import numpy as np
import pytesseract

# Configure Gemini API
genai.configure(api_key="AIzaSyAq9GSOoqOv4-3gHFwrJaoSkPhmVISt1nw")
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Extract JSON using regex
def extract_json_from_text(text):
    pattern = r'\{(?:[^{}]*|(?R))*\}'
    match = re.search(pattern, text)
    if match:
        return match.group(0)
    return None

# Main view
def image_to_text(request):
    text = ''
    context = {}

    if request.method == 'POST':
        file = request.FILES.get('image')
        template_choice = request.POST.get('template_choice', '1')

        if file.name.endswith('.pdf'):
            pdf = fitz.open(stream=file.read(), filetype="pdf")
            for page_number in range(len(pdf)):
                page = pdf.load_page(page_number)
                pix = page.get_pixmap(dpi=300)
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                img = img.convert('L')
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(2.0)
                text += pytesseract.image_to_string(img)

        else:
            image = Image.open(file)
            image = image.convert('L')
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            text += pytesseract.image_to_string(image)

        # Prompt for Gemini API
        prompt = f"""
You are an expert resume parser, grammar corrector, professional content enhancer, and industry-aware keyword researcher.

Given a raw resume text, perform the following actions:

1. **Professional Enhancement**
- Fix grammar, spelling, and punctuation.
- Improve vague or incomplete phrases using realistic, professional, and industry-standard language.
- Organize details clearly and consistently (especially dates, job roles, and project descriptions).
- Enrich the content with relevant, role-specific terminology (marketing, management, design, development, etc.) without inventing false information.

2. **Extract and Map URLs**
- Detect all valid URLs (`http://`, `https://`, or `www.`).
- Categorize them appropriately:
  - LinkedIn → `linkedin_url`
  - GitHub → `github_url` (either profile or repo)
  - Live project/demo → `demo_url` in the project section

3. **Output a Single Structured JSON Object**
Ensure the output follows this exact format:

{{
  "name": "Full Name",
  "title": "Professional Title (e.g., Marketing Manager, Product Designer)",
  "email": "email@example.com",
  "phone": "123-456-7890",
  "location": "City, Country",
  "linkedin_url": "https://linkedin.com/in/username",
  "github_url": "https://github.com/username",
  "summary": "A concise professional summary tailored to the field.",
  "skills": ["Skill1", "Skill2", "..."],
  "work_experience": [
    {{
      "role": "Job Title",
      "company": "Company Name",
      "period": "MM/YYYY – MM/YYYY or Present",
      "achievements": ["Key responsibility or result", "Quantifiable outcome or task"]
    }}
  ],
  "projects": [
    {{
      "name": "Project Name",
      "description": "Purpose, process, and outcome of the project.",
      "tech_stack": ["If applicable"],
      "demo_url": "https://live-demo.com",
      "github_url": "https://github.com/username/project"
    }}
  ],
  "education": [
    {{
      "degree": "Degree Title",
      "institution": "Institution Name",
      "year": "YYYY – YYYY"
    }}
  ]
}}

Resume text:
\"\"\"{text}\"\"\"

Only return the JSON. Do not include any explanation or commentary.
"""

        model = genai.GenerativeModel("models/gemini-1.5-flash")
        response = model.generate_content(prompt)
        json_str = extract_json_from_text(response.text)

        # Store and redirect
        request.session['resume_data'] = json.loads(json_str)
        request.session['template_choice'] = template_choice

        redirect_map = {
            'modern_minimal': 'modern_minimal',
            'tech_professional': 'Tech_Professional',
            'portfolio_grid': 'Portfolio_Grid',
            'creative_bold': 'Creative_Bold',
        }
        template = redirect_map.get(template_choice)
        return redirect(template)

    return render(request, 'index.html', context)

# Templates
def Modern_Minimal(request):
    resume_data = request.session.get('resume_data')
    return render(request, 'Modern_Minimal.html', {'portfolio': resume_data})

def Creative_Bold(request):
    resume_data = request.session.get('resume_data')
    return render(request, 'Creative_Bold.html', {'portfolio': resume_data})

def Tech_Professional(request):
    resume_data = request.session.get('resume_data')
    return render(request, 'Tech_Professional.html', {'portfolio': resume_data})

def Portfolio_Grid(request):
    resume_data = request.session.get('resume_data')
    return render(request, 'Portfolio_Grid.html', {'portfolio': resume_data})

# Save and share
def save_and_share(request):
    if request.method == 'POST':
        resume_data = request.session.get('resume_data')
        if resume_data:
            ocr_data = OCRRecord.objects.create(
                extracted_text=json.dumps(resume_data),
                template_choice=request.session.get('template_choice')
            )
            ocr_data.save()
            return redirect('portfolio_view', resume_id=ocr_data.id)
    return redirect('/')

# View saved portfolio
def portfolio_view(request, resume_id):
    record = OCRRecord.objects.filter(id=resume_id).first()
    resume_data = json.loads(record.extracted_text)
    choice = record.template_choice

    template_map = {
        'modern_minimal': 'Modern_Minimal.html',
        'tech_professional': 'Tech_Professional.html',
        'portfolio_grid': 'Portfolio_Grid.html',
        'creative_bold': 'Creative_Bold.html',
    }
    template_name = template_map.get(choice, 'Modern_Minimal.html')
    share_url = request.build_absolute_uri()

    return render(request, template_name, {
        'portfolio': resume_data,
        'share_url': share_url,
    })
