import os
import re
from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd
import numpy as np
import pickle
from requests.exceptions import ProxyError, RequestException
from pytrends.request import TrendReq
from pytrends.exceptions import TooManyRequestsError
from config import certification_groups, knowledge_groups, abilities_groups, additional_training_groups, experience_groups, learning_resources

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load job data
jobs = pd.read_csv('data/io_jobs_dataset.csv')

# Create a cache for Google Trends data
trends_cache = {}

# Load cache from a file if it exists
cache_file = 'trends_cache.pkl'
if os.path.exists(cache_file):
    with open(cache_file, 'rb') as f:
        trends_cache = pickle.load(f)

def save_cache():
    with open(cache_file, 'wb') as f:
        pickle.dump(trends_cache, f)

def get_google_trends_data(keyword, timeframe='today 5-y'):
    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo='', gprop='')
        trends_data = pytrends.interest_over_time()

        return None if trends_data.empty else trends_data.drop(columns='isPartial')
    except TooManyRequestsError as e:
        print(f"Google Trends rate limit hit: {e}")
        return None
    except RequestException as e:
        print(f"Error retrieving Google Trends data: {e}")
        return None

def normalize(text):
    return text.strip().lower().replace('’', "'").replace('“', '"').replace('”', '"')

def normalize_list(items):
    return [normalize(item) for item in items]

def normalize_user_answers(user_answers, user_key):
    answer = user_answers.get(user_key, "")
    if isinstance(answer, list):
        return set(normalize_list(answer))
    return {normalize(answer)}

def normalize_group_dict(group_dict):
    return {normalize(key): [normalize(item) for item in items] for key, items in group_dict.items()}

# Apply normalization to group dictionaries
certification_groups = normalize_group_dict(certification_groups)
knowledge_groups = normalize_group_dict(knowledge_groups)
abilities_groups = normalize_group_dict(abilities_groups)
additional_training_groups = normalize_group_dict(additional_training_groups)
experience_groups = normalize_group_dict(experience_groups)

unique_skills = sorted(set(normalize_list(jobs['Skills Required'].str.split(';').explode())))
unique_knowledge = sorted(set(normalize_list(jobs['Knowledge Required'].str.split(';').explode())))
unique_abilities = sorted(set(normalize_list(jobs['Abilities Required'].str.split(';').explode())))
unique_experience = sorted(set(normalize_list(jobs['Experience Required'].str.split(';').explode())))
unique_education = sorted(set(normalize_list(jobs['Education Required'].str.split(';').explode())))
unique_certifications = sorted(set(normalize_list(jobs['Certifications Required'].str.split(';').explode())))
unique_training = sorted(set(normalize_list(jobs['Additional Training Required'].str.split(';').explode())))

# Create a mapping of normalized group names to original group names
certification_group_display_names = {normalize(key): key for key in certification_groups.keys()}
knowledge_group_display_names = {normalize(key): key for key in knowledge_groups.keys()}
abilities_group_display_names = {normalize(key): key for key in abilities_groups.keys()}
additional_training_group_display_names = {normalize(key): key for key in additional_training_groups.keys()}
experience_group_display_names = {normalize(key): key for key in experience_groups.keys()}

# Updated quiz_questions with 'type' and 'name' keys
quiz_questions = [
    {
        "question": "What is your highest level of education?",
        "options": unique_education,
        "type": "select",
        "name": "education"
    },
    {
        "question": "Which certifications do you have?",
        "options": list(certification_group_display_names.values()),
        "type": "checkbox",
        "name": "certifications"
    },
    {
        "question": "What additional training have you completed?",
        "options": list(additional_training_group_display_names.values()),
        "type": "checkbox",
        "name": "training"
    },
    {
        "question": "Which skills do you have? (Select all that apply)",
        "options": unique_skills,
        "type": "checkbox",
        "name": "skills"
    },
    {
        "question": "Which knowledge areas do you have? (Select all that apply)",
        "options": list(knowledge_group_display_names.values()),
        "type": "checkbox",
        "name": "knowledge"
    },
    {
        "question": "Which abilities do you possess? (Select all that apply)",
        "options": list(abilities_group_display_names.values()),
        "type": "checkbox",
        "name": "abilities"
    },
    {
        "question": "How many years of experience do you have?",
        "options": list(experience_group_display_names.values()),
        "type": "select",
        "name": "experience"
    }
]

# Education level mapping
education_levels = {
    'bachelors or masters degree in data science research or related field': 1,
    'bachelors or masters degree in human resources business administration or related field': 1,
    'bachelors or masters degree in organizational psychology or related field': 1,
    'masters degree in data science human resources or related field': 2,
    'masters degree in organizational psychology or related field': 2,
    'phd in organizational psychology or related field': 3
}

def get_education_level(education_item):
    # Directly normalize and look up the entire education string
    normalized_item = normalize(education_item)
    return education_levels.get(normalized_item, 0)


def get_experience_level(experience_item):
    # sourcery skip: use-getitem-for-re-match-groups
    import re
    if match := re.search(r'(\d+)-(\d+)', experience_item):
        return int(match.group(1))
    if match := re.search(r'(\d+)\+?', experience_item):
        return int(match.group(1))
    return 0

def calculate_total_possible_matches(job):
    total = 0
    required_fields = [
        'Education Required', 'Certifications Required', 'Additional Training Required',
        'Skills Required', 'Knowledge Required', 'Abilities Required', 'Experience Required'
    ]

    for field in required_fields:
        if field in job:
            job_items = [item.strip() for item in job[field].split(';') if item.strip()]
            if field in ['Education Required', 'Experience Required']:
                if job_items:
                    total += 1  # Count as one possible match
            else:
                total += len(job_items)
    return total

def calculate_match_score(job, user_answers=None):
    total_matches = 0
    matched_criteria = {
        'education': [],
        'certifications': [],
        'training': [],
        'skills': [],
        'knowledge': [],
        'abilities': [],
        'experience': []
    }

    total_possible_matches = calculate_total_possible_matches(job)

    if user_answers:
        # Normalize user education
        user_education = user_answers.get('education', '')
        user_education = normalize(user_education)
        user_education_level = get_education_level(user_education)

        # Normalize and extract job education requirements
        job_education_items = set(normalize_list(job.get('Education Required', '').split(';')))

        for job_item in job_education_items:
            # Normalize job item
            job_item_normalized = normalize(job_item)
            job_education_level = get_education_level(job_item_normalized)  # Direct lookup

            # Allow PhD (level 3) to match lower levels, but not the other way around
            is_matched = user_education_level >= job_education_level or (
                user_education_level == 3 and job_education_level < 3  # Ph.D. matches lower levels
            )

            # Make sure that higher requirements (e.g., PhD) don't match with lower user education (e.g., Bachelor)
            if job_education_level == 3 and user_education_level < 3:
                is_matched = False

            matched_criteria['education'].append({'item': job_item, 'matched': is_matched})
            
            if is_matched:
                total_matches += 1

        # Match experience hierarchically
        user_experience = user_answers.get('experience', '')
        user_experience = normalize(user_experience)
        user_experience_level = get_experience_level(user_experience)

        job_experience_items = set(normalize_list(job.get('Experience Required', '').split(';')))

        for job_item in job_experience_items:
            # Normalize job item
            job_item_normalized = normalize(job_item)
            job_experience_level = get_experience_level(job_item_normalized)
            is_matched = user_experience_level >= job_experience_level
            matched_criteria['experience'].append({'item': job_item, 'matched': is_matched})
            if is_matched:
                total_matches += 1

        # Function to match other categories
        def match_category(user_key, job_field, group_dict=None):
            nonlocal total_matches
            # Normalize user inputs
            user_items = normalize_user_answers(user_answers, user_key)

            # Normalize and extract job-specific items
            job_items = set(normalize_list(job.get(job_field, '').split(';')))
            matched_items = set()

            # Direct matches between user inputs and job requirements
            direct_matches = user_items & job_items
            total_matches += len(direct_matches)

            # Add matched items to matched_criteria
            for item in job_items:
                is_matched = item in direct_matches
                matched_criteria[user_key].append({'item': item, 'matched': is_matched})
                if is_matched:
                    matched_items.add(item)

            # Group matches, if applicable
            if group_dict:
                for group in user_items:
                    normalized_group = normalize(group)
                    group_items = set(normalize_list(group_dict.get(normalized_group, [])))
                    group_matches = group_items & job_items - matched_items
                    total_matches += len(group_matches)
                    for item in group_matches:
                        # Update matched_criteria if not already matched
                        for mc in matched_criteria[user_key]:
                            if mc['item'] == item:
                                mc['matched'] = True
                                break
                        else:
                            # If the item wasn't already in matched_criteria, add it
                            matched_criteria[user_key].append({'item': item, 'matched': True})
                        matched_items.add(item)

        # Match certifications, training, skills, knowledge, and abilities
        match_category('certifications', 'Certifications Required', certification_groups)
        match_category('training', 'Additional Training Required', additional_training_groups)
        match_category('skills', 'Skills Required')
        match_category('knowledge', 'Knowledge Required', knowledge_groups)
        match_category('abilities', 'Abilities Required', abilities_groups)
    else:
        # If no user answers, mark all items as unmatched
        for category, job_field in [
            ('education', 'Education Required'),
            ('certifications', 'Certifications Required'),
            ('training', 'Additional Training Required'),
            ('skills', 'Skills Required'),
            ('knowledge', 'Knowledge Required'),
            ('abilities', 'Abilities Required'),
            ('experience', 'Experience Required')
        ]:
            job_items = set(normalize_list(job.get(job_field, '').split(';')))
            for item in job_items:
                matched_criteria[category].append({'item': item, 'matched': False})

    match_percentage = (total_matches / total_possible_matches) * 100 if total_possible_matches > 0 else 0

    return match_percentage, matched_criteria, total_possible_matches, total_matches


@app.route('/')
def index():
    job_list = jobs['Job Title'].tolist()
    return render_template('index.html', jobs=job_list)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        user_answers = {}
        # Process form data based on updated quiz_questions
        for question in quiz_questions:
            name = question.get('name')
            if question.get('type') == 'select':
                user_answers[name] = request.form.get(name)
            elif question.get('type') == 'checkbox':
                user_answers[name] = request.form.getlist(name)

        # Normalize user answers
        for key in user_answers:
            if isinstance(user_answers[key], list):
                user_answers[key] = [normalize(answer) for answer in user_answers[key]]
            else:
                user_answers[key] = normalize(user_answers[key])

        session['quiz_answers'] = user_answers

        # Calculate match scores for all jobs
        match_results = jobs.apply(lambda job: calculate_match_score(job, user_answers), axis=1)
        jobs['match_percentage'] = match_results.apply(lambda x: x[0])
        jobs['matched_criteria'] = match_results.apply(lambda x: x[1])
        jobs['total_possible_matches'] = match_results.apply(lambda x: x[2])
        jobs['total_matches'] = match_results.apply(lambda x: x[3])

        matched_jobs = jobs.sort_values(by='match_percentage', ascending=False)

        return render_template('quiz.html', quiz_questions=quiz_questions, matched_jobs=matched_jobs, saved_answers=session['quiz_answers'])

    saved_answers = session.get('quiz_answers', None)
    return render_template('quiz.html', quiz_questions=quiz_questions, matched_jobs=None, saved_answers=saved_answers)

def identify_missing_elements(job, match_info):
    missing_elements = {
        'skills': [],
        'knowledge': [],
        'abilities': [],
        'certifications': [],
        'training': [],
        'experience': []
    }

    # Loop over each category to identify missing items
    for category in missing_elements:
        missing_items = [item['item'] for item in match_info.get(category, []) if not item['matched']]
        missing_elements[category].extend(missing_items)

    return missing_elements

def generate_suggestions(missing_elements):
    suggestions = {}

    # Map category to its group dictionary (e.g., certifications, abilities, etc.)
    group_mappings = {
        'certifications': certification_groups,
        'training': additional_training_groups,
        'knowledge': knowledge_groups,
        'abilities': abilities_groups,
        'experience': experience_groups
    }

    for category, items in missing_elements.items():
        if items:
            # If the category has a group mapping (certifications, abilities, etc.)
            if category in group_mappings:
                group_dict = group_mappings.get(category, {})

                for item in items:
                    # Normalize the item before checking
                    normalized_item = normalize(item)

                    # Find the group this item belongs to
                    for group, group_items in group_dict.items():
                        # Normalize group items for comparison
                        normalized_group_items = normalize_list(group_items)

                        if normalized_item in normalized_group_items:
                            # Normalize the group name before checking in learning_resources
                            normalized_group = normalize(group)

                            if normalized_group in learning_resources:
                                # Add learning resources for the group
                                suggestions[normalized_group] = learning_resources[normalized_group]
                            break  # Stop searching once the group is found

            # Special handling for 'skills' since it doesn't have a grouped variable
            elif category == 'skills':
                for item in items:
                    normalized_item = normalize(item)
                    # Check if the skill itself has a direct match in learning_resources
                    if normalized_item in learning_resources:
                        suggestions[normalized_item] = learning_resources[normalized_item]

    return suggestions

@app.route('/new_quiz')
def new_quiz():
    session.pop('quiz_answers', None)
    return redirect(url_for('quiz'))

@app.route('/job/<job_title>')
def job_detail(job_title):
    job = jobs[jobs['Job Title'] == job_title].iloc[0].to_dict()
    saved_answers = session.get('quiz_answers', {})

    # Get trends data (now cached and error-handled)
    trends_data = get_google_trends_data(job_title)

    if trends_data is None:
        max_interest_date = None
        max_interest_value = None
        percent_change = None
    else:
        max_interest_date, max_interest_value, percent_change = calculate_key_insights(trends_data)

    # Check if the quiz has been taken
    quiz_taken = bool(saved_answers)
    match_info, match_percentage, total_possible_matches, total_matches = generate_match_info(job, saved_answers, quiz_taken=quiz_taken)

    # Identify missing elements
    missing_elements = identify_missing_elements(job, match_info)

    # Generate suggestions
    suggestions = generate_suggestions(missing_elements)

    return render_template(
        'job_detail.html',
        job=job,
        match_info=match_info,
        match_percentage=match_percentage,
        total_possible_matches=total_possible_matches,
        total_matches=total_matches,
        trends_data=trends_data,
        max_interest_date=max_interest_date,
        max_interest_value=max_interest_value,
        percent_change=percent_change,
        suggestions=suggestions,
        saved_answers=saved_answers
    )

def calculate_key_insights(trends_data):
    if trends_data is None or trends_data.empty:
        return None, None, None

    max_interest_date = trends_data.idxmax().values[0]
    max_interest_value = trends_data.max().values[0]

    max_interest_date = convert_to_datetime(max_interest_date)

    start_value = trends_data.iloc[0, 0]
    end_value = trends_data.iloc[-1, 0]

    # Safely calculate percent change
    if start_value == 0 or np.isnan(start_value) or np.isnan(end_value):
        percent_change = None  # Handle NaN by returning None
    else:
        percent_change = ((end_value - start_value) / start_value) * 100

    return max_interest_date, max_interest_value, percent_change

def convert_to_datetime(date):
    if isinstance(date, pd.Timestamp):
        return date.to_pydatetime()
    elif isinstance(date, np.datetime64):
        return pd.to_datetime(date).to_pydatetime()
    return date

def generate_match_info(job, user_answers=None, quiz_taken=False):
    match_percentage, matched_criteria, total_possible_matches, total_matches = calculate_match_score(job, user_answers)

    # If the quiz hasn't been taken, mark all items as neutral
    if not quiz_taken:
        for category in matched_criteria:
            for item in matched_criteria[category]:
                item['matched'] = None  # Set to None to indicate neutrality

        match_percentage = None  # Optionally set match percentage to None
        total_matches = 0  # No matches since no answers were provided

    return matched_criteria, match_percentage, total_possible_matches, total_matches

def get_color_for_match(match_percentage):
    if match_percentage >= 75:
        return "#4caf50"
    elif match_percentage >= 50:
        return "#ffeb3b"
    else:
        return "#f44336"

print("The Website is Running")

if __name__ == "__main__":
    app.run()