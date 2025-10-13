from chunking import create_chunks

# chunks = create_chunks("Data/pdf/FALLSEM2025-26_VL_BCSE306L_00100_TH_2025-07-28_Module-2.pdf.txt")
# print(chunks)

chunks = create_chunks("Data/ppts/FALLSEM2025-26_VL_BCSE306L_00100_TH_2025-07-25_Introduction-to-AI.pptx.txt")
for c in chunks:
    print(c)
    print()
    print()