buffer = "hello\r\nworld\r\nparti"
lines = buffer.split("\r\n")
print(repr(lines))
buffer = lines.pop()
print(repr(lines))
print("the buffer is: |" + repr(buffer) + "|")

print("second test:")

buffer = "hello\r\nworld\r\nnot partial\r\n"
lines = buffer.split("\r\n")
print(repr(lines))
buffer = lines.pop()
print(repr(lines))
print("the buffer is: |" + repr(buffer) + "|")
