from functools import wraps

from depdf.base import Base
from depdf.error import ConfigTypeError
from depdf.log import logger_init
from depdf.settings import *

log = logger_init(__name__)


class Config(Base):
    # pdf
    logo_flag = DEFAULT_LOGO_FLAG
    header_footer_flag = DEFAULT_HEADER_FOOTER_FLAG
    temp_dir_prefix = DEFAULT_TEMP_DIR_PREFIX
    unique_prefix = None  # 该参数会根据 pdf 的文件名自动更新

    # page
    table_flag = DEFAULT_TABLE_FLAG
    paragraph_flag = DEFAULT_PARAGRAPH_FLAG
    image_flag = DEFAULT_IMAGE_FLAG
    resolution = DEFAULT_RESOLUTION
    main_frame_tolerance = None  # 该参数可通过页面内容自动分析
    x_tolerance = None  # 该参数可通过页面内容自动分析
    y_tolerance = None  # 该参数可通过页面内容自动分析
    page_num_top_fraction = DEFAULT_PAGE_NUM_TOP_FRACTION
    page_num_left_fraction = DEFAULT_PAGE_NUM_LEFT_FRACTION
    page_num_right_fraction = DEFAULT_PAGE_NUM_RIGHT_FRACTION
    dotted_line_flag = True
    curved_line_flag = False

    # chars
    char_overlap_size = DEFAULT_CHAR_OVERLAP_SIZE
    default_char_size = DEFAULT_CHAR_SIZE
    char_size_upper = DEFAULT_CHAR_SIZE_UPPER
    char_size_lower = DEFAULT_CHAR_SIZE_LOWER

    # table
    snap_flag = DEFAULT_SNAP_FLAG
    add_line_flag = DEFAULT_ADD_LINE_FLAG
    min_double_line_tolerance = DEFAULT_MIN_DOUBLE_LINE_TOLERANCE  # used in page class
    max_double_line_tolerance = DEFAULT_MAX_DOUBLE_LINE_TOLERANCE  # used in page class
    vertical_double_line_tolerance = DEFAULT_VERTICAL_DOUBLE_LINE_TOLERANCE  # used in page class
    table_cell_merge_tolerance = DEFAULT_TABLE_CELL_MERGE_TOLERANCE
    skip_empty_table = DEFAULT_SKIP_EMPTY_TABLE

    # image
    min_image_size = DEFAULT_MIN_IMAGE_SIZE

    # head & tail
    default_head_tail_page_offset_percent = DEFAULT_HEAD_TAIL_PAGE_OFFSET_PERCENT

    # log
    log_level = DEFAULT_LOG_LEVEL
    verbose_flag = DEFAULT_VERBOSE_FLAG
    debug_flag = DEFAULT_DEBUG_FLAG

    # html
    span_class = DEFAULT_SPAN_CLASS
    paragraph_class = DEFAULT_PARAGRAPH_CLASS
    table_class = DEFAULT_TABLE_CLASS
    pdf_class = DEFAULT_PDF_CLASS
    image_class = DEFAULT_IMAGE_CLASS

    def __init__(self, **kwargs):
        # set log level automatically if debug mode enabled
        if kwargs.get('debug_flag'):
            self.log_level = logging.DEBUG
        if kwargs.get('verbose_flag'):
            self.log_level = logging.INFO

        # add configuration parameters
        self.update(**kwargs)

        # set logging level by log_level parameter
        logging.getLogger('depdf').setLevel(self.log_level)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                log.warning('config attributes not found: {}'.format(key))


DEFAULT_CONFIG = Config()
PDF_IMAGE_KEYS = ['srcsize', 'height', 'width', 'bits']
DEFAULT_CONFIG_KEYS = list(DEFAULT_CONFIG.to_dict.keys())


def check_config(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        config = kwargs.get('config')
        if config is None:
            config = DEFAULT_CONFIG
        else:
            check_config_type(config)
        kwargs['config'] = config
        return func(*args, **kwargs)
    return wrapper


def check_config_type(config):
    if not isinstance(config, Config):
        raise ConfigTypeError(config)
