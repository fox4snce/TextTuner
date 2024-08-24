from flask import Flask, render_template, request, jsonify
from llm_utils import generate_response
import re

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        action = request.form['action']

        if action == 'analyze':
            # Analyze the text
            categories = analyze_text(text)
            return jsonify(categories)
        elif action == 'modify':
            # Modify the text based on selected options
            modified_text = modify_text(text, request.form)
            return jsonify({'modified_text': modified_text})

    return render_template('index.html')

def analyze_text(text):
    # Categorize the text
    categorization = generate_response(
        system="You are a text analysis expert.",
        user_message=f"Categorize this text with a few words: {text}"
    )

    # Generate ontological concepts
    concepts_prompt = f"""Based on this categorization: '{categorization}', suggest 5-7 ontological style concepts that could be used to manipulate the text.  These concepts should represent what a human user would most likely want to modify. For each concept, provide a scale of 8-10 levels, described by single words or short phrases, arranged from one extreme to the other.

    Format your response exactly like this example, with no additional text:

    Atmosphere: Bleak, Gloomy, Somber, Neutral, Calm, Peaceful, Hopeful, Vibrant, Radiant
    Pacing: Glacial, Very Slow, Unhurried, Steady, Moderate, Brisk, Swift, Rapid, Frenetic
    Focus: Introspective, Character-centric, Relationship-focused, Balanced, Setting-oriented, Plot-driven, Action-centric, Event-focused
    Emotional Tone: Despairing, Melancholic, Wistful, Neutral, Bittersweet, Nostalgic, Optimistic, Joyful, Exuberant
    Historical Detail: Minimal, Sparse, Light, Moderate, Balanced, Detailed, Rich, Extensive, Immersive
    War Presence: Absent, Hinted, Background, Peripheral, Present, Significant, Prominent, Central, All-encompassing
    Sensory Detail: Stark, Sparse, Subtle, Balanced, Clear, Vivid, Rich, Lush, Overwhelming

    Your response should contain ONLY the concepts and their levels, exactly one concept per line, with the concept name followed by a colon, then the levels separated by commas. Do not include any other text, explanations, or formatting.
    """

    concepts = generate_response(
        system="You are a text manipulation expert specializing in narrative analysis and modification. You excel at creating nuanced scales describing text. You always follow instructions precisely.",
        user_message=concepts_prompt
    )

    # Parse the concepts and levels
    categories = parse_concepts(concepts)

    return categories

def parse_concepts(concepts_string):
    categories = {}
    for line in concepts_string.strip().split('\n'):
        if ':' in line:
            concept, levels = line.split(':', 1)
            categories[concept.strip()] = [level.strip() for level in levels.split(',')]
    return categories

def modify_text(text, form_data):
    # Filter out empty or None values and exclude 'text' and 'action'
    modifications = {k: v for k, v in form_data.items() if k not in ['text', 'action'] and v and v.strip() and v != ""}
    
    # Only include non-empty modifications in the prompt
    changes_list = ', '.join([f"{k}: {v}" for k, v in modifications.items()])
    
    modification_prompt = f"""Rewrite the following text to embody the specified traits from these categories. The goal is to modify the overall feel and style of the text to match these changes, not simply insert the words.

Original Text:
{text}

Desired Changes:
{changes_list}

Guidelines:
1. Maintain the core meaning of the text. If it is a narrative, it should continue to be a narrative. If it is a business letter, it should continue to be a business letter.
2. Adjust the writing style, tone, pacing, and descriptive elements to reflect the desired changes.
3. Do not merely insert the trait words; instead, rewrite the text to embody these characteristics.
4. Ensure the modified text feels cohesive and natural.
5. Use the <changes> tag to explain your modifications.
6. Use the <output> tag to contain the ENTIRE rewritten text with all modifications applied.
7. There should be ONLY one set of <output> tags and one set of <changes> tags.
8. The <output> section should contain a complete rewrite of the original text, not just a partial modification.
9. If no changes are specified, return the original text unchanged within the <output> tags.

Example:
Original Text: The old car sputtered down the dusty road, its rusted frame groaning with each bump. John gripped the steering wheel tightly, his weathered hands telling stories of years of hard work.

Desired Changes:
Atmosphere: Hopeful
Pacing: Brisk
Sensory Detail: Vivid

<changes>
- Shifted the atmosphere to be more hopeful by using positive descriptors and emphasizing potential.
- Increased the pacing by using more dynamic verbs and shorter sentences.
- Enhanced sensory details by adding vivid descriptions of sights, sounds, and smells.
</changes>

<output>
The vintage automobile hummed along the sun-dappled country lane, its lovingly restored chassis gliding smoothly over gentle undulations. John's fingers danced lightly on the steering wheel, his strong yet supple hands a testament to a life filled with passionate pursuits. The warm breeze carried the sweet scent of wildflowers through the open windows, promising new adventures on the horizon.
</output>

Now, please provide the complete modified version of the original text, incorporating all the desired changes. Remember to enclose the entire rewritten text within the <output> tags:"""

    full_response = generate_response(
        system="You are a master of prose adaptation, skilled at rewriting text to embody specific tones, pacing, and stylistic elements while maintaining the core narrative.",
        user_message=modification_prompt
    )
    
    # Extract only the content between <output> tags
    output_match = re.search(r'<output>(.*?)</output>', full_response, re.DOTALL)
    if output_match:
        return output_match.group(1).strip()
    else:
        return "Error: No output found in the generated response."

if __name__ == '__main__':
    app.run(debug=True, port=5501)