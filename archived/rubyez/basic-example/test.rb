=begin
  Require the inital packages that are required for this tool    
=end
require 'pp' #Allows for pretty printing of output
require 'yaml' #Parser toolset for YAML language
require 'net/netconf/jnpr' #Allows for netconf connection
require 'junos-ez/stdlib' #Lib to simplify 
require 'junos-ez/srx'

# login information for NETCONF session 
#
login = { :target => '172.21.203.91', :username => 'root',  :password => 'juniper123',  }
#
# ## create a NETCONF object to manage the device and open the connection ...
#
 ndev = Netconf::SSH.new( login )
 $stdout.print "Connecting to device #{login[:target]} ... "
 ndev.open
 $stdout.puts "OK!"
#
# ## Now bind providers to the device object.
# ## the 'Junos::Ez::Provider' must be first before all others
# ## this provider will setup the device 'facts'.  The other providers
# ## allow you to define the instance variables; so this example
# ## is using 'l1_ports' and 'ip_ports', but you could name them
# ## what you like, yo!
#
Junos::Ez::Provider( ndev )
# Junos::Ez::L1ports::Provider( ndev, :l1_ports )
# Junos::Ez::IPports::Provider( ndev, :ip_ports )
Junos::Ez::SRX::Zones::Provider( ndev, :zones )
# Junos::Ez::SRX::Policies::Provider( ndev, :policies )
#
# ## drop into interactive mode to play around ... let's look
# ## at what the device has for facts ...
#
# #->  
pp ndev.zones.list
# #->  ndev.facts.catalog
# #->  ndev.fact :version
#
# ## now look at specific providers like the zones and policies
#
# #-> ndev.zones.list
# #-> ndev.zones.catalog
#
# binding.pry
#
# ndev.close
