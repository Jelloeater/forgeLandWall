-- ###GET
-- "/get/numberOfPostsToGetAsJSON"
-- "/query/messageToSearchFor"
-- "/msg/IndexOfMessageToGet"
-- ###POST
-- "/post"
-- create=newMessage
-- delete=indexToDelete
-- edit=newMessage&index=indexToEdit

os.loadAPI('jsonV2')

-----------------------------------------------------------------------------------------------------------------------
-- Settings Class
settings = {}  -- the table representing the class, holds all the data, we don't need a singleton because THIS IS LUA.
settings.serverURL = 'http://127.0.0.1:9000'

-----------------------------------------------------------------------------------------------------------------------
-- Message Class
local Message = {}  -- the table representing the class, which will double as the metatable for the instances
Message.__index = Message -- failed table lookups on the instances should fallback to the class table, to get methods

function Message.new(message, timestamp, index)
	local self = setmetatable({},Message) 
	-- Lets class self refrence to create new objects based on the class	
	self.message = message or nil
	self.timestamp = timestamp or nil
	self.index = index or nil
	return self
end


function createMessage()
	print("Enter index to be removed: ")
	local message = read()
	http.post(settings.serverURL..'/post','create='..message)
end

function removeMessage()
	print("Enter index to be removed: ")
	local removeIndex = read()
	http.post(settings.serverURL..'/post','delete='..removeIndex)
end

function editMessage( )
	-- edit=newMessage&index=indexToEdi

end

function getMessages(numberToGet)
	-- Gets message table
	x = http.get(settings.serverURL..'/get/'.. numberToGet)
	jsonStr = x.readAll()
	jsonObj = jsonV2.decode(jsonStr)

	messageTable = {} -- Clears the table
	for i=1,table.getn(jsonObj) do
		table.insert(messageTable, Message.new(
			jsonObj[i].message, jsonObj[i].timestamp,jsonObj[i].index))
	end
end




function main( ... )
	getMessages()
	


	-- print(jsonObj.readAll())

	x = http.get('http://127.0.0.1:9000/msg/2')
	jsonStr = x.readAll()
	-- print(jsonStr)
	jsonObj = jsonV2.decode(jsonStr)
	print (jsonObj.message)

	x = http.get('http://127.0.0.1:9000/query/me')
	jsonStr = x.readAll()
	-- print(jsonStr)
	jsonObj = jsonV2.decode(jsonStr)
	for i=1,table.getn(jsonObj) do
		print(jsonObj[i].index .. " "..jsonObj[i].message .. " ".. jsonObj[i].timestamp)
	end

	msgIn = read()
	http.post('http://127.0.0.1:9000/post','create='..msgIn)

end




main()


