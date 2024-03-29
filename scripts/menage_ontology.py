#!/usr/bin/env python2

## @package exprob_ass1
#
# \file menage_ontology.py
# \brief script to load the cluedo_ontology, to upload the TBox and randomly generate the hypotheses of the game
#
# \author Serena Paneri
# \version 1.0
# \date 11/11/2022
# \details
#
# Subscribes to: <BR>
#     None
#
# Publishes to: <BR>
#     None
#
# Serivces: <BR>
#     None
#
# Client Services: <BR>
#     armor_interface_srv
#
# Action Services: <BR>
#     None
#
# Description: <BR>
#    In this node are defined all the list of individuals, divided in people, weapons and places.
#    In addition we also have a list that contains all the possible ID associated to each hypothesis
#    of the game, and the values of all those lists are stored in a parameter server.
#    This node contains a client for the ARMOR service, to be able to menage the cluedo_ontology.
#    In this node, in particular, the cluedo_ontology is loaded, all the individuals of the
#    game are upload in the ontology, thus forming the TBox of the ontology, the individuals of each
#    class are disjoint from each other and the resoner is started to update the knowledge.
#    Finally a set of random hypothesis is generated and it includes four complete and consistent
#    hypotheses, three uncomplete hypotheses and three complete but inconsistent hypotheses.
#    Then these hypotheses are stored into a parameter server.
 

import rospy
import random
from random import randint
from armor_msgs.srv import *
from armor_msgs.msg import * 

# lists of the individuals of the cluedo game
people = ['Rev. Green', 'Prof. Plum', 'Col. Mustard','Msr. Peacock', 'Miss. Scarlett', 'Mrs. White']
weapons = ['Candlestick', 'Dagger', 'Lead Pipe', 'Revolver', 'Rope', 'Spanner']
places = ['Conservatory', 'Lounge', 'Kitchen', 'Library', 'Hall', 'Study', 'Ballroom', 'Dining room', 'Billiard room']

# list of the ID associated to each hypothesis of the game
ID = ['0000', '0001', '0002', '0003', '0004', '0005', '0006', '0007', '0008', '0009']

# setting the ros parameters of the lists above
rospy.set_param('people', people)
rospy.set_param('weapons', weapons)
rospy.set_param('places', places)
rospy.set_param('ID', ID)

armor_interface = None
hypotheses = []

##
# \brief The main function initializes and handles the client of the ARMOR service.
# \param: None
# \return: None
#
# This is the main function of the node where the node is initialized and handles the client of the
# ARMOR service. It also calls the other functions to load the cluedo_ontology, to upload the Tbox 
# and then it starts the reasoner menage the knowledge of the ontology.
def main():

    global armor_interface
    # initializing the menage_ontology node
    rospy.init_node('menage_ontology')
    
    # armor service
    rospy.wait_for_service('armor_interface_srv')
    print('Waiting for the armor service')
    armor_interface = rospy.ServiceProxy('armor_interface_srv', ArmorDirective)
    
    # loading the cluedo ontology
    load()
    # adding the individuals in the TBox
    tbox()
    # reason 
    reasoner()
    # disjoint the individuals of all the classes
    disjoint_individuals()
    # reason
    reasoner()
    # generating all the hypotheses of the game
    all_hypotheses()
    
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Stopping")

##
# \brief The load function loads the cluedo_ontology.
# \param: None
# \return: None
#
# This function is used to load the cluedo_ontology.
def load():

    req = ArmorDirectiveReq()
    req.client_name = 'menage_ontology'
    req.reference_name = 'cluedontology'
    req.command = 'LOAD'
    req.primary_command_spec = 'FILE'
    req.secondary_command_spec = ''
    req.args = ['/root/ros_ws/src/exprob_ass1/cluedo_ontology.owl', 'http://www.emarolab.it/cluedo-ontology', 'true', 'PELLET', 'true']
    msg = armor_interface(req)
    res = msg.armor_response  


##
# \brief The load function loads the cluedo_ontology.
# \param: None
# \return: None
#
# This function is used to upload all the individuals of all classes in the ontology.
def tbox():

    global people, weapons, places
    req = ArmorDirectiveReq()
    req.client_name = 'menage_ontology'
    req.reference_name = 'cluedontology'
    req.command = 'ADD'
    req.primary_command_spec = 'IND'
    req.secondary_command_spec = 'CLASS'
    
    # individuals of the class suspected person
    for person in people:
    	req.args = [person, 'PERSON']
    	msg = armor_interface(req)
    	res = msg.armor_response
    print('The suspects have been uploaded in the TBox')
    
    # individuals of the class probable implements
    for weapon in weapons:
        req.args = [weapon, 'WEAPON']
        msg = armor_interface(req)
        res = msg.armor_response
    print('The implements have been uploaded in the TBox')
    
    # individuals of the class suspected scenes of murder
    for place in places:
        req.args = [place, 'PLACE']
        msg = armor_interface(req)
        res = msg.armor_response
    print('The scenes of murder have been uploaded in the TBox')


##
# \brief The disjoint_individuals function disjoints the individuals of a class.
# \param: None
# \return: None
#
# This operation needs to be done in order to disjoint the individuals belonging to each class, 
# from each other.
def disjoint_individuals():

    req = ArmorDirectiveReq()
    req.client_name = 'menage_ontology'
    req.reference_name = 'cluedontology'
    req.command = 'DISJOINT'
    req.primary_command_spec = 'IND'
    req.secondary_command_spec = 'CLASS'
    req.args = ['PERSON']
    msg = armor_interface(req)
    res = msg.armor_response
    print('The individuals of the class PERSON have been disjoint')
    req.args = ['WEAPON']
    msg = armor_interface(req)
    res = msg.armor_response
    print('The individuals of the class WEAPON have been disjoint')
    req.args = ['PLACE']
    msg = armor_interface(req)
    res = msg.armor_response
    print('The individuals of the class PLACE have been disjoint')


##
# \brief The reasoner of the ontology.
# \param: None
# \return: None
#
# This function implements the reasoner of the ontology that needs to be started in order to update
# the knowledge of the ontology.
def reasoner():

    req = ArmorDirectiveReq()
    req.client_name = 'menage_ontology'
    req.reference_name = 'cluedontology'
    req.command = 'REASON'
    req.primary_command_spec = ''
    req.secondary_command_spec = ''
    msg = armor_interface(req)
    res = msg.armor_response
          

##
# \brief The reasoner of the ontology.
# \param: None
# \return: hypotheses
#
# This function generates random hypotheses for the game. Some of them are complete and consistent, 
# some of them are uncomplete and some of them are complete but inconsistent. These hypotheses are then
# stored in the parameter server called hypo.
def all_hypotheses():

    hypotheses = [[] for _ in range(10)]
    
    # complete and consistent hypotheses
    hypotheses[0].append(random.choice(people))
    hypotheses[0].append(random.choice(weapons))
    hypotheses[0].append(random.choice(places))
    hypotheses[0].append('0000')
     
    hypotheses[1].append(random.choice(people))
    hypotheses[1].append(random.choice(weapons))
    hypotheses[1].append(random.choice(places))
    hypotheses[1].append('0001')
    
    hypotheses[2].append(random.choice(people))
    hypotheses[2].append(random.choice(weapons))
    hypotheses[2].append(random.choice(places))
    hypotheses[2].append('0002')
     
    hypotheses[3].append(random.choice(people))
    hypotheses[3].append(random.choice(weapons))
    hypotheses[3].append(random.choice(places))
    hypotheses[3].append('0003')
    
    # uncomplete hypotheses 
    hypotheses[4].append(random.choice(people))
    hypotheses[4].append(random.choice(places))
    hypotheses[4].append('0004')
    
    hypotheses[5].append(random.choice(weapons))
    hypotheses[5].append(random.choice(places))
    hypotheses[5].append('0005')
    
    hypotheses[6].append(random.choice(people))
    hypotheses[6].append(random.choice(weapons))
    hypotheses[6].append('0006')
     
    # inconsistent hypotheses
    hypotheses[7].append(random.choice(people))
    hypotheses[7].append(random.choice(weapons))
    hypotheses[7].append(random.choice(weapons))
    hypotheses[7].append(random.choice(places))
    hypotheses[7].append('0007')
    
    hypotheses[8].append(random.choice(people))
    hypotheses[8].append(random.choice(weapons))
    hypotheses[8].append(random.choice(places))
    hypotheses[8].append(random.choice(places))
    hypotheses[8].append('0008')
    
    hypotheses[9].append(random.choice(people))
    hypotheses[9].append(random.choice(people))
    hypotheses[9].append(random.choice(people))
    hypotheses[9].append(random.choice(weapons))
    hypotheses[9].append(random.choice(places))
    hypotheses[9].append(random.choice(places))
    hypotheses[9].append('0009')
    
    # setting the ros parameter of the random hypotheses
    rospy.set_param('hypo', hypotheses)
    return hypotheses
    
if __name__ == '__main__':
    main()
