
`print ("Hello World")` - when running the code it will print out "Hello World"

element - any python data type; string, int, float, list, bool, etc.  
iterable - list, tuple, set, etc.

- `len()` - length of object
- `type()` - type of object
- `range()` - sequence of numbers
- `sum()` - returns sum of elements
- `max()` - max value in iterable
- `min()` - min value in iterable
- `sorted()` - returns sorted list from iterable
- `any()` - returns True if all iterable elements are True
- `round()` - rounds number to nearest int
- `enumerate()` - adds counter to iterable and returns a tuple
- `chr()` - returns a unicode character corresponding to the int that character is mapped to
- `ord()` - opposite of `chr()`

#### Iterables

- `list()` - creates list from iterable
- `tuple()` - creates tuple from iterable
- `set()` - creates set from iterable
- `dict()` - creates dict from key-value pairs

#### Files

`open(file, "r"/"w"/"a")` - opens file

#### Strings

- `.upper()` - converts string to uppercase
- `.lower()` - converts string to lowercase
- `.strip()` - removes leading and trailing whitespace
- `.replace(old, new)` - replaces substring with substring
- `.split(seperator)` - splits string into **_list_** of substrings
- `.join(iterable)` - joins elements of iterable (list, set, etc.)

#### Lists

- `.append(element)` - appends element to end of list
- `.extend(element)` - extends list by appending elements from iterable
- `.pop(index)` - removes and returns element at index
- `.remove(element)` - removes element specified (can be string, int, etc.)
- `.index(element)` - returns index of element (if element is string; index of the first char in string)
- `.count(element)` - number of occurrences of element
- `.sort(reverse=True)` - sorts elements in ascending order (will change values of object it is being used on; can be reversed)
- `.reverse(element)` - reverses order of elements

#### Dictionary

- `.keys()` - returns all keys in dictionary
- `.values()` - returns all values in dictionary
- `.items()` - returns all key/value pairs in individual tuples in one tuple
- `get(key, default)` - returns value for key, or default if no key is present
- `.pop(key)` - removes and returns value for specified key
- `.update(other_dict)` - updates dict with key/value pairs from another dict

Create a list:

```py
movie = ["Pacific Rim", "It", "The Hangover" ]
```

Accessing a list:

```py
print(movie[0]) #would return Pacfic Rim
print(movie[0:2]) #would return Pacific Rim and It
print(movie[0:]) #would return everything after Pacifc Rim
print(movie[:2]) #would return everything before The Hangover
print(movie[-1]) #would return the Hangover
```

Functions:

```py
len(movie) #would return the amont of objects in the list
movie.append("Jaws") #would add Jaws to the END of the list
movie.pop() #would remove the LAST item
movie.pop(0) #would remove the FIRST item
```


```py
print("Monty", "Python", end="")
```

`end=""` or `sep="-"`



`course = "FSCT"` - this would be a variable which store a value. this one is called a string
`port = 12345` - this is another variable, not called a string as it is not a text value

`("127.0.0.1", 12345)` - a tuple as it is a pair

`import socket` - built-in library in python which gives networking capabilities
	sockets send bytes, not ordinary python strings
	`.enncode()` - used to convert text to bytes
	`.decode()` - used to convert bytes to text

EX. 
`message = "Hello"` - message string is created
`data = message.encode()` - data string is created to encode the message
`print(message)` - printing the message as is
`print(data)` - printing/ converting the message to bytes
`print(data.decode())` - printing/ converting the data back to text


socket - endpoint used by an app to communicate over a network

`my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)`
	`socket.AF_INET` - IPv4 option
	`socket.SOCK_STREAM` - TCP option
`my_socket.close()` - closing the socket/connection



`sys` - allows us to interact with the interpreter and contains most information related to the execution in progress
	`sys.argv` - array containing all arguments in the command line
	`sys.platform` - returns the current OS
	`sys.version` - returns the interpreter version
	`sys.getfilesystemencoding()` - returns the encoding used by the filesystem
	`sys.getdefaultencoding()` - returns the default encoding
	`sys.path` - returns a list of all the directories in which the interpreter searches for the modules when the `import` directive is used

`import os` - access different functions in our OS
	`os.getcwd()` - retrieve the current working directory path and store that value on the pwd variable
	`os.listdir()` - method to obtain the filenames and directories in the current working directory
	`os.system()` - can execute a shell command
	`os.listdir(path)` - returns a list with the contents of the directory passed as an argument
	`os.walk(path)` - navigate all directories in the provided path dir and returns three values
		path directory
		names of subdirectories
		list of filenames in the current directory


##### threading

allows developers to work with multiple threads

in the example, 4 threads are created, where each one prints a different message that is passed as a parameter in the `thread_message (message` method

![[Pasted image 20260920012508.png|497]]


![[Pasted image 20260920012741.png|524]]

thread class constructor accepts five arguments as parameters
- **group**: A special parameter that is reserved for future extensions
- **target**: The callable object to be invoked by the **run()** method
- **name**: The thread’s name
- **args**: An argument tuple for target invocation
- **kwargs**: A dictionary keyword argument to invoke the base class constructor

`thread.join()` - used to wait for the thread to finish. join method is used to block the thread until it finishes it's execution

multithreading - can write applications with multiple threads
	can provide copies of our code on additional threads and execute them