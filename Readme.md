# I/O Jobs Profiler

I/O Jobs Profiler is a web application designed to match individuals with various Industrial/Organizational Psychology job roles based on their skills, certifications, knowledge, and other relevant qualifications. It leverages Google Trends data to provide insights into job popularity over time and offers personalized suggestions to improve missing skills or qualifications.

## Features
- **Skill Matching**: Users answer a quiz that assesses their education, certifications, skills, and more, which is then matched with job profiles in the dataset.
- **Job Details**: Each job includes specific required skills, certifications, and experience, along with Google Trends insights.
- **Personalized Suggestions**: Based on the user's answers, the app suggests ways to improve qualifications through learning resources.
- **Google Trends Integration**: The app integrates with Google Trends to show interest trends for job titles over the past five years.

## Tech Stack
- **Flask**: A lightweight web framework for Python used to serve the application.
- **Pandas**: For data manipulation, especially reading and processing the job dataset.
- **Google Trends API**: To gather and visualize job title trends over time.
- **HTML/CSS**: For the front-end UI.
- **Font Awesome**: For icons, including GitHub and other symbols used across the app.

## Dataset
The app uses a custom dataset (`io_jobs_dataset.csv`) which contains job roles, required skills, certifications, experience, and more, used to assess user-job matches.

## Getting Started

### Prerequisites
- Python 3.x
- Flask
- Pandas
- Numpy
- Requests
- PyTrends
- Font Awesome (linked via CDN)

### Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your-github-username/io-jobs-profiler.git
    cd io-jobs-profiler
    ```

2. Install required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Run
   ```bash
   python app.py
   ```