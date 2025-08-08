from flask import Flask, render_template, request, jsonify, redirect, url_for, Response, stream_with_context
from flask_socketio import SocketIO, emit
from kade_last_10 import restorative_reflection
from openai import OpenAI
from nehabackend import report_card_comments, text_rewriter, lesson_plan, professional_email, rubric_generator
import json
import time

client = OpenAI()
app = Flask(__name__)
from flask_cors import CORS
CORS(app)

def ask_openai(conversation_history):
    response = client.chat.completions.create(
        messages=conversation_history,
        model="gpt-3.5-turbo",
        temperature=0,
        stream=True
    )
    with open("response2.jsonl", "w") as f:  # Open a file to save the JSON output
        for chunk in response:
            content = chunk.choices[0].delta.content
            if content:
                res = json.dumps({"text": content})
                f.write(f"{res}\n")  # Write JSON object to file
                yield f"{res}\n"
                print(content, end='', flush=True)
                time.sleep(0.1)

@app.route('/')
def main():
    return render_template('tools_page.html')

# Report card input
@app.route('/report_card_input')
def report_card_input():
    return render_template('report_card_input.html')

# MCQ input
@app.route('/mcq_input')
def mcq_input():
    return render_template('mcq_input.html')

# Text rewriter input
@app.route('/text_rewrite_input')
def text_rewrite_input():
    return render_template('text_rewrite_input.html')

# Lesson plan input
@app.route('/lesson_plan_input')
def lesson_plan_input():
    return render_template('lesson_plan_input.html')

# Restorative reflection input
@app.route('/restorative_ref_input')
def restorative_ref_input():
    return render_template('restorative_ref_input.html')
#rubric gen
@app.route('/rubric_generator')
def rubric_generator_input():
    return render_template('rubric_generator_input.html')
#prof email
@app.route('/professional_email')
def professional_email():
    return render_template('prof_email_input.html')
#info texts
@app.route('/informational_texts')
def informational_texts():
    return render_template('info_texts_input.html')
#academic content
@app.route('/academic_content')
def academic_content():
    return render_template('academic_content_input.html')

@app.route('/text_proofreader')
def text_proofreader():
    return render_template('t_proofreader_input.html')

@app.route('/text_summarizer')
def text_summarizer():
    return render_template('text_summarizer_input.html')



@app.route('/t_proofreader_submit')
def t_proofreader_submit():
    return render_template('t_proofreader_output.html')



@app.route('/academic_content_submit')
def academic_content_submit():
    return render_template('academic_c_output.html')




@app.route('/info_texts_submit')
def info_texts_submit():
    return render_template('info_texts_output.html')



@app.route('/prof_email_submit', methods=['POST'])
def prof_email_submit():
    if request.method == 'POST':
        author = request.form.get('author')
        content = request.form.get('content')
        input_dict = {
            
            "Author Name": author,
            "Content for Email": content
            }
        output_dict = professional_email(input_dict)
        return render_template('prof_email_output.html', output = output_dict['output']
                               )
@app.route('/rubric_gen_submit', methods=['POST'])
def rubric_gen_submit():
    if request.method == 'POST':
        grade_level = request.form.get('grade-level')
        point_scale = request.form.get('Point Scale')
        obj = request.form.get('stan/obj')
        title = request.form.get('title')
        descrip = request.form.get('description')
        custom = request.form.get('custom')
        input_dict = {
            "Grade Level": grade_level,
            "Point Scale": point_scale,
            "Topic/Standard/Objective": obj,
            "Name of Assignment": title,
            "Description of Assignment": descrip,
            "Additional Criteria": custom
        }
        output_dict = rubric_generator(input_dict)
        return render_template('rubric_generator_output.html', output=output_dict['output'])



@app.route('/lesson_plan_submit', methods=['POST'])
def lesson_plan_submit():
    if request.method == 'POST':
        grade_level = request.form.get('grade-level')
        topic = request.form.get('topic')
        criteria = request.form.get('criteria')
        standards = request.form.get('standards')
        input_dict = {
            "Grade Level": grade_level,
            "Topic/Standard/Objective": topic,
            "Additional Criteria": criteria,
            "Aligned Standards": standards
        }
        output_dict = lesson_plan(input_dict)
        print("lesson plan")
        print(output_dict)
        return render_template('lesson_plan_output.html', output=output_dict['output'])

@app.route('/restorative_ref_submit', methods=['POST'])
def restorative_ref_submit():
    if request.method == 'POST':
        grade_level = request.form.get('grade-level')
        num_questions = request.form.get('num-questions')
        details = request.form.get('details')
        input_dict = {
            "grade": grade_level,
            "amount": num_questions,
            "incident": details
        }
        output_dict = restorative_reflection(input_dict)
        print(output_dict)
        return render_template('restorative_ref_output.html', output=output_dict['output'])

@app.route('/text_rewrite_submit', methods=['POST'])
def text_rewrite_submit():
    if request.method == 'POST':
        original_text = request.form.get('original_text')
        rewrite_text = request.form.get('rewrite_text')
        input_dict = {
            "input text": original_text,
            "Rephrasing Instructions": rewrite_text,
        }
        print(input_dict)
        output_dict = text_rewriter(input_dict)
        print("text rewriter")
        print(output_dict['output'])
        return render_template('text_rewrite_output.html', output=output_dict['output'])

@app.route('/report_card_submit', methods=['POST'])
def report_card_submit():
    print("RUNS")
    if request.method == 'POST':
        grade_level = request.form.get('grade_level')
        student_pronouns = request.form.get('pronouns')
        strengths = request.form.get('strengths')
        growth_areas = request.form.get('growth')
        form_data = {
            'Grade Level': grade_level,
            'Student Pronouns': student_pronouns,
            'Strengths': strengths,
            'Weaknesses': growth_areas
        }
        output_dict = report_card_comments(form_data)
        print("***HERE")
        print(output_dict)
        return render_template('report_card_output.html', output=output_dict['output'])

# @app.route('/chatbot', methods=['POST'])
# def chatbot():
#     data = request.json
#     conversation_history = data.get("conversation_history", [])
#     previous_output = data.get("previous_output")
#     input_instructions = data.get("input_instructions")
#     user_message = data.get("message")
    
#     # Update the system message to ensure structured, bulleted format with headings
#     conversation_history.append({
#         'role': 'system', 
#         'content': f'You answer questions about "{previous_output}" and "{input_instructions}" to help teachers. Respond in structured, bulleted format with headings as needed.'
#     })
#     conversation_history.append({'role': 'user', 'content': user_message})
#     answer = ask_openai(conversation_history)
#     conversation_history.append({'role': 'assistant', 'content': answer})
    
    #return jsonify({"answer": answer})
    
@app.route('/chatbot', methods=['POST'])
def chatbot():
    data = request.json
    conversation_history = data.get("conversation_history", [])
    previous_output = data.get("previous_output")
    input_instructions = data.get("input_instructions")
    user_message = data.get("message")
    
    # Update the system message to ensure structured, bulleted format with headings
    conversation_history.append({
        'role': 'system', 
        'content': f'You answer questions about "{previous_output}" and "{input_instructions}" to help teachers. Respond in structured, bulleted format with headings as needed.'
    })
    conversation_history.append({'role': 'user', 'content': user_message})

    return Response(
        stream_with_context(ask_openai(conversation_history)),
        content_type='application/jsonl'
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
