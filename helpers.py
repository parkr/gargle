# Module: helpers
#
#

# Public: Get the HTML of the associated url via its number.
def get_html(num, url='', backup_pages_dir_rel_path='./test3'):
    encoding = False
    try:
        f = open("%s/%s.html" % (backup_pages_dir_rel_path, num), 'r')
    except IOError:
        try:
            f = open("%s/%s.htm" % (backup_pages_dir_rel_path, num), 'r')
            encoding = "iso-8859-1"
        except IOError:
            return None
        
    html = f.read()
    try:
        unicode_html = unicode(html, 'utf-8')
    except UnicodeDecodeError:
        if encoding:
            unicode_html = unicode(html, encoding)
        else:
            unicode_html = unicode(html, 'windows-1252')
    return unicode_html


# Public: creates a hash based on the HTML.
#
# Returns the md5 hash of the HTML
import hashlib
def page_hash(html):
    return hashlib.md5(html.encode(errors='ignore')).hexdigest()