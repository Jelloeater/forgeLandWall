print ("Enter IP address")
ip = read()
print ("Enter Port")
port = read()

url = "http://"..ip..":"..port
print("Connecting to: " .. url)

while true do
	print ("Enter POST data")
    --noinspection GlobalCreationOutsideO
    postData = read()
	http.post(url, postData)
end


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


x = http.get('http://127.0.0.1:9000/get/2')
jsonStr = x.readAll()
-- print(jsonStr)
jsonObj = jsonV2.decode(jsonStr)
for i=1,table.getn(jsonObj) do
    print(jsonObj[i].index .. " "..jsonObj[i].message .. " ".. jsonObj[i].timestamp)
end
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