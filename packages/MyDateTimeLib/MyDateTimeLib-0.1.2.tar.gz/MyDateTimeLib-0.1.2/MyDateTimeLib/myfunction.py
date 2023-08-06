import regex as re
import datefinder


def date_find(string):
    # clean the string
    clean_string = re.sub('[^a-zA-Z0-9-/:. _,]', ' ', string, flags=re.IGNORECASE)
    pattern = re.compile(
        r"((\b(\d{1,2})(\/|-)(\d{1,2})(\/|-)(\d{2,4})([ ,]+\d{1,2}:\d{2}(:\d{2}(.\d{4,8})?)?)?)|((\d{1,2}:\d{2}(:\d{"
        r"2}(.\d{4,8})?)?)?((\d{4})?(([ ,-\/]+)([012]?[0-9]|3[01])?[ ,-\/]*(([Jj]an(uary)?|[Ff]eb(ruary)?|[Mm]ar("
        r"ch)?|[Aa]pr(il)?|[Mm]ay|[Jj]une?|[Jj]uly?|[Aa]ug(ust)?|[Ss]ept?(ember)?|[Oo]ct(ober)?|[Nn]ov(ember)?|["
        r"Dd]ec(ember)?))[ ,-\/]*([012]?[0-9]|3[01])?([ ,-\/]+))(\d{4})?)([ ,]+\d{1,2}:\d{2}(:\d{2}(.\d{4,8})?)?)?)|("
        r"(\d{1,2}:\d{2}(:\d{2}(.\d{4,8})?)?[ ,]+)?(\d{2,4}[ -\/]+(0[1-9]|1[12])[ -\/]+([12][0-9]|3[01]|0?[1-9]))([ ,"
        r"]+\d{1,2}:\d{2}(:\d{2}(.\d{4,8})?)?)?))")

    # dictionary for result
    date_dict = {}

    result = pattern.finditer(clean_string)
    c = 0
    for x in result:
        matches = datefinder.find_dates(x[0])
        for m in matches:
            date_no = 'Date:' + str(c)
            date_dict.__setitem__(date_no, m)
            c += 1
    return date_dict


print(date_find("10-12-1995"))
