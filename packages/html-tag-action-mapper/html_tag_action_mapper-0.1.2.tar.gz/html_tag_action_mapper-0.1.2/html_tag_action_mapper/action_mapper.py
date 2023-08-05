import json
import os
class ActionMapper:
    """
    Instantiate the tag2action dictionary.
    
    """
    
    def __init__(self):
        try : 
            self.tag2actions = json.load(open("./html_tag_action_mapper/static/tag2action.txt"))
        except:
            print("dictionary empty. initializing...")
            self.tag2actions = {}
        
    def save_all(self):
        """
        save the new tag action pairs to the dictionary
        """
        try:
            json.dump(self.tag2actions, open("./html_tag_action_mapper/static/tag2action.txt",'w'))
            return 0
        except : 
            print("there was an unexpected problem")
            return -1

    def get_tags(self):
        return self.tag2actions.keys()
       
    def get_actions(self, tag):
        """
        return the actions possible for a given tags

        :param tag: The tag to add.
        :type tag: string
        
        :param actions: The list of actions.
        :type tag: list of string
        """
        if tag in self.tag2actions.keys() :
            return self.tag2actions[tag]
        else : 
            print("tag not found")
            return None
    
    def add_tag(self, tag, actions):
        """
        Adds a tag and its list of actions it saves.
        
        :param tag: The tag to add.
        :type tag: string
        
        :param actions: The list of actions.
        :type tag: list of string
    
        """
        
        self.tag2actions[tag] = actions
        
        
        