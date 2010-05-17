'''
Created on May 17, 2010

@author: mazurov
'''

def processor(request):
    result = {}
    result['request_from_external'] = (request.META['HTTP_HOST'].find('lbrundb') == 0)
    result['request_from_pit'] = not result['request_from_external']
    return result
