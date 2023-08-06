class RuleFieldValues(object):
    ul_value = None
    dl_value = None

    def __init__(self, ul_value, dl_value):
        self.ul_value = ul_value
        self.dl_value = dl_value

class JitterValues(object):
    jitter = None
    jitter_dist = None
    jitter_dist_corr = None

    def __init__(self, jitter, jitter_dist, jitter_dist_corr):
        self.jitter = jitter
        self.jitter_dist = jitter_dist
        self.jitter_dist_corr = jitter_dist_corr

class LossValues(object):
    loss = None
    loss_corr = None

    def __init__(self, loss, loss_corr):
        self.loss = loss
        self.loss_corr = loss_corr

class ReorderValues(object):
    reorder = None
    reorder_corr = None

    def __init__(self, reorder, reorder_corr):
        self.reorder = reorder
        self.reorder_corr = reorder_corr
