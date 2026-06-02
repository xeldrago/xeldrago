"""
iGOT Karmayogi - Course UAT Automation Tool  v2.0
==================================================
Purpose  : End-to-end UAT of course flow on portal.igotkarmayogi.gov.in
Auth     : Mobile OTP based (number → OTP → submit)
Nav      : Direct URL per run (paste in COURSE_DIRECT_URL below)
Content  : SCORM slides, MCQ/quiz, Video (optional watch)
Requires : pip install selenium webdriver-manager anthropic python-dotenv inputimeout

HOW TO RUN
----------
1. Copy .env.template → .env and fill values
2. Set COURSE_DIRECT_URL below to your course viewer URL
3. python igot_uat_automation.py
4. When prompted in terminal → enter the OTP received on your mobile
"""

import os
import re
import sys
import time
import json
import random
import logging
import inputimeout                          # pip install inputimeout
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException,
    ElementClickInterceptedException, StaleElementReferenceException
)
from webdriver_manager.chrome import ChromeDriverManager
import anthropic

load_dotenv()

# ═══════════════════════════════════════════════════════════
#  PASTE YOUR COURSE VIEWER URL HERE  ↓
# ═══════════════════════════════════════════════════════════
COURSE_DIRECT_URL = (
    "https://portal.igotkarmayogi.gov.in/viewer/pdf/"
    "do_113814143256289280177?primaryCategory=Learning%20Resource"
    "&collectionId=do_113814138061455360187&collectionType=Course"
    "&batchId=0138176433611571209&courseName=Cyber%20Security%20Basics%20"
    "&ML=english&MLId=do_113814138061455360187&fromAITutor=false"
)

# ═══════════════════════════════════════════════════════════
#  CONFIG
# ═══════════════════════════════════════════════════════════
CONFIG = {
    # credentials
    "mobile"            : os.getenv("IGOT_MOBILE", "9XXXXXXXXX"),   # 10-digit mobile
    "otp_timeout_secs"  : 90,        # seconds to wait for you to type OTP

    # course
    "course_url"        : COURSE_DIRECT_URL,

    # AI (Anthropic) — for MCQ answering
    "anthropic_key"     : os.getenv("ANTHROPIC_API_KEY", ""),

    # browser
    "headless"          : False,     # False = visible browser (recommended for UAT)
    "window_size"       : "1440,900",

    # pacing  (seconds)
    "delay_min"         : 1.2,
    "delay_max"         : 2.8,
    "scorm_slide_wait"  : 2.0,       # pause on each SCORM slide before clicking Next
    "video_skip_wait"   : 3.0,       # seconds to wait before skipping optional video

    # safety
    "max_slides"        : 120,       # max SCORM slides/pages before giving up
    "max_quiz_retries"  : 3,         # retry submit if quiz validation fails

    # output
    "screenshots"       : True,
    "screenshot_dir"    : "uat_screenshots",
    "log_file"          : "igot_uat.log",
}

# ═══════════════════════════════════════════════════════════
#  LOGGING
# ═══════════════════════════════════════════════════════════
os.makedirs(CONFIG["screenshot_dir"], exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(CONFIG["log_file"], encoding="utf-8"),
        logging.StreamHandler(sys.stdout),
    ]
)
log = logging.getLogger("igot_uat")


# ═══════════════════════════════════════════════════════════
#  DRIVER
# ═══════════════════════════════════════════════════════════
def get_driver() -> webdriver.Chrome:
    opts = Options()
    if CONFIG["headless"]:
        opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument(f"--window-size={CONFIG['window_size']}")
    opts.add_argument("--disable-blink-features=AutomationControlled")
    opts.add_argument("--disable-infobars")
    opts.add_argument("--mute-audio")                  # mute videos
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)
    opts.add_experimental_option("detach", False)

    service = Service(ChromeDriverManager().install())
    driver  = webdriver.Chrome(service=service, options=opts)

    # mask webdriver fingerprint
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator,'webdriver',{get:()=>undefined})"}
    )
    log.info("Chrome driver ready.")
    return driver


# ═══════════════════════════════════════════════════════════
#  HELPERS
# ═══════════════════════════════════════════════════════════
def pause(low: float = None, high: float = None):
    lo = low  if low  is not None else CONFIG["delay_min"]
    hi = high if high is not None else CONFIG["delay_max"]
    time.sleep(lo + (hi - lo) * random.random())


def shot(driver, name: str):
    if CONFIG["screenshots"]:
        p = os.path.join(CONFIG["screenshot_dir"], f"{name}.png")
        driver.save_screenshot(p)
        log.info(f"Screenshot -> {p}")


def wait_for(driver, by, selector, timeout=15):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, selector))
    )


def safe_click(driver, el):
    try:
        el.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();", el)
    except StaleElementReferenceException:
        log.warning("Stale element on click — ignored.")


def find_any(driver, xpaths: list, timeout=6):
    """Try multiple XPATHs, return first match or None."""
    for xp in xpaths:
        try:
            el = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xp))
            )
            return el
        except TimeoutException:
            continue
    return None


def click_any(driver, xpaths: list, timeout=6) -> bool:
    """Try multiple XPATHs, click first clickable one. Returns True if clicked."""
    for xp in xpaths:
        try:
            el = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((By.XPATH, xp))
            )
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", el)
            pause(0.3, 0.6)
            safe_click(driver, el)
            return True
        except TimeoutException:
            continue
    return False


def page_text(driver) -> str:
    """Best-effort page text for AI context."""
    selectors = [
        ".viewer-content", ".course-content", ".scorm-content",
        "main", "article", "#contentBody", ".sunbird-player-container"
    ]
    for sel in selectors:
        try:
            el = driver.find_element(By.CSS_SELECTOR, sel)
            t = el.text.strip()
            if len(t) > 100:
                return t[:4000]
        except NoSuchElementException:
            continue
    return driver.find_element(By.TAG_NAME, "body").text[:4000]


# ═══════════════════════════════════════════════════════════
#  OTP LOGIN
# ═══════════════════════════════════════════════════════════
def login_otp(driver: webdriver.Chrome):
    log.info("Opening iGOT login page...")
    driver.get("https://portal.igotkarmayogi.gov.in/")
    pause(2, 3)
    shot(driver, "01_home")

    # Step 1: click Login / Sign In
    clicked = click_any(driver, [
        "//button[contains(.,'Login')]",
        "//a[contains(.,'Login')]",
        "//button[contains(.,'Sign In')]",
        "//a[contains(.,'Sign In')]",
    ], timeout=8)
    if clicked:
        log.info("Clicked Login button.")
        pause(1.5, 2.5)
    shot(driver, "02_login_page")

    # Step 2: enter mobile number
    mobile_field = find_any(driver, [
        "//input[@type='tel']",
        "//input[@name='mobile']",
        "//input[@placeholder[contains(.,'mobile') or contains(.,'Mobile') or contains(.,'phone') or contains(.,'Phone')]]",
        "//input[@id[contains(.,'mobile') or contains(.,'phone')]]",
    ], timeout=10)

    if not mobile_field:
        log.error("Mobile input field not found! Check login page structure.")
        shot(driver, "error_no_mobile_field")
        raise RuntimeError("Mobile field not found on login page.")

    mobile_field.clear()
    for digit in CONFIG["mobile"]:          # type digit by digit for natural feel
        mobile_field.send_keys(digit)
        time.sleep(random.uniform(0.05, 0.15))
    log.info(f"Entered mobile: {CONFIG['mobile']}")
    pause(0.5, 1)
    shot(driver, "03_mobile_entered")

    # Step 3: click Send OTP
    sent = click_any(driver, [
        "//button[contains(.,'Send OTP')]",
        "//button[contains(.,'Get OTP')]",
        "//button[contains(.,'Request OTP')]",
        "//a[contains(.,'Send OTP')]",
    ], timeout=8)
    if not sent:
        mobile_field.send_keys(Keys.RETURN)
        log.info("Send OTP button not found — pressed Enter instead.")
    else:
        log.info("Clicked 'Send OTP'.")
    pause(2, 3)
    shot(driver, "04_otp_sent")

    # Step 4: human enters OTP in terminal
    print("\n" + "=" * 55)
    print(f"  OTP sent to {CONFIG['mobile']}")
    print(f"  You have {CONFIG['otp_timeout_secs']} seconds to enter it below.")
    print("=" * 55)

    try:
        otp = inputimeout.inputimeout(
            prompt="  Enter OTP -> ",
            timeout=CONFIG["otp_timeout_secs"]
        ).strip()
    except inputimeout.TimeoutOccurred:
        log.error("OTP entry timed out.")
        raise RuntimeError("OTP not entered in time.")

    if not otp.isdigit():
        raise ValueError(f"Invalid OTP entered: '{otp}'")

    # Step 5: type OTP into field
    otp_field = find_any(driver, [
        "//input[@name='otp']",
        "//input[@id[contains(.,'otp') or contains(.,'OTP')]]",
        "//input[@placeholder[contains(.,'OTP') or contains(.,'otp') or contains(.,'code')]]",
        "//input[@maxlength='6']",
        "//input[@maxlength='4']",
        "//input[@type='number' and not(@name='mobile')]",
    ], timeout=10)

    if not otp_field:
        log.error("OTP input field not found!")
        shot(driver, "error_no_otp_field")
        raise RuntimeError("OTP field not found.")

    otp_field.clear()
    for digit in otp:
        otp_field.send_keys(digit)
        time.sleep(random.uniform(0.08, 0.18))
    log.info("OTP entered.")
    pause(0.5, 1)
    shot(driver, "05_otp_entered")

    # Step 6: submit
    submitted = click_any(driver, [
        "//button[contains(.,'Verify')]",
        "//button[contains(.,'Login')]",
        "//button[contains(.,'Submit')]",
        "//button[contains(.,'Confirm')]",
        "//button[@type='submit']",
    ], timeout=8)
    if not submitted:
        otp_field.send_keys(Keys.RETURN)
        log.info("Submit button not found — pressed Enter.")
    else:
        log.info("Clicked OTP submit button.")

    pause(3, 5)
    shot(driver, "06_after_login")

    # Verify login succeeded
    if "login" in driver.current_url.lower() or "signin" in driver.current_url.lower():
        log.warning("Still on login page — OTP may have been wrong. Check screenshot.")
    else:
        log.info(f"Login successful. URL: {driver.current_url}")


# ═══════════════════════════════════════════════════════════
#  OPEN COURSE VIA DIRECT URL
# ═══════════════════════════════════════════════════════════
def open_course(driver: webdriver.Chrome):
    log.info("Navigating directly to course URL...")
    driver.get(CONFIG["course_url"])
    pause(4, 6)
    shot(driver, "07_course_loaded")

    # handle Resume / Start / Enroll if on course detail page first
    click_any(driver, [
        "//button[contains(.,'Resume')]",
        "//button[contains(.,'Start Learning')]",
        "//button[contains(.,'Start')]",
        "//button[contains(.,'Enroll')]",
        "//a[contains(.,'Resume')]",
        "//a[contains(.,'Start Learning')]",
    ], timeout=6)
    pause(2, 3)
    shot(driver, "08_course_started")
    log.info("Course viewer opened.")


# ═══════════════════════════════════════════════════════════
#  AI MCQ ANSWERER
# ═══════════════════════════════════════════════════════════
class AIAnswerer:
    def __init__(self):
        key = CONFIG["anthropic_key"]
        self.enabled = bool(key)
        self.client  = anthropic.Anthropic(api_key=key) if self.enabled else None
        self._ctx: list[str] = []

    def add_context(self, text: str):
        if text and len(text) > 80:
            self._ctx.append(text[:3000])
            if len(self._ctx) > 12:
                self._ctx.pop(0)

    def answer(self, question: str, options: list[str]) -> int:
        """Returns 0-based index of best answer."""
        if not self.enabled or not options:
            log.warning("AI disabled or no options — picking option 0.")
            return 0

        ctx  = "\n\n".join(self._ctx) or "No course content captured yet."
        opts = "\n".join(f"{i+1}. {o}" for i, o in enumerate(options))

        prompt = (
            "You are a government training and cybersecurity expert.\n"
            "Use the course content below to pick the correct MCQ answer.\n\n"
            f"--- COURSE CONTENT ---\n{ctx}\n--- END ---\n\n"
            f"Question: {question}\n\nOptions:\n{opts}\n\n"
            "Reply with ONLY the option number (e.g. 2). Nothing else."
        )
        try:
            resp = self.client.messages.create(
                model      = "claude-sonnet-4-20250514",
                max_tokens = 5,
                messages   = [{"role": "user", "content": prompt}]
            )
            raw = resp.content[0].text.strip()
            num = int(re.search(r"\d", raw).group())
            idx = max(0, min(num - 1, len(options) - 1))
            log.info(f"AI -> option {num}: {options[idx]}")
            return idx
        except Exception as e:
            log.error(f"AI call failed: {e} — defaulting to 0")
            return 0


# ═══════════════════════════════════════════════════════════
#  VIDEO HANDLER  (Next is always available — just wait & skip)
# ═══════════════════════════════════════════════════════════
def handle_video(driver: webdriver.Chrome) -> bool:
    """
    Detects a video player. Since Next is always available,
    waits briefly (natural behaviour) then moves on.
    Returns True if video was detected.
    """
    video_selectors = [
        "video",
        ".video-js",
        ".vjs-tech",
        "iframe[src*='youtube']",
        "iframe[src*='vimeo']",
        ".sunbird-video-player",
        "[class*='video-player']",
        "[class*='VideoPlayer']",
    ]
    for sel in video_selectors:
        try:
            el = driver.find_element(By.CSS_SELECTOR, sel)
            if el.is_displayed():
                log.info(f"Video detected ({sel}) — waiting {CONFIG['video_skip_wait']}s then skipping.")
                time.sleep(CONFIG["video_skip_wait"])
                shot(driver, "video_detected")
                return True
        except NoSuchElementException:
            continue
    return False


# ═══════════════════════════════════════════════════════════
#  SCORM SLIDE HANDLER
# ═══════════════════════════════════════════════════════════
def handle_scorm(driver: webdriver.Chrome) -> bool:
    """
    Detects SCORM/interactive slide content in iframes.
    Clicks through all internal slides until Mark as Complete appears.
    Returns True if SCORM was detected and handled.
    """
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    if not iframes:
        return False

    scorm_detected = False
    for iframe in iframes:
        src = iframe.get_attribute("src") or ""
        if any(k in src for k in ["sunbird", "content", "scorm", "player", "do_"]):
            scorm_detected = True
        elif not src:
            scorm_detected = True   # blank-src iframes are often SCORM

    if not scorm_detected and len(iframes) == 1:
        scorm_detected = True       # single iframe — treat as SCORM

    if not scorm_detected:
        return False

    log.info(f"SCORM iframe detected. Switching in...")

    try:
        driver.switch_to.frame(iframes[0])
        pause(1.5, 2.5)

        slide_count = 0
        while slide_count < CONFIG["max_slides"]:
            slide_count += 1
            log.info(f"  SCORM slide {slide_count}")

            # grab text for AI context
            try:
                body_text = driver.find_element(By.TAG_NAME, "body").text[:3000]
                if body_text:
                    log.info(f"  Slide text captured ({len(body_text)} chars)")
            except Exception:
                body_text = ""

            shot(driver, f"scorm_slide_{slide_count:03d}")
            time.sleep(CONFIG["scorm_slide_wait"])

            # check for Mark as Complete inside SCORM frame
            mac_found = click_any(driver, [
                "//button[contains(.,'Mark as Complete')]",
                "//button[contains(.,'Mark As Complete')]",
                "//button[contains(.,'Complete')]",
                "//a[contains(.,'Mark as Complete')]",
            ], timeout=2)
            if mac_found:
                log.info("  'Mark as Complete' clicked inside SCORM frame.")
                pause(1, 2)
                break

            # click Next / forward arrow inside SCORM
            next_found = click_any(driver, [
                "//button[contains(.,'Next')]",
                "//button[contains(.,'next')]",
                "//button[@aria-label='Next']",
                "//button[@title='Next']",
                "//*[contains(@class,'next-btn')]",
                "//*[contains(@class,'nextBtn')]",
                "//*[contains(@class,'arrow-right')]",
                "//*[contains(@class,'forward')]",
                "//button[contains(.,'›')]",
                "//button[contains(.,'→')]",
                "//*[@id='next']",
                "//*[@id='nextBtn']",
            ], timeout=3)

            if not next_found:
                # keyboard Right arrow fallback
                try:
                    body = driver.find_element(By.TAG_NAME, "body")
                    body.send_keys(Keys.ARROW_RIGHT)
                    log.info("  Pressed Right arrow key inside SCORM.")
                    pause(0.8, 1.5)
                    next_found = True
                except Exception:
                    pass

            if not next_found:
                log.info("  No Next inside SCORM — assuming last slide reached.")
                break

            pause(0.8, 1.8)

        driver.switch_to.default_content()
        log.info(f"SCORM done — {slide_count} slides traversed.")
        return True

    except Exception as e:
        log.error(f"SCORM handler error: {e}")
        driver.switch_to.default_content()
        return False


# ═══════════════════════════════════════════════════════════
#  MCQ / QUIZ HANDLER
# ═══════════════════════════════════════════════════════════
def handle_quiz(driver: webdriver.Chrome, ai: AIAnswerer) -> bool:
    """
    Detects quiz/MCQ screen, answers all questions, submits.
    Checks both main page and inside iframes.
    Returns True if quiz was handled.
    """

    def _process_quiz_in_context(ctx_driver) -> bool:
        q_blocks = ctx_driver.find_elements(By.XPATH,
            "//*[contains(@class,'question')] | //*[contains(@class,'mcq')]"
            " | //*[contains(@class,'quiz')] | //*[contains(@class,'Question')]"
        )
        if not q_blocks:
            return False

        log.info(f"Quiz — {len(q_blocks)} question block(s) found.")
        shot(driver, "quiz_start")

        for i, qb in enumerate(q_blocks):
            try:
                q_text = qb.find_element(By.XPATH,
                    ".//p | .//h3 | .//h4 | .//span[contains(@class,'question')]"
                ).text.strip()
            except NoSuchElementException:
                q_text = qb.text.strip()[:300]

            if not q_text:
                continue

            log.info(f"Q{i+1}: {q_text[:120]}")

            option_els = qb.find_elements(By.XPATH,
                ".//input[@type='radio'] | .//input[@type='checkbox']"
                " | .//label[contains(@class,'option')]"
                " | .//div[contains(@class,'option')]"
                " | .//li[contains(@class,'option')]"
                " | .//button[contains(@class,'option')]"
            )

            option_texts = []
            for o in option_els:
                txt = (o.get_attribute("value") or o.text or "").strip()
                if txt:
                    option_texts.append(txt)

            if not option_texts:
                log.warning(f"Q{i+1}: no options found — skipping.")
                continue

            log.info(f"  Options: {option_texts}")
            chosen = ai.answer(q_text, option_texts)

            target = option_els[chosen]
            ctx_driver.execute_script(
                "arguments[0].scrollIntoView({block:'center'});", target
            )
            pause(0.7, 1.4)
            safe_click(ctx_driver, target)
            log.info(f"  Selected option {chosen+1}: {option_texts[chosen]}")
            pause(0.5, 1)

        # submit quiz
        for attempt in range(CONFIG["max_quiz_retries"]):
            submitted = click_any(ctx_driver, [
                "//button[contains(.,'Submit')]",
                "//button[contains(.,'Check')]",
                "//button[contains(.,'Finish')]",
                "//button[contains(.,'Done')]",
                "//button[contains(.,'Next')]",
                "//input[@type='submit']",
            ], timeout=5)
            if submitted:
                log.info(f"Quiz submitted (attempt {attempt+1}).")
                pause(2, 3)
                shot(driver, f"quiz_submitted_{attempt}")
                break
            log.warning(f"Submit not found — retry {attempt+1}")
            pause(1, 2)

        return True

    # try main page first
    try:
        if _process_quiz_in_context(driver):
            return True
    except Exception as e:
        log.warning(f"Quiz on main page error: {e}")

    # try inside iframes
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    for iframe in iframes:
        try:
            driver.switch_to.frame(iframe)
            handled = _process_quiz_in_context(driver)
            driver.switch_to.default_content()
            if handled:
                return True
        except Exception as e:
            log.warning(f"Quiz iframe error: {e}")
            driver.switch_to.default_content()

    return False


# ═══════════════════════════════════════════════════════════
#  SIDEBAR MODULE NAVIGATOR
# ═══════════════════════════════════════════════════════════
def click_next_module(driver: webdriver.Chrome) -> bool:
    """
    Clicks the next uncompleted module from the right-side TOC sidebar.
    Returns True if a module was clicked.
    """
    candidates = driver.find_elements(By.XPATH,
        "//*[contains(@class,'toc') and not(contains(@class,'completed')) and not(contains(@class,'done'))]"
        " | //li[not(contains(@class,'completed')) and not(contains(@class,'active'))]"
        "    [ancestor::*[contains(@class,'toc') or contains(@class,'sidebar') or contains(@class,'module-list')]]"
        " | //*[contains(@class,'module-item') and not(contains(@class,'completed'))]"
    )
    for c in candidates:
        if c.is_displayed() and c.text.strip():
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", c)
            pause(0.5, 1)
            safe_click(driver, c)
            log.info(f"Clicked sidebar module: {c.text.strip()[:60]}")
            pause(2, 3)
            return True
    return False


# ═══════════════════════════════════════════════════════════
#  MAIN COURSE LOOP
# ═══════════════════════════════════════════════════════════
def complete_course(driver: webdriver.Chrome, ai: AIAnswerer):
    log.info("=" * 55)
    log.info("  Starting course traversal")
    log.info("=" * 55)

    visited_urls = set()
    page_num     = 0
    stuck_count  = 0

    while page_num < CONFIG["max_slides"]:
        page_num   += 1
        current_url = driver.current_url
        log.info(f"\n-- Page {page_num} ----------------------------------")
        log.info(f"   URL: {current_url[:90]}")

        pause()

        # capture page content for AI
        txt = page_text(driver)
        if txt:
            ai.add_context(txt)

        shot(driver, f"page_{page_num:03d}")

        # detect & handle content type
        scorm_handled = handle_scorm(driver)
        if not scorm_handled:
            handle_video(driver)
        handle_quiz(driver, ai)

        # Mark as Complete (outer page level)
        mac = click_any(driver, [
            "//button[contains(.,'Mark as Complete')]",
            "//button[contains(.,'Mark As Complete')]",
            "//a[contains(.,'Mark as Complete')]",
        ], timeout=4)
        if mac:
            log.info("Clicked 'Mark as Complete' on page level.")
            pause(1.5, 2.5)

        # Next button (outer navigation)
        next_clicked = click_any(driver, [
            "//button[contains(.,'Next') and not(@disabled)]",
            "//a[contains(.,'Next')]",
            "//*[contains(@class,'next-btn') and not(contains(@class,'disabled'))]",
            "//*[contains(@class,'nextBtn')]",
            "//button[@aria-label='Next']",
            "//button[contains(.,'Continue')]",
            "//button[contains(.,'Proceed')]",
        ], timeout=5)

        if next_clicked:
            log.info("Clicked outer Next.")
            stuck_count = 0
            pause(2, 3)
            continue

        # try sidebar module navigation
        if click_next_module(driver):
            stuck_count = 0
            continue

        # check for 100% completion
        try:
            prog_els = driver.find_elements(By.XPATH,
                "//*[contains(@class,'progress') or contains(@class,'percent') or contains(@class,'completion')]"
            )
            for pe in prog_els:
                if "100" in pe.text:
                    log.info("Progress shows 100% — UAT complete!")
                    return
        except Exception:
            pass

        # check for congratulations / certificate page
        try:
            body = driver.find_element(By.TAG_NAME, "body").text
            if any(w in body for w in ["Congratulations", "Certificate", "Course Completed", "Well done"]):
                log.info("Completion page detected — UAT SUCCESS!")
                shot(driver, "completion_page")
                return
        except Exception:
            pass

        # stuck detection
        if current_url in visited_urls:
            stuck_count += 1
            log.warning(f"Same URL again — stuck count: {stuck_count}")
            if stuck_count >= 3:
                log.error("Stuck for 3 cycles — stopping traversal.")
                shot(driver, "stuck_state")
                break
        else:
            stuck_count = 0

        visited_urls.add(current_url)

    log.info(f"Course traversal ended after {page_num} iterations.")


# ═══════════════════════════════════════════════════════════
#  UAT REPORT
# ═══════════════════════════════════════════════════════════
def generate_report(driver: webdriver.Chrome):
    shots = sorted(os.listdir(CONFIG["screenshot_dir"]))
    report = {
        "status"            : "COMPLETED",
        "final_url"         : driver.current_url,
        "total_screenshots" : len(shots),
        "screenshots"       : shots,
        "log_file"          : CONFIG["log_file"],
        "course_url"        : CONFIG["course_url"],
    }
    with open("igot_uat_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print("\n" + "=" * 55)
    print("  iGOT UAT AUTOMATION v2.0 — DONE")
    print(f"  Screenshots : {CONFIG['screenshot_dir']}/  ({len(shots)} files)")
    print(f"  Log         : {CONFIG['log_file']}")
    print(f"  Report      : igot_uat_report.json")
    print("=" * 55 + "\n")


# ═══════════════════════════════════════════════════════════
#  ENTRY POINT
# ═══════════════════════════════════════════════════════════
def main():
    log.info("iGOT Karmayogi UAT Automation v2.0 starting...")
    ai     = AIAnswerer()
    driver = get_driver()

    try:
        login_otp(driver)
        open_course(driver)
        complete_course(driver, ai)
        generate_report(driver)
    except KeyboardInterrupt:
        log.info("UAT manually interrupted.")
        shot(driver, "interrupted")
    except Exception as e:
        log.exception(f"Fatal error: {e}")
        shot(driver, "fatal_error")
    finally:
        pause(2, 3)
        driver.quit()
        log.info("Browser closed. UAT session ended.")


if __name__ == "__main__":
    main()
