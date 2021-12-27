from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import ui
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait


PATH = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(PATH)

driver.get('https://www.probuilds.net/champions')

try:
    champions_list = []
    champions = ui.WebDriverWait(driver, 10).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, ".champion-details2")))
    for champ_details in champions:
        champions_list.append(champ_details.text)
        champions_list.append(champ_details.text)

    champs_blocks = driver.find_elements_by_xpath("//a[@class='block id=']")

    hrefs = []
    for link in champs_blocks:
        hrefs.append(link.get_attribute("href"))
    print('hrefs', hrefs)

    stat_header_list = []
    final_items_list = []
    final_runes_list = []
    for href in hrefs:
        driver.get(href)

        stat_header_of_a_champ = driver.find_element_by_class_name("stats-header-flex")
        print(stat_header_of_a_champ.text)
        stat_header_list.append(stat_header_of_a_champ.text)
        stat_header_list.append(stat_header_of_a_champ.text)

        # here i take hrefs from game data each player
        timeout = 120
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'live-feed-match-link'))
        WebDriverWait(driver, timeout).until(element_present)
        from_game_data = driver.find_elements_by_class_name('live-feed-match-link')
        game_data_hrefs = []

        for link in from_game_data:
            game_data_hrefs.append(link.get_attribute("href"))
        print(game_data_hrefs)
        game_data_hrefs = game_data_hrefs[:2]
        # in below 'for' enter every game and save builds and runes
        for href in game_data_hrefs:
            driver.get(href)
            print(href)
            final_items = driver.find_elements_by_class_name("text-center")
            print(final_items)

            for item in final_items:
                # print(my_item)
                final_items_list.append(item.text)
                print(item.text)

            runes = driver.find_elements_by_class_name("rune")
            for rune in runes:
                print(rune.text)
                final_runes_list.append(rune.text)
            driver.back()
        driver.back()
finally:
    driver.quit()


def preparing_list(item_list):
    new_list = []
    # n = hrefs (quantity of champs) * 10 (quantity of players checked for each champ)
    n = len(hrefs) * len(game_data_hrefs)

    divide_num = int(len(item_list)/n)
    for i in range(0, len(item_list), divide_num):
        new_list.append(list(item_list[i:i + divide_num]))
    item_list = new_list
    return item_list


final_items_list = preparing_list(final_items_list)
final_runes_list = preparing_list(final_runes_list)

print(champions_list)
print(stat_header_list)
print(final_items_list)
print(final_runes_list)

data = {
    'Champ': champions_list,
    'Stats': stat_header_list,
    'Items': final_items_list,
    'Runes': final_runes_list}

end_df = pd.DataFrame(data)
end_df.to_csv('end_df.csv')

