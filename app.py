def create_chunks(full_text,chunksize = 500,overlap=100):
  chunks = []
  start = 0
  while start<len(full_text):  #0<1000       400<1000     800<1000
    end = start + chunksize    #500          400+500 900   800+500=1300
    chunk = full_text[start:end] #[0:500]    [400:900]     [800:1300]
    if chunk.strip():
      chunks.append(chunk)
    start = end - overlap #500-100 = 400    900-100=800    1300-100=1200
  return chunks
