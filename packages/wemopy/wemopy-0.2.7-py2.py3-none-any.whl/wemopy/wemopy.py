"""Main module."""
from typing import List

import grpc

from wemopy import internal
from wemopy.internal import rules_pb2, rules_pb2_grpc
from wemopy.types import RuleFieldValues, ReorderValues, LossValues, JitterValues


class WEMOClient(object):

    host = ""
    port = -1
    channel = None
    client = None
    request_id = 0

    def __init__(self, host:str, port:int):
        self.host = host
        self.port = port

    def __request_id__(self):
        self.request_id += 1
        return self.request_id

    def __update_rule__(self, rule: rules_pb2.Rule) -> bool:
        req = rules_pb2.WanemdRequest(request_id=self.__request_id__(), rule=rule)
        response = self.client.UpdateRule(req)
        return response.status == 1

    def connect(self, host:str=None, port:int=None) -> bool:
        if host is not None:
            self.host = host

        if port is not None:
            self.port = port

        self.channel = grpc.insecure_channel(f"{self.host}:{self.port}")
        self.client = rules_pb2_grpc.ServiceManagerStub(self.channel)

        return True

    def disconnect(self) -> bool:
        if self.client is not None:
            self.client.Stop()
            self.client = None
        if self.channel is not None:
            self.channel.close()
            self.channel = None
        return True

    def clear(self, rule_id:int=1) -> bool:

        # Get the rule
        rule = self.get_rule(rule_id)
        # Clear the rule
        clear_rule = rules_pb2.Rule(id=rule.id, name=rule.name, enabled=rule.enabled)
        return self.__update_rule__(clear_rule)

    def get_rules(self) -> List[rules_pb2.Rule]:

        req = rules_pb2.WanemdRequest(request_id=self.__request_id__())
        response = self.client.ListAllRules(req)
        rules = []
        for rule in response.rules:
            rules.append(rule)

        return rules

    def get_rule(self, rule_id:int=1) -> rules_pb2.Rule:

        req = rules_pb2.WanemdRequest(request_id=self.__request_id__(), rule_id=rule_id)
        response = self.client.ListRule(req)
        return response.rules[0]

    def get_name(self, rule_id:int=1) -> str:
        rule = self.get_rule(rule_id=rule_id)
        return rule.name

    def set_name(self, name:str, rule_id:int=1) -> bool:
        return self.set(rule_id, name)

    def get_enabled(self, rule_id:int=1) -> bool:
        return self.get_rule(rule_id=rule_id).enabled

    def set_enabled(self, enabled:bool, rule_id:int=1) -> bool:
        return self.set(rule_id, enabled=enabled)

    def get_latency(self, rule_id:int=1) -> RuleFieldValues:
        rule = self.get_rule(rule_id=rule_id)
        return RuleFieldValues(rule.ul_latency, rule.dl_latency)

    def set_latency(self, rule_id:int=1, latency:float=None, ul_latency:float=None, dl_latency:float=None, clear=False) -> bool:

        return self.set(rule_id=rule_id, latency=latency, ul_latency=ul_latency, dl_latency=dl_latency, clear=clear)

    def get_rate(self, rule_id:int=1) -> RuleFieldValues:
        rule = self.get_rule(rule_id=rule_id)
        return RuleFieldValues(rule.ul_rate, rule.dl_rate)

    def set_rate(self, rule_id:int=1, rate:int=None, ul_rate:int=None, dl_rate:int=None, clear:bool=False) -> bool:

        return self.set(rule_id=rule_id, rate=rate, ul_rate=ul_rate, dl_rate=dl_rate, clear=clear)

    def get_jitter(self, rule_id:int=1) -> RuleFieldValues:
        rule = self.get_rule(rule_id=rule_id)
        return RuleFieldValues(JitterValues(rule.ul_jitter, rule.ul_jitter_dist, rule.ul_jitter_corr),
                               JitterValues(rule.dl_jitter, rule.dl_jitter_dist, rule.dl_jitter_corr))

    def set_jitter(self, rule_id:int=1, jitter:float=None, ul_jitter:float=None, dl_jitter:float=None,
                   jitter_dist:str=None, ul_jitter_dist:str=None, dl_jitter_dist:str=None,
                   jitter_corr:float=None, ul_jitter_corr:float=None, dl_jitter_corr:float=None, clear:bool=False) -> bool:
        return self.set(rule_id=rule_id, jitter=jitter, ul_jitter=ul_jitter, dl_jitter=dl_jitter, jitter_dist=jitter_dist,
                        ul_jitter_dist=ul_jitter_dist, dl_jitter_dist=dl_jitter_dist, jitter_corr=jitter_corr,
                        ul_jitter_corr=ul_jitter_corr, dl_jitter_corr=dl_jitter_corr, clear=clear)

    def get_loss(self, rule_id:int=1) -> RuleFieldValues:
        rule = self.get_rule(rule_id=rule_id)
        return RuleFieldValues(LossValues(rule.ul_loss, rule.ul_loss_corr), LossValues(rule.dl_loss, rule.dl_loss_corr))

    def set_loss(self, rule_id:int=1, loss:float=None, ul_loss:float=None, dl_loss:float=None,
                 loss_corr:float=None, ul_loss_corr:float=None, dl_loss_corr:float=None, clear:bool=False) -> bool:
        return self.set(rule_id=rule_id, loss=loss, ul_loss=ul_loss, dl_loss=dl_loss, loss_corr=loss_corr,
                        ul_loss_corr=ul_loss_corr, dl_loss_corr=dl_loss_corr, clear=clear)

    def get_duplication(self, rule_id:int=1) -> RuleFieldValues:
        rule = self.get_rule(rule_id=rule_id)
        return RuleFieldValues(rule.ul_duplication, rule.dl_duplication)

    def set_duplication(self, rule_id:int=1, duplication:float=None, ul_duplication:float=None, dl_duplication:float=None,
                        clear=False) -> bool:
        return self.set(rule_id=rule_id, duplication=duplication, ul_duplication=ul_duplication,
                        dl_duplication=dl_duplication, clear=clear)

    def get_corruption(self, rule_id:int=1) -> RuleFieldValues:
        rule = self.get_rule(rule_id=rule_id)
        return RuleFieldValues(rule.ul_corruption, rule.dl_corruption)

    def set_corruption(self, rule_id:int=1, corruption:float=None, ul_corruption:float=None, dl_corruption:float=None,
                       clear=False) -> bool:
        return self.set(rule_id=rule_id, corruption=corruption, ul_corruption=ul_corruption,
                        dl_corruption=dl_corruption, clear=clear)

    def get_reorder(self, rule_id:int=1) -> RuleFieldValues:
        rule = self.get_rule(rule_id=rule_id)
        return RuleFieldValues(ReorderValues(rule.ul_reorder, rule.ul_reorder_corr), ReorderValues(rule.dl_reorder, rule.dl_reorder_corr))

    def set_reorder(self, rule_id:int=1, reorder:float=None, ul_reorder:float=None, dl_reorder:float=None,
                    reorder_corr:float=None, ul_reorder_corr:float=None, dl_reorder_corr:float=None, clear=False) -> bool:
        return self.set(rule_id=rule_id, reorder=reorder, ul_reorder=ul_reorder, dl_reorder=dl_reorder,
                        reorder_corr=reorder_corr, ul_reorder_corr=ul_reorder_corr, dl_reorder_corr=dl_reorder_corr,
                        clear=clear)

    def set(self, rule_id:int=1, name:str=None, enabled:bool=None, rate:int=None, ul_rate:int=None, dl_rate:int=None,
            latency:float=None, ul_latency:float=None, dl_latency:float=None, jitter:float=None, ul_jitter:float=None,
            dl_jitter:float=None, jitter_dist:str=None, ul_jitter_dist:str=None, dl_jitter_dist:str=None,
            jitter_corr:float=None, ul_jitter_corr:float=None, dl_jitter_corr:float=None, loss:float=None,
            ul_loss:float=None, dl_loss:float=None, loss_corr:float=None, ul_loss_corr:float=None, dl_loss_corr:float=None,
            duplication:float=None, ul_duplication:float=None, dl_duplication:float=None, corruption:float=None,
            ul_corruption:float=None, dl_corruption:float=None, reorder:float=None, ul_reorder:float=None, dl_reorder:float=None,
            reorder_corr:float=None, ul_reorder_corr:float=None, dl_reorder_corr:float=None, clear:bool=False) -> bool:

        if clear:
            self.clear(rule_id=rule_id)

        rule = self.get_rule(rule_id=rule_id)

        # Name
        if name is not None:
            rule.name = name

        # Enabled
        if enabled is not None:
            rule.enabled = enabled

        # Rates
        if any(v is not None for v in [rate, ul_rate, dl_rate]):

            if rate is not None:
                rule.ul_rate = rate / 2
                rule.dl_rate = rate / 2

            if ul_rate is not None:
                rule.ul_rate = ul_rate

            if dl_rate is not None:
                rule.dl_rate = dl_rate

        # Latency
        if any(v is not None for v in [latency, ul_latency, dl_latency]):

            if latency is not None:
                rule.ul_latency = latency / 2
                rule.dl_latency = latency / 2

            if ul_latency is not None:
                rule.ul_latency = ul_latency

            if dl_latency is not None:
                rule.dl_latency = dl_latency

        # Jitter
        if any(v is not None for v in [jitter, ul_jitter, dl_jitter, jitter_dist, ul_jitter_dist, dl_jitter_dist,
                                       jitter_corr, ul_jitter_corr, dl_jitter_corr]):

            if jitter is not None:
                rule.ul_jitter = jitter / 2
                rule.dl_jitter = jitter / 2

            if ul_jitter is not None:
                rule.ul_jitter = ul_jitter

            if dl_jitter is not None:
                rule.dl_jitter = dl_jitter

            if jitter_dist is not None:
                rule.ul_jitter_dist = ul_jitter_dist
                rule.dl_jitter_dist = dl_jitter_dist

            if ul_jitter_dist is not None:
                rule.ul_jitter_dist = ul_jitter_dist

            if dl_jitter_dist is not None:
                rule.dl_jitter_dist = dl_jitter_dist

            if jitter_corr is not None:
                rule.ul_jitter_corr = jitter_corr
                rule.dl_jitter_corr = jitter_corr

            if ul_jitter_corr is not None:
                rule.ul_jitter_corr = ul_jitter_corr

            if dl_jitter_corr is not None:
                rule.dl_jitter_corr = dl_jitter_corr

        # Loss
        if any(v is not None for v in [loss, ul_loss, dl_loss, loss_corr, ul_loss_corr, dl_loss_corr]):

            if loss is not None:
                rule.ul_loss = loss / 2
                rule.dl_loss = loss / 2

            if ul_loss is not None:
                rule.ul_loss = ul_loss

            if dl_loss is not None:
                rule.dl_loss = dl_loss

            if loss_corr is not None:
                rule.ul_loss_corr = loss_corr
                rule.dl_loss_corr = loss_corr

            if ul_loss_corr is not None:
                rule.ul_loss_corr = ul_loss_corr

            if dl_loss_corr is not None:
                rule.dl_loss_corr = dl_loss_corr

        # Duplication
        if any(v is not None for v in [duplication, ul_duplication, dl_duplication]):

            if duplication is not None:
                rule.ul_duplication = duplication / 2
                rule.dl_duplication = duplication / 2

            if ul_duplication is not None:
                rule.ul_duplication = ul_duplication

            if dl_duplication is not None:
                rule.dl_duplication = dl_duplication

        # Corruption
        if any(v is not None for v in [corruption, ul_corruption, dl_corruption]):

            if corruption is not None:
                rule.ul_corruption = corruption / 2
                rule.dl_corruption = corruption / 2

            if ul_corruption is not None:
                rule.ul_corruption = ul_corruption

            if dl_corruption is not None:
                rule.dl_corruption = dl_corruption

        # Reorder
        if any(v is not None for v in [reorder, ul_reorder, dl_reorder, reorder_corr, ul_reorder_corr, dl_reorder_corr]):

            if reorder is not None:
                rule.ul_reorder = reorder / 2
                rule.dl_reorder = reorder / 2

            if ul_reorder is not None:
                rule.ul_reorder = ul_reorder

            if dl_reorder is not None:
                rule.dl_reorder = dl_reorder

            if reorder_corr is not None:
                rule.ul_reorder_corr = reorder_corr
                rule.dl_reorder_corr = reorder_corr

            if ul_reorder_corr is not None:
                rule.ul_reorder_corr = ul_reorder_corr

            if dl_reorder_corr is not None:
                rule.dl_reorder_corr = dl_reorder_corr

        # Apply Update
        return self.__update_rule__(rule)
