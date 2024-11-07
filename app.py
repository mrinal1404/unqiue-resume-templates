import random
from flask import Flask, request, jsonify, render_template_string
from transformers import pipeline
from transformers import pipeline,TFAutoModelForCausalLM,AutoTokenizer

app = Flask(__name__)

# Load the language model from Hugging Face
model_name = "gpt2"
model = TFAutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Initialize the text-generation pipeline
generator = pipeline("text-generation", model=model, tokenizer=tokenizer, framework="tf")
# Generate random colors and font styles
def generate_dynamic_styles():
    colors = {
        "header_color": f"#{random.randint(0, 0xFFFFFF):06x}",
        "section_title_color": f"#{random.randint(0, 0xFFFFFF):06x}",
        "text_color": f"#{random.randint(0, 0xFFFFFF):06x}",
        "background_color": f"#{random.randint(0, 0xFFFFFF):06x}"
    }
    fonts = ["Arial, sans-serif", "Georgia, serif", "Verdana, sans-serif", "Courier New, monospace"]
    styles = {
        "font_family": random.choice(fonts),
        "header_font_size": f"{random.randint(18, 24)}px",
        "section_font_size": f"{random.randint(14, 18)}px",
        "text_font_size": f"{random.randint(12, 16)}px",
        **colors
    }
    return styles

# Generate resume content based on input fields
def generate_resume_content(data):
    prompt = f"""
    Create a professional resume summary for a candidate with these details:
    Name: {data['name']}
    Objective: {data['objective']}
    Experience: {data['experience']}
    Skills: {data['skills']}
    Education: {data['education']}
    Projects: {data['projects']}
    """
    
    response = generator(prompt, max_length=300, num_return_sequences=1)[0]['generated_text']
    return response

# Define API endpoint to generate unique resume template
@app.route('/generate-resume', methods=['POST'])
def generate_resume():
    data = request.json
    resume_content = generate_resume_content(data)

    # Generate unique styles for each resume
    styles = generate_dynamic_styles()
    
    # Define a base template with placeholders for dynamic styling
    template = """
    <html>
      <head>
        <style>
          body {{
            font-family: {font_family};
            background-color: {background_color};
            color: {text_color};
            padding: 20px;
          }}
          h1 {{
            color: {header_color};
            font-size: {header_font_size};
          }}
          .section-title {{
            color: {section_title_color};
            font-size: {section_font_size};
            font-weight: bold;
            margin-top: 20px;
          }}
          .content {{
            font-size: {text_font_size};
            margin-left: 20px;
          }}
        </style>
      </head>
      <body>
        <h1>{{{{ name }}}}</h1>
        <p><strong>Objective:</strong> {{{{ objective }}}}</p>
        <div class="section-title">Experience</div>
        <div class="content">{{{{ experience }}}}</div>
        <div class="section-title">Skills</div>
        <div class="content">{{{{ skills }}}}</div>
        <div class="section-title">Education</div>
        <div class="content">{{{{ education }}}}</div>
        <div class="section-title">Projects</div>
        <div class="content">{{{{ projects }}}}</div>
      </body>
    </html>
    """.format(**styles)

    # Render the template with the user's data
    rendered_resume = render_template_string(template, name=data['name'],
                                             objective=data['objective'],
                                             experience=data['experience'],
                                             skills=data['skills'],
                                             education=data['education'],
                                             projects=data['projects'])

    return jsonify({"resume": rendered_resume})

if __name__ == '__main__':
    app.run(debug=True,port=5001)
