import logging

# General
""" 
This number is used to determine the page NO. the 
current task starts from: start_pageno = first_pageno - SEARCH_BACK 
"""
SEARCH_BACK = 10
DEFAULT_PIC_PER_TASK = 200
PICUTURE_ID_PREFIX = "comment-"
"""
File to store the picture ID which last task starts at
"""
LAST_TASK_STOP = "last_stop"
JANDAN_PIC_URL = "http://jandan.net/pic"
JANDAN_PIC_URL_PAGENO = "%s/page-{}" % JANDAN_PIC_URL

# Beautiful Soup
BEAUTIFUL_SOUP_BUILDER = "lxml"  # Can be "html.parser", "html5lib" or "lxml"

# Logging
LOG_FILE = "spider.log"
LOG_LEVEL = logging.DEBUG
LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s'
LOG_DATE_FORMAT = '%Y/%m/%d %H:%M:%S'