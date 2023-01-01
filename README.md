# Online-Chatroom
 an online chatroom using TCL 4G LTE Linkhub. The functions included private messages, file/image transmission, and self-defined user interfaces.
 
 **Please refer to report.pdf for detailed information.**
 
 # Introduction

- User Guide:
Enter your computer’s IP and port in the code
Make sure the server and the clients(no limited number) use the same internet
The server will request you to enter your name and let everyone else in the chat room know
Press ‘Enter’ or ‘Send’ Button to send your message

- Other Functions:
  - Thumb up: randomly generate positive comments
  - Encode and Decode:
    - encode:After striping the punctuation and lower the alphabets, encode your message with ‘0’ and ‘1’ with designed Huffman code (26 alphabets, 0-9, spaces are valid inputs)
    - decode:Convert the code into alphabets after entering the correct code ( default : {0814} )
  - Private talk: You can choose a user and have private talk with him.Remember that you should follow the instructions that server provides you.ex: you should type {private} to get into private talk and {over} to quit and if you agree to talk with the user that tries to connect with you privately, please type {Yes} (the user’s name) with a space between two words.
  - Send files and photos: You can choose a file in your computer, and send it to all the other people in the chat room. However, you can only send txt. You can also choose a photo in your computer, and send it to all the other people in the chatroom. However, the size of the photo can’t be too large.
  - Calculator: You can type an equation, and press ‘OK’. Then the program will show the answer. This function isn’t related to chat room, which means nobody else will see what you have calculated.
