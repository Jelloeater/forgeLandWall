print ("Enter IP address")
ip = read()
print ("Enter Port")
port = read()

url = "http://"..ip..":"..port
print("Connecting to: " .. url)

while true do
	print ("Enter POST data")
	postData = read()
	http.post(url, postData)
end