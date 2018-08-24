#Python SIP cllient *****Group 5*****
import pjsua as sf
import time
import threading
import sys


# Printing log of callback class

def cblog(lvl,str,len):
    
  print(str),



# Defining ActCB class to get notifications of registration
class ActCB(sf.AccountCallback):
      
  def __init__(self, acc):

    sf.AccountCallback.__init__(self, acc)


#  Defining Callbackcall class For receiving call events from Call

class Callbackcall(sf.CallCallback):
      
  def __init__(self, cl=None):

	  sf.CallCallback.__init__(self, cl)




  def crr_st(self):

    print("Call State is: " + self.call.info().state_text)

    print("The Last code was:", self.call.info().last_code)

    print("||" + self.call.info().last_reason + "||")

     
# to get notifications on change in call media state

  def curr_mediastate(self):
	
    global x

    if (self.call.info().media_state == sf.Mediatate_ACTIVE):

	   # Connect the sound device to call

	   callslot = self.call.info().conf_slot

	   x.cnf_connect(callslot, 0)
	   x.cnf_connect(0, callslot)

	   print(" Hey hope u are good")

	   print(x)

# Start of main loop

try:

  #starting main class

  # Creating instance of Lib of module pjsua in x

  x = sf.Lib()

  # Instantiating default configurations
    
  x.init( log_cfg = sf.LogConfig(level=3 , callback= cblog))

  # Configuring traffic object to listen SIP's port 5060 and UDP

  tc= sf.TransportConfig()

  print("*********************************   WELCOME TO MY SIP CLIENT   ********************************")
  print("\n\n")
  
  print("***********************************************************************************************")
  print("\n\n")
  print("*********This is a personalised SIP client for Domain: 192.168.110.135 with SIP port 5060******")
  print("\n\n")
  print("----------                 Please begin registration as guided below:                ----------")
  

  tc.port = 5060
  
 


  #taking user's IP address
  uip= raw_input("Enter the user's IP address:")

  tc.bound_addr = uip

  trans=x.create_transport(sf.TransportType.UDP, tc)




  # Starting lib's instance

  x.start()
  x.set_null_snd_dev()


  # Gathering information to register at SIP server and construct SIP header


  dom= "192.168.110.135"
  #Authentication
  print("*********************************** Let's authenticate you ***********************************")
  user= raw_input("Please enter the Username :")
  psw= raw_input("Please enter the password for " + user +  ":")
  disp = raw_input("Do you want your Username to be your Displayname?[Y/N]")

  if (disp == "y" or disp == "Y"):
    disp= user

  else: 
    disp = raw_input("Please enter the desired Display Name for " + user+ "  :")


  ac= sf.AccountConfig(domain= dom, username= user, password= psw, display= disp)  # configuring SIP based on input

  ac.id=  "sip:"+user
  ac.reg_uri= "sip:"+dom+":5060" 
  ac_callback = ActCB(ac)

  acct = x.create_account(ac,cb=ac_callback)

  acct.set_callback(ac_callback)

  print("\n")

  print("*******Registration Complete*******")

  print('Status= ',acct.info().reg_status, \

        '(' + acct.info().reg_reason + ')')



  y = raw_input("Do you want to make call right now?  [Y/N] ")
  print("\n\n\n")

  if (y==y or y==Y):
	  u= raw_input("Enter the destination username")
          d= "sip:"+u+"@"+dom+":5060"
	  call = acct.make_call(d, Callbackcall())
	  # Waiting for exit command from client
	  print("Press <ENTER> to exit and destroy library")
	  input= sys.stdin.readline().rstrip("\r\n")
	  # Shutting down the library
	  x.destroy()
	  x = None

  else:	
	  print("**********Client Unregistering**********")
	  time.sleep(2)
	  print("**********Deleting Created Libraries")
	  time.sleep(2)
	  x.destroy()
	  x = None
	  sys.exit(1)


except sf.Error as e:

  print("Exception: " + str(e))

  x.destroy()

  x = None

  sys.exit(1)
