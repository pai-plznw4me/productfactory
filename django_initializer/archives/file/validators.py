import re
from django.core.exceptions import ValidationError


def validate_version_format(value):
    # "v.x.x.x"와 같은 형식인지 검사
    pattern = re.compile(r'^v\.\d+\.\d+\.\d+$')
    if not pattern.match(value):
        raise ValidationError('Invalid version format. Use "v.x.x.x" format.')
