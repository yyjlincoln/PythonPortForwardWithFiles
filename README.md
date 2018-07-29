# Best for school internet and intranet.
We cannot use proxy at school and we cannot access intranet. It is blocked. We can only browse some limited internet such as google search.
# It's a "Proxy" using shared file system (Such as ftp)
You can set the work dir in the program and run it. It will then access the workdir and generate files. By logging to the same account among computers (which can access/edit the same file), you can simply convert socket request to files.
# How can I use it?
By simply create another .py script and type:
## Server Mode - it connects to the Server
import <Whatever you named it> as example:
example.server.forward(('targetaddress',targetport))

## Client Mode
import <name> as example:
example.client.forward(('targetaddress',targetport),('localhostedaddress',localhostedport))
  
# USE IT WISELY
I, as the developer and a student, do not take any responsibility if you use this program and:
1) Be punished at school
2) The program damage your computer
3) Be banned for internet
4) etc.
Only non-commercial and personal use are permitted
PLEASE USE IT WISELY.
