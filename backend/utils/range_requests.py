import re
from typing import Tuple, Optional

def parse_range_header(range_header: Optional[str], file_size: int) -> Tuple[int, int, int]:
    if not range_header or not range_header.startswith("bytes="):
        return 0, file_size - 1, file_size

    match = re.match(r"bytes=(\d*)-(\d*)", range_header)
    if not match:
        return 0, file_size - 1, file_size

    start_str, end_str = match.groups()
    if start_str and end_str:
        start, end = int(start_str), int(end_str)
    elif start_str:
        start, end = int(start_str), file_size - 1
    elif end_str:
        start, end = file_size - int(end_str), file_size - 1
    else:
        start, end = 0, file_size - 1

    start = max(0, min(start, file_size - 1))
    end = max(start, min(end, file_size - 1))
    content_length = (end - start) + 1
    return start, end, content_length
