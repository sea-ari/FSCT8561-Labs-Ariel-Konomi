### PART1

message = input("Enter a message: ")
print("You typed:", message)

print()
print()

count = 0

while True:
    print("Loop is running")
    count = count + 1

    if count == 3:
        break

print()
print()

command = "HELLO"

if command == "HELLO":
    print("Start session")
elif command == "MSG":
    print("Process message")
else:
    print("Unknown command")

print()
print()

message = "HELLO|Ariel"

command, data = message.split("|", 1)

print("Command:", command)
print("Data:", data)


print()
print()

try:
    number = int("abc")
except ValueError:
    print("Invalid value")