# PythonChatLocalhost
Locally hosted python server for chatting 

HELLO-FROM <name>\n Client First hand-shake message.
HELLO <name>\n Server Second hand-shake message.
WHO\n Client Request for all currently logged-in users.
WHO-OK <name1>,...,<namen>\n Server A list containing all currently logged-in users.
SEND <user> <msg>\n Client A chat message for a user. Note that the
message cannot contain the newline character,
because it is used as the message delimiter.
SEND-OK\n Server Response to a client if their ‘SEND’ message
is processed successfully.
UNKNOWN\n Server Sent in response to a SEND message to
indicate that the destination user is not
currently logged in.
DELIVERY <user> <msg>\n Server A chat message from a user.
IN-USE\n Server Sent during handshake if the user cannot log
in because the chosen username is already in
use.
BUSY\n Server Sent during handshake if the user cannot log
in because the maximum number of clients
has been reached.
BAD-RQST-HDR\n Server Sent if the last message received from the
client contains an error in the header.
BAD-RQST-BODY\n Server sent if the last message received from the
client contains an error in the body.
