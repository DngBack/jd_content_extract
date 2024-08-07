from langchain.text_splitter import CharacterTextSplitter

def character_chunking(content: str,
                       chunk_size: int = 500,
                       chunk_overlap: int = 50, 
                       separator: str ='', 
                       strip_whitespace: bool =False):
    
    text_splitter = CharacterTextSplitter(chunk_size = chunk_size,
                                        chunk_overlap=chunk_overlap, separator=separator)
    output = text_splitter.split_text(text=content)
    # text_splitter = text_splitter.create_documents([text])
    return output


