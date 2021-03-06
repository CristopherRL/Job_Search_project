######################################### IMPORTING LIBRARIES #################################################
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import time
import re
import pandas as pd
from datetime import datetime, timedelta
import getpass
import platform

######################################### IMPORTING DATA #################################################
def getting_data():

    os.system('clear')
    repeat = '2' #default value
    profile = pd.DataFrame({'A': []}) #empty df
    job = pd.DataFrame({'A': []}) #empty df

    while repeat == '2':
        # STARTING
        print("""
    *******************  OPTIMIZED JOB SEARCH ON LINKEDIN *******************

    Welcome!

    This search has been created initially to find job posts on LinkedIn related with: 
    Data Analyst - Data Scientist - Data Engineer

    Please tell me what would you like to do >>>
    1: Start a new search in LinkedIn
    2: Load a recorded search""")

        option_selected = input("    > ")

        if option_selected == '1':
            browser = open_selenium('https://www.linkedin.com/login')
            driver = linkedin_session(browser)
            if driver.current_url == "https://www.linkedin.com/feed/":
                print("     >>> Successful login !")
                profile, job, repeat = new_search(driver)
            else:
                print("     >>> User and/or password are wrong!!! Please try again")
                driver.close()
                repeat = '2'
            option = 1
        elif option_selected == '2':
            profile, job, repeat = recorded_search()
            option = 2
        else:
            raise ValueError("Sorry! The option selected is not allowed. Exit and try again")

        print('\n   ... Click to continue')
        input()
        os.system('clear')
        #os.system("pause")

    return profile, job, option


def new_search(browser):
    ### PARAMETERS ###
    # Defining current date time
    now = datetime.now()
    now_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    now_file = now_str.replace(':', '.')

    # wating time
    w = 10

    ################################## LINKEDIN PROFILE ######################################

    ### MAIN PAGE
    # Click on profile button (up-rigth)
    profile = WebDriverWait(browser, w).until(EC.presence_of_element_located((By.ID,\
        'profile-nav-item')))
    # profile = browser.find_element_by_xpath('/html/body/header/div/nav/ul/li[6]/div/artdeco-dropdown/artdeco-dropdown-trigger/div')
    profile.click()
    # Click on View profile button
    # link_profile = browser.find_element_by_xpath('/html/body/header/div/nav/ul/li[6]/div/artdeco-dropdown/artdeco-dropdown-content/div/ul/li[1]/a/div[2]/span')
    link_profile = WebDriverWait(browser, w).until(EC.presence_of_element_located((By.XPATH,
        "//span[@class='artdeco-button artdeco-button--tertiary artdeco-button--fluid']")))
    link_profile.click()


    ### PROFILE PAGE
    browser.maximize_window()
    html_body = WebDriverWait(browser, w).until(EC.presence_of_element_located((By.XPATH, '/html/body')))
    html_body.send_keys(Keys.PAGE_DOWN)
    time.sleep(3) #just to be sure
    linkedin_profile = browser.current_url.split('/')[4]
    print(f"""\n
    > LINKEDIN PROFILE: {linkedin_profile}
    """)

    ### HEADLINE
    try:
        profile_headline = WebDriverWait(browser, w).until(EC.presence_of_element_located \
                            ((By.XPATH, "//h2[@class='mt1 t-18 t-black t-normal']")))
        headline = profile_headline.text.lower()
        print('     Loading HEADLINE > OK')
    except:
        try:
            html_body.send_keys(Keys.PAGE_DOWN)
            profile_headline = WebDriverWait(browser, w).until(EC.presence_of_element_located \
                ((By.XPATH, "//h2[@class='mt1 t-18 t-black t-normal']")))
            headline = profile_headline.text.lower()
            print('     Loading HEADLINE > OK')
        except:
            headline = ""


    ### OPEN STATUS
    try:
        profile_open = WebDriverWait(browser, w).until(EC.presence_of_element_located \
                         ((By.XPATH,"//div[@class='artdeco-carousel__content']")))
        if profile_open.text.split(" ")[0] == 'Open':
            open_status = 'YES'
        else:
            open_status = 'NO'
        print('     Loading OPEN STATUS > OK')
    except:
        try:
            html_body.send_keys(Keys.PAGE_DOWN)
            profile_open = WebDriverWait(browser, w).until(EC.presence_of_element_located \
            ((By.XPATH, "//div[@class='artdeco-carousel__content']")))
            if profile_open.text.split(" ")[0] == 'Open':
                open_status = 'YES'
            else:
                open_status = 'NO'
            print('     Loading OPEN STATUS > OK')
        except:
            open_status = ''

    ### ABOUT
    # show MORE > button "see more "
    profile_show_about = WebDriverWait(browser, w).until(EC.presence_of_element_located \
                            ((By.XPATH,"//span[@class='lt-line-clamp__line lt-line-clamp__line--last']")))
    ActionChains(browser).move_to_element(profile_show_about).perform()
    profile_show_about.click()
    # getting info
    profile_about = WebDriverWait(browser, w).until(EC.presence_of_element_located\
                   ((By.XPATH,"//p[@class='pv-about__summary-text mt4 t-14 ember-view']")))
    about = profile_about.text.lower()
    print('     Loading ABOUT > OK')

    ### JOB EXPERIENCE
    html_body.send_keys(Keys.PAGE_DOWN * 5)
    time.sleep(0.2)
    html_body.send_keys(Keys.PAGE_DOWN * 5)
    time.sleep(0.2)
    # show MORE experiences > button "show more experience"
    profile_show_experience = WebDriverWait(browser, 3).until(EC.presence_of_element_located\
    ((By.XPATH,"//button[@class='pv-profile-section__see-more-inline pv-profile-section__text-truncate-toggle link link-without-hover-state']")))
    ActionChains(browser).move_to_element(profile_show_experience).perform()
    profile_show_experience.click()
    html_body.send_keys(Keys.PAGE_UP)
    profile_experience = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.ID,'experience-section')))
    # getting info: time experience
    pattern_t1 = 'Employment Duration\n(.*)\nLocation'
    time_experience = list(re.findall(pattern_t1, profile_experience.text))
    # getting info: name experience
    pattern_n1 = '\n(.*)\ncompany name'
    name_experience1 = list(re.findall(pattern_n1, profile_experience.text.lower()))
    pattern_n2 = 'title\n(.*)\n'
    name_experience2 = list(re.findall(pattern_n2, profile_experience.text.lower()))
    name_experience = name_experience1 + name_experience2
    if 'see more' in name_experience:
        name_experience.remove('see more')

    # Calculating years of experience
    y, m = 0, 0
    for t in time_experience:
        if re.findall('[0-9] yr', t):
            year = re.findall('[0-9] yr', t)[0].split(" ")[0]
            y += int(year)
        if re.findall('[0-9] mo', t):
            month = re.findall('[0-9] mo', t)[0].split(" ")[0]
            m += int(month)
    y_nuevo = y + m % 12
    print('     Loading JOB EXPERIENCE > OK')

    ### EDUCATION
    profile_education = WebDriverWait(browser, w).until(EC.presence_of_element_located\
                   ((By.ID,'education-section')))
    # getting info: degrees
    pattern_e1 = 'degree name\n(.*)\n'
    degrees = re.findall(pattern_e1, profile_education.text.lower())
    # getting info: grades
    pattern_e2 = 'field of study\n(.*)\n'
    fields = re.findall(pattern_e2, profile_education.text.lower())
    print('     Loading EDUCATION > OK')



    ### SKILLS
    # show MORE skills > > button "show more..."
    profile_more_skills = WebDriverWait(browser, w).until(EC.presence_of_element_located\
                   ((By.XPATH,"//button[@data-control-name='skill_details']")))
    ActionChains(browser).move_to_element(profile_more_skills).perform()
    profile_more_skills.click()
    html_body.send_keys(Keys.PAGE_UP)
    # skill table> text
    profile_skills_details = WebDriverWait(browser, w).until(EC.presence_of_element_located\
    ((By.XPATH,"//section[@class='pv-profile-section pv-skill-categories-section artdeco-container-card ember-view']")))
    # Extracting skills
    skills = profile_skills_details.text.split("\n")
    not_needed_words = ['Skills & Endorsements',
                        'Add a new skill',
                        'Take skill quiz',
                        'Passed: LinkedIn Assessments',
                        'Tools & Technologies',
                        'Interpersonal Skills',
                        'Languages',
                        'Other Skills',
                        'Show less',
                        ]
    # Getting just necesary skills
    skills_delete = []
    for s in skills:
        if (s in not_needed_words) or re.search('ndorse', s) or re.search('Show only', s) or re.search('[0-9]', s):
            skills_delete.append(s)
    skills_clean = list(set(skills) - set(skills_delete))
    skills_clean = [x.lower().split(' (')[0] for x in skills_clean]
    skills_clean.sort()
    print('     Loading SKILLS > OK')

    ### LANGUAGES
    languages = WebDriverWait(browser, w).until(EC.presence_of_element_located\
                   ((By.ID,'languages-expandable-content'))).text.split(' ')
    languages = [x.lower() for x in languages]
    print('     Loading LANGUAGES > OK')

    ### TOTAL SKILLS
    total_skills = sorted(list(set(degrees + fields + skills_clean + languages)))

    ### RAW PROFILE
    profile_raw = WebDriverWait(browser, w).until(EC.presence_of_element_located\
                   ((By.XPATH,"//main[@class='core-rail']"))).text.replace("\n"," ")

    ### DF PROFILE (1ST RESULT)
    # Creating df_profile
    profile = [linkedin_profile, headline, open_status, about, name_experience, time_experience,
               y_nuevo, degrees, fields, skills_clean, languages, total_skills, profile_raw]

    df_profile = pd.DataFrame(profile,
                              index=['profile',
                                     'headline',
                                     'open new jobs',
                                     'about',
                                     'experiences',
                                     'years of experiences',
                                     'total years',
                                     'degrees',
                                     'fields',
                                     'skills',
                                     'languages',
                                     'total skills',
                                     'profile raw'

                                     ],
                              columns=['info']
                              )

    # LINUX
    now_file = now_str.replace(':', '.')
    if platform.system() == 'Linux':
        df_profile.to_csv(f'data/raw/df_profile/df_profile_{linkedin_profile}_{now_file}.csv',
                          sep=';',
                          encoding='utf8'
                          )
    # WINDOWS
    elif platform.system() == 'Windows':
        df_profile.to_csv(f'\\data\\raw\\df_profile\\df_profile_{linkedin_profile}_{now_file}.csv',
                          sep=';',
                          encoding='utf8'
                          )


    print(f"""     >>> PROFILE LOADED AND SAVED!!! > data/raw/df_profile/df_profile_{linkedin_profile}_{now_file}.csv\n""")

    ################################## LINKEDIN JOB SEARCH ######################################

    ### PARAMETERS
    jobs_list_es = ['analista datos', 'cientifico datos', 'ingeniero datos']
    jobs_list_en = ['data analyst', 'data scientist', 'data engineer']

    ### FUNCTIONS > AT THE END

    print(f"""\n\n    > LINKEDIN JOB SEARCH:""")

    repeat_search = '0' #default value
    df_jobs = pd.DataFrame({'A': []}) #empty df
    while repeat_search == '0':

        # location
        location_input = input("""
    Please enter the location (CITY) where you'd like to search: 
    > """)
        location = location_input.capitalize()


        jobs_version = input(f"""
    Which version of job searching would you like to choose:
    1: Spanish version > {jobs_list_es}
    2: English version > {jobs_list_en}
    > """)
        print('')

        # Jobs search
        jobs_list_lang = ""
        if   jobs_version== '1':
            jobs_list = ['analista datos', 'cientifico datos', 'ingeniero datos']
            jobs_list_lang = 'es'
        elif jobs_version == '2':
            jobs_list = ['data analyst', 'data scientist', 'data engineer']
            jobs_list_lang = 'en'


        # Creating empty df with columns
        df_jobs = pd.DataFrame(columns=['JOB TITLE',
                                        'LOCATION',
                                        'SEARCH DATETIME',
                                        'Current Job Id',
                                        'Job html',
                                        'Job name',
                                        'Company name',
                                        'Company location',
                                        'Posted date',
                                        'Estimated post date',
                                        'Easy apply',
                                        'Job Description',
                                        'Skills match',
                                        'Seniority Level',
                                        'Industry',
                                        'Employment Type',
                                        'Job Functions',
                                        'Job info'
                                        ])

        ### ITERATOR OF JOBS
        try:

            # *************************************************************************
            ### ITERATOR OF JOBS LIST
            for j in jobs_list:
                count = 0

                # Getting each job for the search
                print(f'    ++++++++++++++++  {j} +++++++++++++++++++')
                job_title_df = j
                job_title_s = j.replace(' ', '%20')

                # Getting number of pages for each search
                n_pages = n_pages_linkedin(browser, job_title_s, location)
                # total_results +=results
                last_job_page = n_pages * 25
                #time.sleep(2)

                # *************************************************************************
                # iterator of JOB PAGES
                for p in range(0, last_job_page, 25):

                    # Exploring each page with maximum 25 job posts > not necessary for first page
                    if p>0:
                        JOB_URL = f'https://www.linkedin.com/jobs/search/?keywords={job_title_s}&location={location}&start={p}'
                        browser.get(JOB_URL)

                    # if p == 0:
                    #     time.sleep(1.5)
                    # else:
                    #     time.sleep(0.5)

                    # Taking table of job posts
                    tabla_izq = WebDriverWait(browser, 2).until(EC.presence_of_element_located\
                    ((By.XPATH,"//div[@class='jobs-search-results jobs-search-results--is-two-pane']")))


                    # *************************************************************************
                    # iterator of JOB LIST - jobs posts
                    i = 1
                    error = False
                    while i <= 25 and error == False:

                        try:

                            # Selecting job post in order to click on it
                            job_post = j_post(browser, i)
                            job_post.click()
                            #time.sleep(0.1)

                            # Getting current job ID
                            currentJobId = browser.current_url.split('currentJobId=')[1].split('&')[0]  # col1_pd
                            # if you wanna watch the job page
                            job_html = f'https://www.linkedin.com/jobs/view/{currentJobId}/'

                            # Extracting job information on the right side
                            job_post_right = WebDriverWait(browser, 1).until(EC.presence_of_element_located\
                            ((By.XPATH,"//div[@class='jobs-search-two-pane__details pt4 ph3 jobs-search-two-pane__details ember-view']")))



                            ############# Extracting JOB INFO

                            # Job name
                            job_post_name = job_post_right.text.split('\n', 1)[0]

                            # Company name > Sometimes there is no info here
                            if job_post_right.text.split('Company Name\n', 1)[1].split('\n')[0] == 'Company Location':
                                job_post_company_name = ""
                            else:
                                job_post_company_name = job_post_right.text.split('Company Name\n', 1)[1].split('\n')[0]

                            # Location
                            job_post_company_location = job_post_right.text.split('Company Location\n', 1)[1].split('\n')[0]

                            # Posted date
                            job_post_posted_date = job_post_right.text.split(' ago', 1)[0].split('Posted Date\nPosted ')[1]
                            if job_post_posted_date.split(" ")[1] in ['hour', 'hours']:
                                job_post_estimated_date = now - timedelta(hours=int(job_post_posted_date.split(" ")[0]))
                            elif job_post_posted_date.split(" ")[1] in ['day', 'days']:
                                job_post_estimated_date = now - timedelta(days=int(job_post_posted_date.split(" ")[0]))
                            elif job_post_posted_date.split(" ")[1] in ['week', 'weeks']:
                                job_post_estimated_date = now - timedelta(weeks=int(job_post_posted_date.split(" ")[0]))
                            elif job_post_posted_date.split(" ")[1] in ['month', 'months']:
                                job_post_estimated_date = now - timedelta(weeks=4 * int(job_post_posted_date.split(" ")[0]))
                            elif job_post_posted_date.split(" ")[1] in ['year', 'years']:
                                job_post_estimated_date = now - timedelta(weeks=365 * int(job_post_posted_date.split(" ")[0]))
                            else:
                                job_post_estimated_date = ""

                            # Easy apply: T/F
                            try:
                                if job_post_right.text.split('Save\n', 1)[1].split('\n', 2)[1] == 'Easy Apply':
                                    job_post_easy_apply = True
                                else:
                                    job_post_easy_apply = False
                            except:
                                if job_post_right.text.split('Unsave\n', 1)[1].split('\n', 2)[1] == 'Easy Apply':
                                    job_post_easy_apply = True
                                else:
                                    job_post_easy_apply = False

                            # Skills match
                            if re.search('\nHow you match', job_post_right.text):
                                # if '\nHow you match' in job_post_right.text:
                                y = 'Match\n(.*)\n'
                                n = 'No match\n(.*)\n'
                                job_post_skills_match = re.findall(y, job_post_right.text)
                                job_post_skills_nomatch = re.findall(n, job_post_right.text)
                                job_post_skills = {'yes': job_post_skills_match,
                                                   'no': job_post_skills_nomatch,
                                                   'all': job_post_skills_match + job_post_skills_nomatch
                                                   }
                            else:
                                job_post_skills = {}

                            ### Job description
                            # Extracting job information on the right side
                            job_post_right_description = \
                                browser.find_element_by_xpath(
                                    "//div[@class='jobs-box jobs-box--fadein jobs-box--full-width jobs-box--with-cta-large jobs-description jobs-description--reformatted ember-view']").text

                            # Seniority Level
                            try:
                                job_post_seniority_level = \
                                    job_post_right.text.split('Seniority Level\n', 1)[1].split('\n')[0]
                            except:
                                job_post_seniority_level = ""

                            # Industry
                            try:
                                job_post_industry = \
                                    job_post_right.text.split('Industry\n', 1)[1].split('\n')[0]
                            except:
                                job_post_industry = ""

                            # Employment Type
                            try:
                                job_post_employment_type = \
                                    job_post_right.text.split('Employment Type\n', 1)[1].split('\n')[0]
                            except:
                                job_post_employment_type = ""

                            # Job Functions
                            try:
                                job_post_job_functions = \
                                    job_post_right.text.split('Job Functions\n', 1)[1].split('\n')[0]
                            except:
                                job_post_job_functions = ""

                            # Job info
                            job_post_info = job_post_right.text.split('\n', 5)[5]

                            # Dataframe
                            df_jobs = df_jobs.append({
                                'JOB TITLE': job_title_df,
                                'LOCATION': location,
                                'SEARCH DATETIME': now_str,
                                'Current Job Id': currentJobId,
                                'Job html': job_html,
                                'Job name': job_post_name,
                                'Company name': job_post_company_name,
                                'Company location': job_post_company_location,
                                'Posted date': job_post_posted_date,
                                'Estimated post date': job_post_estimated_date.strftime('%Y-%m-%d %H:%M'),
                                'Easy apply': job_post_easy_apply,

                                'Skills match': job_post_skills,
                                'Job Description': job_post_right_description,
                                'Seniority Level': job_post_seniority_level,
                                'Industry': job_post_industry,
                                'Employment Type': job_post_employment_type,
                                'Job Functions': job_post_job_functions,
                                'Job info': job_post_info,
                            }, ignore_index=True)

                            if i % 5 == 0:  # each 5 job post, one execution of 2 pages down to see more jobs
                                tabla_izq.send_keys(Keys.PAGE_DOWN * 2)
                                time.sleep(0.1)
                            count+=1


                        except:
                            error = True  # if an error ocurred when the algorith tried to get a post, this loop finishs and goes to the next page
                        finally:
                            i += 1  # next job post >>>>>>>>>>>>>>>>
                print(f'    SEARCH RESULTS: {count} RESULTS')

            #Calculating time of process
            end = datetime.now()
            dif = str(round((end - now).total_seconds()/60, 2))

            print(f"""\n    WEB SCRAPPING FINISHED IN {dif} MINUTES!!!
    >>> {df_jobs.shape[0]} job posts have been loaded""")


        except: #windowsclosed

            # Calculating time of process
            end = datetime.now()
            dif = str(round((end - now).total_seconds()/60, 2))

            #erasing last row
            df_jobs.drop(df_jobs.tail(1).index, inplace=True)

            print(f"""\n    WEB SCRAPPING FINISHED IN {dif} MINUTES!!!
    >>> {df_jobs.shape[0]} job posts have been loaded """)
            if df_jobs.shape[0]>0:
                print('     * last row of dataframe have been deleted by an error in web scrapping')
            pass
        df_rows = df_jobs.shape[0]
        ### Exporting to csv

        # LINUX

        if platform.system() == 'Linux':
            df_jobs.to_csv(f'data/raw/df_jobs/df_jobs_{location}_{jobs_list_lang}_{now_file}_{df_rows}.csv',
                           sep=';',
                           encoding='utf8',
                           index=False,
                           )
        # WINDOWS
        elif platform.system() == 'Windows':
            df_jobs.to_csv(f'\\data\\raw\\df_jobs\\df_jobs_{location}_{jobs_list_lang}_{now_file}_{df_rows}.csv',
                           sep=';',
                           encoding='utf8',
                           index=False,
                           )
        print(f'    >>> A csv file have been saved: data/raw/df_jobs/df_jobs_{location}_{jobs_list_lang}_{now_file}_{df_rows}.csv')

        #NEW QUESTION
        repeat_search = input("""\n     WOULD YOU LIKE TO REPEAT THIS SEARCH WITH A NEW LOCATION?
    0: YES, I would like to try again with a new city
    1: NO, I want to continue with this results and analyze the data
    2: I prefer to come back to the first menu
    > """)

        if repeat_search == '0':
            print("""\n
    *********** NEW SEARCH :""")

    #Closing session
    try:
        browser.close() #browser.quit()
    except:
        pass

    return df_profile , df_jobs, repeat_search




def recorded_search():

    ### SEARCH INFORMATION
    print("""\n\n*********** LOAD SEARCH :""")

    ################################## LINKEDIN PROFILE ######################################

    df_profile = pd.DataFrame({'A': []})  # empty df

    print(f"""\n\n    >LINKEDIN PROFILE:
    Please select one of the Job Profile file writing the number at the end """)

    # Reading files
    files_list = []
    if platform.system() == 'Linux':
        for files in os.walk('data/raw/df_profile'):
            for f in files:
                files_list= f
    elif platform.system() == 'Windows':
        for files in os.walk('\\data\\raw\\df_profile'):
            for f in files:
                files_list= f

    # Selecting file
    i = 0
    for file in f:
        print(f'    {i}: {file}')
        i += 1
    index = int(input('    >'))
    df_profile_file = f[index]

    # Importing file
    if platform.system() == 'Linux':
        df_profile = pd.read_csv(f'data/raw/df_profile/{df_profile_file}',
                                 sep=';',
                                 encoding='utf8',
                                 index_col=0
                                 )

    elif platform.system() == 'Windows':
        df_profile = pd.read_csv(f'\\data\\raw\\df_profile\\{df_profile_file}',
                                 sep=';',
                                 encoding='utf8',
                                 index_col=0
                                 )

    ################################## RECORDED SEACH ######################################

    print(f"""\n\n    >LINKEDIN JOB SEARCH:
    Please select one of the Job Search file, writing the number at the end """)

    # Reading files
    files_list = []
    if platform.system() == 'Linux':
        for files in os.walk('data/raw/df_jobs'):
            for f in files:
                files_list = f
    elif platform.system() == 'Windows':
        for files in os.walk('\\data\\raw\\df_jobs'):
            for f in files:
                files_list = f

    # Selecting file
    i = 0
    for file in f:
        print(f'    {i}: {file}')
        i+=1
    index = int(input('    >'))
    df_profile_file = f[index]

    # Importing file
    df_jobs = pd.DataFrame({'A': []}) #empty df
    if platform.system() == 'Linux':
        df_jobs = pd.read_csv(f'data/raw/df_jobs/{df_profile_file}',
                                 sep=';',
                                 encoding='utf8'
                                 )

    elif platform.system() == 'Windows':
        df_jobs = pd.read_csv(f'\\data\\raw\\df_jobs\\{df_profile_file}',
                                 sep=';',
                                 encoding='utf8'
                                 )

    print(f"""\n    FILES READY !!!
    >>> {df_jobs.shape[0]} job posts have been loaded """)

    # If I take the option of loading a file, this is because I dont want to come again to first menu
    # If I'm here, I wanna ANALYSE
    repeat_search = '1'

    return df_profile , df_jobs, repeat_search

######################################### FUNCTIONS #################################################

# Iterator of JOB POSTS > the only way is considering XPATH with an iteration
def j_post(browser, i):

    w=10

    block = WebDriverWait(browser, w).until(EC.presence_of_element_located \
    ((By.XPATH,f"//ul[@class='jobs-search-results__list artdeco-list']/li[{i}]")))

    job_post = block.find_element_by_xpath(f"div/div[1]/div/h3/a")

    #job_post.click()

    return job_post


# Iterator of JOB POSTS > the only way is considering XPATH with an iteration
def j_post_old(browser, i):

    w=5

    if WebDriverWait(browser, w).until(EC.presence_of_element_located \
        ((By.XPATH,f'/html/body/div[8]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]/div[2]/div/ul/li[{i}]/div/div[1]/div/h3/a'))):
        job_post = WebDriverWait(browser, w).until(EC.presence_of_element_located \
        ((By.XPATH,f'/html/body/div[8]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]/div[2]/div/ul/li[{i}]/div/div[1]/div/h3/a')))

    elif WebDriverWait(browser, w).until(EC.presence_of_element_located \
        ((By.XPATH,f'/html/body/div[8]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]/div[2]/div[2]/ul/li[{i}]/div/div[1]/div/h3/a'))):
        job_post = WebDriverWait(browser, w).until(EC.presence_of_element_located \
        ((By.XPATH,f'/html/body/div[8]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]/div[2]/div[2]/ul/li[{i}]/div/div[1]/div/h3/a')))


    elif WebDriverWait(browser, w).until(EC.presence_of_element_located \
        ((By.XPATH,f'/html/body/div[6]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]/div[2]/div/ul/li[{i}]/div/div[1]/div/h3/a'))):
        job_post = WebDriverWait(browser, w).until(EC.presence_of_element_located \
        ((By.XPATH,f'/html/body/div[6]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]/div[2]/div/ul/li[{i}]/div/div[1]/div/h3/a')))

    elif WebDriverWait(browser, w).until(EC.presence_of_element_located \
        ((By.XPATH,f'/html/body/div[6]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]/div[2]/div[2]/ul/li[{i}]/div/div[1]/div/h3/a'))):
        job_post = WebDriverWait(browser, w).until(EC.presence_of_element_located \
        ((By.XPATH,f'/html/body/div[6]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]/div[2]/div[2]/ul/li[{i}]/div/div[1]/div/h3/a')))


    elif WebDriverWait(browser, w).until(EC.presence_of_element_located \
        ((By.XPATH,f'/html/body/div[5]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]/div[2]/div/ul/li[{i}]/div/div[1]/div/h3/a'))):
        job_post = WebDriverWait(browser, w).until(EC.presence_of_element_located \
        ((By.XPATH,f'/html/body/div[5]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]/div[2]/div/ul/li[{i}]/div/div[1]/div/h3/a')))

    elif WebDriverWait(browser, w).until(EC.presence_of_element_located \
        ((By.XPATH,f'/html/body/div[5]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]/div[2]/div[2]/ul/li[{i}]/div/div[1]/div/h3/a'))):
        job_post = WebDriverWait(browser, w).until(EC.presence_of_element_located \
        ((By.XPATH,f'/html/body/div[5]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]/div[2]/div[2]/ul/li[{i}]/div/div[1]/div/h3/a')))


    return job_post


# number of pages with job posts considering job title given to thi
def n_pages_linkedin(browser, job_title_s, location):

    JOB_URL = f'https://www.linkedin.com/jobs/search/?keywords={job_title_s}&location={location}&start=0'
    browser.get(JOB_URL)

    # Total results
    results = WebDriverWait(browser, 1).until(EC.presence_of_element_located \
            ((By.XPATH,"//small[@class='display-flex t-12 t-black--light t-normal']"))).text
    print(f'    TOTAL RESULTS:{results}')
    results = int(results.split(" ")[0])

    if results > 25:
        pages = WebDriverWait(browser, 1).until(EC.presence_of_element_located \
                ((By.XPATH,"//ul[@class='artdeco-pagination__pages artdeco-pagination__pages--number']")))
        n_pages = int(pages.text.split('\n')[-1])
        return n_pages  # ,results

    else:
        n_pages = 1
        return n_pages  # ,results


def open_selenium(URL):

    ### SELENIUM DRIVER
    # LINUX
    if platform.system() == 'Linux':
        os.environ['PATH'] = f'{os.environ["PATH"]}:/home/cristopherrl/Documents/program/selenium/drivers/'

    elif platform.system() == 'Windows':
        os.environ['PATH'] = f'{os.environ["PATH"]};C:\\Users\\x385645\\Documents\\Selenium'

    ### SIGN IN - URL
    browser = webdriver.Chrome()
    browser.get(URL)

    return browser


def linkedin_session(browser):

    ### SEARCH INFORMATION
    print("""\n
    *********** NEW SEARCH :
    Please enter your information to sign in on LINKEDIN and begin the search >>>
    """)
    SECRET_USER = input("    EMAIL: ")
    SECRET_PASS = getpass.getpass("    PASSWORD: ")

    try:
        # user box
        user = browser.find_element_by_xpath('/html/body/div/main/div/form/div[1]/input')
        user.send_keys(SECRET_USER)
        time.sleep(0.5)

        # password box
        password = browser.find_element_by_xpath('/html/body/div/main/div/form/div[2]/input')
        password.send_keys(SECRET_PASS)
        time.sleep(0.5)

        # sign in button
        sign_in = browser.find_element_by_class_name('login__form_action_container')
        sign_in.click()
        time.sleep(0.5)

    except:
        raise ValueError("  WRONG INFORMATION GIVEN!!! Please close and try again ... ")

    time.sleep(0.5)

    return browser