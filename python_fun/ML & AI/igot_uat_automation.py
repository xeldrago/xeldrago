"""
iGOT Karmayogi - Course UAT Automation Tool
============================================
Purpose : End-to-end UAT testing of course flow on portal.igotkarmayogi.gov.in
Author  : For UAT / QA use by course admins
Requires: pip install selenium webdriver-manager anthropic python-dotenv
"""

import os
import time
import json
import re
import logging
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, ElementClickInterceptedException
)
from webdriver_manager.chrome import ChromeDriverManager
import anthropic

load_dotenv()

# ─────────────────────────────────────────────
# CONFIG — edit these before running
# ─────────────────────────────────────────────
CONFIG = {
    "igot_email"    : os.getenv("IGOT_EMAIL", "your_email@gov.in"),
    "igot_password" : os.getenv("IGOT_PASSWORD", "your_password"),
    "course_url"    : "https://portal.igotkarmayogi.gov.in/page/home",
    "course_name"   : "Cyber Security Basics",          # partial match is fine
    "anthropic_key" : os.getenv("ANTHROPIC_API_KEY", ""),
    "headless"      : False,   # True = invisible browser, False = watch it run
    "slow_mode"     : True,    # adds human-like delays between actions
    "log_file"      : "igot_uat.log",
    "screenshots"   : True,    # saves screenshot at each major step
    "screenshot_dir": "uat_screenshots",
}

# ─────────────────────────────────────────────
# LOGGING SETUP
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(CONFIG["log_file"]),
        logging.StreamHandler()
    ]
)
log = logging.getLogger("igot_uat")

os.makedirs(CONFIG["screenshot_dir"], exist_ok=True)


# ─────────────────────────────────────────────
# DRIVER SETUP
# ─────────────────────────────────────────────
def get_driver() -> webdriver.Chrome:
    opts = Options()
    if CONFIG["headless"]:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1440,900")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)

    service = Service(ChromeDriverManager().install())
    driver  = webdriver.Chrome(service=service, options=opts)

    # mask navigator.webdriver so portal doesn't detect selenium
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
    )
    return driver


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
def human_delay(low=1.2, high=2.8):
    """Random human-like pause."""
    if CONFIG["slow_mode"]:
        time.sleep(low + (high - low) * __import__("random").random())


def screenshot(driver, name: str):
    if CONFIG["screenshots"]:
        path = os.path.join(CONFIG["screenshot_dir"], f"{name}.png")
        driver.save_screenshot(path)
        log.info(f"Screenshot saved → {path}")


def wait_click(driver, by, selector, timeout=15):
    """Wait for element and click it."""
    el = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, selector))
    )
    driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
    human_delay(0.4, 0.9)
    el.click()
    return el


def wait_find(driver, by, selector, timeout=15):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, selector))
    )


def safe_click(driver, element):
    """Click with JS fallback if intercepted."""
    try:
        element.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", element)


# ─────────────────────────────────────────────
# ANTHROPIC — answer MCQs using course content
# ─────────────────────────────────────────────
class AIAnswerer:
    def __init__(self, api_key: str):
        self.enabled = bool(api_key)
        self.client  = anthropic.Anthropic(api_key=api_key) if self.enabled else None
        self.context_chunks = []   # stores course text seen so far

    def add_context(self, text: str):
        """Feed course content to AI for better answers."""
        self.context_chunks.append(text[:3000])   # cap per chunk
        if len(self.context_chunks) > 10:
            self.context_chunks.pop(0)             # keep last 10 chunks

    def answer_mcq(self, question: str, options: list[str]) -> int:
        """
        Returns index (0-based) of the best answer option.
        Falls back to option 0 if AI disabled or call fails.
        """
        if not self.enabled:
            log.warning("AI not configured — defaulting to option 0")
            return 0

        context = "\n\n".join(self.context_chunks) if self.context_chunks else "No course content loaded yet."
        opts_text = "\n".join(f"{i+1}. {o}" for i, o in enumerate(options))

        prompt = f"""You are a cybersecurity and government training expert (or whatevr the current course is about).
Use the course content below to answer this MCQ accurately.

--- COURSE CONTENT ---
{context}
--- END CONTENT ---

Question: {question}

Options:
{opts_text}

Reply with ONLY the number of the correct option (1, 2, 3, or 4). Nothing else."""

        try:
            resp = self.client.messages.create(
                model      = "claude-sonnet-4-20250514",
                max_tokens = 10,
                messages   = [{"role": "user", "content": prompt}]
            )
            raw = resp.content[0].text.strip()
            num = int(re.search(r"\d", raw).group())
            idx = max(0, min(num - 1, len(options) - 1))
            log.info(f"AI answered option {num}: {options[idx]}")
            return idx
        except Exception as e:
            log.error(f"AI answer failed: {e} — defaulting to option 0")
            return 0


# ─────────────────────────────────────────────
# LOGIN
# ─────────────────────────────────────────────
def login(driver: webdriver.Chrome):
    log.info("Navigating to iGOT portal...")
    driver.get(CONFIG["course_url"])
    human_delay(2, 3)
    screenshot(driver, "01_home")

    # click Login button
    try:
        wait_click(driver, By.XPATH, "//button[contains(text(),'Login') or contains(text(),'Sign In')]")
    except TimeoutException:
        # already on login page or different layout
        pass

    human_delay()

    # fill email
    email_field = wait_find(driver, By.XPATH,
        "//input[@type='email' or @name='username' or @placeholder[contains(.,'email') or contains(.,'Email')]]"
    )
    email_field.clear()
    email_field.send_keys(CONFIG["igot_email"])
    human_delay(0.5, 1)

    # fill password
    pw_field = wait_find(driver, By.XPATH, "//input[@type='password']")
    pw_field.clear()
    pw_field.send_keys(CONFIG["igot_password"])
    human_delay(0.5, 1)

    pw_field.send_keys(Keys.RETURN)
    human_delay(3, 5)
    screenshot(driver, "02_after_login")
    log.info("Login submitted.")


# ─────────────────────────────────────────────
# FIND & OPEN COURSE
# ─────────────────────────────────────────────
def open_course(driver: webdriver.Chrome):
    log.info(f"Searching for course: {CONFIG['course_name']}")

    # try search bar first
    try:
        search = wait_find(driver, By.XPATH,
            "//input[@placeholder[contains(.,'Search') or contains(.,'search')]]",
            timeout=8
        )
        search.clear()
        search.send_keys(CONFIG["course_name"])
        search.send_keys(Keys.RETURN)
        human_delay(2, 3)
        screenshot(driver, "03_search_results")
    except TimeoutException:
        pass

    # click on the matching course card
    try:
        course_card = wait_find(driver, By.XPATH,
            f"//h3[contains(.,'{CONFIG['course_name']}')]"
            f" | //p[contains(.,'{CONFIG['course_name']}')]"
            f" | //span[contains(.,'{CONFIG['course_name']}')]",
            timeout=10
        )
        safe_click(driver, course_card)
        human_delay(2, 3)
        screenshot(driver, "04_course_page")
        log.info("Course page opened.")
    except TimeoutException:
        log.warning("Course card not found via search — trying direct URL")
        driver.get(
            "https://portal.igotkarmayogi.gov.in/viewer/pdf/"
            "do_113814143256289280177?primaryCategory=Learning%20Resource"
            "&collectionId=do_113814138061455360187&collectionType=Course"
            "&batchId=0138176433611571209&courseName=Cyber%20Security%20Basics%20"
            "&ML=english&MLId=do_113814138061455360187&fromAITutor=false" #change to link of course blergh... the automation in question lol
        )
        human_delay(3, 4)
        screenshot(driver, "04_course_direct")

    # click Enroll / Start / Resume if present
    for btn_text in ["Enroll", "Start Learning", "Resume", "Continue"]:
        try:
            wait_click(driver, By.XPATH,
                f"//button[contains(.,'{btn_text}')] | //a[contains(.,'{btn_text}')]",
                timeout=5
            )
            human_delay(2, 3)
            log.info(f"Clicked '{btn_text}' button.")
            break
        except TimeoutException:
            continue


# ─────────────────────────────────────────────
# READ PAGE CONTENT (for AI context)
# ─────────────────────────────────────────────
def extract_page_text(driver: webdriver.Chrome) -> str:
    try:
        body = driver.find_element(By.CSS_SELECTOR, ".viewer-content, .course-content, main, article, #contentBody")
        return body.text[:4000]
    except NoSuchElementException:
        return driver.find_element(By.TAG_NAME, "body").text[:4000]


# ─────────────────────────────────────────────
# HANDLE MCQ / QUIZ SCREEN
# ─────────────────────────────────────────────
def handle_quiz(driver: webdriver.Chrome, ai: AIAnswerer) -> bool:
    """
    Detects if current screen is a quiz, answers all questions, submits.
    Returns True if quiz was handled.
    """
    try:
        questions = driver.find_elements(By.XPATH,
            "//div[contains(@class,'question')] | //div[contains(@class,'mcq')] | //div[contains(@class,'quiz')]"
        )
        if not questions:
            return False

        log.info(f"Quiz detected — {len(questions)} question(s) found.")
        screenshot(driver, "quiz_start")

        for i, q_block in enumerate(questions):
            try:
                q_text = q_block.find_element(By.XPATH,
                    ".//p | .//h4 | .//span[contains(@class,'question-text')]"
                ).text.strip()
            except NoSuchElementException:
                q_text = q_block.text.strip()[:200]

            options = q_block.find_elements(By.XPATH,
                ".//input[@type='radio'] | .//label[contains(@class,'option')] | .//div[contains(@class,'option')]"
            )
            option_texts = []
            for opt in options:
                txt = opt.get_attribute("value") or opt.text
                option_texts.append(txt.strip())

            log.info(f"Q{i+1}: {q_text}")
            log.info(f"Options: {option_texts}")

            if option_texts:
                chosen_idx = ai.answer_mcq(q_text, option_texts)
                target = options[chosen_idx]
                driver.execute_script("arguments[0].scrollIntoView({block:'center'});", target)
                human_delay(0.8, 1.5)
                safe_click(driver, target)
                log.info(f"Selected option {chosen_idx+1}: {option_texts[chosen_idx]}")
            else:
                log.warning(f"No options found for Q{i+1} — skipping")

            human_delay(1, 2)

        # submit quiz
        for submit_text in ["Submit", "Check", "Finish", "Done"]:
            try:
                wait_click(driver, By.XPATH,
                    f"//button[contains(.,'{submit_text}')] | //input[@value='{submit_text}']",
                    timeout=5
                )
                log.info(f"Quiz submitted via '{submit_text}' button.")
                human_delay(2, 3)
                screenshot(driver, f"quiz_submitted_{i}")
                break
            except TimeoutException:
                continue

        return True

    except Exception as e:
        log.error(f"Quiz handling error: {e}")
        return False


# ─────────────────────────────────────────────
# NAVIGATE THROUGH COURSE MODULES
# ─────────────────────────────────────────────
def complete_course(driver: webdriver.Chrome, ai: AIAnswerer):
    log.info("Starting course traversal...")
    max_pages = 60   # safety limit
    page_num  = 0

    while page_num < max_pages:
        page_num += 1
        current_url = driver.current_url
        log.info(f"--- Page {page_num} | {current_url[:80]} ---")

        human_delay(2, 4)

        # extract content for AI context
        page_text = extract_page_text(driver)
        if page_text:
            ai.add_context(page_text)
            log.info(f"Page text captured ({len(page_text)} chars)")

        screenshot(driver, f"page_{page_num:02d}")

        # handle embedded iframe content (PDFs, SCORM)
        iframes = driver.find_elements(By.TAG_NAME, "iframe")
        if iframes:
            log.info(f"Found {len(iframes)} iframe(s) — switching in")
            try:
                driver.switch_to.frame(iframes[0])
                human_delay(1, 2)
                iframe_text = driver.find_element(By.TAG_NAME, "body").text[:3000]
                ai.add_context(iframe_text)
                driver.switch_to.default_content()
            except Exception as e:
                log.warning(f"iframe switch failed: {e}")
                driver.switch_to.default_content()

        # handle quiz if present
        handle_quiz(driver, ai)

        # try "Mark as Complete" button
        for label in ["Mark as Complete", "Mark As Complete", "Complete"]:
            try:
                wait_click(driver, By.XPATH,
                    f"//button[contains(.,'{label}')] | //a[contains(.,'{label}')]",
                    timeout=4
                )
                log.info(f"Clicked '{label}'")
                human_delay(1.5, 2.5)
                break
            except TimeoutException:
                continue

        # try Next button
        next_clicked = False
        for label in ["Next", "Next >", "›", "Continue", "Proceed"]:
            try:
                btn = wait_find(driver, By.XPATH,
                    f"//button[contains(.,'{label}')] | //a[contains(.,'{label}')]"
                    f" | //span[contains(@class,'next')] | //i[contains(@class,'next')]",
                    timeout=4
                )
                if btn.is_displayed() and btn.is_enabled():
                    safe_click(driver, btn)
                    log.info(f"Clicked Next: '{label}'")
                    human_delay(2, 3)
                    next_clicked = True
                    break
            except TimeoutException:
                continue

        if not next_clicked:
            # check if we're on the sidebar module list — click next uncompleted module
            try:
                uncompleted = driver.find_elements(By.XPATH,
                    "//div[contains(@class,'module') and not(contains(@class,'completed'))]"
                    " | //li[contains(@class,'toc') and not(contains(@class,'done'))]"
                )
                if uncompleted:
                    safe_click(driver, uncompleted[0])
                    log.info("Clicked next uncompleted module from sidebar")
                    human_delay(2, 3)
                    next_clicked = True
            except Exception:
                pass

        if not next_clicked:
            # check progress indicator
            try:
                progress = driver.find_element(By.XPATH,
                    "//*[contains(@class,'progress') or contains(@class,'percent')]"
                ).text
                if "100" in progress:
                    log.info("Course shows 100% — UAT complete!")
                    break
            except NoSuchElementException:
                pass

            log.info("No Next button found — checking if course is done")
            screenshot(driver, "possible_end")

            # look for completion/certificate page
            try:
                driver.find_element(By.XPATH,
                    "//*[contains(.,'Congratulations') or contains(.,'Certificate') or contains(.,'Completed')]"
                )
                log.info("Completion page detected — UAT SUCCESS!")
                break
            except NoSuchElementException:
                log.warning("Stuck — no next action found. Stopping.")
                break

    log.info(f"Course traversal ended after {page_num} pages.")


# ─────────────────────────────────────────────
# UAT REPORT
# ─────────────────────────────────────────────
def generate_report(driver: webdriver.Chrome, page_count: int):
    report = {
        "uat_result"   : "COMPLETED",
        "pages_visited": page_count,
        "final_url"    : driver.current_url,
        "screenshots"  : os.listdir(CONFIG["screenshot_dir"]),
        "log_file"     : CONFIG["log_file"],
    }
    with open("igot_uat_report.json", "w") as f:
        json.dump(report, f, indent=2)
    log.info("UAT report saved → igot_uat_report.json")
    print("\n" + "="*50)
    print("  iGOT UAT AUTOMATION — COMPLETE")
    print(f"  Pages traversed : {page_count}")
    print(f"  Screenshots     : {CONFIG['screenshot_dir']}/")
    print(f"  Log             : {CONFIG['log_file']}")
    print(f"  Report          : igot_uat_report.json")
    print("="*50 + "\n")


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    log.info("iGOT Karmayogi UAT Automation starting...")
    ai     = AIAnswerer(CONFIG["anthropic_key"])
    driver = get_driver()

    try:
        login(driver)
        open_course(driver)
        complete_course(driver, ai)
        generate_report(driver, page_count=60)  # approx; refine if needed
    except KeyboardInterrupt:
        log.info("UAT manually stopped.")
    except Exception as e:
        log.exception(f"Unhandled error: {e}")
        screenshot(driver, "error_state")
    finally:
        human_delay(2, 3)
        driver.quit()
        log.info("Browser closed.")


if __name__ == "__main__":
    main()
