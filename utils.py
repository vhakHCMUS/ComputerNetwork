import pandas
import numpy as np

def dicToHTML(dic={}, tranpose=False):
    table = pandas.DataFrame([dic]) if not tranpose else pandas.DataFrame([dic],index=['Times']).T
    table.replace('', np.nan, inplace=True)
    table.dropna(inplace=True)
    table = table.to_html()
    return table

def newliToBr(log=''):
    res = '<br>'.join(log.splitlines())
    return res