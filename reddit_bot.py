import os
import random
import time
import json
import undetected_chromedriver as uc
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


# Load environment variables from .env file
load_dotenv()

class RedditBot:
    def __init__(self):
        # Initialize Undetected ChromeDriver
        options = uc.ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        self.driver = uc.Chrome(options=options)
        
        # Load credentials and paths from environment variables
        self.username = os.getenv("REDDIT_USERNAME")
        self.password = os.getenv("REDDIT_PASSWORD")
        self.image_folder = os.getenv("IMAGE_FOLDER")
        self.comments_file = os.getenv("COMMENTS_FILE")
        self.titles_file = os.getenv("TITLES_FILE")
        self.target_post_url = os.getenv("TARGET_POST_URL")
        
        # Load image titles
        self.image_titles = self.load_image_titles()

    def load_image_titles(self):
        """Load image titles from JSON file"""
        try:
            with open(self.titles_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            # Create default mapping if file doesn't exist
            return {f: f"Default Title for {f}" for f in os.listdir(self.image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))}

    def login(self):
        """Login to Reddit"""
        self.driver.get('https://www.reddit.com/login/')
        
        # Wait for and fill username
        username_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )
        username_field.send_keys(self.username)
        
        # Fill password and submit
        password_field = self.driver.find_element(By.NAME, 'password')
        password_field.send_keys(self.password)
        password_field.send_keys(Keys.RETURN)
        
        time.sleep(3)

    def load_comments(self):
        """Load comments from comments.txt"""
        try:
            with open(self.comments_file, 'r') as f:
                return [line.strip() for line in f.readlines() if line.strip()]
        except FileNotFoundError:
            print(f"Error: The file {self.comments_file} does not exist.")
            return []

    def select_random_image(self):
        """Select a random image and its corresponding title"""
        images = [f for f in os.listdir(self.image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))]
        if not images:
            raise FileNotFoundError(f"No images found in the folder {self.image_folder}.")
        image = random.choice(images)
        title = self.image_titles.get(image, f"Default Title for {image}")
        return os.path.join(self.image_folder, image), title

    def create_post(self, subreddit='memes'):
        """Create a post in a specific subreddit"""
        self.driver.get(f'https://www.reddit.com/submit?type=IMAGE')
        image_path, post_title = self.select_random_image()
        
        # Fill title
        title_field = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'title'))
        )
        self.driver.execute_script("arguments[0].scrollIntoView(true);", title_field)
        title_field.click()
        title_field.send_keys(post_title)
        
        # Upload image
        upload_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "svg[icon-name='upload-outline']"))
        )
        actions = ActionChains(self.driver)
        actions.move_to_element(upload_button).click().perform()
        file_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
        )
        file_input.send_keys(os.path.abspath(image_path))
        
        # Submit post
        time.sleep(3)
        submit_button = self.driver.find_element(By.XPATH, "//button[contains(text(), 'Post')]")
        submit_button.click()
        time.sleep(5)
        return self.driver.current_url

    def post_comment(self, post_url):
        """Post a random comment on a specific post"""
        
        # Navigate to the target post URL
        self.driver.get(post_url)
        
        # Wait for the comment box to be present and clickable
        comment_box = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@contenteditable='true' and @aria-placeholder='Add a comment']"))
        )
        
        # Click the div to focus on it
        comment_box.click()

        # Load comments from the file
        comments = self.load_comments()
        if not comments:
            print("No comments found in comments.txt.")
            return

        # Select a random comment
        comment_text = random.choice(comments)

        # Insert the comment into the comment box
        comment_box.send_keys(comment_text)

        # Wait for the comment button to be clickable
        comment_button = WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[span[text()='Comment']]"))
        )

        # Click the comment button to submit the comment
        comment_button.click()

    def run(self):
        """Main bot execution method"""
        try:
            self.login()
            self.post_comment(self.target_post_url)
            post_url = self.create_post()
            print(f"Post created: {post_url}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            self.driver.quit()

# Run the bot
if __name__ == "__main__":
    bot = RedditBot()
    bot.run()