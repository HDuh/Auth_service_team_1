from user_agents import parse

browsers = ['Chrome', 'Firefox', 'Opera', 'Safari', 'Yandex']


def get_browser(user_agent_string):
    """ Парсинг user agent-а и нахождение браузера """
    user_agent = parse(user_agent_string)
    browser_name = user_agent.browser.family
    for browser_i in browsers:
        if browser_i in browser_name:
            return browser_i

    return 'Unknown'
