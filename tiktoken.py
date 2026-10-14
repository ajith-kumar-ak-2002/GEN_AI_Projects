# pyrefly: ignore [missing-import]
import tiktoken

text = "Hello, world! This is a test string to count tokens."

tokenizer = tiktoken.encoding_for_model("gpt-4")

tokenIds = tokenizer.encode(text)

print(tokenIds)

result = [2323, 291, 46594, 35691, 29125, 0]

resultIds = tokenizer.decode(result)

print(resultIds)