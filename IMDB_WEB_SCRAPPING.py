# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import pandas as pd
# import time
# import re

# # Setup Chrome
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# driver.maximize_window()

# # Starting URL (all 2024 movies)
# url = "https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31"
# driver.get(url)

# # Data list
# all_movies = []

# while True:
#     try:
#         # Wait until movie containers are loaded
#         WebDriverWait(driver, 10).until(
#             EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item"))
#         )
        
#         movies = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")

#         for movie in movies:
#             try:
#                 titleName = movie.text.split("\n")[0]
#                 title = titleName.split(".")[1].strip()
#             except:
#                 title = ""

#             try:
#                 year_match = re.search(r'\b(\d{4})', movie.text)
#                 year = year_match.group(1) if year_match else ""

#                 # year = movie.find_element(By.CSS_SELECTOR, "span.ipc-metadata-list-summary-item__li").text
#             except:
#                 year = ""

#             try:
                
#                 durationValue=movie.text.split("\n")[1]
#                 durationTime = durationValue[4:]

#                 trimmed = durationTime

#                 # Extract up to and including the first 'm'
#                 match = re.search(r'^.*?m', trimmed)
#                 duration = match.group(0) if match else None


#                 # duration = movie.find_element(By.XPATH, ".//li[contains(text(),'h') or contains(text(),'m')]").text
#             except:
#                 duration = ""

#             try:
#                 rating = movie.find_element(By.CSS_SELECTOR, "span.ipc-rating-star").text
#             except:
#                 rating = ""

#             # Put into dictionary
#             all_movies.append({
#                 "Title": title,
#                 "Year": year,
#                 "Duration": duration,
#                 "Rating": rating
#             })

#         print(f"Scraped {len(all_movies)} movies so far...")

#         # Go to next page if exists
#         next_button = driver.find_elements(By.CSS_SELECTOR, "a.ipc-pagination__btn[aria-label='Next Page']")
#         if next_button:
#             next_button[0].click()
#             time.sleep(3)
#         else:
#             break

#     except Exception as e:
#         print("Error:", e)
#         break

# driver.quit()

# # Save to Excel
# df = pd.DataFrame(all_movies)
# df.to_excel("imdb_movies_2024.xlsx", index=False)
# print("✅ Saved imdb_movies_2024.xlsx")






# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.service import Service
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from webdriver_manager.chrome import ChromeDriverManager
# import pandas as pd
# import time
# import re

# # ---------- Helper to parse movie block ----------
# def parse_movie_block(block_text):
#     lines = block_text.strip().split("\n")
#     movie = {}

#     try:
#         movie["name"] = lines[0]
#     except:
#         movie["name"] = None

#     try:
#         year_dur = lines[1]
#         movie["year"] = year_dur[:4] if year_dur[:4].isdigit() else None
#         movie["duration"] = year_dur[4:].strip()
#     except:
#         movie["year"] = None
#         movie["duration"] = None

#     try:
#         rating_line = lines[2]
#         movie["rating"] = rating_line.strip()
#         if "(" in rating_line:
#             movie["votes"] = rating_line.split("(")[1].split(")")[0]
#         else:
#             movie["votes"] = None
#     except:
#         movie["rating"] = None
#         movie["votes"] = None

#     try:
#         movie["story"] = lines[-1]
#     except:
#         movie["story"] = None

#     return movie


# # ---------- Start Selenium ----------
# options = webdriver.ChromeOptions()
# options.add_argument("--start-maximized")
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# base_url = "https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31"
# driver.get(base_url)
# time.sleep(3)

# # Keep clicking "See more" until button disappears
# while True:
#     try:
#         see_more_btn = WebDriverWait(driver, 5).until(
#             EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ipc-see-more__button"))
#         )
#         driver.execute_script("arguments[0].click();", see_more_btn)
#         time.sleep(2)  # wait for new movies to load
#         print("🔽 Loaded more movies...")
#         break
#     except:
#         print("✅ No more 'See more' button found. All movies loaded.")
#         break

# # Now scrape all movies
# all_movies = []
# movie_blocks = driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")

# print(f"Total movies found: {len(movie_blocks)}")

# for movie in movie_blocks:
#     # movie = parse_movie_block(block.text)


#     try:
#         titleName = movie.text.split("\n")[0]
#         title = titleName.split(".")[1].strip()
#     except:
#         title = ""

#     try:
#         year_match = re.search(r'\b(\d{4})', movie.text)
#         year = year_match.group(1) if year_match else ""

#         # year = movie.find_element(By.CSS_SELECTOR, "span.ipc-metadata-list-summary-item__li").text
#     except:
#         year = ""

#     try:
        
#         durationValue=movie.text.split("\n")[1]
#         durationTime = durationValue[4:]

#         trimmed = durationTime

#         # Extract up to and including the first 'm'
#         match = re.search(r'^.*?m', trimmed)
#         duration = match.group(0) if match else None


#         # duration = movie.find_element(By.XPATH, ".//li[contains(text(),'h') or contains(text(),'m')]").text
#     except:
#         duration = ""

#     try:
#         rating = movie.find_element(By.CSS_SELECTOR, "span.ipc-rating-star").text
#     except:
#         rating = ""




#     all_movies.append(movie)

# # ---------- Save to Excel ----------
# df = pd.DataFrame(all_movies)
# df.to_excel("imdb_movies_2024.xlsx", index=False)

# driver.quit()
# print("🎉 All movies scraped and saved to imdb_movies_2024.xlsx")





from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import re
import os



genre_keywords = {
    "Thriller": ["threat", "murder", "detective", "haunted", "danger", "suspense"],
    "Drama": ["relationships", "emotional", "conflict", "identity", "outsiders"],
    "Comedy": ["funny", "hilarious", "laugh", "misfits", "play", "jokes"],
    "Horror": ["haunted", "ghost", "eerie", "terrifying", "nightmare"],
    "Romance": ["love", "romantic", "affair", "heart", "passion"],
    "Action": ["fight", "battle", "explosion", "chase", "war"]
}

def infer_genre(description):
    description = description.lower()
    matched_genres = []
    for genre, keywords in genre_keywords.items():
        if any(keyword in description for keyword in keywords):
            matched_genres.append(genre)
    return ", ".join(matched_genres) if matched_genres else "Unknown"


def extract_rating(rating_text):
    match = re.search(r"\b(\d\.\d)\b", rating_text)
    return float(match.group(1)) if match else None


# ---------- Helper to parse movie block ----------
def parse_movie_block(block):
    movie = {}
    try:
        titleName = block.text.split("\n")[0]
        movie["Movie"] = titleName.split(".")[1].strip()
    except:
        movie["Movie"] = ""

    try:
        year_match = re.search(r'\b(\d{4})', block.text)
        movie["Year"] = year_match.group(1) if year_match else ""
    except:
        movie["Year"] = ""

    try:
        durationValue = block.text.split("\n")[1]
        trimmed = durationValue[4:]
        match = re.search(r'^.*?m', trimmed)
        movie["Duration"] = match.group(0) if match else ""
    except:
        movie["Duration"] = ""

    try:
        last_line = block.strip().split('\n')[-1]
        sentences = re.split(r'(?<=[.!?])\s+', last_line)
        genre = infer_genre(sentences[-1] if sentences else last_line)
        movie["Genre"]  = genre
        
    except:
        movie["Genre"] =None
    try:
        movie["Rating"] = extract_rating(block)
    except:
        movie["Rating"] = None

    return movie


# ---------- Start Selenium ----------
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
# options.add_argument("--headless=new")  # uncomment for headless mode

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

base_url = "https://www.imdb.com/search/title/?title_type=feature&release_date=2024-01-01,2024-12-31"
driver.get(base_url)
time.sleep(3)

batch_size = 500   # movies per batch before saving
batch_num = 1
excel_file = "imdb_movies_2024.xlsx"

while True:
    try:
        # Click "See more" until we load batch_size movies
        while len(driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")) < batch_size:
            see_more_btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button.ipc-see-more__button"))
            )
            driver.execute_script("arguments[0].click();", see_more_btn)
            time.sleep(2)
    except:
        print("✅ No more 'See more' button found.")
        # even if < batch_size, process remaining
        pass

    # Extract current batch of movies
    movie_blocks =  driver.find_elements(By.CSS_SELECTOR, "li.ipc-metadata-list-summary-item")
    print(f"🎬 Extracting {len(movie_blocks)} movies from batch {batch_num}...")

    batch_movies = []
    for block in movie_blocks:
        batch_movies.append(parse_movie_block(block))

    # Save this batch to Excel (append if file exists)
    df = pd.DataFrame(batch_movies)

    if os.path.exists(excel_file):
        with pd.ExcelWriter(excel_file, mode="a", if_sheet_exists="overlay", engine="openpyxl") as writer:
            # Find the last row to start appending
            startrow = writer.sheets['Sheet1'].max_row
            df.to_excel(writer, index=False, header=False, startrow=startrow)
    else:
        df.to_excel(excel_file, index=False)

    print(f"💾 Appended batch {batch_num} ({len(df)} movies).")

    # Clear the DOM to free memory
    driver.execute_script(
        "document.querySelectorAll('li.ipc-metadata-list-summary-item').forEach(e => e.remove());"
    )

    batch_num += 1

    # If no "See more" exists anymore, break
    try:
        driver.find_element(By.CSS_SELECTOR, "button.ipc-see-more__button")
    except:
        break

driver.quit()
print("🎉 All movies scraped and saved into one Excel file!")