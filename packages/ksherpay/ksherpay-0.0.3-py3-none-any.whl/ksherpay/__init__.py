from ksherpay.order import Order


class Payment(object):

    def __init__(self, base_url, token=None, provider='Ksher', mid=None, timeout=10, verify=True):
        self.order = Order(base_url, 
                            token=token, 
                            provider=provider, 
                            mid=mid, 
                            timeout=timeout,
                            verify=verify)
        