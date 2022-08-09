import os
import time
import json
from datetime import datetime
from datetime import timedelta

from os.path import expanduser
home = expanduser("~")


directory = home + '/Library/Application Support/EverQuest/PlayerLogs/'



def add_trigger(config_file, trigger_word_dict, add_trigger_command, text):
  #gross
  new_trigger_word = text[text.strip().index(add_trigger_command) + len(add_trigger_command):].strip()
  new_trigger_word = new_trigger_word[:-1]
  print "New Trigger Word: " + new_trigger_word
  trigger_word_dict[new_trigger_word] = datetime.now()

  #opening and writing the file can likely be done as a separate function since it is used in a few places
  with open(config_file, 'r+') as config_file_pointer:
    config = json.load(config_file_pointer)
    trigger_words = set(config["config"]["triggers"]["words"])
    trigger_words.add(new_trigger_word.encode("utf-8"))
    config["config"]["triggers"]["words"] = list(trigger_words)
    config_file_pointer.seek(0)        # <--- should reset file position to the beginning.
    json.dump(config, config_file_pointer, indent=4)
    config_file_pointer.truncate()     # remove remaining part


def remove_trigger(config_file, trigger_word_dict, remove_trigger_command, text):
  removed_trigger_word = text[text.strip().index(remove_trigger_command) + len(remove_trigger_command):].strip()
  removed_trigger_word = removed_trigger_word[:-1]
  trigger_word_dict.pop(removed_trigger_word, 'None')
  
  with open(config_file, 'r+') as config_file_pointer:
    config = json.load(config_file_pointer)
    trigger_words = set(config["config"]["triggers"]["words"])
    if removed_trigger_word in trigger_words: trigger_words.remove(removed_trigger_word)
    config["config"]["triggers"]["words"] = list(trigger_words)
    config_file_pointer.seek(0)        # <--- should reset file position to the beginning.
    json.dump(config, config_file_pointer, indent=4)
    config_file_pointer.truncate()     # remove remaining part
    
    
def add_ignore(config_file, ignore_words, add_ignore_command, text):
  new_ignore_word = text[text.strip().index(add_ignore_command) + len(add_ignore_command):].strip()
  new_ignore_word = new_ignore_word[:-1]

  with open(config_file, 'r+') as config_file_pointer:
    config = json.load(config_file_pointer)
    print "New Ignore Word: " + new_ignore_word
    ignore_words = set(ignore_words)
    ignore_words.add(new_ignore_word.encode("utf-8"))
    config["config"]["ignore"]["words"] = list(ignore_words)
    print "New Ignore Words: " + str(ignore_words)
    config_file_pointer.seek(0)        # <--- should reset file position to the beginning.
    json.dump(config, config_file_pointer, indent=4)
    config_file_pointer.truncate()     # remove remaining part

def remove_ignore(config_file, ignore_words, remove_ignore_command, text):
  removed_ignore_word = text[text.strip().index(remove_ignore_command) + len(remove_ignore_command):].strip()
  removed_ignore_word = removed_ignore_word[:-1]

  with open(config_file, 'r+') as config_file_pointer:
    config = json.load(config_file_pointer)
    print "Removed Ignore Word: " + removed_ignore_word
    ignore_words = set(ignore_words)
    if removed_ignore_word in ignore_words: ignore_words.remove(removed_ignore_word)
    config["config"]["ignore"]["words"] = list(ignore_words)
    print "New Ignore Words: " + str(ignore_words)
    config_file_pointer.seek(0)        # <--- should reset file position to the beginning.
    json.dump(config, config_file_pointer, indent=4)
    config_file_pointer.truncate()     # remove remaining part

def add_timer(timer_list, start_timer_command, text):
  #text must come in the form of #add_timer [word], [time in seconds]
  text = text[text.strip().index(start_timer_command) + len(start_timer_command):].strip().split(',')
  print text
  try:
    alarm_word = text[0].strip()
    seconds_timed = text[1].strip()
    start = datetime.now()
    print start
    end = start + timedelta(seconds=int(seconds_timed[:-1]))
    timer_list.append([alarm_word, end])
    print end
  except:
    print "Timer format incorrect, must be of form #add_timer [word], [time in seconds]"
    pass
  
def not_spam(prev_time, spam_delay):
  
  current_time = datetime.now()
  delta = (current_time - prev_time).seconds
  if delta > int(spam_delay):
    print "Not spam"
    return True
  else:
    print delta
    print spam_delay
    print "Spam"
    return False

#iterates through logs in the PlayerLogs directory and creates a pointer to the last line of each file
#this function needs to be optimized
def get_file_pointers(directory):
    
    file_pointers = []
    
    for file_name in os.listdir(directory):
      file_path = directory + file_name

      try:
        fp = open(file_path, 'r')
        fp.seek(-2, os.SEEK_END) #set file pointer to last line in the file
        file_pointers.append(fp)
      except:
        print file_name + " not readable"
    
    return file_pointers
  
def thread_files(directory):
  
    #####
    ## initialize config here... can this be done in a separate function?
    #####
    config_file = 'eqparse_config.json' #config file must be in the same folder as this script
    config_file_pointer = open(config_file, 'r')

    config = json.load(config_file_pointer)
    #print config
    
    trigger_words = config["config"]["triggers"]["words"]
    print trigger_words
    
    trigger_word_dict = {}
    timer_list = []
    
    for word in trigger_words:
      trigger_word_dict[word] = datetime.now()
    
    ignore_words = config["config"]["ignore"]["words"]
    print ignore_words
    
    add_trigger_command = config["config"]["update_commands"]["add_trigger"]
    print add_trigger_command
    
    remove_trigger_command = config["config"]["update_commands"]["remove_trigger"]
    print remove_trigger_command

    add_ignore_command = config["config"]["update_commands"]["add_ignore"]
    print add_ignore_command

    remove_ignore_command = config["config"]["update_commands"]["remove_ignore"]
    print remove_ignore_command

    start_timer_command = config["config"]["update_commands"]["start_timer"]
    print start_timer_command
    
    spam_delay = config["config"]["spam_delay"]

    config_file_pointer.close()

    file_pointers = get_file_pointers(directory)

    while True:
      line_set = set()
      ignore = False
      

      for fp in file_pointers:
        new = fp.readline()
        line_set.add(new)
    
      if line_set:
        for text in line_set:
          
          if text:
            #This removes the timestamp from being parsed. Highly prone to bugs if log line has additional brackets in it.
            subtext = text.split("]")
            if len(subtext) > 1:
              

          
              if add_trigger_command in text:
                  add_trigger(config_file, trigger_word_dict, add_trigger_command, text)
                  
              if remove_trigger_command in text:
                  remove_trigger(config_file, trigger_word_dict, remove_trigger_command, text)
    
              if add_ignore_command in text:
                  add_ignore(config_file, ignore_words, add_ignore_command, text)
                  
              if remove_ignore_command in text:
                  remove_ignore(config_file, ignore_words, remove_ignore_command, text)
    
              if start_timer_command in text:
                  add_timer(timer_list, start_timer_command, text)
                  print timer_list
              
              first_word = subtext[1].split(" ")[1]
              #Could be smarter. Create a list of currently played character names based on active logs i.e. Taelor, Sayil, Lucid
              #check if first_word in active_chars
              
              if first_word == "Taelor":
                print "ignoring line: " + text
                
              else:
                for timer in timer_list:
                  if (timer[1] - datetime.now()).seconds <= 5:
                    os.system("say 5 seconds " + timer[0])
                    timer_list.remove(timer)
                    
                for word in trigger_word_dict.keys():
                  for ignore_word in ignore_words:
                    if ignore_word in text:
                      ignore = True
                  try:
                    prev_time = trigger_word_dict[word]
                    if word in text and not ignore and not_spam(prev_time, spam_delay):
                      print "First word is: " + first_word
                      print text
                      trigger_word_dict[word] = datetime.now()
                      os.system("say " + word)
                  except:
                    pass

      else:
        time.sleep(1)


thread_files(directory)
