import allure
import json
from loguru import logger


def allure_title(title: str) -> None:
    """allure中显示的用例标题"""
    allure.dynamic.title(title)


def allure_feature(feature: str) -> None:
    """allure中显示的用例模块"""
    allure.dynamic.feature(feature)

def allure_testcase(_case_link,caseName) -> None:
    allure.dynamic.testcase(_case_link, caseName)

def allure_story(storyName: str, storyLink:str) -> None:
    """allure中显示的用例的需求和需求连接"""
    allure.dynamic.story(storyName)
    # allure_link(storyLink, f'需求详情：{storyName}')


def allure_case_link(caseName, _case_link:str)-> None:
    allure_link(_case_link, f'用例详情：{caseName}')


def allure_link(_link: str, _name=None) -> None:
    """allure中显示的用例模块"""
    allure.dynamic.link(url=_link, name=_name)


def allure_suite(_name: str) -> None:
    """allure中显示的用例模块"""
    # _list=_name.strip("/")
    allure.dynamic.suite(_name)
    # allure.dynamic.parent_suite(_list[0])
    # if len(_list) == 2:
    #     allure.dynamic.suite(_list[1])
    # if len(_list) >2:
    #     allure.dynamic.sub_suite(_list[2])


def allure_tag(_name: str) -> None:
    """allure中显示的用例模块"""
    allure.dynamic.tag(_name)

def allure_severity(severity_level: str) -> None:
    """allure中显示的用例等级"""
    if severity_level.strip() == 'P0':
        allure_tag('冒烟测试,回归测试')
    if severity_level.strip() == 'P1':
        allure_tag('回归测试')
    if severity_level.strip() == 'P2':
        allure_tag('回归测试')
    allure.dynamic.severity(convert_severity(severity_level))


def allure_step(step: str, content: str) -> None:
    """
    :param step: 步骤及附件名称
    :param content: 附件内容
    """
    logger.info(f'{step}:{content}')
    try:
        with allure.step(step):
            allure.attach(json.dumps(content, ensure_ascii=False, indent=4), step, allure.attachment_type.TEXT)
    except Exception as e:
        logger.warning(f'{step}无用例上下文：{str}')

def convert_severity(_str):
    return _str.replace("P0", "critical").replace("P1", "normal") \
        .replace("P2", "minor").replace("P3", "trivial")







