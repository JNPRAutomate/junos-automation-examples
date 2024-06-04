#Require the inital packages that are required for this tool    
require 'pp'                #Allows for pretty printing of output
require 'net/netconf/jnpr'  #Allows for netconf connection
require 'junos-ez/stdlib'   #Library to simplify junos management
require 'junos-ez/srx'      #Library to simplify srx management

# login information for NETCONF session 
#
login = { :target => '10.0.1.161', :username => 'root',  :password => 'PiZZ@!@#!@#',  }

#create a connection object
dev = Netconf::SSH.new( login )

print "Connecting to device #{login[:target]} ... "
#open connection to SRX
dev.open()
puts "OK!"

#Bind provider to our connection
#This basic provider gives us facts about the device
Junos::Ez::Provider( dev )
#Add a new provider for zones
Junos::Ez::SRX::Zones::Provider( dev, :zones )
#Add a new provider for the config
#Junos::Ez::Config::Utils( dev, :cu )

#Prints out the device facts in a pretty formated way
#pp dev.facts.catalog

#Prints out the zones list in a pretty formatted way
print dev.zones.catalog

#Close the netconf connection to the SRX
dev.close
