from selenium import  webdriver 
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
import logging

def crawl_webpages(url_list):
    service = Service('C:\Program Files\Google\Chrome\Application\chromedriver.exe')
    logging.getLogger('selenium.webdriver.chrome.service').setLevel(logging.WARNING)
    driver1 = webdriver.Chrome(service=service)
    firstopen=0
    for url in url_list:
        print("-----------------------------------------------------")
        driver1.get(url) # 访问页面
        firstopen+=1
        if firstopen==1:
            time.sleep(15) # 暂停5秒，扫码登录，时间不够可以自己调节
        else:
            time.sleep(1)
        try:
            # 尝试查找是否存在class="Forbidden-view"的元素
            driver1.find_element(By.CLASS_NAME, 'Forbidden-view')
            print("未选此课,已跳过")
            continue
        except:
            kechengname=driver1.find_element(By.CLASS_NAME, 'text-ellipsis.title-inner-wrapper').text #提取课程名称
            open_button = driver1.find_element(By.CLASS_NAME, 'blue.ml20').click()# 定位到【展开】按钮
            time.sleep(1) # 等待一秒
            lessones = WebDriverWait(driver1, 2).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'el-tooltip.activity-info')))
            lessenstates = WebDriverWait(driver1, 2).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'aside')))
            calssstate = lessenstates[2].find_element(By.CSS_SELECTOR, "use[data-v-3ef83e2f]").get_attribute('xlink:href')#查找课程是否已经完成
            time.sleep(0.5) 
            if calssstate=="#icon--yiwancheng":#若完成课程则跳过
                print(kechengname+" 之前已做完")
                continue
            print(kechengname+" 开始刷课")
            for index in range(len(lessones)):
                try:
                    lessonstate = lessenstates[3+index].find_element(By.CSS_SELECTOR, "use[data-v-1c75131d]").get_attribute('xlink:href')
                    if lessonstate=="#icon--yiwancheng":#若完成小节课程则跳过
                        print("之前已完成第"+str(index+1)+"小节课")
                        continue
                except:
                    pass
                lesson = WebDriverWait(driver1, 2).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'el-tooltip.activity-info')))[index]
                lesson.click()
                time.sleep(2)
                try:
                    video_layer = WebDriverWait(driver1, 2).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'xt_video_player_big_play_layer.pause_show'))
                    )
                    # 如果找到视频层，则点击播放按钮
                    driver1.find_element(By.CLASS_NAME, 'xt_video_bit_play_btn').click()
                    # 关闭音量
                    driver1.find_element(By.CLASS_NAME, 'xt_video_player_common_icon').click()
                    # 寻找时长
                    video_time_father = driver1.find_element(By.CLASS_NAME, 'xt_video_player_controls_inner')
                    video_time = video_time_father.find_element(By.CLASS_NAME, 'xt_video_player_current_time_display.fl')
                    text_content = video_time_father.text
                    # 根据可能的格式进行处理，例如去除不需要的字符
                    extracted_time = text_content.replace('<xt-time class=xt_video_player_current_time_display fl">=$0 ', '')
                    hours, minutes, seconds = map(int, extracted_time[11:19].split(':'))
                    total_seconds = hours * 3600 + minutes * 60 + seconds
                    # print(total_seconds)
                    time.sleep(int(total_seconds))
                except:
                    try:
                        # 如果是评论题，复制第一个评论提交
                        discussion_text = driver1.find_element(By.CSS_SELECTOR, '.title-fl span').text
                        if "讨论" or "答疑" in discussion_text:
                            content_to_copy = driver1.find_element(By.CSS_SELECTOR, '.cont_detail.word-break').text
                            time.sleep(1)
                            textarea = driver1.find_element(By.CLASS_NAME, 'el-textarea__inner')
                            textarea.clear()
                            textarea.send_keys(content_to_copy)
                            time.sleep(1)
                            driver1.find_element(By.CLASS_NAME, 'el-button.submitComment.el-button--primary.addColor').click()
                            time.sleep(2)
                    except:
                        # 找不到元素时不做任何操作
                        pass
                print("已刷完第"+str(index+1)+"小节课")
                driver1.back()
                driver1.refresh()
                time.sleep(1)
                open_button = driver1.find_element(By.CLASS_NAME, 'blue.ml20')# 定位到【展开】按钮
                open_button.click() # 点击【提交】按钮
                time.sleep(1) # 等待两秒
                lessenstates = WebDriverWait(driver1, 2).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, 'aside')))
        print(kechengname+" over")
    driver1.close()
    print("-----------------------------------------------------")
    print("所有课程全刷完了")


urls_to_crawl = {
    '艺术的启示':'https://www.yuketang.cn/v2/web/studentLog/23441178/',
    '心理健康':'https://www.yuketang.cn/v2/web/studentLog/23441172/',
    '工程伦理':'https://www.yuketang.cn/v2/web/studentLog/23441173/',
    '道德规范':'https://www.yuketang.cn/v2/web/studentLog/23441174/',
    '科技检索':'https://www.yuketang.cn/v2/web/studentLog/23441177/'
}
crawl_webpages(urls_to_crawl.values())