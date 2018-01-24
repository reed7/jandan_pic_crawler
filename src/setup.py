import logging

# General
""" 
This number is used to determine the page NO. the 
current task starts from: start_pageno = first_pageno - SEARCH_BACK 
"""
SEARCH_BACK = 2
# This value will be used if the last stop point file doesn't exist
# or the picture to grab on this task is larger than this number
DEFAULT_PIC_PER_TASK = 100
PICUTURE_ID_PREFIX = "comment-"
"""
File to store the picture ID which last task starts at
"""
LAST_TASK_STOP = "last_stop"
JANDAN_PIC_URL = "http://jandan.net/pic"
JANDAN_PIC_URL_PAGENO = "%s/page-{}" % JANDAN_PIC_URL
TUCAO_URL = "http://jandan.net/tucao/%s"

# Beautiful Soup
BEAUTIFUL_SOUP_BUILDER = "lxml"  # Can be "html.parser", "html5lib" or "lxml"

# Logging
LOG_FILE = "spider.log"
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '%(asctime)s %(levelname)s: %(module)s[%(lineno)d]-%(message)s'
LOG_DATE_FORMAT = '%Y/%m/%d %H:%M:%S'