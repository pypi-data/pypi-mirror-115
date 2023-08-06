import csv

def _process_tsv(stream):
    items = []

    reader = csv.reader(stream, delimiter="\t")
    headers = next(reader)  # First line contains header titles

    for row in reader:
        item = {}
        for index, value in enumerate(row):
            if index >= len(headers):
                break
            item[headers[index]] = value
        items.append(item)

    return items

# files = ["/Users/aaron/Documents/Github/hkscs_unicode_converter/src/hkscs_unicode_converter/data/hkscs2004.tsv",
#         "/Users/aaron/Documents/Github/hkscs_unicode_converter/src/hkscs_unicode_converter/data/hkscs2008.tsv"]
files = ["/Users/aaron/Documents/Github/hkscs_unicode_converter/src/hkscs_unicode_converter/data/gccs.tsv",
        "/Users/aaron/Documents/Github/hkscs_unicode_converter/src/hkscs_unicode_converter/data/hkscs1999.tsv"]

# chars = [
#     "F2A1",
#     "F2A2",
#     "F2A3",
#     "F2A5",
#     "F2A9",
#     "F2AA",
#     "F2AB",
#     "F2AC",
#     "F2AD",
#     "F2C4",
#     "F2C6",
#     "F2CB",
#     "F2CE",
#     "F2D1",
#     "F2D3",
#     "F2D5",
#     "F2D6",
#     "F2D7",
#     "F2D8",
#     "F2D9",
#     "F2DA",
#     "F2DC",
#     "F2DE",
#     "F2E0",
#     "F2E3",
# ]

content_1 = set()
content_2 = set()

# content_1 = set()
# # content_2 = set()

items_1 = _process_tsv(open(files[0], "r"))
content_1 = set([item["Big5Alternate"][2:] for item in items_1])

# for char in chars:
#     for item in items_1:
#         if item["ISO/IEC_10646-1:2000"] == char:
#             print(item["ISO/IEC_10646:2003_Amendment"])
#             continue
#         if item["ISO/IEC_10646-1:1993"] == char:
#             print(item["ISO/IEC_10646:2003_Amendment"])
# for item in items_1:
#     if item["ISO/IEC_10646-1:2000"] != item["ISO/IEC_10646:2003_Amendment"]:
#         content_1.add(item["ISO/IEC_10646-1:2000"])
#         if item["ISO/IEC_10646-1:1993"] != item["ISO/IEC_10646:2003_Amendment"]:
#             content_1.add(item["ISO/IEC_10646-1:1993"])

items_2 = _process_tsv(open(files[1], "r"))
content_2 = set([item["UnicodeAlternate"][2:] for item in items_2])
# for item in items_2:
#     if item["ISO/IEC_10646-1:2000"] != item["ISO/IEC_10646:2003_Amendment"]:
#         content_2.add(item["ISO/IEC_10646-1:2000"])
#         if item["ISO/IEC_10646-1:1993"] != item["ISO/IEC_10646:2003_Amendment"]:
#             content_2.add(item["ISO/IEC_10646-1:1993"])

content_3 = content_2 - content_1
chars = sorted(list(content_3))

mapping = {}
for char in chars:
    for item in items_2:
        if item["UnicodeAlternate"][2:] == char:
            mapping[char] = (item["Unicode"][2:])

print(mapping)