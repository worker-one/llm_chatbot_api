import docx

content = ""
doc = docx.Document("tests/functional/bruno/mocks/miso.docx")
for paragraph in doc.paragraphs:
    content += paragraph.text + "\n"
print(content.strip("\n"))