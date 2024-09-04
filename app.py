import os
from flask import Flask, render_template, request, session, redirect, url_for
import pandas as pd
import numpy as np
from pytrends.request import TrendReq
from config import unique_certifications, unique_training, certification_groups, knowledge_groups, abilities_groups, additional_training_groups, experience_groups, learning_resources

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Load job data
jobs = pd.read_csv('data/io_jobs_dataset.csv')

# Function to get Google Trends data
def get_google_trends_data(keyword, timeframe='today 5-y'):
    pytrends = TrendReq(hl='en-US', tz=360)
    pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo='', gprop='')
    trends_data = pytrends.interest_over_time()
    return None if trends_data.empty else trends_data.drop(columns='isPartial')


def normalize(text):
    return text.strip().lower()

def normalize_list(items):
    return [normalize(item) for item in items]

# # Clean and extract unique education options from the dataset
unique_education = sorted(set(normalize_list(jobs['Education Required'].str.split(';').sum())))

# # Combine all certifications and training options for removal
combined_exclusions = normalize_list(unique_certifications + unique_training)

# # Filter out certifications and training from the education list
unique_education = [edu for edu in unique_education if edu not in combined_exclusions]

unique_skills = sorted(set(normalize_list(jobs['Skills Required'].str.split(';').sum())))
unique_knowledge = sorted(set(normalize_list(jobs['Knowledge Required'].str.split(';').sum())))
unique_abilities = sorted(set(normalize_list(jobs['Abilities Required'].str.split(';').sum())))
# unique_experience = sorted(set(normalize_list(jobs['Experience Required'].str.split(';').sum())))
# unique_education = sorted(set(normalize_list(jobs['Education Required'].str.split(';').sum())))
# unique_certifications = sorted(set(normalize_list(unique_certifications)))

def extract_certifications_and_training(job):
    education_list = []
    certifications_list = []
    training_list = []

    for item in job['Education Required'].split(';'):
        normalized_item = normalize(item.strip())
        if any(cert in normalized_item for cert in [c.lower() for c in unique_certifications]):
            certifications_list.append(item.strip())
        elif any(train in normalized_item for train in [t.lower() for t in unique_training]):
            training_list.append(item.strip())
        else:
            education_list.append(item.strip())

    return {
        'education': education_list,
        'certifications': certifications_list,
        'training': training_list
    }

# Function to extract and update the job dataset
def update_job_dataset_with_extracted_fields(jobs):
    # Initialize empty lists to store the extracted data
    education_list = []
    certifications_list = []
    training_list = []

    # Iterate through each job in the dataset
    for index, row in jobs.iterrows():
        # Extract education, certifications, and training
        extracted_data = extract_certifications_and_training(row)
        
        # Append the extracted data to respective lists
        education_list.append(';'.join(extracted_data['education']))
        certifications_list.append(';'.join(extracted_data['certifications']))
        training_list.append(';'.join(extracted_data['training']))

    # Add new columns to the jobs dataframe
    jobs['Education Required'] = education_list
    jobs['Certifications Required'] = certifications_list
    jobs['Additional Training Required'] = training_list

    return jobs

# Update the jobs dataset with the new columns
jobs = update_job_dataset_with_extracted_fields(jobs)

# Quiz Questions dynamically generated
quiz_questions = [
    {"question": "What is your highest level of education?", "options": unique_education},
    {"question": "Which certifications do you have?", "options": list(certification_groups.keys())},
    {"question": "What additional training have you completed?", "options": additional_training_groups},
    {"question": "Which skills do you have? (Select all that apply)", "options": unique_skills},
    {"question": "Which knowledge areas do you have? (Select all that apply)", "options": knowledge_groups},
    {"question": "Which abilities do you possess? (Select all that apply)", "options": abilities_groups},
    {"question": "How many years of experience do you have?", "options": list(experience_groups.keys())}
]

def match_groups(user_selections, job_requirements, group_dict, weight):
    job_requirements_set = set(job_requirements)
    matched_criteria = []
    match_score = 0

    for group in user_selections:
        items = group_dict.get(group, [])
        for item in items:
            if item in job_requirements_set:
                matched_criteria.append((group, item))
                match_score += weight / len(user_selections)
            else:
                matched_criteria.append((group, None))

    return match_score, matched_criteria


def calculate_total_possible_matches(job):
    required_fields = [
        'Education Required', 'Certifications Required', 'Additional Training Required',
        'Skills Required', 'Knowledge Required', 'Abilities Required', 'Experience Required'
    ]

    return sum(
        len(job[field].split(';')) for field in required_fields if field in job
    )

def calculate_match_score(job, user_answers=None, total_possible_matches=None):
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

    if total_possible_matches is None:
        total_possible_matches = calculate_total_possible_matches(job)

    if user_answers:
        def match_category(user_key, job_key, group_dict=None):
            nonlocal total_matches
            if user_key in user_answers and job_key in job:
                user_items = set(normalize_list(user_answers[user_key]))  # Deduplicate user items
                job_items = set(normalize_list(job[job_key].split(';')))  # Deduplicate job items
                matched_items = set()  # Track matched items to avoid duplicates

                # Check for direct matches
                direct_matches = user_items & job_items
                total_matches += len(direct_matches)
                matched_criteria[user_key].extend(direct_matches)
                matched_items.update(direct_matches)

                # Check for PhD qualification for lower education levels
                if user_key == 'education' and 'phd' in user_items:
                    for job_item in job_items:
                        if "bachelor’s" in job_item.lower() or "master’s" in job_item.lower():
                            matched_criteria[user_key].append(job_item)
                            total_matches += 1

                # Check for group matches if applicable
                if group_dict:
                    for group in user_answers[user_key]:
                        job_group_items = set(normalize_list(group_dict.get(group, [])))
                        group_matches = job_group_items & job_items - matched_items
                        total_matches += len(group_matches)
                        matched_criteria[user_key].extend(group_matches)
                        matched_items.update(group_matches)

        match_category('education', 'Education Required')
        match_category('certifications', 'Certifications Required', certification_groups)
        match_category('training', 'Additional Training Required', additional_training_groups)
        match_category('skills', 'Skills Required')
        match_category('knowledge', 'Knowledge Required', knowledge_groups)
        match_category('abilities', 'Abilities Required', abilities_groups)
        match_category('experience', 'Experience Required', experience_groups)

    match_percentage = (total_matches / total_possible_matches) * 100 if total_possible_matches > 0 else 0

    return match_percentage, matched_criteria, total_possible_matches, total_matches





@app.route('/')
def index():
    job_list = jobs['Job Title'].tolist()
    return render_template('index.html', jobs=job_list)

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        user_answers = {
            'education': request.form.get('education'),
            'certifications': request.form.getlist('certifications'),
            'training': request.form.getlist('training'),
            'skills': request.form.getlist('skills'),
            'knowledge': request.form.getlist('knowledge'),
            'abilities': request.form.getlist('abilities'),
            'experience': request.form.get('experience')
        }

        session['quiz_answers'] = user_answers

        jobs['match_percentage'], jobs['matched_criteria'], jobs['total_possible_matches'], jobs['total_matches'] = zip(
            *jobs.apply(lambda job: calculate_match_score(job, user_answers), axis=1)
        )

        matched_jobs = jobs.sort_values(by='match_percentage', ascending=False)

        return render_template('quiz.html', quiz_questions=quiz_questions, matched_jobs=matched_jobs, saved_answers=session['quiz_answers'])

    saved_answers = session.get('quiz_answers', None)
    return render_template('quiz.html', quiz_questions=quiz_questions, matched_jobs=None, saved_answers=saved_answers)

def identify_missing_elements(job, user_answers):
    missing_elements = {
        'skills': [],
        'knowledge': [],
        'abilities': [],
        'certifications': [],
        'training': []
    }

    # Helper function to map items to their group
    def map_items_to_groups(items, group_dict):
        grouped_items = set()
        for item in items:
            normalized_item = normalize(item)
            # Check if the item is in any group
            for group, group_items in group_dict.items():
                if normalized_item in normalize_list(group_items):
                    grouped_items.add(group)
                    break
            else:
                # If not found in any group, add the individual item
                grouped_items.add(normalized_item)
        return grouped_items

    # Iterate through each category and check for missing groups/items
    for category in missing_elements:
        # Get job items, ensuring the field exists and is not empty
        job_items = set(normalize_list(job.get(f"{category.capitalize()} Required", "").split(';')))

        # Get user items, ensuring the category exists in user_answers
        user_items = set(normalize_list(user_answers.get(category, [])))

        # Get the group dictionary for the current category
        group_dict = {
            'certifications': certification_groups,
            'training': additional_training_groups,
            'knowledge': knowledge_groups,
            'abilities': abilities_groups
        }.get(category, {})

        # Map job items and user items to their respective groups (if applicable)
        if group_dict:
            job_items = map_items_to_groups(job_items, group_dict)
            user_items = map_items_to_groups(user_items, group_dict)

        # Identify missing elements
        missing_elements[category].extend(list(job_items - user_items))

    return missing_elements




def generate_suggestions(missing_elements):
    suggestions = {}

    for category, items in missing_elements.items():
        for item in items:
            # Normalize the item before checking
            normalized_item = normalize(item)

            # Check if the normalized item exists in learning_resources
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

    # Use a specific search term for "Diversity, Equity & Inclusion"
    search_term = job_title
    if search_term == "Diversity, Equity & Inclusion":
        search_term = "DEI"

    trends_data = get_google_trends_data(search_term)

    max_interest_date, max_interest_value, percent_change = calculate_key_insights(trends_data)

    # Check if the quiz has been taken
    quiz_taken = bool(saved_answers)
    match_info, match_percentage, total_possible_matches, total_matches = generate_match_info(job, saved_answers, quiz_taken=quiz_taken)

    # Identify missing elements
    missing_elements = identify_missing_elements(job, saved_answers)

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
        percent_change=percent_change,
        suggestions=suggestions
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


def map_certification_to_group(cert, certification_groups):
    return next(
        (
            group
            for group, cert_list in certification_groups.items()
            if cert in cert_list
        ),
        None,
    )

def generate_match_info(job, user_answers=None, quiz_taken=False):
    def populate_match_info(category, items, matched_criteria_key):
        for item in items:
            item_normalized = normalize(item.strip())
            is_matched = any(item_normalized == normalize(jr) for jr in matched_criteria[matched_criteria_key]) if quiz_taken else None
            match_info[category].append({'item': item, 'matched': is_matched})

    match_info = {key: [] for key in ['education', 'certifications', 'training', 'skills', 'knowledge', 'abilities', 'experience']}

    match_percentage, matched_criteria, total_possible_matches, total_matches = calculate_match_score(job, user_answers)

    # Combine all categories into one loop
    categories = {
        'education': 'Education Required',
        'certifications': 'Certifications Required',
        'training': 'Additional Training Required',
        'skills': 'Skills Required',
        'knowledge': 'Knowledge Required',
        'abilities': 'Abilities Required',
        'experience': 'Experience Required'
    }

    for category, job_field in categories.items():
        if job_field in job and isinstance(job[job_field], str):
            items = job[job_field].split(';')
            populate_match_info(category, items, category)

    return match_info, match_percentage, total_possible_matches, total_matches


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
