from __future__ import annotations
import os, re, unicodedata, json, csv, locale
from datetime import datetime, date
from subprocess import CompletedProcess


#------------------------------------------------------------------------------
# Colors
#------------------------------------------------------------------------------

BLACK="\033[0;30m%s\033[0m"
RED="\033[0;31m%s\033[0m"
GREEN="\033[0;32m%s\033[0m"
YELLOW="\033[0;33m%s\033[0m"
BLUE="\033[0;34m%s\033[0m"
GRAY="\033[0;90m%s\033[0m"

BOLD_RED="\033[0;1;31m%s\033[0m"


#------------------------------------------------------------------------------
# Numbers
#------------------------------------------------------------------------------

class _PowerValue():
    def __init__(self, value, unit='B', base="decimal", maxrank=None):
        self.base = base
        if base == "binary":
            power = 1024
            self.rank_labels = []
            for rank in ['', 'Ki', 'Mi', 'Gi', 'Ti']:
                self.rank_labels.append(rank)
                if maxrank and rank != '' and maxrank.upper() == rank[0].upper():
                    break
        elif base == "decimal":
            power = 1000
            self.rank_labels = []
            for rank in ['', 'k', 'M', 'G', 'T']:
                self.rank_labels.append(rank)
                if maxrank and rank != '' and maxrank.upper() == rank[0].upper():
                    break
        else:
            raise ValueError(f'invalid base: {base}')

        self.unit = unit
        self.value = value
        self.rank = 0

        if self.value is None:
            return

        while self.value > power and self.rank < len(self.rank_labels) - 1:
            self.value /= power
            self.rank += 1
        
    def __str__(self):
        if self.value is None:
            return ''
        return ('{:,.1f}' if self.rank > 0 else '{:,.0f}').format(self.value) + ' ' + self.rank_labels[self.rank] + self.unit


def human_bytes(value, base="binary", maxrank=None):
    if value is None:
        return ''

    if base not in ["binary", "decimal", "both"]:
        raise ValueError("invalid base '%s'" % base)
        
    if base in ["binary", "both"]:
        binary_str = str(_PowerValue(value, base="binary", maxrank=maxrank))
        if base == "binary":
            return binary_str

    if base in ["decimal", "both"]:
        decimal_str = str(_PowerValue(value, base="decimal", maxrank=maxrank))
        if base == "decimal":
            return decimal_str
    
    if base == "both":
        return '%-12s' % binary_str + ' (' + decimal_str + ')'


#------------------------------------------------------------------------------
# Text
#------------------------------------------------------------------------------

# If tuple, second element is the original Django's slugify result
SLUGEN_EXAMPLES = {
    "Hello world":                  "hello-world",
    "  \"Privilège\" : élevé!-:) ": "privilege-eleve",
    "--__ _-ADMIN_-_SYS_#_":        ("admin-sys", "admin_-_sys"),
    "Pas d'problème":               ("pas-d-probleme", "pas-dprobleme"),
    "L ' horloge":                  "l-horloge",
    "Main (detail)":                "main-detail",
    "__-__":                        "",
    "---":                          "",
    "-":                            "",
    "#":                            "",
    "":                             "",
    None:                           ("", "none"),
}

def slugen(value, separator='-') -> str:
    """ 
    Generate a slug.

    Simplier alternative to `django.utils.text.slugify`.
    See `SLUGEN_EXAMPLES` for differences.
    """
    if value is None:
        return ""
    
    # Remove accents and other diacritic/non-ascii characters
    value = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode("ascii")

    # Lowercase the string
    value = value.lower()

    # Replace everything that is not a letter or digit by hyphens
    value = re.sub(r"[^a-z0-9]", "-", value)

    # Trim leading, trailing, and consecutive hyphens
    return re.sub(r"-+", separator, value).strip(separator)


def format_help_text(docstring: str):
    if docstring is None:
        return None
    
    docstring = docstring.strip()
    try:
        return docstring[0:docstring.index('\n')].strip()
    except:
        return docstring


def format_description_text(docstring: str):
    if docstring is None:
        return None
    
    description = None
    indent_size = 0
    
    for line in docstring.splitlines(keepends=False):
        if description:
            description += '\n' + line[indent_size:]
        else:
            indent_size = 0
            for char in line:
                if char not in [' ', '\t']:
                    description = line[indent_size:]
                    break
                else:
                    indent_size += 1

    return description


#------------------------------------------------------------------------------
# JSON
#------------------------------------------------------------------------------

def extended_json_decode_hook(obj):
    if isinstance(obj, dict):
        for key, value in obj.items():
            obj[key] = extended_json_decode_hook(value)

    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            obj[i] = extended_json_decode_hook(value)

    elif isinstance(obj, str):
        if len(obj) < 10:
            return obj # ignore
        
        if re.match(r'^\d{4}-\d{2}-\d{2}$', obj):
            # date only
            return datetime.strptime(obj, "%Y-%m-%d").date()
        
        m = re.match(r'^(\d{4}-\d{2}-\d{2}T)(\d{2}:\d{2}:\d{2})(\.\d{3,6})?(Z|[\+\-]\d{2}:\d{2})?$', obj)
        if not m:
            return obj # ignore

        datepart = m.group(1) # mandatory
        timepart = m.group(2) # mandatory
        microsecondpart = m.group(3) # optional
        timezone = m.group(4) # optional
        
        # adapt timezone: replace 'Z' with +0000, or +XX:YY with +XXYY
        if timezone == 'Z':
            timezone = '+0000'
        elif timezone:
            timezone = timezone[:-3] + timezone[-2:]
        
        # NOTE: we don't decode XX:XX:XX into a time: too much risky that it's not actually a time
        # if not datepart:
        #     # time only: we only handle non-timezone-aware times, see: DjangoJSONEncoder
        #     if timezone:
        #         return obj

        #     if microsecondpart:
        #         return time.strptime(f"{timepart}{microsecondpart}", "%H:%M:%S.%f")
        #     else:
        #         return time.strptime(f"{timepart}", "%H:%M:%S")

        # datetime
        if microsecondpart:
            return datetime.strptime(f"{datepart}{timepart}{microsecondpart}{timezone}", "%Y-%m-%dT%H:%M:%S.%f%z")
        else:
            return datetime.strptime(f"{datepart}{timepart}{timezone}", "%Y-%m-%dT%H:%M:%S%z")

    return obj


class ExtendedJSONDecoder(json.JSONDecoder):
    """
    JSONDecoder subclass that knows how to decode date/time, decimal types, and UUIDs.
    Reverse of: ExtendedJSONEncoder.
    Usage example: json.loads(data, cls=ExtendedJSONDecoder)
    """
    def __init__(self, **kwargs):
        if not 'object_hook' in kwargs:
            kwargs['object_hook'] = extended_json_decode_hook
        super().__init__(**kwargs)


class ExtendedJSONEncoder(json.JSONEncoder):
    """
    Adapted from: django.core.serializers.json.DjangoJSONEncoder
    Usage example: json.dumps(data, indent=2, cls=ExtendedJSONEncoder)
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def default(self, o):
        # See "Date Time String Format" in the ECMA-262 specification.
        if isinstance(o, datetime):
            r = o.isoformat()
            if o.microsecond and o.microsecond % 1000 == 0:
                r = r[:23] + r[26:]
            if r.endswith("+00:00"):
                r = r[:-6] + "Z"
            return r
        elif isinstance(o, date):
            return o.isoformat()
        # elif isinstance(o, datetime.time):
        #     if is_aware(o):
        #         raise ValueError("JSON can't represent timezone-aware times.")
        #     r = o.isoformat()
        #     if o.microsecond:
        #         r = r[:12]
        #     return r
        # elif isinstance(o, datetime.timedelta):
        #     return duration_iso_string(o)
        # elif isinstance(o, (decimal.Decimal, uuid.UUID, Promise)):
        #     return str(o)
        else:
            return super().default(o)


#------------------------------------------------------------------------------
# CSV
#------------------------------------------------------------------------------

class excel_fr(csv.excel):
    """ French version of Excel. """
    delimiter = ";"

csv.register_dialect('excel_fr', excel_fr())


def get_default_csv_dialect_name() -> str:
    dialect = os.environ.get("CSV_DIALECT", None)
    if dialect:
        return dialect
    
    available_dialects = csv.list_dialects()

    for loc in locale.getlocale():
        m = re.match(r"^([a-z]{2})(?:_[A-Z]{2})?$", loc)
        if m:
            lang = m.group(1)
            name = f"excel-{lang}"
            if name in available_dialects:
                return name
    
    return "excel"


#------------------------------------------------------------------------------
# Subprocess
#------------------------------------------------------------------------------

def format_subprocess_result(cp: CompletedProcess, ignore_returncode: int|list[int] = None, ignore_stderr = False, ignore_stdout = False) -> str:
    def include_returncode(returncode):
        if isinstance(ignore_returncode, int):
            return returncode != ignore_returncode
        elif isinstance(ignore_returncode, list):
            return returncode not in ignore_returncode
        else:
            return True

    parts = []

    if include_returncode(cp.returncode):
        parts.append(f"returncode: {YELLOW}" % cp.returncode)

    if not ignore_stderr:
        if isinstance(cp.stderr, str):
            stderr = cp.stderr.strip()
        else: # byte array
            stderr = cp.stderr
        if stderr:
            parts.append(f"stderr: {YELLOW}" % stderr)

    if not ignore_stdout:
        if isinstance(cp.stdout, str):
            stdout = cp.stdout.strip()
        else: # byte array
            stdout = cp.stdout
        if stdout:
            parts.append(f"stdout: {YELLOW}" % stdout)
    
    return " - ".join(parts)
