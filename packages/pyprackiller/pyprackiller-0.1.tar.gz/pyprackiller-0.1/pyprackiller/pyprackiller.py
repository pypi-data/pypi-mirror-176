class PyPracKiller:
    def avail_prog():
        """
        1. f_to_c()
        
        2. tkinter_gui()
        
        3. palin()
        
        4. string_op()
        
        5. string_rever()
        
        6. print_words_in_alpha()
        
        7. prime()
        
        8. list_op()
        
        9. greatest_no()
        
        10. fact_using_recur()
        
        11. date_time()
        
        12. database()
        
        13. calc_no_of_lines()
        
        14. calc_pow()
        
        15. fibo()
        
        """
    def f_to_c():
        """
	print("UNIT CONVERSION")
	print("---------------")
	a=0
	while(a!=3):
	 print("PRESS 1 TO CONVERT CELSIUS TO FAREHNHEIT PRESS 2 \
	TO CONVERT FAREHNHEIT TO CELSIUS PRESS 3 TO QUIT")
	 a=int(input("ENTER YOUR CHOICE:"))
	 if(a==1):
	     c=int(input("ENTER THE CELSIUS VALUE:"))
	     f=(c*(9/5))+32
	     print("CORRESPONDING FAREHNHEIT VALUE:",f)
	     print("-----------------------------------")
	 elif(a==2):
	     f=int(input("ENTER THE FAREHNHEIT VALUE:"))
	     c=(5/9)*(f-32)
	     print("CORRESPONDING CELSIUS VALUE WILL BE:",c)
	     print("-----------------------------------------")
	 elif(a==3):
	     print("**PROGRAM ENDS**")
	 else:
	     print("ENTERED VALUE IS INVALID!!")
	     print("-----------------------------")
        
        """
        
    def tkinter_gui():
        """ 
	from tkinter import *
	def add():
	 res=int(a.get())+int(b.get())
	 myText.set(res)
	win=Tk()
	win.geometry('650x550')
	win.title("ADDITION")
	myText=StringVar()
	Label(win,text="SUM OF TWO NUMBERS").grid(row=0)
	Label(win,text="FIRST NUMBER").grid(row=1)
	Label(win,text="SECOND NUMBER").grid(row=2)
	Label(win,text="RESULT:").grid(row=4)
	result=Label(win,text="",textvariable=myText).grid(row=4,column=1)
	a=Entry(win)
	b=Entry(win)
	a.grid(row=1,column=1)
	b.grid(row=2,column=1)
	Button(win,text="CALCULATE",command=add).grid(row=3,column=1)
	mainloop()
        """
    def palin():
       """
	class Rever:
	 def Palin(self):
	  a=(input("Enter the string:"))
	  s = a[::-1]
	  if(s==a):
	     print("",a, "is a palindrome")
	  else:
	     print("",a, "is not a palindrome")
	print(" CHECK STRING PALINROME USING CLASS, USER DEFINED \
	FUNCTION")
	print(" -----------------------------")
	p=Rever()
	c=0
	p.Palin()
	while(c!=2):
	 print("PRESS 1 CONTINUE PRESS 2 TO QUIT")
	 c=int(input("ENTER YOUR CHOICE:"))
	 if(c==1):
	     p.Palin()
	 elif(c==2):
	     print("**PROGRAM ENDS**")
	 else:
	     print("ENTERED VALUE IS INVALID!!")
	 print("-----------------------------")
       """
       
    def string_op():
       """ 
	print("STRING OPERATIONS")
	print("-----------------------------------------------------")
	num=0
	while(num!=4):
	     print(" Press 1 to concate string \n Press 2 to accessing the string  Press 3 to \
	replicate string  Press 4 to quit ")
	     num=int(input(" Enter your choice (1/2/3):"))
	     if(num==1):
		    print("STRING CONCATENATION:")
		    print("-----------------------")
		    str1 = input(" Enter String 1: ")
		    str2 = input(" Enter String 2: ")
		    str3 = str1+str2
		    print(" The concatenated string is:",str3)
	     elif(num==2):
		     print(" STRING ACCESSING:")
		     print("-------------------")
		     str4=input(" Enter the string to access it's substring:")
		     start=int(input("Enter the range to start:"))
		     end=int(input("Enter the range to end:"))
		     print(" Accessed substring from the given string is:",str4[start:end])
	     elif(num==3):
		     print(" STRING REPLICATION:")
		     print("----------------------")
		     str5=input("Enter string to replicate: ")
		     num2=int(input("How many times to replicate:"))
		     print(" Replicated string is ",str5*num2)
	     else:
		 print("Entered value is greater than 3 ")
	print("The program quits")
       """
    def string_rever():
        """ 
	class word:
	 def reverse_w(self,n):
	   a=n.split(" ")
	   b=reversed(a)
	   return ' '.join(b)
	print("***** REVERSING THE STRING WORD BY WORD USING CLASS \
	*****")
	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \
	~")
	string_val=input("Enter the statement:")
	print("-----------------------")
	result=word().reverse_w(string_val)
	print("REVERSED SENTENCE:") 
	print(result)
	print()
	while True:
	 num=input("Do you want to continue the work(yes/no):") 
	 if(num=="yes"):
	   s1=input("Enter the Statement:")
	   print("--------------------")
	   s2=word().reverse_w(s1)
	   print("REVERSED SENTENCE:")
	   print(s2)
	   print(" ")
	 elif(num=="no"):
	   print("-------------------------------------------")
	   print("The Program ends")
	   break
	 else:
	   print("Enter the correct format(yes/no)")
        """
        
    def print_words_in_alpha():
          """ 
		print(" INPUT A TEXTFILE AND PRINTS WORDS IN ALPHABETICAL \ORDER")
		print("------------------------------------------------------------")
		print("")
		msg = input("Enter the sentence to be inserted in the file: ")
		print("")
		f = open('file.txt','w') 
		f.write(msg) 
		f.close()
		f = open('file.txt','r') 
		lst = [] 
		words=[] 
		for line in f: 
		 words += line.split()
		 print("")
		 print("Given Sentence in the file: ",*words)
		 print("")
		words.sort() 
		print("")
		print("The unique words in alphabetical order are:")
		print("")
		for a in words:
		 if a in lst: 
		      continue 
		 else: 
		     lst.append(a) 
		     print(a) 
     
         """
    def prime():
          """ 
		print("PRIME NUMBERS LESS THAN 20")
		print("--------------------------")
		n=20
		for n in range(2,n+1):
		    for i in range(2,n):
			if((n%i)==0):
			 break
		    else:
			print(n)
		 
		print("--------------------------") 
          
          """   
    def list_op():
          """ 
		print("***LIST OPERATION***")
		print("-------------------")
		st=[]
		m=int(input("Enter total number of values in list:"))
		for i in range (0,m):
		      k=input("Enter the value:")
		      st.append(k)
		print("list is:",st)
		a=0
		while(a!=3):
		    print("PRESS 1 to INSERT VALUE IN THE LIST PRESS 2 TO DELETE THE VALUE IN THE LIST PRESS 3 TO QUIT")
		    a=int(input("ENTER YOUR CHOICE:"))
		    if(a==1):
			n=int(input("Insert before which index value:"))
			s=input("Enter the value:")
			st.insert(n,s)
			print("list is:",st)
		    elif(a==2):
			b=input("which element you want to delete:")
			st.remove(b)
			print("list is:",st)
		    elif(a==3):
			print("**PROGRAM ENDS**")
		    else:
			print("ENTERED VALUE IS INVALID!!")
			print("-----------------------------")
          """
    
    def greatest_no():
          """  
		print("GREATEST AMONG THREE NUMBERS")
		print("----------------------------")
		a=int(input("Enter the first number(a)="))
		b=int(input("Enter the second number(b)="))
		c=int(input("Enter the third number(c)="))
		if(a==b and a>c):
		 print(f"",a," and ",b ," are the greatest")
		elif(b==c and b>a):
		 print(f"",b," and ",c ,"are the greatest")
		elif(a==c and a>b):
		 print(f"",a ,"and ",c ,"are the greatest ")
		elif(a>b and a>c):
		 print(f" ",a ,"is the greatest among the three numbers")
		elif(b>a and b>c):
		 print(f"",b ,"is the greatest among the three numbers")
		elif(c>a and c>b):
		 print(f"",c ,"is the greatest among the three numbers")
		else:
		 print("All values are equal")
          
          """      
    def fact_using_recur():
          """           
		def fact(n):
		 if(n==0 or n==1): #factorial of 0 and 1 is 1
		  return 1
		 else:
		  return (n*fact(n-1)) #fact function calls itself(recursion)
		#main program starts
		print("FACTORIAL OF A NUMBER USING RECURSION FUNCTION")
		print("----------------------------------------------")
		n=int(input("Enter a number to find factorial:"))
		if(n<0): #checks for negative number
		 print("Factorial is not possible for negative numbers")
		else: #calls fact function
		 print("Factorial of",n,"is:",fact(n))
          
          """     
    def date_time():
          """ 
		import datetime 
		import calendar 
		import time
		print("*** DISPLAYING CURRENT DATE AND TIME & \
		CORRESPONDING DAY BY READING A DATE***")
		print("---------------------------------------------------------------------------------")
		choice=0
		while(choice!=3):
		     print(" Choose 1 To know The Current Data Choose 2 To know the day of \
		a specific date: Choose 3 toquit")
		     choice=int(input("Enter the choice(1/2/3):"))
		     if choice==1:
			 local=time.localtime()
			 c_current= time.strftime(" %a %b %d %H:%M:%S %Z %Y",local)
			 print(" The Current Date&Time Is:",c_current)
		     elif choice==2:
			date=input(" Enter the date in the format(dd mm yyyy):") 
			born=datetime.datetime.strptime(date,'%d %m %Y').weekday() 
			day=calendar.day_name[born]
			print("",day)
		     elif choice==3:
			 print("program quits")
			 break
		     else:
			 print("Entered choice is invalid")
		print("**************************************")
          
          """
    def database():
          """
		import sqlite3
		conn=sqlite3.connect('test.db')
		cur=conn.cursor()
		print("Database Connectivity Using SQL")
		print("______________________________")
		print("")
		print("Records in the Table:")
		cur.execute("drop table t1")
		cur.execute("create table t1(name,age,dept)")
		cur.execute(""insert into t1 values('aaa',20,'cs')"") Add another double Quotes within the bracket
		cur.execute(""insert into t1 values('bbb',21,'cs')"") Add another double Quotes within the bracket
		cur.execute(""insert into t1 values('ccc',30,'cs')"") Add another double Quotes within the bracket
		conn.commit()
		res=cur.execute("select * from t1")
		a=res.fetchall()
		print(*a, sep = "")
          
          """
          
    def calc_no_of_lines():
          """
		print("***CALCULATING THE NUMBER OF LINE, WORDS AND \
		CHARACTERS IN A FILE***")
		file__IO =input("Enter the path to the file: ")
		with open(file__IO, 'r') as f:
		 data = f.read()
		 line = data.splitlines()
		 words = data.split()
		 spaces = data.split(" ")
		 charc = (len(data) - len(spaces))
		 s_charc = len(data)
		print('Number Of Lines :', len(line), 'Number Of Words :',\
		 len(words),'Number Of Characters Without Space:', charc+1,\
		 ' Numbers Of Characters With Spaces:',s_charc+1)
          
          """   
          
    def calc_pow():
          """ 
		print("CLASS TO IMPLEMENT POWER")
		print("--------------------------")
		print("")
		class py_pow:
		 def powr(self, x, n):
		   if x==0 or x==1 or n==1:
		     return x 
		   if x==-1:
		     if n%2 ==0:
		       return 1
		     else:
			return -1
		   if n==0:
		     return 1
		   if n<0:
		      return 1/self.powr(x,-n)
		   val = self.powr(x,n//2)
		   if n%2 ==0:
		     return val*val
		   return val*val*x
		pp=py_pow()
		x=int(input("Enter x value :"))
		print("")
		n=int(input("Enter n value :"))
		print("")
		print("Value of",x,"Power",n,"is :",pp.powr(x,n));
          
          """ 
    def fibo():
          """ 
          
               fibonacci.py
		
		import mymod #name of the module file
		print("FIBONACCI NUMBER")
		print("----------------")
		n=int(input("Enter a number:"))
		print("Fibonacci Number of",n,"is",mymod.fib(n))
		
		mymod.py
		
		    def fib(n):
		    a = 0
		    b = 1
		    if n < 0: 
			 print()
		    elif n == 0: 
			return 0
		    elif n == 1: 
			return 1
		    else: 
			for i in range(1, n):
			    c = a + b
			    a = b
			    b = c
			return b
          
          
          """      
