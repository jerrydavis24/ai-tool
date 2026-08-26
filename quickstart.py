import anthropic


client = anthropic.Anthropic()
message = client.messages.create(
    model="claude-opus-5",
    max_tokens=1000,
    messages=[
        {"role": "user", "content": "Explain recursion in one paragraph."}
    ],
)
for block in message.content:
    if block.type == "text":
        print(block.text)