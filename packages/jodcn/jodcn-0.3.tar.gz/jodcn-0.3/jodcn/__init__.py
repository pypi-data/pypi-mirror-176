a = """ 
-------------------------------------------------------------------------------------------------------------------------------------

EXP-5  USE SIMULATOR TO UNDERSTAND FUNCTIONING OF ALOHA/CSMD

II. INSTALL NS2
1. Download the NS2 files from the Internet http://sourceforge.net/projects/nsnam/files/ns-2/2.34/
2. Extract the files
3. Put the files in the Home folder
4. Set the appropriate permissions for the ns-allinone-2.34 to allow executing the files inside it. To do that:
Right click the folder -> Properties -> Permissions , and choose the appropriate group with the appropriate
file access, then click "Allow executing file as program" and then click "Apply permissions to enclosed
files"
5. From the Accessories -> Terminal
6. Type the following command to know in which directory you are: ~$ pwd
7. You need to be in the directory where you placed the ns-allinone-2.34 folder
8. If you are not in the /home/e , then move to it by using the command cd
9. Now, supposing you are in the directory /home/e (e can be any other user) type the following command to
move inside the ns-allinone-2.34 using the command cd $ cd ns-allinone-2.34
10. Then, type the following command (you will be asked to enter the system password to process. Also, you
will be asked if you want to continue, type: y to continue): $ sudo apt-get install build-essential
autoconfautomakelibxmu-dev
11. Type the following command to install NS2 $ ./install


III. SET ENVIRONMENTAL VARIABLES
1. Write the following line: gedit ~/.bashrc
2. After the previous command, a file will open to you. Add the following lines to the end of the file.
Replace "/your/path" by the folder where you placed the extracted ns-allinone-2.34 (For example, if your
Linux user name is e, and you placed the ns-allinone-2.34 in the home directory, you have to change
/your/path to /home/e)
# LD_LIBRARY_PATH OTCL_LIB=/your/path/ns-allinone-2.34/otcl-1.13 NS2_LIB=/your/path/nsallinone-2.34/lib X11_LIB=/usr/X11R6/lib USR_LOCAL_LIB=/usr/local/lib export
LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$OTCL_LIB:$NS2_LIB:$X11_LIB:$USR_LOCAL_LIB
# TCL_LIBRARY TCL_LIB=/your/path/ns-allinone-2.34/tcl8.4.18/library USR_LIB=/usr/lib export
TCL_LIBRARY=$TCL_LIB:$USR_LIB
# PATH XGRAPH=/your/path/ns-allinone-2.34/bin:/your/path/ns-allinone2.34/tcl8.4.18/unix:/your/path/nsallinone-2.34/tk8.4.18/unix NS=/your/path/ns-allinone-2.34/ns-2.34/ NAM=/your/path/ns-allinone2.34/nam-1.14/ PATH=$PATH:$XGRAPH:$NS:$NAM
3. Save the file changes after your edit
4. Ensure that it immediately takes effect:
$ source ~/.bashrc
Note: the previous step is important; else you cannot successfully run ns-2.
5. Now, the installation has been completed. Try: $ ns 6. The "%" symbol appears on the screen. Type "exit"
to quit.


IV. Validation
1. To run the ns validation suite: $ cd ns-2.34 $ ./validate
2. The validation will take long time, wait until it finish.


V. RUN YOUR FIRST NAM EXAMPLE
1. From the terminal type the following: $ cd ns-allinone-2.34 $ cd nam-1.14 $ cd edu $ exec nam A2-stopn-wait-loss.nam
2. The following window appears, click the Play button to see the protocol animation
Input for Sample 1: Node 1 transmits data to Node
Simulation Time - 10 Seconds
(Note: The Simulation Time can be selected only after doing the following two tasks: Set the properties of
Nodes and then click on the Simulate button).
Input for Sample 2: Node 1 transmits data to Node 2, Node 2 transmits data to Node 1.
Simulation Time - 10 Seconds
(Note: The Simulation Time can be selected only after doing the following two tasks: Set the properties of
Nodes and Then click on the Simulate button).
Experiment 1: Node 1 transmits data to Node 2. Experiment 1: Node 1 transmits data to Node 2.
Experiment 2: Node 1 transmits data to Node 2, and Node 2 transmits data to Node 1.
Experiment 3: Node 1 transmits data to Node 2, and Node 2 transmits data to Node 3, and Node 3 transmits
data to Node 1.
And so on do the experiment by increasing the number of nodes generating traffic as 4, 5, 7, 9, 10, 15, 20 22
and 24 nodes.
Simulation Time - 10 Seconds
(Note: The Simulation Time can be selected only after doing the following two tasks: Set the properties of
Nodes and then click on the Simulate button).
We have obtained the following characteristic plot for the Slotted ALOHA, which matches the
theoretical result.

CONCLUSION: Thus, we have studied and successfully understand functioningofALOHA.

--------------------------------------------------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------

    Expt-6  JAVA SOCKET PROGRAMMING

    1. open text editor save program as MyServer.java && MyClient.java
    2. then in terminal 1 type :  javac MyClient.java
    				   :  java MyClient
    3 then in terminal 2 type   : javac MyServer.java
			          : java MyServer

+++++++++++++++++++++++++++++++++

server.java file
-----------------
    import java.io.*;
    import java.net.*;

    public class server{
    	public static void main(String[] args) throws IOException
    		ServerSocket ss = new ServerSocket(6666);
    		Socket s = ss.acept();

    		System.out.println("client connected");

    		InputStreamReader in = new InputStreamReader(s.getInputStream());
    		BufferedReader bf = new BufferedReader(in);
    
    		sting str = bf.readLine();
    		system.out.println("clent : "+ str);

    	}
    }
 
+++++++++++++++++++++++++++++++++++++++++

client.java file
-----------------
    import java.io.*;
    import java.net.*;

    public class client{
    	public static void main(String[] args) throws IOException{
    		Socket s=new Socket("localhost",6666);
    
    		PrintWriter pr + new PrintWriter(s.getOutputStream());
    		pr.println("hello");
    		pr.flush();

    	}
    }

----------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------------------------------

    Expt-3  Perform network discovry tools using nmap 

    Basic commands working in Nmap:
    • For target specifications: nmap<target's URL or IP with spaces between them>
    • For OS detection: nmap -O <target-host's URL or IP>
    • For version detection: nmap -sV<target-host's URL or IP>
    SYN scan is the default and most popular scan option for good reasons. It can be performed quickly,
    scanning thousands of ports per second on a fast network not hampered by restrictive firewalls. It is
    also relatively unobtrusive and stealthy since it never completes TCP connections
    Algorithm\Implementation Steps\Installation Steps:
    1. Download Nmap from www.nmap.org and install the Nmap Software with WinPcapDriver
    utility.
    2. Execute the Nmap-Zenmap GUI tool from Program Menu or Desktop Icon
    3. Type the Target Machine IP Address(ie.GuestOS or any website Address)
    4. Perform the profiles shown in the utility.

------------------------------------------------------------------------------------------------------------------------------------
------------------------------------------------------------------------------------------------------------------------------------

    Expt-1 networking commands in linux    

    ifconfig
    NSLOOKUP website
    ping ip
    traceroute
    netstat -a
    arp -a
    ip addr show 
       dig website

-------------------------------------------------------------------------------------------------------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------

    CISCO PACKET TRACER

    asign ip to all devices
    use ping and destination ip

    1. bus topology ---- switch PT      4switch+4pc
    2. star topolgy ---- switch 2960/hub PT	1switch/hub+5pc
    3. ring topology --- switch	4switch+4pc
    4. tree topology --- 7pc+7switch

    5. design vpn RIP ---- 2-1841 router | 2-switches2940-24 | 4-pc
       ip addresses                                RIP(router)
       1.4/3.2 | 2.4/3.3	router		    	 1	|	2
       1.4 | 2.4	default gateawy		     1.0    |    2.0
       1.2/1.3 | 2.2/2.3	pc           	     3.0    |    3.0

    6. static routing ---- 2-1841 router | 2-switches2950-24 | 4-pc
       same as above ip add
    	else,
       in router 
        static routing
         		1        |       2
    	192.168.2.0    |	 192.168.1.0                     
          255.255.255.0  |   255.255.255.0                                         
            192.168.3.3    |   192.168.3.2

----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------

    wire shark
    capture packet 
    save 
    open
    use filter or type "TCP" above in "apply a display filter"
    explore !!!
----------------------------------------------------------------------------------------------------------


other code for java

ChatSystemClient.java

import java.io.*;
import java.net.InetAddress;
import java.net.Socket;

public class ChatSystemClient {
    public static void main(String[] args) throws IOException {

        InetAddress addressOfTheServer = InetAddress.getByName("127.0.0.1");

        // Connecting to the server
        Socket client = new Socket(addressOfTheServer, 3000);


        // Getting the server input/output streams
        BufferedReader inputFromServer = new BufferedReader(new InputStreamReader(client.getInputStream()));
        PrintWriter outputStream = new PrintWriter(new OutputStreamWriter(client.getOutputStream()));

        // Getting the keyboard input stream
        BufferedReader keyboardInput = new BufferedReader(new InputStreamReader(System.in));

        Thread messagePrinter = new Thread(new Runnable() {
            @Override
            public void run() {
                while(true) {
                    try {
                        String messageFromServer = inputFromServer.readLine();
                        if(messageFromServer != null) {
                            System.out.println("Message from the server: " + messageFromServer);
                        }
                    } catch (IOException e) {
                        e.printStackTrace();
                    }

                }
            }
        });

        // Start the message printer Thread
        messagePrinter.start();

        while(true) {

            // Reading message from the keyboard
            String line = keyboardInput.readLine();

            // Sending the message to the server
            outputStream.println(line);
            outputStream.flush();

        }

    }
}

code for Server - java

ChatSystemServer.java

import java.io.*;
import java.net.InetAddress;
import java.net.ServerSocket;
import java.net.Socket;


public class ChatSystemServer {

    public static void main(String[] args) throws IOException, InterruptedException {

        InetAddress address = InetAddress.getByName("localhost");
        ServerSocket server = new ServerSocket(3000,3, address);

        while(true) {

            Socket newClient = server.accept();

            ChatServerWorker serverWorker = new ChatServerWorker(newClient);
            serverWorker.start();

        }
    }
}

class ChatServerWorker extends Thread {

    private Socket clientSocket;

    public ChatServerWorker(Socket clientSocket) {
        this.clientSocket = clientSocket;
    }

    @Override
    public void run() {
        try {
            startWorker();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    void startWorker() throws IOException {


        // Getting the input/output streams of the client
        BufferedReader clientInput = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
        PrintWriter clientOutput = new PrintWriter(new OutputStreamWriter(clientSocket.getOutputStream()));

        // Getting the keyboard input stream
        BufferedReader keyboardInput = new BufferedReader(new InputStreamReader(System.in));


        Thread messagePrinter = new Thread(new Runnable() {
            @Override
            public void run() {
                while(true) {
                    if(clientSocket.isClosed()) {
                        Thread.interrupted();
                        break;
                    }
                    try {
                        if(clientInput == null) {
                            break;
                        }

                        String messageFromTheClient = clientInput.readLine();
                        if(messageFromTheClient != null) {
                            System.out.println("Message from the client: " + messageFromTheClient);
                        }

                        if(messageFromTheClient.equals("exit")) {
                            clientSocket.close();
                            break;
                        }

                    } catch (IOException e) {
                        e.printStackTrace();
                    }

                }
            }
        });

        // Starting the message printer on a new Thread
        messagePrinter.start();

        while(true) {
            if(clientSocket.isClosed()) {
                break;
            }
            String messageBack = keyboardInput.readLine();

            if(messageBack.equals("exit")) {
                Thread.interrupted();
            }
            clientOutput.println(messageBack);
            clientOutput.flush();

        }

        clientSocket.close();

    }

}



 Priya Client Server Code : 
 filename : client.java 

    import java.io.*;
    import java.net.*;
    class client{
    public static void main(String[]args){
    try{
    Socket s=new Socket("localhost",6666);
    DataOutputStream dout=new DataOutputStream(s.getOutputStream());
    dout.writeUTF("Hello");
    dout.flush();
    dout.close();
    s.close();
    }
    catch(Exception e){System.out.println(e);}
    }
    }
    
    
    // file name : server.java
    
    import java.io.*;
    import java.net.*;
    class server{
    public static void main(String[]args){
    try{
    ServerSocket ss=new ServerSocket(6666);
    Socket s=ss.accept();
    DataInputStream dis=new DataInputStream(s.getInputStream());
    String str=(String)dis.readUTF();
    System.out.println("message= "+str);
    ss.close();
    }
    catch(Exception e){System.out.println(e);}
    }
    }
    
    
    
    
    // Run server.java file first then open new terminal and run client.java
"""
print(a)