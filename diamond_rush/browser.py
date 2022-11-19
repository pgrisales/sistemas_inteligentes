import cv2
import numpy as np
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time

class Browser:
  def __init__(self, level):
    self.driver = webdriver.Firefox()
    self.driver.get("https://www.miniplay.com/embed/diamond-rush")

    iframe = self.driver.find_element("css selector", "iframe")
    self.driver.switch_to.frame(iframe)

    self.map_moves = {
        "l": Keys.ARROW_LEFT,
        "r": Keys.ARROW_RIGHT,
        "u": Keys.ARROW_UP,
        "d": Keys.ARROW_DOWN
    }
    self.select_level(level)

  def close(self):
    self.driver.close()

  def select_level(self, level):
    script = f"window.localStorage.setItem('levelToStart','Level {level}')"
    self.driver.execute_script(script)
    self.driver.refresh()

    iframe = self.driver.find_element("css selector", "iframe")
    self.driver.switch_to.frame(iframe)

  def move(self, movements):
    actions = ActionChains(self.driver)

    for move in movements:
      move = self.map_moves[move]
      actions.key_down(move).pause(0.13).perform()
      actions.key_up(move).pause(0.13).perform()

  def get_board(self):
    time.sleep(3)
    canvas = self.driver.find_element("css selector", "canvas")
    ss = canvas.screenshot_as_png
    img = np.frombuffer(ss, dtype=np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img
