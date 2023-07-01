# https://stackoverflow.com/a/70419609/6461688
def is_ajax(request):
    """
    Return True if the request was sent with XMLHttpRequest, False otherwise.
    """
    return request.META.get("HTTP_X_REQUESTED_WITH") == "XMLHttpRequest"
