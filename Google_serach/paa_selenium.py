import glob
import hashlib
import json
import os
import pathlib
import random
import re
import shutil
import time
import mysql.connector as mysql
import pysftp
import xlsxwriter

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

mode = input("[1] = Scrape or [2] = Upload: ")

if mode == "1":

    # how it works:
    # 1) - feed in a .txt file of keywords and loop them.
    # 2) - extract all questions & answers from the pages.
    # 3) - save all data to .xlxs & .json files.
    # 4) - skip the extraction if the .html file already exists as this means mode 2 has already run.

    def init_driver(using_linux, proxy):
        """ This function launches the chrome driver. """
        script_directory = pathlib.Path().absolute()
        try:
            options = Options()
            options.headless = False
            options.add_argument('start-maximized')
            options.add_argument('--disable-popup-blocking')
            options.add_argument('--disable-notifications')
            options.add_argument('--log-level=3')
            options.add_argument('--ignore-certificate-errors')
            options.add_argument('--ignore-ssl-errors')
            options.add_argument(f"user-data-dir={script_directory}\\profile")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            prefs = {'profile.default_content_setting_values.notifications': 2}
            options.add_experimental_option('prefs', prefs)

            if proxy == "0.0.0.0:00":
                print("--> PROXY DISABLED ...")
            else:
                print("--> PROXY: " + str(proxy) + " ...")
                options.add_argument('--proxy-server=%s' % proxy)

            if using_linux:
                return webdriver.Chrome(options=options)
            else:
                return webdriver.Chrome(options=options)
        except Exception as e:
            print(e)


    def google_search_url(_question):
        """ This function sets the Google URL. """
        base = "https://www.google.com/search?q="
        url = base + _question.lower().replace(" ", "+").replace("?", "%3F").replace("'", "%27")
        return url


    def click_on_questions(_driver, the_question, _total_clicks):
        """ This function will click on the questions' dropdown. """
        _driver.get(google_search_url(the_question))
        time.sleep(1)

        if _driver.find_elements(By.CSS_SELECTOR, 'div.related-question-pair'):
            questionIndex = 0
            all_questions = _driver.find_elements(By.CSS_SELECTOR, 'div.related-question-pair')
            actions = ActionChains(_driver)
            actions.move_to_element(all_questions[0]).perform()

            while questionIndex < _total_clicks:
                all_questions[questionIndex].click()
                time.sleep(1)
                all_questions = _driver.find_elements(By.CSS_SELECTOR, 'div.related-question-pair')
                actions = ActionChains(_driver)
                actions.move_to_element(all_questions[questionIndex + 1]).perform()
                questionIndex = questionIndex + 1

        return _driver


    def save_related_questions_for_further_scrapes(seed, related_question):
        """ This function will save related questions to file. """
        if not os.path.exists("output/related/related-[" + seed + "].txt"):
            open("output/related/related-[" + seed + "].txt", "w").close()

        with open("output/related/related-[" + seed + "].txt", "r+", encoding="utf-8", errors="ignore") as file:
            lines = [line.rstrip() for line in file.readlines()]
            if related_question.strip("?") in lines:
                print("[+] - DUPLICATE [ " + related_question.strip("?") + " ] ...")
            else:
                print("[+] - ADDING [ " + related_question.strip("?") + " ] ...")
                file.write(related_question.strip("?") + '\n')


    def extract_question_data(_soup, _seed):
        """ This function will extract all the data we need, this is the important one. """
        questionList = []

        dupe1 = None
        dupe2 = None

        for _question in _soup.findAll("div", class_="related-question-pair")[:total_clicks + 1]:

            questionDict = {'relatedQuestion': _question.find("div").find("div").text}

            dupe1 = _question.find("div").find("div").text

            if _question.find("h3"):
                questionDict['titleTag'] = _question.find("span").text
                questionDict['titleTagLength'] = len(questionDict['titleTag'])
            else:
                questionDict['titleTag'] = "N/A - ERROR?"
                questionDict['titleTagLength'] = "N/A - ERROR?"

            if _question.find("div", {"role": "heading"}):
                questionDict['answer'] = _question.find("div", {"role": "heading"}).text
                questionDict['answerLength'] = len(questionDict['answer'])
                dupe2 = _question.find("div", {"role": "heading"}).text
            else:
                try:
                    questionDict['answer'] = _question.find("div").findAll("div")[2].text
                    questionDict['answerLength'] = len(questionDict['answer'])
                    dupe2 = _question.find("div").findAll("div")[2].text
                except:
                    questionDict['answer'] = "N/A"
                    questionDict['answerLength'] = "N/A"

            if _question.find("a"):
                questionDict['questionUrl'] = _question.find("a")['href']
            else:
                questionDict['questionUrl'] = "N/A - ERROR"

            if questionDict['titleTag'] != 'N/A - ERROR?':
                questionDict['answer'].replace(questionDict['titleTag'], '')

                # this will not save pairs where the question/answer are the same.
                if dupe1 != dupe2:
                    questionList.append(questionDict)
                else:
                    print("[+] - " + dupe1 + " -> " + dupe2 + " DUPE!")

            save_related_questions_for_further_scrapes(_seed, _question.find("div").find("div").text)

            print("QUESTION: " + dupe1)
            print("ANSWER:" + dupe2)

        return questionList


    def clean_up_dates(answer):
        """ This function removes the dates from the strings. """
        date_pattern = re.search(r'\d{1,2}\s\w*\s\d{4}', answer)
        if date_pattern is not None and date_pattern != 'None':
            answer_cleaned = re.sub(r'\d{1,2}\s\w*\s\d{4}', '', answer)
            print("CLEANED: " + answer_cleaned)
            return answer_cleaned
        else:
            return answer


    def write_to_excel_file(all_data_extracted, seed_question):
        """ This function will create an Excel file. """
        workbook = xlsxwriter.Workbook("output/xlsx/seed-[" + seed_question + "].xlsx",
                                       {'strings_to_urls': True})
        worksheet01 = workbook.add_worksheet("Data")
        worksheet01.write(0, 0, "Initial Question")
        worksheet01.write(0, 1, "Related Question")
        worksheet01.write(0, 2, "Title Tag")
        worksheet01.write(0, 3, "Title Tag Length")
        worksheet01.write(0, 4, "Answer")
        worksheet01.write(0, 5, "Answer Length")
        worksheet01.write(0, 6, "Question URL")
        row = 1
        for questionData in all_data_extracted:
            for relatedQuestion in questionData['relatedQuestionData']:
                worksheet01.write(row, 0, questionData['initialQuestion'])
                worksheet01.write(row, 1, relatedQuestion['relatedQuestion'])
                worksheet01.write(row, 2, relatedQuestion['titleTag'])
                worksheet01.write(row, 3, relatedQuestion['titleTagLength'])
                worksheet01.write(row, 4, relatedQuestion['answer'])
                worksheet01.write(row, 5, relatedQuestion['answerLength'])
                worksheet01.write(row, 6, relatedQuestion['questionUrl'])
                row = row + 1
        workbook.close()


    def write_to_json_file(all_data_extracted, seed_question):
        """ This function will create the json files. """
        json_list = []  # you need a list to collect all dictionaries
        temp_list = []
        for questionData in all_data_extracted:
            for relatedQuestion in questionData['relatedQuestionData']:
                if questionData['initialQuestion'] not in temp_list:
                    json_list.append({
                        "seed": questionData['initialQuestion'],
                        "question": relatedQuestion['relatedQuestion'],
                        "answer": clean_up_dates(relatedQuestion['answer']),
                        "url": relatedQuestion['questionUrl']
                    })
            temp_list.append(questionData['initialQuestion'])

        with open("output/json/seed-[" + seed_question + "].json", "w") as file:
            json.dump(json_list, file, indent=4)


    def get_starting_keywords():
        """ This function will read a list of keywords into an array. """
        with open("seeds/keywords.txt", "r", encoding="utf8") as file:
            return [line.rstrip('\n') for line in file]


    def delete_seed_keyword_from_file(seed):
        print("[+] - SEED -> " + seed)
        with open("seeds/keywords.txt", "r") as input:
            lines = input.readlines()
        with open("seeds/keywords.txt", "w") as output:
            for line in lines:
                if seed not in line:
                    output.write(line)


    # seed questions.
    questions = get_starting_keywords()

    # the number of questions to click.
    total_clicks = 5

    # array.
    all_data = []

    # loop the data and save.
    for question in questions:

        if not os.path.isfile("output/html/seed-[" + question + "].html"):

            # create driver session.
            driver = init_driver(False, "0.0.0.0:00")

            # click on and expand the questions.
            driver = click_on_questions(driver, question, total_clicks)

            if driver.find_elements(By.CSS_SELECTOR, 'div.related-question-pair'):

                soup = BeautifulSoup(driver.page_source, "lxml")
                extractedData = extract_question_data(soup, question)
                currentQuestionDict = {'initialQuestion': question, 'relatedQuestionData': extractedData}
                all_data.append(currentQuestionDict)

                # quit once done.
                driver.quit()

                # write the data to excel.
                write_to_excel_file(all_data, question)

                # write the data to JSON.
                write_to_json_file(all_data, question)

                # delete the seed keyword from the "keywords.txt" file.
                delete_seed_keyword_from_file(question)

                # quit once done.
                driver.quit()

            else:
                # stop.
                print("No Questions Found For: " + question)

                # delete the seed keyword from the "keywords.txt" file.
                delete_seed_keyword_from_file(question)
        else:
            print("[+] - SKIPPING [ " + question + " ] ...")

    print("[+] - FINISHED! NO MORE KEYWORDS ...")

if mode == "2":

    # how it works:
    # 1) - loop the .json files.
    # 2) - if the .html version exists, do NOT process that .json file.

    IMAGES_FOLDER = 'rice-cookers'


    def write_to_html_file(file_name, html):
        """ This function will create the html file. """
        with open("output/html/" + file_name, "a", encoding="utf-8") as file:
            file.write(html)


    def process_json(old_location, new_location):
        shutil.move(old_location, new_location)


    def get_html_file_contents_to_send(file_name):
        """  This function will read the html file contents into a variable. """
        with open("output/html/" + file_name, "r", encoding="utf-8") as file:
            return file.read()


    def connect_and_insert_into_mysql(seed, html, urls):
        """ This function will upload the newly created post to the live server. """
        HOST = "209.250.228.223"  # or "domain.com"
        DATABASE = "admin_topricecookers.org"
        USER = "admin_archie"
        PASSWORD = "PDwSZRTXbw"
        db_connection = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)

        print("[+] - Connected to:", db_connection.get_server_info())

        # need an image.
        def upload_image(image_location, image_name_only):
            """ uploads image to the server. """
            try:
                cnopts = pysftp.CnOpts()
                cnopts.hostkeys = None
                with pysftp.Connection(host='209.250.228.223', username='root', password='%Dv3hste.G1b]Cko',
                                       cnopts=cnopts) as ftp:
                    with ftp.cd("/home/admin/web/topricecookers.org/public_html/uploads/"):
                        ftp.put(image_location, image_name_only)
                ftp.close()
            except Exception as e:
                print(e)

        def get_a_random_image_rename_it_and_upload_it(folder_location):
            random_image = random.choice(os.listdir(f"./photos/{folder_location}/"))
            random_rename = hashlib.sha256(random_image.encode('utf-8')).hexdigest()
            file_extension = os.path.splitext(random_image)[1]
            os.rename(f"./photos/{folder_location}/" + random_image,
                      f"./photos/{folder_location}/" + random_rename + file_extension)
            return random_rename + file_extension

        def delete_image(random_image_full_location):
            return os.remove(random_image_full_location)

        random_image = get_a_random_image_rename_it_and_upload_it(IMAGES_FOLDER)
        upload_image(f"./photos/rice-cookers/" + random_image, random_image)
        delete_image(f"./photos/rice-cookers/" + random_image)

        cursor = db_connection.cursor(buffered=True, dictionary=True)

        fix = seed.title().replace("'", "\\'")

        dupe = f"SELECT * FROM posts WHERE post_title='{fix}' LIMIT 1"
        print(f"[+] - SELECT * FROM posts WHERE post_title='{fix}'")

        cursor.execute(dupe)

        print("[+] - " + str(cursor.rowcount))

        if cursor.rowcount < 1:
            sql = "INSERT INTO posts (post_category_id, " \
                  "post_member_id, " \
                  "post_title, " \
                  "post_body, " \
                  "post_seo_title, " \
                  "post_seo_description, " \
                  "post_image, " \
                  "post_image_alt_text, " \
                  "post_status, " \
                  "post_source_url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            val = (16, 2, seed.title(), html, seed.title(), seed.title(), random_image, seed.title(), "published",
                   json.dumps(urls))

            cursor.execute(sql, val)
            db_connection.commit()
            db_connection.close()

            print("[+] - %d row(s) were inserted" % cursor.rowcount)


    counter = 0

    for filename in os.listdir("output/json/"):
        """ Entry point. """
        if filename.endswith(".json"):

            print("[+] - UPLOADING ...")
            print("[+] - " + filename)

            filename_without_ext = os.path.splitext(filename)[0]

            # if the html file exists no need to add it again to the server (ignore).
            # print(os.path.isfile("output/json/" + filename_without_ext + ".json"))
            # print(os.path.isfile("output/html/" + filename_without_ext + ".html"))
            print(os.path.isfile("output/json/" + filename_without_ext + ".json"))
            print(os.path.isfile("output/html/" + filename_without_ext + ".html"))

            with open("output/json/" + filename_without_ext + ".json", "r", encoding="utf-8") as json_file:
                json_file = json.load(json_file)

                temp = []
                urls = []
                for json_data in json_file:
                    temp.append(json_data['question'] + "|" + json_data['answer'])
                    urls.append(json_data['url'])

                de_duped = list(dict.fromkeys(temp))

                for html_ready in de_duped:
                    ready = html_ready.split("|")
                    write_to_html_file(filename_without_ext + "].html",
                                       "<h2>" + ready[0] + "</h2><p>" + ready[1] + "</p>")

                    # print(json_data['question'])

                    write_to_html_file("seed-[" + json_data['seed'] + "].html",
                                       "<h2>" + json_data['question'] + "</h2>")
                    write_to_html_file("seed-[" + json_data['seed'] + "].html",
                                       "<p>" + json_data['answer'] + "</p>")

                connect_and_insert_into_mysql(json_data['seed'],
                                              get_html_file_contents_to_send(filename_without_ext + "].html"), urls)

                counter = counter + 1

                print("[+] - POSTED!")

            process_json("output/json/" + filename_without_ext + ".json",
                         "output/processed/" + filename_without_ext + ".json")

    print("[+] - FINISHED [ " + str(counter) + " ] POSTS UPLOADED...")

if mode == "3":
    print("[+] - SANDBOX - [+]")

    # def upload_image(image_location, image_name_only):
    #     """ uploads image to the server. """
    #     try:
    #         cnopts = pysftp.CnOpts()
    #         cnopts.hostkeys = None
    #         with pysftp.Connection(host='209.250.228.223', username='root', password='%Dv3hste.G1b]Cko',
    #                                cnopts=cnopts) as ftp:
    #             with ftp.cd("/home/admin/web/topricecookers.org/public_html/uploads/"):
    #                 ftp.put(image_location, image_name_only)
    #         ftp.close()
    #     except Exception as e:
    #         print("ERROR: " + e)
    #
    # def get_a_random_image_rename_it_and_upload_it(folder_location):
    #     random_image = random.choice(os.listdir(f"./photos/{folder_location}/"))
    #     random_rename = hashlib.sha256(random_image.encode('utf-8')).hexdigest()
    #     file_extension = os.path.splitext(random_image)[1]
    #     os.rename(f"./photos/{folder_location}/" + random_image, f"./photos/{folder_location}/" + random_rename + file_extension)
    #
    #
    # get_a_random_image_rename_it_and_upload_it("rice-cookers")

    # upload_image("photos/387cb56f4-25a5-4822-b433-3f8d012d7ed5.jpg", "387cb56f4-25a5-4822-b433-3f8d012d7ed5.jpg")

    # def downloadimages(search_term, resolution, amount):  # Define the function to download images
    #     print(f"https://source.unsplash.com/random/{resolution}/?" + str(
    #         search_term) + ", allow_redirects=True")  # State the URL
    #
    #     for x in range(int(amount)):  # Loop for chosen amount of times
    #         response = requests.get(f"https://source.unsplash.com/random/{resolution}/?" + str(
    #             search_term) + ", allow_redirects=True")  # Download the photo(s)
    #         print("Saving to: ./photos/" + str(search_term) + "_" + str(x + 1) + ".png")  # State the filename
    #         open("./photos/" + str(search_term) + "_" + str(x + 1) + ".png", 'wb').write(
    #             response.content)  # Write image file
    #
    #
    # downloadimages("rice-cooker", "1080x1920", 15)  # Call the Function

if mode == "4":
    print("[+] - SANDBOX - ParaPhrasing [+]")

    # def get_paraphrased_sentences(model, tokenizer, sentence, num_return_sequences=5, num_beams=5):
    #     # tokenize the text to be form of a list of token IDs
    #     inputs = tokenizer([sentence], truncation=True, padding="longest", return_tensors="pt")
    #     # generate the paraphrased sentences
    #     outputs = model.generate(
    #         **inputs,
    #         num_beams=num_beams,
    #         num_return_sequences=num_return_sequences,
    #     )
    #     # decode the generated sentences using the tokenizer to get them back to text
    #     return tokenizer.batch_decode(outputs, skip_special_tokens=True)
    #
    # model = PegasusForConditionalGeneration.from_pretrained("tuner007/pegasus_paraphrase")
    # tokenizer = PegasusTokenizerFast.from_pretrained("tuner007/pegasus_paraphrase")
    # sentence = "Learning is the process of acquiring new understanding, knowledge, behaviors, skills, values, attitudes, and preferences."
    # get_paraphrased_sentences(model, tokenizer, sentence, num_beams=10, num_return_sequences=10)

if mode == "5":

    os.chdir(r"C:\Users\Graham\Desktop\files\programming\Languages\Python\paa_selenium\output\related")
    files = glob.glob("*.txt")

    with open('keywords.txt', 'a') as result:
        for file_ in files:
            for line in open(file_, 'r'):
                result.write(line)

    print("[+] - DONE!")

    # with open("seeds/keywords.txt", "a") as outfile:
    #     for f in files:
    #         print(f)
    #         with open(f, "r") as infile:
    #             outfile.write(infile.read())
