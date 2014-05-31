# A Computercraft web based Todo List
## About:

This application allows a computer craft computer to submit a various commands to interact with a web server, generating a text via a SQLLite database... It's a task / message list.

FYI the computercaft client is located in the /cc directory

## API
###GET
"/get/numberOfPostsToGetAsJSON"
"/query/messageToSearchFor"
(Entry not found returns "]")
"/msg/IndexOfMessageToGet"
###POST
"/post" (Ex returns "Request Received (create=newMessage) : [indexesThatMatchInput]")
create=newMessage
delete=indexToDelete
edit=newMessage&index=indexToEdit

## Licence / copying:
If you fork me, at least let me know, it's polite. Plus I'd love to see what you do with my code.