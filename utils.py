import re

# Simple string data cleaner
def cleaner(text, mode="general"):
    if mode == "url":
        text = "https://www1.president.go.kr" + text
        return text

    elif mode == "category":
        text = re.sub("분류 ", "", text)
        text = re.sub("\s{2,}|\"|'|\`|\,|\…|\.|\n|\t|\r|▲|【|】|▶|©|\*", "", text)
        return text

    elif mode == "title":
        text = re.sub("제목 ", "", text)
        text = re.sub("\s{2,}|\"|'|\`|\,|\…|\.|\n|\t|\r|▲|【|】|▶|©|\*", "", text)
        return text

    elif mode == "expired_date":
        text = re.sub("청원 종료일 ", "", text)
        text = re.sub("\s{2,}|\"|'|\`|\,|\…|\.|\n|\t|\r|▲|【|】|▶|©|\*", "", text)
        return text

    elif mode == "count":
        text = re.sub("참여인원 ", "", text)
        text = re.sub("\s{2,}|\"|'|\`|\,|\…|\.|\n|\t|\r|▲|【|】|▶|©|\*", "", text)
        return text

    elif mode == "general":
        text = re.sub("\s{2,}|\"|'|\`|\,|\…|\.|\n|\t|\r|▲|【|】|▶|©|\*", "", text)
        return text
