from docx import Document

def obtainText(docFileName:str = ""):
    document = Document(docFileName)
    finalText = []
    for line in document.paragraphs:
        finalText.append(line.text)
    return '\n'.join(finalText)

print(obtainText('dataset\data\第三営業本部＿第二新卒.docx'))