import json
from bs4 import BeautifulSoup

# Step 1: Read the JSON file
with open('C://Users//cheny//Desktop//Eli Project//JobSpider//indeedSpider//jobs.json', 'r') as file:
    jobs = json.load(file)

filtered_jobs = []
for job in jobs:
    if 'jobLocation' in job and any(substring in job['jobLocation'] for substring in ['AB', 'ab', 'Ab', 'Alberta']):
        html_content = job['jobDescription']
        # Convert HTML to plain text
        plain_text = BeautifulSoup(html_content, 'html.parser').get_text(separator="\n")
        
        # Clean up the text
        # Remove or replace unwanted newline characters 
        plain_text = plain_text.replace('\n\n', '').strip()
        plain_text = plain_text.replace('\n', '').strip()
        # Optional: Remove specific unicode characters like \u00e2\u20ac\u00a6
        plain_text = plain_text.replace('\u00e2\u20ac\u00a6', '').strip()
        
        # Replace the jobDescription in the JSON
        job['jobDescription'] = plain_text
        if 'salary' in job:
            salary_text = job['salary']
            if salary_text is None:
                continue
            # Replace specific unicode sequence with a dash
            salary_text = salary_text.replace('\u00e2\u20ac\u201c', '-').strip()
            # Replace the salary in the JSON
            job['salary'] = salary_text
        filtered_jobs.append(job)
        
# Step 4: Save the modified JSON to a file (optional)
with open('jobs_modified.json', 'w', encoding='utf-8') as file:
    json.dump(jobs, file, indent=4, ensure_ascii=False)

# If you want to print the result to the console
print(json.dumps(jobs, indent=4, ensure_ascii=False))
