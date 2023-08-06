import copy
import os
from os import listdir
from os.path import isfile, join
import dependency_miner.settings as settings
#import Miner.to_petri_net_bordered as discover_net
#from Miner.helper_functions import *

from pm4py.objects.log.importer.xes import importer as xes_importer
import pm4py.objects.process_tree as pt
from pm4py.analysis import check_soundness

from pm4py.algo.evaluation.precision import algorithm as precision_evaluator
from pm4py.algo.evaluation.replay_fitness import algorithm as replay_fitness_evaluator

from pm4py.visualization.petri_net import visualizer as pn_visualizer

from pm4py.objects.process_tree.utils import bottomup as b
from pm4py.algo.discovery.inductive import algorithm as inductive_miner
from pm4py.visualization.process_tree import visualizer as pt_visualizer

from pm4py.objects.petri_net.exporter import exporter as pnml_exporter
from pm4py.objects.petri_net.importer import importer as pnml_importer
from pm4py.objects.petri_net.obj import PetriNet, Marking

from pm4py.statistics.traces.generic.log import case_statistics

from pm4py.objects.process_tree.obj import Operator as pt_op
from pm4py.objects.process_tree.utils import generic as util

from pm4py.objects.petri_net import obj
from pm4py.objects.petri_net.utils import petri_utils as pn_util

log_attributes = {}

def miner(log_path, support, confidence, lift, sound):
    """
    Extracts long-term dependencies between the task using the given input thresholds.
    Parameters:
        logpath (str): Path of event log
        support (str): Threshold value for support
        confidence (str) : Threshold value for confidence 
        lift (str): Threshold value for confidence 
        sound (str) : sound model requirement Yes/No
    Returns:
        rules (dict): Rules added to the repaired precise net
        precision (float): Improved precision value
        fitness (float): Fitness of the repaired Petri net
        net_path (str) : Path of the .SVG file generated for the repaired net
        pnml_path (str) : Path of the .pnml file generated for the repaired net
    """
    settings.init()
    eventlogs, attributes, log, tree, net, im, fm = set_event_log(log_path)
    #process_tree_path = display_process_tree()
    if sound == 'Yes' or sound == 'yes':
        sound = 'on'
    net_path, precision, fitness, rules, pnml_path =  repair_petri_net(support, confidence, lift, sound)
    
    print("Added rules in the repaired Petri net", rules)
    print("Precision of the repaired Petri net", precision)
    print("Fitness of the repaired Petri net", fitness)
    print("Saved Path of the repaired Petri net in .SVG format", net_path)
    print("Saved Path of the repaired Petri net in .pnml format", pnml_path)
    
    return rules, precision, fitness, net_path, pnml_path

def set_event_log(file_path):
    """
    Given an input event log, the function imports the log and returns discovered process tree 
    and petri net model along with the details of the log. 
    Parameters:
        file_path (str): Path of event log
        
    Returns:
        eventlogs (list): List of event logs
        log_attributes (dict): Details of the log
        log (EventLog) : Imported event log 
        tree (processtree): Discovered Process tree from the given event log
        net (PetriNet) : Discovered Petri net from the given event log
        im (Marking) : Initial marking of the generated Petri net
        fm (Marking) : Final marking of the generated Petri net
    """
    filename = os.path.basename(file_path)
    settings.EVENT_LOG_NAME = filename
    settings.EVENT_LOG_PATH = file_path
    
    log = import_event_log(file_path)
    settings.EVENT_LOG = log
    no_traces = len(log)
    no_events = sum([len(trace) for trace in log])
    log_attributes['no_traces'] = no_traces
    log_attributes['no_events'] = no_events     
    
    #discover Tree
    tree = None
    tree = discover_process_tree(log)   
    
    #discover net
    net = None
    im = None
    fm = None
    settings.RULES_DICT = {}
    settings.RULES = {}
    settings.PRECISION = None
    settings.FITNESS = None
    net, im, fm = discover_petri_net(tree)
    
    
    pnml_path = export_pnml(net, im, fm)
    
    # disover rules
    rules_dict = {}
    xor_tree = []
    rules_dicts, xor_tree = findAsociationRules()
    settings.RULES_DICT = copy.deepcopy(rules_dicts)
    settings.XOR_TREES = copy.deepcopy(xor_tree)
    
    #eventlogs = [f for f in listdir(file_path) if isfile(join(file_path, f))]
    eventlogs = ""
    return eventlogs, log_attributes, log, tree, net, im, fm


def findAsociationRules():
    """
    This function mines the long-term dependency rules between XOR branches of the process tree. 
    Parameters:
        
    Returns:
        Rules (dict) : Discovered rules between XOR branches of the process tree
        XOR blocks (dict) : Candidate XOR blocks present in the process tree 
    """
    
    tree = settings.PROCESS_TREE 
    log = settings.EVENT_LOG 
    # Explore Log
    total_traces = 0
    xor_tree = {}
    rules_dict = {}
    
    
    variants_count = case_statistics.get_variant_statistics(log)
    variants_count = sorted(variants_count, key=lambda x: x['count'], reverse=True)
    rules_values = {}
    
    for ele in variants_count:
        total_traces += ele['count']
    
    rule_dicti = {}
    ## Firstly, get all XOR tree list if it has no tau at the leaves.
    xor_tree = {}
    xor_tree = get_xor_trees(tree)
    
    ## find all valid XOR combinations
    for i in range(1, len(xor_tree)):
        for j in range(i+1, len(xor_tree)+1):
            max_v = 0
            rules_values = {}
            LCA = util.common_ancestor(xor_tree[f'X{i}'], xor_tree[f'X{j}'])
            if LCA.operator == pt_op.SEQUENCE and (pt_op.XOR not in get_ancestors_operator(xor_tree[f'X{i}'], LCA)) and (pt_op.XOR not in get_ancestors_operator(xor_tree[f'X{j}'], LCA)) and (pt_op.LOOP not in get_ancestors_operator(xor_tree[f'X{i}'], LCA)) and (pt_op.LOOP not in get_ancestors_operator(xor_tree[f'X{j}'], LCA)):
                xor_children = []
                source, target = get_candidates(xor_tree[f'X{i}'], xor_tree[f'X{j}'])
                for s in source:
                    for t in target:
                        values = []
                        support = get_support_updated([s,t], variants_count, total_traces, source, target)
                        conf_value = get_confidence([s,t], support[tuple(s), tuple(t)], variants_count, total_traces)
                        lift_value = get_lift([s, t], conf_value, variants_count, total_traces)
                        
                        values.append(support[tuple(s), tuple(t)])
                        values.append(conf_value)
                        values.append(lift_value)
                        l = [s,t]
                        rules_values[(f"{s}", f"{t}")] = values
                        if values[2] > max_v:
                            max_v = values[2]
                rules_values['Max'] = max_v
                rule_dicti[(f"X{i}", f"X{j}")] = rules_values
    
    sorted_rule_dict = dict(sorted(rule_dicti.items(), key=lambda item: item[1]['Max'], reverse=True))
    return sorted_rule_dict, xor_tree

def import_event_log(log_path):
    EVENT_LOG = xes_importer.apply(log_path)
    return EVENT_LOG


def discover_petri_net(tree):
    """
    Given a process tree, the function generates the corresponding petri net. 
    
    Parameters:
        tree (ProcessTree): The discovered process tree from the given event log
        
    Returns:
        net (PetriNet): Generated Petri net of the log
        im (Marking) : Initial marking of the generated Petri net
        fm (Marking) : Final marking of the generated Petri net
    """
    orig_net = None
    im = None
    fm = None
    settings.sink_dict = {}
    settings.src_dict = {}
    
    orig_net, im, fm  = apply(tree)
    
    settings.PETRI_NET_ORIG = orig_net
    settings.I_MARKS_ORIG = im 
    settings.F_MARKS_ORIG = fm
    
    settings.PETRI_NET = orig_net
    return orig_net, im, fm


def discover_process_tree(log):
    """
    Given an event log, the function discovers the process tree using inductive miner algorithm. 
    
    Parameters:
        log (EventLog): Given event log
        
    Returns:
        tree (ProcessTree): The generated Process tree from the log
    """
    tree = inductive_miner.apply_tree(log)
    settings.PROCESS_TREE = tree
    return tree


def export_pnml(precise_net, im, fm, net_name=None):
    """
    The function exports the Petri net in pnml format and saves it in current directory
    
    Parameter:
        precise_net (PetriNet) :  Petri net model to be stored in .pnml format
        im (Marking) :  Initial marking of the generated Petri net
        fm (Marking) :  Final marking of the generated Petri net 
        net_name (str) : Any prefered name to be stored, by default it is the log name
    
    Returns:
        pnml_path (str): The path of the saved Petri net model in .pnml form
    """
    if net_name == None:
        net_name = f"{settings.EVENT_LOG_NAME}"
        net_name = net_name.rsplit('.', 1)[0]
        net_name = net_name+".pnml"
    
    settings.PNML_PATH = None
    log_path = os.path.dirname(copy.deepcopy(settings.EVENT_LOG_PATH))
    pnml_path = os.path.join(log_path, net_name)
    pnml_exporter.apply(precise_net, im, pnml_path)
    pnml_exporter.apply(precise_net, im, pnml_path , final_marking=fm)
    settings.PNML_PATH = pnml_path
    return pnml_path


def get_xor_trees(pt, xor_tree = None):
    """
        Given a process tree, it extracts all XOR block from the process tree
        
        Parameter:
            pt (ProcessTree) : Generated process tree from the log
            xor_tree (list) : All XOR blocks list, at the beginning it is empty
        
        Returns:
            xor_tree (str): All extracted XOR blocks from the process tree     
    """
    
    xor_tree = xor_tree if xor_tree is not None else {}
    if pt.operator != None:
        for node in pt.children:
            if node.operator != None and node.operator == pt_op.XOR and not check_for_tau(node):
                xor_tree[f'X{len(xor_tree)+1}'] = node
            else:
                xor_tree = get_xor_trees(node, xor_tree)
                                               
    return xor_tree


def get_candidates(node1, node2):
    """
    Given two XOR branches, checks whether the given branches are in sequential order.
    
    Parameter:
        node1 (ProcessTree) : Source XOR blocks
        node2 (ProcessTree) : All XOR blocks list, at the beginning it is empty
    
    Returns:
        XOR_source (list) : source branches of the candidate XOR blocks pair
        XOR_target (list) : target branches of the candidate XOR blocks pair
    """
    XOR_source = []
    XOR_target = []
    if util.common_ancestor(node1, node2).operator == pt_op.SEQUENCE:
        XOR_source = get_xor_children(node1, XOR_source)
        XOR_target = get_xor_children(node2, XOR_target)
        
    return XOR_source, XOR_target


def get_ancestors_operator(t, until, include_until = True):
    """
    Given an XOR block and lowest common ancestor(LCA), 
    the method returns all operators present in the path from XOR branch to LCA, adapted from PM4Py.
    
    Parameter:
        t (ProcessTree) : Source XOR block 
        until (ProcessTree) : LCA of those XOR blocks
    
    Returns:
        ancestors (Operator): All operators present in the path from XOR block to the given LCA
    """
    ancestors = list()
    if t == until:
        return ancestors
    parent = t.parent
    while parent != until:
        ancestors.append(parent.operator)
        parent = parent.parent
        if parent is None:
            return None
    if include_until:
        ancestors.append(until.operator)
    return ancestors


def get_lift(pair, confidence, variants, total):
    """
    Given a long-term dependency rules, confidence value of the rule,
    It calculates the lift of the rule.
    
    Parameter:
        pair (dict) : Long-term dependency rules
        confidence (str) : Confidence of the rule
        variants (dict) : Unique traces with the count of those traces
        total (str) : Total number of traces in Event log
    
    Returns:
        lift (str): Lift value of the rule
    """
    rhs_c = 0
    for item in variants:
        for i in range(0, len(pair[1])):
            if not repr(pair[1][i]) in item['variant']: 
                continue
            else:
                rhs_c += item['count']
                break
    sup_c = round((rhs_c / total),3)
    lift = round((confidence / sup_c), 3)
    return lift


def get_support_updated(pair, variants, total, source, target):
    """
    Given a long-term dependency rules, variants of the event log and total number of traces
    It calculates the support value of the rule.
    
    Parameter:
        pair (dict) : Long-term dependency rules
        variants (dict) : Unique traces with the count of those traces
        total (str) : Total number of traces in Event log
        source (list) : All source XOR branches
        target (list) : All target XOR branches
    
    Returns:
        sup (dict): Support value of the rule
    """
    lhs_c = 0
    rule_count = 0
    l_found = 0
    r_found = 0
    sup = {}
    for item in variants:
        trace = item['variant'].split(",")
        #added line
        temp_src = [str(i) for i in pair[0]]
        temp_tgt = [str(i) for i in pair[1]]
        
        for i in range(0, len(trace)):
            if not str(trace[i]) in temp_src:#repr(pair[0]):
                continue
            else:
                l_found = 1
                track = 0
                for j in range(i, len(trace)):
                    track = j
                    if str(trace[j]) in temp_tgt:#repr(pair[1]):
                        if l_found:
                            r_found = 1
                            rule_count += item['count']
                            i = j
                            break
                    else:
                        if str(trace[j]) in list(str(source)) and str(trace[j]) not in temp_src: #repr(pair[0]):
                            l_found = 0
                            break
                 
                if track == len(trace) - 1:
                    break

            if l_found and r_found:
                break
                               
    sup[tuple(pair[0]), tuple(pair[1])] = round((rule_count / total), 3) 
    return sup


def get_confidence(pair, sup, variants, total):
    """
    Given a long-term dependency rules, variants of the event log and total number of traces
    It calculates the support value of the rule.
    
    Parameter:
        pair (dict) : Long-term dependency rules
        support (dict) : support of the rule
        variants (dict) : Unique traces with the count of those traces
        total (str) : Total number of traces in Event log
    
    Returns:
        conf (str): Confidence value of the rule
    """
    lhs_c = 0
    for item in variants:
        trace = item['variant'].split(",")
        for i in range(0, len(pair[0])):
            if not repr(pair[0][i]) in trace:#item['variant']: 
                continue
            else:
                lhs_c += item['count']
                break
    sup_c = round((lhs_c / total),3)
    conf = round((sup / sup_c), 3)
    return conf


def check_for_tau(tree):
    """
    Given a process tree, this function checks whether invisible node exists in the tree.
    
    Parameter:
        tree (ProcessTree): Generated Process tree for the given log
    
    Returns:
        bool : True if tau exists, else False
    """
    for node in tree.children:
        leaves = util.get_leaves(node)
        if len(leaves) == 1:
            for leaf in leaves:
                if util.is_tau_leaf(leaf):
                    return True
                

def get_xor_children(node, xor_list=None):
    """
    Given a process tree, this function returns the activity involved in the tree.
    
    Parameter:
        xor_list (list): Activity involved in the branch tree
    
    Returns:
        bool : True if tau exists, else False
    """
    xor_list = xor_list if xor_list is not None else {}
    for child in node.children:
        if len(get_xor_leaves(child)) > 0:
            xor_list.append(get_xor_leaves(child))
    return xor_list


def get_xor_leaves(xor_tree, leaves=None):
    """
    Given a xor tree, this function returns the leaves of the tree.
    
    Parameter:
        xor_tree (ProcessTree): XOR block
    
    Returns:
        leaves (list) : Leaves of the XOR trees
    """
    
    tau_exist = 0
    leaves = leaves if leaves is not None else []
    if len(xor_tree.children) == 0:
        if xor_tree.label is not None:
            leaves.append(xor_tree)
    else:
        for c in xor_tree.children:
            leaves = get_xor_leaves(c, leaves)
    return leaves

def repair_petri_net(support, confidence, lift, sound):
    """
    Given a Petri net and threshold values, the functions repair the free-choice Petri net
    
    Parameter:
        support (str): Threshold value for support
        confidence (str) : Threshold value for confidence 
        lift (str): Threshold value for confidence 
        sound (str) : sound model requirement Yes/No    
    
    Returns:
        net_path (str) : Path of the .SVG file generated for the repaired net
        precision (float): Improved precision value
        fitness (float): Fitness of the repaired Petri net
        rules (dict): Rules added to the repaired precise net
        pnml_path (str) : Path of the .pnml file generated for the repaired net
    """
    p_net = None
    im = None
    fm = None
    repaired_net = None
    sound_net = None
    
    p_net, im, fm = discover_petri_net(settings.PROCESS_TREE)

    rules_dict = dict(settings.RULES_DICT)
    
    if sound == 'on':
        print("Sound Model Requirement is On") 
        rules_dict_sound = soundness_at_XOR_tree(rules_dict)
    else:
        print("Sound Model Requirement is Off") 
        rules_dict_sound = rules_dict
    
    repair_net = 1
    
    rules_dicti = {}
    if rules_dict_sound != {}:
        for pair, value in rules_dict_sound.items():
            rules_dicti.update(value)
        
        if sound == 'on':
            maxi = list()
            for key, value in rules_dict_sound.items():
                for k, v in value.items():
                    if k == 'Max':
                        maxi.append(v)
                
            if max(maxi) < float(lift):
                repair_net = 0
                settings.RULES = {}
                
        del rules_dicti['Max']
    
    if repair_net:
        repaired_net = None
        if sound == 'on':
            sound_net = discover_sound_petrinet(rules_dicti, p_net)
            repaired_net, rules = repair_sound_Model(sound_net, rules_dicti, support, confidence, lift, sound)
            check_soundness(repaired_net, im, fm)
        else:
            repaired_net, rules = repair_unsound_model(p_net, rules_dicti, support, confidence, lift)
    
    settings.PETRI_NET = None
    settings.PETRI_NET = repaired_net
    settings.RULES = rules
        
    precision = get_precision(settings.PETRI_NET ,im, fm)
    fitness = get_fitness(settings.PETRI_NET, im, fm)
    

    net_path = display_petri_net(settings.PETRI_NET)
    pnml_path = export_pnml(settings.PETRI_NET, im,fm)

    return net_path, round(precision,2), round(fitness['average_trace_fitness'], 2), settings.RULES, pnml_path

def get_soundness():
    """
    Returns the soundness of the model.
    """
    return check_soundness(settings.PETRI_NET, settings.I_MARKS_ORIG, settings.F_MARKS_ORIG)
    

def get_precision(pn_net, im, fm):
    """
    Returns the precision of the model.
    Parameter: 
        net (PetriNet): Generated Petri net of the log
        im (Marking) : Initial marking of the generated Petri net
        fm (Marking) : Final marking of the generated Petri net
    Return:
        Precision (float) : Precision value measured using pm4py 
    
    """
    log = settings.EVENT_LOG
    prec = precision_evaluator.apply(log, pn_net, im, fm, variant=precision_evaluator.Variants.ALIGN_ETCONFORMANCE)
    return prec

def get_fitness(net, im, fm):
    """
    Returns the precision of the model.
    Parameter: 
        net (PetriNet): Generated Petri net of the log
        im (Marking) : Initial marking of the generated Petri net
        fm (Marking) : Final marking of the generated Petri net
    Return:
        Fitness (float) : Fitness value measured using pm4py 
    
    """
    log = settings.EVENT_LOG
    fitness = replay_fitness_evaluator.apply(log, net, im, fm, variant=replay_fitness_evaluator.Variants.ALIGNMENT_BASED)
    return fitness


def repair_unsound_model(net, rules_dict, support, confidence, lift):
    """
    Repairing a bordered Petri net generated from Process tree to include long-term dependencies in it and
    create a precise Petri net. Soundness parameter is not given.
    
    Parameter: 
        net (PetriNet): Generated Petri net of the log
        rules (dict) : Discovered rules with the association rule metrics values
        support (str): Threshold value for support
        confidence (str) : Threshold value for confidence 
        lift (str): Threshold value for confidence 
    
    Return:
        net (PetriNet): Repaired Petri net of the log
        rules (dict) : Added rules to the net with their association rule metrics values
    """
    
    rules = {}
    for pair, value in rules_dict.items():
        if str(value[2]) > lift and str(value[0]) > support and str(value[1]) > confidence and value[2] > 1.001:
            rules[pair] = value
            trans_exist = 0
            #if the place already exists, We do not need to add new places, just use existing ones
            tau_t = PetriNet.Transition(f"tau_{pair[0]}{pair[1]}", None)
            for trans in net.transitions:
                if str(trans) == str(tau_t):
                    trans_exist = 1
                    break
            if(trans_exist == 0):
                net.transitions.add(tau_t)
                s_place = f"ps_{pair[0]}"
                t_place = f"pt_{pair[1]}"
                source_found = 0
                target_found = 0
                for place in net.places:
                    if place.name == s_place:
                        source_found = 1
                        
                        pn_util.add_arc_from_to(place, tau_t, net)

                    elif place.name == t_place:
                        target_found = 1
                        pn_util.add_arc_from_to(tau_t, place, net)

                    if (source_found and target_found):
                        break
                
                ## Handle Source Side
                # Adding new place after source
                if (not source_found):
                    source = PetriNet.Place(s_place)
                    net.places.add(source)
                    pn_util.add_arc_from_to(source, tau_t, net)
                    all_src = pair[0][1:-1].split(", ")
                    for k,v in settings.sink_dict.items():
                        if all(item in list(map(str,settings.sink_dict[k])) for item in list(all_src)):
                            for t in net.transitions:
                                if str(t) == str(k):
                                    pn_util.add_arc_from_to(t, source, net)
                                    break
                            
                                
                if (not target_found):
                    target = PetriNet.Place(t_place)
                    net.places.add(target)
                    pn_util.add_arc_from_to(tau_t, target, net)
                    all_tgt = pair[1][1:-1].split(", ")
                    for k,v in settings.src_dict.items():
                        if all(item in list(map(str,settings.src_dict[k])) for item in list(all_tgt)):
                            for t in net.transitions:
                                if str(t) == str(k):
                                    pn_util.add_arc_from_to(target, t, net)
                                    break
                    
    return net, rules


def soundness_at_XOR_tree(rules):
    """
    Preserving Soundness between XOR blocks based on the highest lift value.
    
    Parameters:
        rules (dict) : Discovered rules and their XOR blocks
    
    Return:
        Sound XOR blocks pair (dict) : Sound XOR block pairs to be used for generating sound Precise net
    
    """
    sound_xor_rule = {}
    keys_to_be_removed = []
    key_copy = tuple(rules.keys())
    for i in range(len(rules.keys())):
        if len(rules.keys()) != 0:
            sound_xor_rule[next(iter(rules))] = rules[next(iter(rules))]
            for k,v in rules.items():
                if k[0] == list(sound_xor_rule.items())[len(sound_xor_rule)-1][0][0]:
                    keys_to_be_removed.append(k)
                elif k[1] == list(sound_xor_rule.items())[len(sound_xor_rule)-1][0][1]:
                    keys_to_be_removed.append(k)
            for k in keys_to_be_removed:
                if k in rules.keys():
                    del rules[k]
    return sound_xor_rule


def discover_sound_petrinet(rules_dict, net):
    """
    Discover Intermediate Petri net which preserves soundness between XOR branches.
    
    Parameter: 
        rules (dict) : Discovered rules with the association rule metrics values
        net (PetriNet): Generated Petri net of the log
    
    Return:
        net (PetriNet): Intermediate Petri net of the log
    """
    
    for pair in rules_dict:
        trans_exist = 0
        #if the place already exists, We do not need to add new places, just use existing ones
        tau_t = PetriNet.Transition(f"tau_{pair[0]}{pair[1]}", None)
        for trans in net.transitions:
            if str(trans) == str(tau_t):
                trans_exist = 1
                break
        if(trans_exist == 0):
            net.transitions.add(tau_t)
            s_place = f"ps_{pair[0]}"
            t_place = f"pt_{pair[1]}"
            source_found = 0
            target_found = 0
            for place in net.places:
                if place.name == s_place:
                    source_found = 1
                    
                    pn_util.add_arc_from_to(place, tau_t, net)

                elif place.name == t_place:
                    target_found = 1
                    pn_util.add_arc_from_to(tau_t, place, net)

                if (source_found and target_found):
                    break
            
            ## Handle Source Side
            # Adding new place after source
            if (not source_found):
                source = PetriNet.Place(s_place)
                net.places.add(source)
                pn_util.add_arc_from_to(source, tau_t, net)
                all_src = pair[0][1:-1].split(", ")
                for k,v in settings.sink_dict.items():
                    if all(item in list(map(str,settings.sink_dict[k])) for item in list(all_src)):
                        for t in net.transitions:
                            if str(t) == str(k):
                                pn_util.add_arc_from_to(t, source, net)
                                break
                        
                            
            if (not target_found):
                target = PetriNet.Place(t_place)
                net.places.add(target)
                pn_util.add_arc_from_to(tau_t, target, net)
                all_tgt = pair[1][1:-1].split(", ")
                for k,v in settings.src_dict.items():
                    if all(item in list(map(str,settings.src_dict[k])) for item in list(all_tgt)):
                        for t in net.transitions:
                            if str(t) == str(k):
                                pn_util.add_arc_from_to(target, t, net)
                                break
            
    return net

def repair_sound_Model(s_net, rules_dict, support, confidence, lift, sound=1):
    """
    Repairing a bordered Petri net generated from Process tree to include long-term dependencies in it and
    create a precise Petri net. Soundness parameter is a given requirement.
    
    Parameter: 
        net (PetriNet): Generated Petri net of the log
        rules (dict) : Discovered rules with the association rule metrics values
        support (str): Threshold value for support
        confidence (str) : Threshold value for confidence 
        lift (str): Threshold value for confidence 
        sound (str) : Yes
    
    Return:
        net (PetriNet): Repaired Sound Petri net of the log
        rules (dict) : Added rules to the net with their association rule metrics values
    """
    rules = {}
    
    rules_dict = dict(sorted(rules_dict.items(), key=lambda item: item[1][2]))

    for pair, value in rules_dict.items():
        trans = None
        if value[2] < 1.001 or str(value[2]) < lift or str(value[0]) < support or str(value[1]) < confidence:
            tau_t = f"tau_{pair[0]}{pair[1]}"
            for t in s_net.transitions:
                s_place_valid = 0
                t_place_valid = 0
                if str(t) == str(tau_t):
                    trans = t
                    source_places = set([x.source for x in t.in_arcs])
                    for p in source_places:
                        s_place = f"ps_{pair[0]}"
                        if str(p) == s_place:
                            if sound == 'on' and len(p.out_arcs) > 1:
                                s_place_valid = 1
                            elif sound == None:
                                s_place_valid = -1
                                if len(p.out_arcs) == 1:
                                    pn_util.remove_place(s_net, p)
                                    
                        if sound == 'on' and len(p.out_arcs) == 1:
                            rules[pair] = value            
                    target_places =  set([x.target for x in t.out_arcs])   
                    for p in target_places:
                        t_place = f"pt_{pair[1]}"
                        if str(p) == t_place:
                            if sound == 'on' and len(p.in_arcs) > 1:
                                t_place_valid = 1
                            elif sound== None:
                                t_place_valid = -1
                                if len(p.in_arcs) == 1:
                                    pn_util.remove_place(s_net, p)
                            
                            if sound == 'on' and len(p.in_arcs) == 1:
                                rules[pair] = value
                    if s_place_valid==1 and t_place_valid==1:
                        s_net = pn_util.remove_transition(s_net, trans)
                        break
                    elif s_place_valid == -1 and t_place_valid == -1:
                        s_net = pn_util.remove_transition(s_net, trans)
                        break
        else:
            rules[pair] = value
    return s_net, rules


def display_petri_net(net=None):
    """
    The function exports the Petri net in .SVG format and saves it in current directory
    
    Parameter:
        net (PetriNet) :  Petri net model to be stored in .SVG format
    
    Returns:
        net_path (str): The path of the saved Petri net model in .SVG form
    """
    
    if net == None :
        net = settings.PETRI_NET
    
        
    im = settings.I_MARKS_ORIG
    fm = settings.F_MARKS_ORIG
    parameters = {pn_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "SVG"}
    gviz = pn_visualizer.apply(net, im, fm, parameters=parameters)
    log_name = settings.EVENT_LOG_NAME
    log_name = log_name.rsplit('.', 1)[0]
    log_name = log_name.replace(" ", "")
    log_path = os.path.dirname(copy.deepcopy(settings.EVENT_LOG_PATH))
    image_path = os.path.join(log_path, f"{log_name}.SVG")
    pn_visualizer.save(gviz, image_path)
    return image_path


def apply(tree, parameters=None):
    '''
    Generation of bordered Petri net from the given tree, adapted from PM4Py
    Only supports loops with 2 children!
    :param tree:
    :return:
    '''
    net = obj.PetriNet(name=str(tree))
    if len(tree.children) == 0:
        pn_util.add_transition(net, label=tree.label, name=str(id(tree)))
    else:
        sub_nets = list()
        for c in tree.children:
            sub_net, ini, fin = apply(c)
            sub_nets.append(sub_net)
        pn_util.merge(net, sub_nets)
        switch = {
            pt_op.SEQUENCE: construct_sequence_pattern,
            pt_op.XOR: construct_xor_pattern,
            pt_op.PARALLEL: construct_and_pattern,
            pt_op.LOOP: construct_loop_pattern
        }
        net, ini, fin = switch[tree.operator](net, sub_nets)
    if tree.parent is None:
        p_ini = pn_util.add_place(net)
        p_fin = pn_util.add_place(net)
        pn_util.add_arc_from_to(p_ini, _get_src_transition(net), net)
        pn_util.add_arc_from_to(_get_sink_transition(net), p_fin, net)
        return net, obj.Marking({p_ini: 1}), obj.Marking({p_fin: 1})
    return net, obj.Marking(), obj.Marking()


def _get_src_transition(sub_net):
    for t in sub_net.transitions:
        if len(pn_util.pre_set(t)) == 0:
            return t
    return None


def _get_sink_transition(sub_net):
    for t in sub_net.transitions:
        if len(pn_util.post_set(t)) == 0:
            return t
    return None


def _add_src_sink_transitions(net, p_s, p_t):
    src = pn_util.add_transition(net)
    pn_util.add_arc_from_to(src, p_s, net)
    sink = pn_util.add_transition(net)
    pn_util.add_arc_from_to(p_t, sink, net)
    return net, obj.Marking(), obj.Marking()


def construct_sequence_pattern(net, sub_nets):
    places = [None] * (len(sub_nets) + 1)
    for i in range(len(sub_nets) + 1):
        places[i] = pn_util.add_place(net)
    for i in range(len(sub_nets)):
        pn_util.add_arc_from_to(places[i], _get_src_transition(sub_nets[i]), net)
        pn_util.add_arc_from_to(_get_sink_transition(sub_nets[i]), places[i + 1], net)
    src = pn_util.add_transition(net)
    pn_util.add_arc_from_to(src, places[0], net)
    sink = pn_util.add_transition(net)
    pn_util.add_arc_from_to(places[len(places) - 1], sink, net)
    return net, obj.Marking(), obj.Marking()


def construct_xor_pattern(net, sub_nets):
    p_s = pn_util.add_place(net)
    p_o = pn_util.add_place(net)
    for n in sub_nets:
        #settings.src_dict[tuple(n.transitions)] = _get_src_transition(n)
        #settings.sink_dict[tuple(n.transitions)] = _get_sink_transition(n)
        settings.src_dict[_get_src_transition(n)] = n.transitions
        settings.sink_dict[_get_sink_transition(n)] = n.transitions
        pn_util.add_arc_from_to(p_s, _get_src_transition(n), net)
        pn_util.add_arc_from_to(_get_sink_transition(n), p_o, net)
    return _add_src_sink_transitions(net, p_s, p_o)


def construct_and_pattern(net, sub_nets):
    p_s = [None] * len(sub_nets)
    p_t = [None] * len(sub_nets)
    for i in range(len(sub_nets)):
        p_s[i] = pn_util.add_place(net)
        p_t[i] = pn_util.add_place(net)
        pn_util.add_arc_from_to(p_s[i], _get_src_transition(sub_nets[i]), net)
        pn_util.add_arc_from_to(_get_sink_transition(sub_nets[i]), p_t[i], net)
    src = pn_util.add_transition(net)
    for p in p_s:
        pn_util.add_arc_from_to(src, p, net)
    sink = pn_util.add_transition(net)
    for p in p_t:
        pn_util.add_arc_from_to(p, sink, net)
    return net, obj.Marking(), obj.Marking()


def construct_loop_pattern(net, sub_nets):
    assert (len(sub_nets) == 2)
    p_s = pn_util.add_place(net)
    p_t = pn_util.add_place(net)
    pn_util.add_arc_from_to(p_s, _get_src_transition(sub_nets[0]), net)
    pn_util.add_arc_from_to(p_t, _get_src_transition(sub_nets[1]), net)
    pn_util.add_arc_from_to(_get_sink_transition(sub_nets[0]), p_t, net)
    pn_util.add_arc_from_to(_get_sink_transition(sub_nets[1]), p_s, net)
    net, ini, fin = _add_src_sink_transitions(net, p_s, p_t)
    return net, obj.Marking(), obj.Marking()


def deepcopy_net():
    im = obj.Marking()
    fm = obj.Marking()
    p_net = copy.deepcopy(settings.PETRI_NET_ORIG)
    for place in p_net.places:
        for p_ini in settings.I_MARKS_ORIG:
            if str(p_ini) == str(place):
                im = obj.Marking({place : 1})
        for p_f in settings.F_MARKS_ORIG:
            if str(p_f) == str(place):
                fm = obj.Marking({place : 1})
    return p_net, im, fm


if __name__ == "__main__":
    file_path = "<path>\<file>.xes"
    support = "0.2"
    confidence = "0.3"
    lift = "1.0"
    sound = "No"
    
    rules, precision, fitness, net_path, pnml_path =  miner(file_path, support, confidence, lift, sound)
    
    