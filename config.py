from flask import Flask

certification_groups = {
    "Change Management Certifications (e.g., Prosci)": [
        "Certification in Change Management (e.g., Prosci)",
        "Certification in change management (e.g. prosci)"
    ],
    "Project Management Certifications (e.g., PMP, PRINCE2)": [
        "Certification in Project Management (e.g., PMP, PRINCE2)",
        "Certification in project management (e.g. pmp prince2)"
    ],
    "Global HR Certifications (e.g., GPHR)": [
        "Certification in Global Talent Management (e.g., GPHR)",
        "Additional certifications in international HR practices"
    ],
    "HR Certifications (e.g., SHRM-CP, PHR)": [
        "HR certification (e.g., PHR, SHRM-CP)",
        "Certification in HR operations or equivalent",
        "Certification in Human Capital Management or equivalent",
        "Hr certification (e.g. phr shrm-cp)"
    ],
    "Talent Development & Learning Certifications (e.g., ATD)": [
        "Certification in Talent Development or equivalent",
        "Certification in Learning and Development or equivalent",
        "Certification in Workforce Planning or equivalent",
        "Certification in Talent Analytics or equivalent",
        "Certification in Team Development or equivalent",
        "Certification in Talent Management or equivalent",
        "Certification in Leadership Development or equivalent",
        "Certification in Leadership Consulting or equivalent",
        "Certification in Workforce Insights or equivalent",
        "Certification in Employee Engagement or equivalent"
    ],
    "Organizational Development & Effectiveness Certifications": [
        "Certification in Organizational Development or equivalent",
        "Certification in Organizational Effectiveness or equivalent",
        "Certification in Strategy Development or equivalent",
        "Certification in Strategy and Analytics or equivalent"
    ],
    "HR & Workforce Analytics Certifications": [
        "Certification in HR Analytics or equivalent",
        "Certification in Workforce Analytics or equivalent",
        "Certification in Research Analytics or equivalent",
        "Certification in Research Methodologies or equivalent",
        "Certification in Applied Psychology or equivalent",
        "Certification in People Analytics or equivalent",
        "Certification in People Insight or equivalent",
        "Certification in People Research or equivalent",
        "Certification in People Science or equivalent",
        "Certification in Talent Insights or equivalent",
        "Certification in Talent Research or equivalent"
    ],
    "Diversity & Inclusion Certifications": [
        "Certification in Diversity Management or equivalent",
        "Certification in Cultural Competency or equivalent"
    ],
    "Research & Development Certifications": [
        "Certification in Research and Development or equivalent",
        "Certification in Innovation and Project Management"
    ],
    "Strategy & Business Certifications": [
        "Certification in Strategy Development or equivalent",
        "Certification in Business Strategy or equivalent",
        "Certification in Organizational Change or equivalent"
    ],
    "Human Capital Management Certifications": [
        "Certification in Human Capital Management or equivalent"
    ]
}

# **Updated Additional Training Groups**
additional_training_groups = {
    "Instructional Design and E-Learning": [
        "Additional training in instructional design and team dynamics",
        "Additional training in instructional design and e-learning"
    ],
    "Labor Laws and Organizational Behavior": [
        "Additional training in labor laws and regulations",
        "Additional training in employment law and organizational behavior"
    ],
    "Organizational Behavior and Project Management": [
        "Additional training in organizational behavior and project management",
        "Additional training in innovation and project management",
        "Additional training in coaching and program design"
    ],
    "Performance Management and Employee Development": [
        "Additional training in performance management and employee development",
        "Additional training in performance management and process improvement",
        "Additional training in coaching and executive development"
    ],
    "Research Methodologies and Data Analysis": [
        "Additional training in research methodologies and data analysis",
        "Additional training in statistical analysis and research design",
        "Additional training in data science and statistical analysis",
        "Additional training in data analysis and survey design",
        "Additional training in survey design and data analysis",
        "Additional training in strategic planning and data analysis",
        "Additional training in data analysis and reporting"
    ],
    "Workforce Planning and Talent Management": [
        "Additional training in workforce planning and talent management"
    ],
    "Assessment and Intervention Techniques": [
        "Additional training in assessment and intervention techniques"
    ],
    "Cultural Competency and Sensitivity": [
        "Additional training in cultural competency and sensitivity"
    ],
    "Strategic Planning and Data Analysis": [
        "Additional training in strategic planning and data analysis"
    ]
}

# **Updated Knowledge Groups**
knowledge_groups = {
    "HR Administration and Operations": [
        "Awareness of best practices in HR administration",
        "Awareness of best practices in HR service delivery",
        "Familiarity with HRIS (Human Resources Information Systems) and payroll systems",
        "Familiarity with HR analytics software and systems",
        "In-depth knowledge of HR operations and administration",
        "Understanding of HR metrics and key performance indicators",
        "In-depth knowledge of employment law and HR best practices",
        "Familiarity with compensation and benefits administration",
        "Familiarity with global recruitment and staffing processes",
        "Advanced knowledge of data analysis and HR metrics",
        "Familiarity with organizational development and human resources practices",
        "Understanding of employee relations and conflict resolution techniques",
        "Awareness of employee relations and conflict resolution techniques",
        "Familiarity with hris and payroll systems",
        "In-depth knowledge of hr operations and service delivery"
    ],
    "Talent Management and Development": [
        "Awareness of best practices in talent development",
        "Understanding of talent acquisition and retention strategies",
        "Understanding of performance management and succession planning",
        "Advanced knowledge of talent management and development strategies",
        "Comprehensive knowledge of talent management strategies",
        "In-depth knowledge of talent management and strategy",
        "Familiarity with workforce planning methodologies",
        "Understanding of workforce planning methodologies",
        "Understanding of talent analytics software and systems",
        "Awareness of best practices in talent optimization",
        "Awareness of best practices in executive development",
        "Familiarity with assessment and measurement tools",
        "Understanding of employee engagement and retention strategies",
        "Understanding of talent management and succession planning",  # Ensured inclusion
        "Comprehensive knowledge of human capital management strategies",
        "Comprehensive knowledge of training and development methodologies"
    ],
    "Organizational Development and Change Management": [
        "Awareness of best practices in organizational development",
        "Understanding of organizational behavior and development principles",
        "Understanding of organizational behavior and dynamics",
        "Advanced knowledge of change management frameworks and methodologies",
        "Understanding of change management principles and practices",
        "Comprehensive knowledge of organizational assessment and intervention techniques",
        "In-depth knowledge of strategic planning and development",
        "Familiarity with organizational behavior and culture change",
        "Understanding of group dynamics and team development",
        "Awareness of organizational behavior and development principles",  # Added missing item
        "Understanding of organizational behavior and effectiveness strategies",
        "Awareness of best practices in change implementation"
    ],
    "Learning and Development": [
        "Awareness of best practices in corporate training",
        "Understanding of adult learning principles and instructional design",
        "Understanding of instructional design and training delivery",
        "Comprehensive knowledge of instructional design and training development",
        "Familiarity with e-learning platforms and tools",
        "Familiarity with training evaluation and ROI measurement",
        "In-depth knowledge of instructional design and training delivery methods",
        "Advanced knowledge of leadership development and coaching principles",
        "Familiarity with curriculum development",
        "Understanding of learning needs assessment and gap analysis",
    ],
    "Research, Data Analysis, and Methodology": [
        "Awareness of best practices in HR research and reporting",
        "Familiarity with research analytics tools and software",
        "Familiarity with statistical analysis and reporting techniques",
        "Familiarity with statistical analysis software and tools",
        "Advanced knowledge of research methodologies and data analysis",
        "Advanced knowledge of statistical analysis and research design",
        "Comprehensive knowledge of research methodologies and data analysis",
        "In-depth knowledge of data analysis and workforce metrics",
        "Understanding of data analysis and visualization",
        "Understanding of data collection and reporting techniques",
        "Familiarity with data analysis and visualization tools",
        "Awareness of data privacy and security regulations",
        "Comprehensive knowledge of applied psychology and research methods",
        "Awareness of best practices in psychological research and application",
        "Understanding of survey design and administration",
        "Understanding of HR metrics and key performance indicators",
        "In-depth knowledge of research and development processes",  # Added missing item
        "Awareness of best practices in research implementation",  # Added missing item
        "Comprehensive knowledge of data analysis and workforce metrics"
    ],
    "Strategic Planning and Business Optimization": [
        "Awareness of best practices in business optimization",
        "Familiarity with strategic planning and implementation",
        "Advanced knowledge of strategic planning and workforce analytics",
        "Comprehensive knowledge of business strategy and analytics",
        "In-depth knowledge of business processes and operations",
        "Understanding of business strategy and acumen",
        "Familiarity with metrics and measurement tools",
        "Understanding of project management methodologies",
        "Understanding of business processes and operations",
        "Understanding of innovation and product development",  # Added missing item
        "Awareness of best practices in organizational optimization"
    ],
    "Diversity, Inclusion, and Cultural Competence": [
        "Awareness of cultural competencies and sensitivity training",
        "Understanding of cultural differences and global business practices",
        "Understanding of employment laws and regulations related to diversity and inclusion",
        "Deep knowledge of diversity and inclusion principles and best practices",
        "Comprehensive knowledge of global talent management strategies",
        "Understanding of global mobility and expatriate management"
    ],
    "Employee Engagement and Feedback": [
        "Awareness of best practices in employee feedback and improvement",
        "Comprehensive knowledge of employee engagement theories and practices",
        "Familiarity with employee engagement and retention techniques",
        "Familiarity with workforce insights tools and systems",
        "Understanding of survey design and implementation",
        "Understanding of employee engagement and retention strategies"
    ],
    "Legal and Regulatory Compliance": [
        "Awareness of data privacy and security regulations",
        "Awareness of industry-specific regulations and standards",
        "Awareness of international labor laws and regulations",
        "Understanding of labor laws and regulations",
        "In-depth knowledge of employment law and HR best practices",
        "Understanding of compliance with labor laws and regulations"
    ],
    "Project and Performance Management": [
        "Familiarity with project management methodologies",
        "Familiarity with project management methodologies and tools (e.g., Agile, Scrum)",
        "In-depth knowledge of performance management and process improvement",
        "Understanding of stakeholder management and communication strategies",
        "Advanced knowledge of data analysis techniques and tools",
        "Understanding of change management frameworks and methodologies",
        "Familiarity with project management methodologies and tools (e.g. agile scrum)"
    ],
    "Team Dynamics and Facilitation": [
        "Awareness of best practices in team building and facilitation",
        "Understanding of group dynamics and team development",
        "Advanced knowledge of team dynamics and development",
        "Familiarity with coaching and facilitation methods",
        "Understanding of leadership development and coaching principles"
    ],
    "Tools and Systems": [
        "Familiarity with HR analytics tools and systems",
        "Familiarity with workforce analytics tools and systems",
        "Familiarity with data analysis and visualization tools",
        "Familiarity with assessment and feedback tools",
        "Familiarity with metrics and measurement tools",
        "Understanding of survey design and implementation",
        "Awareness of best practices in HR research and reporting",
        "Proficiency in HR analytics software",
        "Proficiency in talent analytics software",
        "Proficiency in workforce analytics software"
    ]
}

# **Updated Abilities Groups**
abilities_groups = {
    "Data Analysis and Interpretation": [
        "Ability to analyze and interpret complex data sets",
        "Ability to analyze and interpret data and metrics",
        "Ability to analyze and interpret HR data and metrics",
        "Ability to analyze and interpret HR metrics and data",
        "Ability to analyze and interpret organizational data",
        "Ability to analyze and interpret research data",
        "Ability to analyze and interpret workforce data and metrics",
        "Ability to analyze survey data and provide actionable insights",
        "Ability to analyze and interpret data",
        "Ability to maintain data integrity and confidentiality",
        "Ability to develop and implement data-driven HR strategies",
        "Ability to develop and implement workforce analytics strategies"
    ],
    "Effective Communication": [
        "Ability to communicate data findings clearly and effectively",
        "Ability to communicate effectively with employees at all levels",
        "Ability to communicate effectively with stakeholders",
        "Ability to communicate effectively with team members",
        "Ability to communicate research findings clearly and effectively",
        "Ability to communicate research findings effectively",
        "Ability to communicate strategy and analysis effectively",
        "Ability to provide recommendations based on research results",
        "Ability to conduct needs assessments and gap analyses"
    ],
    "Talent Management and Development": [
        "Ability to assess and provide feedback on leadership performance",
        "Ability to assess training needs and evaluate program effectiveness",
        "Ability to develop and implement talent analytics strategies",
        "Ability to develop and implement talent management strategies",
        "Ability to manage talent acquisition and retention processes",
        "Ability to provide coaching and support to individuals and teams",
        "Ability to coach and mentor employees",
        "Ability to provide leadership and guidance to executives",
        "Ability to facilitate executive coaching sessions",
        "Ability to design and implement leadership development programs",
        "Ability to administer compensation and benefits programs",
        "Ability to develop and implement learning solutions",
        "Ability to conduct assessments and provide feedback",
        "Ability to manage talent acquisition and retention processes",
        "Ability to handle employee relations and conflict resolution",
        "Ability to implement and sustain inclusive practices and policies"
    ],
    "Organizational Change and Development": [
        "Ability to analyze and improve organizational processes",
        "Ability to develop and execute change management plans",
        "Ability to identify and address resistance to change",
        "Ability to manage and implement change initiatives",
        "Ability to manage and lead diverse teams effectively",
        "Ability to assess and diagnose organizational issues",
        "Ability to implement and sustain inclusive practices and policies",
        "Ability to design and implement effective interventions",
        "Ability to foster and maintain a global corporate culture",
        "Ability to apply psychological principles to organizational issues",
        "Ability to conduct assessments and provide feedback",
        "Ability to lead and manage human capital initiatives"
    ],
    "Learning and Development Programs": [
        "Ability to design and deliver effective training programs",
        "Ability to design and deliver instructional materials",
        "Ability to facilitate training sessions and workshops",
        "Ability to assess training needs and evaluate program effectiveness",
        "Ability to evaluate training programs and measure ROI",
        "Ability to develop and implement learning solutions",
        "Ability to design and deliver effective team development programs",
        "Ability to conduct training and workshops on diversity and inclusion",
        "Ability to coach and mentor employees",
        "Ability to provide coaching and support to individuals and teams"
    ],
    "Strategic Planning and Business Solutions": [
        "Ability to develop and implement HR analytics strategies",
        "Ability to develop and implement data-driven HR strategies",
        "Ability to develop and implement business strategies",
        "Ability to develop and implement strategic plans",
        "Ability to develop and implement strategic workforce plans",
        "Ability to provide recommendations for HR practices and policies",
        "Ability to provide recommendations for process improvements",
        "Ability to innovate and develop new products and solutions",
        "Ability to support and drive development projects to completion",
        "Ability to analyze and interpret data and metrics",
        "Ability to develop and implement employee engagement initiatives",
        "Ability to analyze and interpret organizational data",
        "Ability to collaborate with cross-functional teams",
        "Ability to measure and evaluate organizational effectiveness",  # Added missing item
        "Ability to measure and evaluate organizational effectiveness",
        "Ability to develop and implement workforce insights strategies"
    ],
    "Leadership and Team Management": [
        "Ability to lead and manage cross-functional teams",
        "Ability to lead and manage human capital initiatives",
        "Ability to lead and manage research and development projects",
        "Ability to manage HR operations and services effectively",
        "Ability to manage and oversee HR operations and services",
        "Ability to administer compensation and benefits programs",
        "Ability to handle multiple tasks and priorities effectively",
        "Ability to navigate and manage international assignments and relocations",
        "Ability to provide leadership and guidance to executives",
        "Ability to collaborate with cross-functional teams",
        "Ability to manage and lead diverse teams effectively",
        "Ability to assess team dynamics and provide feedback",  # Added missing item
        "Ability to facilitate team-building activities" 
    ],
    "Employee Relations and Cultural Competence": [
        "Ability to build and maintain positive employee relations",
        "Ability to handle sensitive situations with empathy and professionalism",
        "Ability to handle employee relations and conflict resolution",
        "Ability to handle global recruitment and staffing efficiently",
        "Ability to foster and maintain a global corporate culture",
        "Ability to collaborate with diverse teams across different time zones",
        "Ability to implement and sustain inclusive practices and policies",
        "Ability to navigate and manage international assignments and relocations",
        "Ability to communicate effectively with employees at all levels"
    ],
    "Research and Application": [
        "Ability to design and conduct research studies",
        "Ability to design and implement effective interventions",
        "Ability to apply psychological principles to organizational issues",
        "Ability to analyze and interpret research data",
        "Ability to design and administer employee engagement surveys",
        "Ability to conduct assessments and provide feedback",
        "Ability to analyze survey data and provide actionable insights",
        "Ability to maintain data integrity and confidentiality"
    ],
    "Project Management and Execution": [
        "Ability to support and drive development projects to completion",
        "Ability to handle and resolve technical issues and challenges",
        "Ability to develop and implement performance management systems",
        "Ability to manage and implement change initiatives",
        "Ability to manage and lead diverse teams effectively",
        "Ability to manage and oversee HR operations and services",
        "Ability to handle multiple tasks and priorities effectively",
        "Ability to design and implement interventions",
        "Ability to manage and oversee HR operations and services"
    ],
    "Adaptability and Compliance": [
        "Ability to adapt to changing environments and requirements",
        "Ability to ensure compliance with labor laws and regulations",
        "Ability to handle sensitive situations with empathy and professionalism",
        "Ability to maintain data integrity and confidentiality"
    ]
}

# **Updated Experience Groups**
experience_groups = {
    "3-5 Years of Experience": [
        "3-5 years of experience in human resources or related roles",
        "3-5 years of experience in talent development or related roles",
        "3-5 years of experience in talent insights or related roles",
        "3-5 years of experience in people operations or related roles",
        "3-5 years of experience in HR operations or related roles",
        "3-5 years of experience in learning and development or related roles",
        "3-5 years of experience in team development or related roles",
        "3-5 years of experience in workforce planning or related roles",
        "3-5 years of experience in organizational development or related roles",
        "3-5 years of experience in strategy development or related roles",
        "3-5 years of experience in talent strategy and culture or related roles",
        "3-5 years of experience in people insight or related roles",
        "3-5 years of experience in people science or related roles",
        "3-5 years of experience in HR analytics or related roles",
        "3-5 years of experience in people analytics or related roles",
        "3-5 years of experience in workforce analytics or related roles",
        "3-5 years of experience in research analytics or related roles",
        "3-5 years of experience in workforce insights or related roles",
        "3-5 years of experience in talent analytics or related roles",
        "3-5 years of experience in people research or related roles",
        "3-5 years of experience in talent research or related roles",
        "3-5 years of experience in diversity and inclusion roles",
        "3-5 years of experience in people research or related roles",
        "3-5 years of experience in talent research or related roles"
    ],
    "5-7 Years of Experience": [
        "5-7 years of experience in talent management or related roles",
        "5-7 years of experience in human capital management or related roles",
        "5-7 years of experience in change management, project management or related roles",
        "5-7 years of experience in organizational effectiveness or related roles",
        "5-7 years of experience in leadership consulting or related roles",
        "5-7 years of experience in strategy and analytics or related roles",
        "5-7 years of experience in research and development or related roles",
        "5-7 years of experience in change management or related roles"
    ],
    "No Experience": [
        "No experience required for any job"
    ]
}

learning_resources = {
    'python': [
        'Coursera - Python for Everybody (Specialization)',
        'Harvard CS50 - Introduction to Computer Science (Free Online Course)',
        'Textbook: "Python Programming: An Introduction to Computer Science" by John Zelle',
        'Article: "Python for Data Science: A Practical Guide" (Journal of Data Science)'
    ],
    'data analysis': [
        'Coursera - Data Analysis and Statistical Inference (Duke University)',
        'Textbook: "Applied Multiple Regression/Correlation Analysis for the Behavioral Sciences" by Cohen, Cohen, West, & Aiken',
        'Article: "Big Data Analytics in Industrial and Organizational Psychology" (Journal of Applied Psychology)',
        'College Course: Introductory Statistics, Applied Data Analysis, or Quantitative Methods'
    ],
    'analysis': [
        'Coursera - Applied Data Analysis (University of Michigan)',
        'Textbook: "Data Analysis for Business, Economics, and Policy" by Gábor Békés and Gábor Kézdi',
        'Article: "Data Analytics in I-O Psychology" (Journal of Applied Psychology)',
        'College Course: Data Analysis, Quantitative Analysis, or Research Methods'
    ],
    'change management certifications (e.g., prosci)': [
        'Prosci - Change Management Certification Program',
        'Coursera - Leading Organizational Change (Northwestern University)',
        'Textbook: "Organization Development and Change" by Cummings & Worley',
        'Article: "Ambivalence toward Imposed Change: The Conflict Between Dispositional Resistance to Change and the Orientation Toward the Change Agent" (Journal of Applied Psychology)',
        'College Course: Organizational Change, Management, or Leadership'
    ],
    'project management certifications (e.g., pmp, prince2)': [
        'PMI - Project Management Professional (PMP) Certification',
        'PRINCE2 - PRINCE2 Foundation and Practitioner Certification',
        'Coursera - Project Management: The Basics for Success (University of California, Irvine)',
        'Textbook: "Project Management: A Systems Approach to Planning, Scheduling, and Controlling" by Harold Kerzner',
        'College Course: Project Management, Operations Management, or Business Administration'
    ],
    'global hr certifications (e.g., gphr)': [
        'Coursera - Global Human Resources for International Business (University of London)',
        'Textbook: "Global HR Competencies" by Dave Ulrich',
        'Article: "Managing a Globally Distributed Workforce: Social and Interpersonal Issues" (APA Handbook of Industrial and Organizational Psychology)',
        'College Course: International HRM, Global Business, or Cross-Cultural Management'
    ],
    'hr certifications (e.g., shrm-cp, phr)': [
        'SHRM - SHRM Certified Professional (SHRM-CP)',
        'HRCI - Professional in Human Resources (PHR) and Senior Professional in Human Resources (SPHR)',
        'Textbook: "Human Resource Selection" by Gatewood, Barrick, & Feild',
        'College Course: Human Resource Management, Personnel Management, or Labor Relations'
    ],
    'talent development & learning certifications (e.g., atd)': [
        'ATD - Talent Development Certification (CPTD)',
        'Coursera - Learning and Development in Organizations (University of Minnesota)',
        'Textbook: "Employee Training and Development" by Raymond A. Noe',
        'Article: "Benefits of Training and Development for Individuals, Teams, Organizations, and Society" (Annual Review of Psychology)',
        'College Course: Adult Learning, Training and Development, or Instructional Design'
    ],
    'organizational development & effectiveness certifications': [
        'Coursera - Organizational Analysis (Stanford University)',
        'Textbook: "Organization Development: The Process of Leading Organizational Change" by Donald L. Anderson',
        'Article: "Organizational Effectiveness: A Behavioral View" (Journal of Organizational Behavior)',
        'College Course: Organizational Behavior, Organizational Development, or Business Strategy'
    ],
    'hr & workforce analytics certifications': [
        'Coursera - HR Management Analytics: Unlocking HR Data (University of Minnesota)',
        'Textbook: "The Power of People: Learn How Successful Organizations Use Workforce Analytics" by Nigel Guenole, Jonathan Ferrar, and Sheri Feinzig',
        'Article: "People Analytics: Reframing Human Resource Practices" (Journal of Applied Psychology)',
        'College Course: HR Analytics, Workforce Planning, or Data-Driven Decision Making'
    ],
    'research & methodologies certifications': [
        'Coursera - Research Methods (University of London)',
        'Textbook: "Research Design: Qualitative, Quantitative, and Mixed Methods Approaches" by John W. Creswell',
        'Textbook: "Handbook of Research Methods in Industrial and Organizational Psychology" by Steven G. Rogelberg',
        'College Course: Research Methods, Experimental Design, or Social Science Research'
    ],
    'diversity & inclusion certifications': [
        'Coursera - Diversity and Inclusion in the Workplace (University of Pittsburgh)',
        'Textbook: "The Inclusion Dividend: Why Investing in Diversity & Inclusion Pays Off" by Mark Kaplan and Mason Donovan',
        'Article: "Employee Engagement: A Review of Current Thinking" (Journal of Organizational Effectiveness)',
        'College Course: Diversity and Inclusion, Employee Relations, or HR Operations'
    ],
    'applied psychology certifications': [
        'Coursera - Introduction to Clinical Psychology (University of Toronto)',
        'Textbook: "Psychology Applied to Work: An Introduction to Industrial and Organizational Psychology" by Paul M. Muchinsky',
        'Article: "Applied Psychology: Principles and Methods" (Journal of Applied Psychology)',
        'College Course: Applied Psychology, Social Psychology, or Behavioral Science'
    ],
    'learning and development programs': [
        'Coursera - Learning and Development in Organizations (University of Minnesota)',
        'Textbook: "Employee Training and Development" by Raymond A. Noe',
        'Article: "Benefits of Training and Development for Individuals, Teams, Organizations, and Society" (Annual Review of Psychology)',
        'College Course: Adult Learning, Training and Development, or Instructional Design'
    ],
    'strategic planning and business solutions': [
        'Coursera - Strategic Planning and Execution (University of Virginia)',
        'Textbook: "The Strategy-Focused Organization" by Robert S. Kaplan and David P. Norton',
        'Article: "Strategic Planning in I-O Psychology" (Journal of Business Strategy)',
        'College Course: Business Strategy, Strategic Management, or Organizational Behavior'
    ],
    'leadership and team management': [
        'Coursera - Leadership and Management Specialization (University of Illinois)',
        'Textbook: "Leadership: Theory and Practice" by Peter G. Northouse',
        'Article: "Leadership in Organizational Contexts" (Journal of Leadership Studies)',
        'College Course: Leadership Studies, Organizational Behavior, or Business Management'
    ],
    'employee relations and cultural competence': [
        'Coursera - Cultural Competence: Engaging and Empowering Others (University of Michigan)',
        'Textbook: "Cultural Competence in Organizations: Theory, Research, and Practice" by Randall B. Lindsey',
        'Article: "The Importance of Cultural Competency in Organizational Settings" (Journal of Cross-Cultural Psychology)',
        'College Course: Cross-Cultural Communication, Global Studies, or Diversity and Inclusion'
    ],
    'research and application': [
        'Coursera - Research Methods and Data Analysis (University of London)',
        'Textbook: "Research Methods in Organizational Behavior" by Eugene F. Stone-Romero',
        'Article: "Quantitative and Qualitative Research Methods in I-O Psychology" (Journal of Applied Psychology)',
        'College Course: Research Methods, Data Analysis, or Quantitative Methods'
    ],
    'project management and execution': [
        'Coursera - Project Management: The Basics for Success (University of California, Irvine)',
        'Textbook: "Project Management: A Systems Approach to Planning, Scheduling, and Controlling" by Harold Kerzner',
        'Article: "Project Management and Leadership Skills: Insights from I-O Psychology" (Project Management Journal)',
        'College Course: Project Management, Operations Management, or Business Administration'
    ],
    'data analysis and interpretation': [
        'Coursera - Data Analysis and Statistical Inference (Duke University)',
        'Coursera - Applied Data Analysis (University of Michigan)',
        'Textbook: "Applied Multiple Regression/Correlation Analysis for the Behavioral Sciences" by Cohen, Cohen, West, & Aiken',
        'Article: "Data Analytics in I-O Psychology" (Journal of Applied Psychology)',
        'College Course: Data Analysis, Quantitative Analysis, or Research Methods'
    ],
    'effective communication': [
        'Coursera - Effective Communication: Writing, Design, and Presentation (University of Colorado Boulder)',
        'Textbook: "Communicating at Work: Strategies for Success in Business and the Professions" by Ronald B. Adler and Jeanne Marquardt Elmhorst',
        'Article: "Effective Communication in Organizations" (Journal of Business and Psychology)',
        'College Course: Communication Studies, Public Speaking, or Business Communication'
    ],
    'talent management and development': [
        'Coursera - Talent Management in HR (University of Minnesota)',
        'Textbook: "Talent Management: A Critical Introduction" by David G. Collings, Kamel Mellahi, and Wayne F. Cascio',
        'Article: "Global Talent Management and Performance in Multinational Enterprises" (Journal of World Business)',
        'College Course: Human Resource Management, Talent Management, or Organizational Behavior'
    ],
    'organizational change and development': [
        'Coursera - Organizational Change and Development (University of Illinois)',
        'Textbook: "Managing Organizational Change: A Multiple Perspectives Approach" by Ian Palmer, Richard Dunford, and Gib Akin',
        'Article: "The Psychology of Organizational Change" (Journal of Applied Behavioral Science)',
        'College Course: Organizational Development, Change Management, or Business Strategy'
    ],
    'leadership development': [
        'Coursera - Leadership Development for Professionals (University of Michigan)',
        'Textbook: "The Leadership Challenge" by James M. Kouzes and Barry Z. Posner',
        'Article: "Leadership Development: Research and Practice" (Journal of Leadership Development)',
        'College Course: Leadership, Organizational Behavior, or Human Resource Development'
    ],
    'problem-solving': [
        'Coursera - Problem Solving and Decision Making Skills (University of California, Irvine)',
        'Textbook: "Problem Solving 101" by Ken Watanabe',
        'Article: "Problem-Solving and Critical Thinking in Organizations" (Journal of Applied Psychology)',
        'College Course: Cognitive Psychology, Critical Thinking, or Business Strategy'
    ],
    'team dynamics and facilitation': [
        'Coursera - Team Dynamics and Collaboration (University of Michigan)',
        'Textbook: "Team Dynamics and Performance: Research and Practice" (Journal of Organizational Behavior)',
        'Article: "Facilitation Skills in Organizational Development" (Journal of Organizational Behavior)',
        'College Course: Organizational Behavior, Group Dynamics, or Leadership'
    ],
    'strategic planning': [
        'Coursera - Strategic Planning and Execution (University of Virginia)',
        'Textbook: "The Strategy-Focused Organization" by Robert S. Kaplan and David P. Norton',
        'Article: "Strategic Planning in I-O Psychology" (Journal of Business Strategy)',
        'College Course: Business Strategy, Strategic Management, or Organizational Behavior'
    ],
    'workforce planning': [
        'Coursera - Workforce Planning and Development (University of California, Irvine)',
        'Textbook: "Strategic Workforce Planning: Developing Optimized Talent Strategies for Future Growth" by Tracey Smith',
        'Article: "The Role of Workforce Planning in Modern Talent Management" (HR Magazine)',
        'College Course: Human Resource Management, Strategic Planning, or Organizational Behavior'
    ],
    'employee engagement and feedback': [
        'Coursera - Employee Engagement and Motivation (University of London)',
        'Textbook: "Employee Engagement 2.0" by Kevin Kruse',
        'Article: "Employee Engagement: A Review of Current Thinking" (Journal of Organizational Effectiveness)',
        'College Course: Organizational Behavior, Human Resource Management, or Employee Relations'
    ],
    'legal and regulatory compliance': [
        'Coursera - Employment Law and Compliance (University of California, Irvine)',
        'Textbook: "Employment Law for Business" by Dawn D. Bennett-Alexander and Laura Hartman',
        'Article: "Labor Law and the Modern Workforce" (Journal of Labor and Employment Law)',
        'College Course: Employment Law, Labor Relations, or HR Legal Environment'
    ],
    'data analysis and interpretation': [
        'Coursera - Data Analysis and Statistical Inference (Duke University)',
        'Coursera - Applied Data Analysis (University of Michigan)',
        'Textbook: "Applied Multiple Regression/Correlation Analysis for the Behavioral Sciences" by Cohen, Cohen, West, & Aiken',
        'Article: "Data Analytics in I-O Psychology" (Journal of Applied Psychology)',
        'College Course: Data Analysis, Quantitative Analysis, or Research Methods'
    ],
    'effective communication': [
        'Coursera - Effective Communication: Writing, Design, and Presentation (University of Colorado Boulder)',
        'Textbook: "Communicating at Work: Strategies for Success in Business and the Professions" by Ronald B. Adler and Jeanne Marquardt Elmhorst',
        'Article: "Effective Communication in Organizations" (Journal of Business and Psychology)',
        'College Course: Communication Studies, Public Speaking, or Business Communication'
    ],
    'talent management and development': [
        'Coursera - Talent Management in HR (University of Minnesota)',
        'Textbook: "Talent Management: A Critical Introduction" by David G. Collings, Kamel Mellahi, and Wayne F. Cascio',
        'Article: "Global Talent Management and Performance in Multinational Enterprises" (Journal of World Business)',
        'College Course: Human Resource Management, Talent Management, or Organizational Behavior'
    ],
    'organizational change and development': [
        'Prosci - Change Management Certification Program',
        'Coursera - Leading Organizational Change (Northwestern University)',
        'Textbook: "Organization Development and Change" by Cummings & Worley',
        'Article: "The Psychology of Organizational Change" (Journal of Applied Behavioral Science)',
        'College Course: Organizational Development, Change Management, or Business Strategy'
    ],
    'learning and development programs': [
        'ATD - Talent Development Certification (CPTD)',
        'Coursera - Learning and Development in Organizations (University of Minnesota)',
        'Textbook: "Employee Training and Development" by Raymond A. Noe',
        'Article: "Benefits of Training and Development for Individuals, Teams, Organizations, and Society" (Annual Review of Psychology)',
        'College Course: Adult Learning, Training and Development, or Instructional Design'
    ],
    'strategic planning and business solutions': [
        'Coursera - Strategic Planning and Execution (University of Virginia)',
        'Textbook: "The Strategy-Focused Organization" by Robert S. Kaplan and David P. Norton',
        'Article: "Strategic Decision Making in Organizations" (Academy of Management Journal)',
        'College Course: Business Strategy, Strategic Management, or Organizational Behavior'
    ],
    'leadership and team management': [
        'Coursera - Leadership and Management Specialization (University of Illinois)',
        'Textbook: "Leadership: Theory and Practice" by Peter G. Northouse',
        'Article: "Leadership and Team Dynamics" (Journal of Applied Psychology)',
        'College Course: Leadership Studies, Organizational Behavior, or Business Management'
    ],
    'employee relations and cultural competence': [
        'Coursera - Cultural Competence: Engaging and Empowering Others (University of Michigan)',
        'Textbook: "Cultural Competence in Organizations: Theory, Research, and Practice" by Randall B. Lindsey',
        'Article: "Cultural Competence in Organizational Contexts" (International Journal of Intercultural Relations)',
        'College Course: Cross-Cultural Communication, Global Studies, or Diversity and Inclusion'
    ],
    'research and application': [
        'Coursera - Research Methods (University of London)',
        'Textbook: "Research Methods in Organizational Behavior" by Eugene F. Stone-Romero',
        'Article: "Quantitative and Qualitative Research Methods in I-O Psychology" (Journal of Applied Psychology)',
        'College Course: Research Methods, Data Analysis, or Quantitative Methods'
    ],
    'project management and execution': [
        'PMI - Project Management Professional (PMP) Certification',
        'Coursera - Project Management: The Basics for Success (University of California, Irvine)',
        'Textbook: "Project Management: A Systems Approach to Planning, Scheduling, and Controlling" by Harold Kerzner',
        'Article: "Project Management and Leadership Skills: Insights from I-O Psychology" (Project Management Journal)',
        'College Course: Project Management, Operations Management, or Business Administration'
    ],
    'adaptability and compliance': [
        'Coursera - Adaptive Leadership in Development (University of Queensland)',
        'Textbook: "Adaptive Leadership: Accelerating Enterprise Agility" by Jim Highsmith',
        'Article: "Regulatory Compliance and Human Behavior" (Journal of Business Ethics)',
        'College Course: Business Ethics, Compliance Management, or Organizational Behavior'
    ],
    
    # Certification Groups
    'change management certifications': [
        'Prosci - Change Management Certification Program',
        'ACMP - Certified Change Management Professional (CCMP)',
        'Textbook: "ADKAR: A Model for Change in Business, Government and our Community" by Jeffrey M. Hiatt',
        'Article: "A Review of Change Management Certification Programs" (Journal of Change Management)'
    ],
    'project management certifications': [
        'PMI - Project Management Professional (PMP) Certification',
        'PRINCE2 - PRINCE2 Foundation and Practitioner Certification',
        'Textbook: "Project Management Best Practices: Achieving Global Excellence" by Harold Kerzner',
        'Article: "Certification and Project Management Effectiveness" (International Journal of Project Management)'
    ],
    'global hr certifications': [
        'HRCI - Global Professional in Human Resources (GPHR)',
        'SHRM - SHRM Global Certification',
        'Textbook: "Global Human Resource Management" by Carol Reade and Paul Sparrow',
        'Article: "Global HR Certifications and Their Impact on HR Professionals" (Journal of International Business Studies)'
    ],
    'hr certifications': [
        'SHRM - SHRM Certified Professional (SHRM-CP) and Senior Certified Professional (SHRM-SCP)',
        'HRCI - Professional in Human Resources (PHR) and Senior Professional in Human Resources (SPHR)',
        'Textbook: "Fundamentals of Human Resource Management" by Noe, Hollenbeck, Gerhart, and Wright',
        'Article: "The Value of HR Certification: A Review of the Evidence" (Human Resource Management Review)'
    ],
    'talent development & learning certifications': [
        'ATD - Certified Professional in Talent Development (CPTD)',
        'Textbook: "ATD’s Handbook for Training and Talent Development" by Elaine Biech',
        'Article: "Certifications in Talent Development: Benefits and Considerations" (International Journal of Training and Development)',
        'College Course: Talent Development, Adult Learning, or Training and Development'
    ],
    'organizational development & effectiveness certifications': [
        'NTL Institute - Organization Development Certification Program',
        'IOD - Certified Organizational Development Professional (CODP)',
        'Textbook: "Practicing Organization Development" by William J. Rothwell and Jacqueline M. Stavros',
        'Article: "Professional Certifications in Organizational Development" (OD Practitioner Journal)'
    ],
    'hr & workforce analytics certifications': [
        'IHRIM - Human Resource Information Professional (HRIP) Certification',
        'HCI - People Analytics for HR (PAHR) Certification',
        'Textbook: "The Power of People: Learn How Successful Organizations Use Workforce Analytics" by Nigel Guenole, Jonathan Ferrar, and Sheri Feinzig',
        'Article: "Workforce Analytics: A Critical Evaluation" (Journal of Human Resource Management)'
    ],
    'research & methodologies certifications': [
        'AAPOR - Professional Researcher Certification (PRC)',
        'Textbook: "Research Design: Qualitative, Quantitative, and Mixed Methods Approaches" by John W. Creswell',
        'Article: "Certification in Research Methodologies: Enhancing Credibility" (Journal of Applied Psychology)'
    ],
    'diversity & inclusion certifications': [
        'Cornell University - Diversity and Inclusion Certificate Program',
        'SHRM - Inclusive Workplace Culture Specialty Credential',
        'Textbook: "The Inclusion Dividend: Why Investing in Diversity & Inclusion Pays Off" by Mark Kaplan and Mason Donovan',
        'Article: "The Impact of Diversity Certification on Organizational Inclusion" (Equality, Diversity and Inclusion Journal)'
    ],
    'applied psychology certifications': [
        'American Board of Professional Psychology (ABPP) Certification',
        'Textbook: "Psychology Applied to Work: An Introduction to Industrial and Organizational Psychology" by Paul M. Muchinsky',
        'Article: "Certification in Applied Psychology: Benefits for Practitioners" (Professional Psychology: Research and Practice)'
    ],
    'strategy & business certifications': [
        'Association for Strategic Planning (ASP) Certifications',
        'Textbook: "Good Strategy Bad Strategy" by Richard Rumelt',
        'Article: "The Role of Certifications in Strategic Management" (Strategic Management Journal)'
    ],
    'human capital management certifications': [
        'HCI - Strategic HR Business Partner (sHRBP) Certification',
        'Textbook: "Human Capital Management: Leveraging Your Workforce for a Competitive Advantage" by Angela Baron and Michael Armstrong',
        'Article: "Human Capital Certifications and Organizational Performance" (Journal of Human Capital)'
    ],
    
    # Additional Training Groups
    'instructional design and e-learning': [
        'Coursera - Instructional Design MasterTrack Certificate (University of Illinois)',
        'Textbook: "The Systematic Design of Instruction" by Dick & Carey',
        'Article: "Best Practices in Instructional Design and Technology" (Journal of Educational Psychology)',
        'College Course: Instructional Design, Educational Technology, or Curriculum Development'
    ],
    'labor laws and organizational behavior': [
        'Coursera - Employment Law for Business (University of California, Irvine)',
        'Textbook: "Employment Law for Business" by Dawn D. Bennett-Alexander and Laura Hartman',
        'Article: "Labor Law and the Modern Workforce" (Journal of Labor and Employment Law)',
        'College Course: Employment Law, Labor Relations, or HR Legal Environment'
    ],
    'organizational behavior and project management': [
        'Coursera - Organizational Behavior: How to Manage People (IE Business School)',
        'Textbook: "Organizational Behavior" by Stephen P. Robbins and Timothy A. Judge',
        'Article: "Linking Organizational Behavior and Project Management: Insights from I-O Psychology" (Journal of Applied Psychology)',
        'College Course: Organizational Behavior, Project Management, or Leadership'
    ],
    'performance management and employee development': [
        'Coursera - Performance Management: Employee Engagement and Development (University of London)',
        'Textbook: "Performance Management" by Herman Aguinis',
        'Article: "Best Practices in Employee Development and Performance Management" (Journal of HRM)',
        'College Course: Performance Management, Employee Development, or HR Management'
    ],
    'research methodologies and data analysis': [
        'Coursera - Quantitative Research Methods (University of London)',
        'Textbook: "Research Methods in Organizational Behavior" by Eugene F. Stone-Romero',
        'Article: "Quantitative and Qualitative Research Methods in I-O Psychology" (Journal of Applied Psychology)',
        'College Course: Research Methods, Data Analysis, or Quantitative Methods'
    ],
    'workforce planning and talent management': [
        'Coursera - Workforce Analytics for Strategic Decisions (University of California, Irvine)',
        'Textbook: "Strategic Workforce Planning: Developing Optimized Talent Strategies for Future Growth" by Tracey Smith',
        'Article: "The Role of Workforce Planning in Modern Talent Management" (HR Magazine)',
        'College Course: Workforce Planning, Talent Management, or Strategic HRM'
    ],
    'assessment and intervention techniques': [
        'Coursera - Psychological First Aid (Johns Hopkins University)',
        'Textbook: "Psychological Assessment and Intervention Techniques" by Jay C. Thomas',
        'Article: "Best Practices in Psychological Assessment and Intervention" (Journal of Applied Psychology)',
        'College Course: Psychological Assessment, Intervention Techniques, or Clinical Psychology'
    ],
    'coaching and executive development': [
        'Coursera - Executive Coaching Specialization (Northwestern University)',
        'Textbook: "The Art and Practice of Leadership Coaching" by Howard Morgan, Phil Harkins, and Marshall Goldsmith',
        'Article: "Executive Coaching and Leadership Development" (Journal of Leadership and Organizational Studies)',
        'College Course: Coaching, Executive Development, or Leadership'
    ],
    'cultural competency and sensitivity': [
        'Coursera - Cultural Competence: Engaging and Empowering Others (University of Michigan)',
        'Textbook: "Cultural Competence in Organizations: Theory, Research, and Practice" by Randall B. Lindsey',
        'Article: "The Importance of Cultural Competency in Organizational Settings" (Journal of Cross-Cultural Psychology)',
        'College Course: Cross-Cultural Communication, Global Studies, or Diversity and Inclusion'
    ],
    'strategic planning and data analysis': [
        'Coursera - Strategic Planning and Execution (University of Virginia)',
        'Coursera - Data Analysis and Statistical Inference (Duke University)',
        'Textbook: "Strategic Planning for Public and Nonprofit Organizations" by John M. Bryson',
        'Article: "Data-Driven Strategic Planning in Organizations" (Strategic Management Journal)',
        'College Course: Strategic Management, Data Analysis, or Business Strategy'
    ],
}
